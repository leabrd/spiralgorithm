#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 13:57:36 2023

@author: leabraud
"""


def Export2ExcelPerDb (dbdir, db_name, act_list):
    '''
    Function that exports a BW database as an Excel file. The Excel file can be 
    used to manually add and comment uncertainty information to be added back to
    the database.

    Parameters
    ----------
    dbdir : str
        Directory in which the database is stored.
    db_name : str
        Name of the database.
    act_list : list
        list of the foreground activities included in the database.

    Returns
    -------
    None.

    '''
        
    import os
    import pandas as pd
    import brightway2 as bw

    directory = os.path.join(dbdir, str(db_name + '.xlsx'))

    db = bw.Database(db_name)

    with pd.ExcelWriter(directory, mode = 'w') as writer:

        col_labels = ['name','amount', 'unit', 'location', 'type', 'database', 'identifier', 'uncertainty type', 
                          'pedigree', 'negative', 'loc', 'scale', 'comment']

        # create a sheet in the Excel file for each activity in the database
        for act_name in act_list:
            
            df = pd.DataFrame(columns = col_labels)

            act = [act for act in db if act['name'] == act_name][0]

            # each dataframe is filled with information about each exchange
            for i in range(len(act.exchanges())):

                exc = list(act.exchanges())[i]

                exc_input_name = exc.input
               
                # get the ecoinvent activity corresponding to the exchange input
                exc_act = bw.Database(exc['input'][0]).get(exc['input'][1])        

                data_dict = {'name': exc_act['name'],
                             'amount': exc['amount'],
                             'unit' : exc['unit'],
                             'location' : exc_act['location'], # is the exchange location the same as the input or else??
                             'type' : exc['type'],
                             'database' : exc['input'][0],
                             'identifier' : exc['input'][1], # expecting ecoinvent ID
                             'uncertainty type' : None, # expecting int
                             'pedigree' : None, # expecting dictionary
                             'negative': None, # expecting True or False
                             'loc' : None, # expecting float
                             'scale': None, # expecting float
                             'comment': None # expecting text
                            }

                df.loc[i] = data_dict.values()

            df.to_excel(writer, sheet_name = act_name) 

    return directory


def Export2Excel (dbdir, rdir, recipe_name):
    
    
    import yaml
    import os
    import pathlib
    
    # create directory to save the Excel files
    result_dir = os.path.join(dbdir,'fg_db')   
    if os.path.exists(result_dir) == False:
    	pathlib.Path(result_dir).mkdir(parents=True, exist_ok=True)
    
    recipe_dir = os.path.join(rdir, recipe_name)
    
    print('Directory: %s' %recipe_dir)
    
    with open(recipe_dir) as file:
       recipe = yaml.load(file, Loader=yaml.FullLoader)
       
    recipe = recipe['input']
    
    for db_name in recipe['databases'].keys(): 
                
        act_list = recipe['databases'][db_name]
        
        Export2ExcelPerDb (result_dir, db_name, act_list)
        
        print('Database %s exported as an Excel file.' %db_name)

            
    
    return 







