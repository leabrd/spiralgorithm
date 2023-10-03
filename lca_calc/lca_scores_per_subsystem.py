# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 18:03:48 2022

@author: leabr
"""

def dict_LCA_score_per_subsystem (recipe):
    
    '''
    This function creates a nested dictionary with LCA scores calculated per 
    subsystem only. This functions does not calculate the impact of each 
    activity as dict_LCA_scores_per_processes and is therefore a lot faster.
    The output dictionary groups LCA scores per method analysed, per database, 
    per subsystem.
 
    :param recipe: YAML file containing all the information to conduct the LCA analysis.
    :type recipe: yml
    :return: master_output, recipe
    :rtype: TYPE
    '''
    
    from brightway2 import Database, LCA, methods
    import numpy as np
    
    # main dictionary that will contain the LCA scores
    master_output = {} 
    
    # only do the calculations if asked in the recipe
    if all(np.array(list(recipe['analyses']['CA_subsystems'].values())) == False):
        print('\nWARNING: To perform a contribution analysis per subsystem, set any of the "CA_subsystems" items to "True" in the recipe (input > analyses > CA_subsystems).')
        return master_output, recipe
    
    ## START THE CONTRIBUTION ANALYSIS        
    print('\n> CONTRIBUTION ANALYSIS PER SUBSYSTEM: \n  ---------------------------------------------')
    
    ## DEFINE THE GRAPHS TO PLOT ACCORDING TO THE RECIPE
    do_relative_stacked = False
    do_bar_chart = False
    
    if recipe['analyses']['CA_subsystems']['relative_stacked_bar_plot'] ==  True:
        do_relative_stacked = True
        
    if recipe['analyses']['CA_subsystems']['bar_chart_one_ic'] ==  True:
        do_bar_chart = True    

    # GET THE LCIA METHOD(S) AND DATABASE NAME(S) FROM THE RECIPE
    if do_bar_chart:
        lcia_methods = recipe['CA_subsystems']['bar_chart_one_ic']['lcia_methods']
        databases_scenarios = recipe['CA_subsystems']['bar_chart_one_ic']['databases']
    
    if do_relative_stacked:
        lcia_methods = recipe['CA_subsystems']['relative_stacked_bar_plot']['lcia_methods']
        databases_scenarios = recipe['CA_subsystems']['relative_stacked_bar_plot']['databases'] 
    
    ## CHECK THAT THE LCIA METHODS ARE TUPLES (does not work if not tuples)    
    lcia_methods = [tuple(i) for i in lcia_methods]
    
    print('\nImpact categories selected (%s):' %len(lcia_methods))
    for method in lcia_methods: 
        print('\t- %s (%s)' %(str(method[1]),str(method[2])))
        
    # CREATE A DICTIONARY WITH THE DATABASES TO ASSESS
    # dictionary that will contain all imported databases
    db_dict = {}
    # for each database name, load the database into db_dict
    for db_i in databases_scenarios: 
        # convert the file in a database format (to access all functions)
        db = Database(db_i) 
        # store the database in the dictionary
        db_dict[db_i] = db   
        
    print('\nForeground database retrieved (%s):' %len(list(db_dict.keys())))
    for db in db_dict.keys(): 
        print('\t- %s' %db)

    # CREATE A NESTED DICTIONARY PER METHOD
    '''Create the nested dictionary to store all the data after LCA calculations.
    The dictionary is organised per method. For each method, sub-dictionaries contain 
    LCA scores for each process/exchange.'''

    # create the output dictionary (nested dict) with one sub-dict per method
    for method in lcia_methods:
        # create sub-dictionary for each method
        master_output[method] = {} 
        for db in db_dict:
            # create sub-dictionary for each database (per method)
            master_output[method][db] = {}
            # db_dict['SpiralG_base_case']=Brightway2 SQLiteBackend: SpiralG_base_case
            master_output[method][db]['database identification'] = db_dict[db] 
            
    #-------------------------------------------------------------------------    
    # INITIAL LCA CALCULATION
            
    '''For each method, do an initial LCA calculation and redo the LCIA for each 
    process and exchange in the database.'''

    for method in master_output:
        '''Do the initial LCA calculation for each database. It gives the aggregated LCA score (per method)'''
        
        method_unit = methods.get(method).get('unit')

        print('\n>> LCA calculations - %s' %method[2])
        print('   -------------------------')

        for db_name in master_output[method]: # for each biorefinery scenarios
                        
            ## CALCULATE THE TOTAL LCA SCORE OF THE BIOREFINERY FROM THE MODEL ACTIVITY
            print('\nDatabase name/scenario: %s' %db_name)
            FU_activity_name = str('model_'+db_name)
            print('Functional unit name: %s' %str(FU_activity_name))
            FU_value = recipe['CA_subsystems']['scaling'][db_name]
            FU_unit = 'units'
            print('Functional unit value: %s %s' %(FU_value, FU_unit))

            activity_FU = [act for act in master_output[method][db_name]['database identification'] if FU_activity_name in act['name']][0]           
            
            FU = {activity_FU:FU_value}

            lca_iter = LCA(FU, method)
            lca_iter.lci(factorize=True)
            lca_iter.lcia() 
        
            # total LCA score for each database for each method
            master_output[method][db_name]['total_lca_score'] = lca_iter.score
            print('LCA score database %s: %.4f %s' %(db_name, lca_iter.score, method_unit))
            
                  
    return master_output, recipe
