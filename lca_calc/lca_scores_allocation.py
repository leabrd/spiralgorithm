#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 09:50:33 2023

@author: leabraud
"""


def dict_LCA_score_allocation (recipe):
    
    
    from brightway2 import Database, LCA, methods
    import numpy as np
    
    # main dictionary that will contain the LCA scores
    master_output = {} 
    
    # only do the calculations if asked in the recipe
    if all(np.array(list(recipe['analyses']['allocation'].values())) == False):
        print('\nWARNING: To perform an allocation on for S2, S1-2, or S1-2-3, set any of the "allocation" items to "True" in the recipe (input > analyses > allocation).')
        return master_output, recipe
    
    ## START THE ALLOCATION    
    print('\n> ALLOCATION OF THE ENVIRONMENTAL IMPACTS: \n  ---------------------------------------------')
    
    
    ## DEFINE THE GRAPHS TO PLOT ACCORDING TO THE RECIPE
    allocation_S2 = False
    allocation_S12 = False
    allocation_S123 = False    
    
    if recipe['analyses']['allocation']['allocation_S2'] ==  True:
        allocation_S2 = True
        allocation_scenario = 'allocation_S2'
        
    if recipe['analyses']['allocation']['allocation_S12'] ==  True:
        allocation_S12 = True
        allocation_scenario = 'allocation_S12'
        
    if recipe['analyses']['allocation']['allocation_S123'] ==  True:
        allocation_S123 = True   
        allocation_scenario = 'allocation_S123'

    # GET THE LCIA METHOD(S) AND DATABASE NAME(S) FROM THE RECIPE
    if allocation_S2:
        lcia_methods = recipe['allocation']['allocation_S2']['lcia_methods']
        databases_scenarios = recipe['allocation']['allocation_S2']['databases']
        allocation_factors = recipe['allocation']['allocation_S2']['allocation_factors']
        scaling_factors = recipe['allocation']['allocation_S2']['scaling_factors'] 

    if allocation_S12:
        lcia_methods = recipe['allocation']['allocation_S12']['lcia_methods']
        databases_scenarios = recipe['allocation']['allocation_S12']['databases']    
        allocation_factors = recipe['allocation']['allocation_S12']['allocation_factors']
        scaling_factors = recipe['allocation']['allocation_S12']['scaling_factors'] 
    
    if allocation_S123:
        lcia_methods = recipe['allocation']['allocation_S123']['lcia_methods']
        databases_scenarios = recipe['allocation']['allocation_S123']['databases']    
        allocation_factors = recipe['allocation']['allocation_S123']['allocation_factors']
        scaling_factors = recipe['allocation']['allocation_S123']['scaling_factors'] 

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
        
        
        ## CALCULATE THE TOTAL LCA SCORE FOR THE COMBINATION OF SUBSYSTEMS
        lca_score_system = 0 # LCA score of S2, S12, or S123
                    
        for db_name in master_output[method]: # for each of the period
        
            ## CALCULATE THE TOTAL LCA SCORE OF S2 FROM THE MODEL ACTIVITY
            print('\nDatabase name/scenario: %s' %db_name)
            FU_activity_name = str('model_'+db_name)
            print('Functional unit name: %s' %str(FU_activity_name))
            #recipe['CA_subsystems']['scaling'][db_name]
            FU_value = recipe['allocation'][allocation_scenario]['scaling_factors'][db_name]
            FU_unit = 'units'
            print('Functional unit value: %s %s' %(FU_value, FU_unit))
            
            activity_FU = [act for act in master_output[method][db_name]['database identification'] if FU_activity_name in act['name']][0]           
            
            FU = {activity_FU:FU_value}

            lca_iter = LCA(FU, method)
            lca_iter.lci(factorize=True)
            lca_iter.lcia() 
            
            print('LCA score database %s: %.2f %s' %(db_name, lca_iter.score, method_unit))
            
            lca_score_system += lca_iter.score # add the LCA score of the subsystem to the total
            
        print('\nLCA score of %s: %.2f %s' % (allocation_scenario.replace('allocation_', ''), lca_score_system, method_unit))      
        
        ### APPLICATION OF THE ALLOCATION FACTORS
        
        for allocation_type in allocation_factors.keys(): # allocation can be mass or economic
            print('\nApplication of the %s allocation approach:'%allocation_type)
            master_output[method][db_name][allocation_type] = {}
            
            for biomass_fraction in allocation_factors[allocation_type].keys():
                
                lca_score_biomass_fraction = (lca_score_system * allocation_factors[allocation_type][biomass_fraction])
                master_output[method][db_name][allocation_type][biomass_fraction] = round(lca_score_biomass_fraction, 2)
                
                print('-%s (%s): %.2f %s' %(biomass_fraction, allocation_factors[allocation_type][biomass_fraction], lca_score_biomass_fraction, method_unit))

       
            ## PLOT A BAR CHART FOR EACH ALLOCATION METHOD
            import matplotlib.pyplot as plt
            from sizing import set_size
            from colours import graph_colours
            #plt.style.use('style_paper.mplstyle')
            
            col_width_latex = 330
            
            short_names = {'blue_extract': 'BE',
                           'CPA_unprocessed': 'CPA',
                           'CPA_concentrate': 'CPAc',
                           'CPD_concentrate': 'CPDc'}
            
            colours = {'gold':'#FFDC3C','blue': '#08519c', 'medium red': '#CB3F2B'}
            
            fig = plt.figure(figsize = set_size(500,0.5))
            ax1 = fig.add_subplot(111)
            
            indices = np.arange(len(master_output[method][db_name][allocation_type].values()))
            bar_width = 0.85
            colours = graph_colours(  indices )
           # ax1.bar(indices, [i for i in master_output[method][db_name][allocation_type].values()], color=list(colours.values()))
            ax1.bar(indices, 
                    [i for i in master_output[method][db_name][allocation_type].values()], 
                    width =0.5,
                    color=colours)

            # add values above the graphs
            addlabels(ax1 , indices, [i for i in master_output[method][db_name][allocation_type].values()])
            
            xlabels = []
            for long_name in master_output[method][db_name][allocation_type].keys():
                if long_name in short_names.keys():
                    xlabels.append(short_names[long_name])
            
            ax1.set_xticks(indices)
            
            ax1.set_xticklabels(xlabels , rotation = 0)
            
            right_side = ax1.spines["right"]
            right_side.set_visible(False)
            top = ax1.spines["top"]
            top.set_visible(False)
            
            ax1.set_ylabel('Impact on %s (%s)' %(method[1], method_unit))
            ax1.set_xlabel('Biomass fraction')
            
            plt.show()
            fig.tight_layout()
            
            fig.savefig(str(recipe['rdir'] + '/allocation/graph_' + allocation_type + '_allocation_' + allocation_scenario.replace('allocation_', '') + '.pdf'),bbox_inches='tight')

    
    return master_output, recipe     


def addlabels(ax ,x,y):
    import matplotlib.pyplot as plt
    for i in range(len(x)):
        ax.text(i, y[i], y[i], ha = 'center',va = 'bottom')