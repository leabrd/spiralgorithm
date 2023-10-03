#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 08:50:52 2023

@author: leabraud
"""

def dict_LCA_score_per_input_category (recipe, dataset_file_directory):
    
    '''
    This function creates a nested dictionary with LCA scores calculated per 
    input category (e.g. electricity, water, nutrient). 
    '''
    
    import numpy as np
    
    # main dictionary that will contain the LCA scores
    master_output = {} 
    
    # only do the calculations if asked in the recipe
    if all(np.array(list(recipe['analyses']['CA_input_category'].values())) == False):
        
        print('\n WARNING: To perform a contribution analysis per input category, set any of the "CA_input_category" items to "True" in the recipe (input > analyses > CA_input_category).')
        
        return master_output, recipe
        
    print('\n> CONTRIBUTION ANALYSIS PER INPUT CATEGORY: \n  ---------------------------------------------')

    from brightway2 import Database, LCA, methods
    
    #-------------------------------------------------------------------------    
    # DEFINE THE KIND OF GRAPH TO DO 
    do_stacked_bar_plot = False
    do_heatmap = False
    
    if recipe['analyses']['CA_input_category']['stacked_bar_plot'] == True:
        do_stacked_bar_plot = True
    
    if recipe['analyses']['CA_input_category']['heatmap'] == True:
        do_heatmap = True
    
    #-------------------------------------------------------------------------    
    # GET THE LCIA METHOD(S) AND DATABASE NAME(S) FROM THE RECIPE

    if do_stacked_bar_plot:
        lcia_methods = recipe['CA_input_category']['stacked_bar_plot']['lcia_methods']
        databases_scenarios = recipe['CA_input_category']['stacked_bar_plot']['databases']
        
    if do_heatmap:
        lcia_methods = recipe['CA_input_category']['heatmap']['lcia_methods']
        databases_scenarios = recipe['CA_input_category']['heatmap']['databases']
 
    # make sure the LCIA methods are tuples (does not work if not tuples)
    lcia_methods = [tuple(i) for i in lcia_methods]
    
    print('\nNumber of impact categories analysed: %s' %len(lcia_methods))
    print('Initiate LCA calculations...')

    #-------------------------------------------------------------------------    
    # CREATE A DATABASE DICTIONARY

    # dictionary that will contain all imported databases
    db_dict = {}
    
    # for each database name, load the database into db_dict
    for db_i in databases_scenarios: 
        # convert the file in a database format (to access all functions)
        db = Database(db_i) 
        # store the database in the dictionary
        db_dict[db_i] = db 

    #-------------------------------------------------------------------------    
    # CREATE A NESTED DICTIONARY PER METHOD
        
    '''Create the nested dictionary to store all the data after LCA calculations.
    The dictionary is organised per method. For each method, sub-dictionaries contain 
    LCA scores for each process/exchange.'''

    # create the output dictionary (nested dict) with one sub-dict per method
    
    for i in db_dict:
        # create sub-dictionary for each method
        master_output[i] = {} 
        for method in lcia_methods:

            # create sub-dictionary for each database (per method)
            master_output[i][method] = {}
            # db_dict['SpiralG_base_case']=Brightway2 SQLiteBackend: SpiralG_base_case
            master_output[i][method]['database identification'] = db_dict[i] 
            
            
    #-------------------------------------------------------------------------
    # GET THE CATEGORIES FROM EXCEL FILE
    import pandas as pd
            
    category_dict = {} # create a new dictionary to store the ecoinvent datasets to get
    df = pd.read_excel(dataset_file_directory) # convert the Excel file into a dataframe
    ds_temp_dict = df.to_dict(orient = 'index') # convert the dataframe into a temporary dictionary

    for i in range(len(ds_temp_dict.keys())): # for each foreground activity listed
                    
        if ds_temp_dict[i]['ecoinvent dataset'] not in category_dict.keys():
                                                
            category_dict[ds_temp_dict[i]['ecoinvent dataset']] = ds_temp_dict[i]['category']
            
    # CREATE A UNIQUE LIST OF CATEGORIES
    unique_category_list = []
    for category in category_dict.values():
        if category not in unique_category_list:
            unique_category_list.append(category)
            
    #-------------------------------------------------------------------------    
    # INITIAL LCA CALCULATION
            
    '''For each method, do an initial LCA calculation and redo the LCIA for each 
    process and exchange in the database.'''
    
    for db_name in master_output:

        '''Do the initial LCA calculation for each database. It gives the aggregated LCA score (per method)'''
        
        print('\nLCA calculations for the LCIA method: %s' %str(method))

        # Do the LCA calculations for each database i.e. each subsystem in the bioref
        for method in master_output[db_name]:
            
            # Put the category counters to zero
            for category in unique_category_list:
                master_output[db_name][method][category] = 0
                
  

            print('\nDatabase name/scenario: %s' %db_name)
            print('----------------------')

            # The FU used to initiate the LCA calculations is the activity producing the main product
            FU_activity_name = recipe['all_databases'][db_name]['FU_activity_name']
            print('Functional unit name: %s' %str(FU_activity_name))
            
            FU_value = recipe['all_databases'][db_name]['FU_value']
            FU_unit = recipe['all_databases'][db_name]['FU_unit']
            print('Functional unit value: %s %s' %(FU_value, FU_unit))
            
            activity_FU_list = [act for act in master_output[db_name][method]['database identification'] if FU_activity_name in act['name']] 
            activity_FU = activity_FU_list[0]
            FU = {activity_FU:FU_value}
            print('FU = %s' %str(FU))
            
            lca_iter = LCA(FU, method)
            lca_iter.lci(factorize=True)
            lca_iter.lcia()    
            
            method_unit = methods.get(method).get('unit')

            # For each activity, recalculate the LCIA for each exchange using the exchange and its amount as FU.
            # the LCA scores are sumed by category (i.e. loose the information about which activity they belong to.)
            print('\nLCA calculations per exchange:')
            
            # for all the activities in the database except the model activity
            for activity in master_output[db_name][method]['database identification']:
                
                if 'model' in activity['name']: pass
            
                else: 
            
                    print('\nActivity: %s' %str(activity))
                    print('---------')
                                    
                    for exc in activity.exchanges():
                        
                        if exc['type'] == 'production': pass
                    
                        else:
                            # remove the unit from the exchange name for simplicity
                            exchange_key = str(exc.input).split("' ")[0].replace("'",'') 
                            print('\nExchange name: %s' %exchange_key)
                            # get the category of the exchange
                            category = category_dict[exchange_key]
                            print('Category: %s' %category)
                            # get the exchange amount and unit
                            print('Amount: %.2f %s' %(exc.amount, exc.unit))
                            # redo the lca calculation
                            lca_iter.redo_lcia({exc.input: exc['amount']})
                            print('LCA score: %.2f %s' %(lca_iter.score,method_unit))
                            # add the lca score to the good category
                            
                            master_output[db_name][method][category]+=lca_iter.score

    return master_output