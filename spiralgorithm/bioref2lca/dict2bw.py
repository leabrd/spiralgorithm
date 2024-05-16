#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 11:13:00 2023

@author: leabraud
"""


def GetEcoinventDatasets (ei_datasets_file_dir):
    '''
    Function that gets the name and location of the datasets to retrieve from the 
    ecoinvent database based on the information contained in the Excel file.
    The function gets the datasets of all the activities included in the file.

    Parameters
    ----------
    ei_datasets_file_dir : str
        Directory of the Excel file with the information regarding the ecoinvent
        datasets used in the study.

    Returns
    -------
    ds_dict : dict
        Dictionary of the ecoinvent datasets retrieved.

    '''

    import pandas as pd
            
    ds_dict = {} # create a new dictionary to store the ecoinvent datasets to retrieve
    df = pd.read_excel(ei_datasets_file_dir) # convert the Excel file into a dataframe
    ds_temp_dict = df.to_dict(orient = 'index') # convert the dataframe into a temporary dictionary

    for i in range(len(ds_temp_dict.keys())): # for each foreground activity listed
                    
        if ds_temp_dict[i]['ecoinvent dataset'] not in ds_dict.keys():
                                                
            ds_dict[ds_temp_dict[i]['short name']] = {}
            ds_dict[ds_temp_dict[i]['short name']]['dataset name'] = ds_temp_dict[i]['ecoinvent dataset']
            ds_dict[ds_temp_dict[i]['short name']]['location'] = ds_temp_dict[i]['location']
            ds_dict[ds_temp_dict[i]['short name']]['unit'] = ds_temp_dict[i]['unit']
            ds_dict[ds_temp_dict[i]['short name']]['database'] = ds_temp_dict[i]['database']
    
    print('\nExtraction of the Ecoinvent dataset references: %s/%s unique datasets extracted from the Excel file.' %(len(ds_dict.keys()), len(ds_temp_dict.keys())))
   
    return ds_dict



def CreateForegroundDatabase (wdir, project_name, ei_name, eidir, comparison_dict, ei_datasets_file_dir, database_name, PerSubsystem = False):
    '''
    Function that converts the data dictionaries obtained from the python models 
    (e.g. biorefinery model) into BW2Package files and Excel files. 
    
    => THE FUNCTION RELIES ON THE USE OF ECOINVENT 3.6: UPDATE TO ANY VERSION

    Parameters
    ----------
    wdir : str
        Working directory.
    project_name : str
        Name of the BW2 project in which the databases will be created.
    comparison_dict_per_FU : dict
        Nested dictionary of data built as follows: subsystem > tech period > act.
        Can be scaled or not as long as the structure of the dict remains the same.
    ei_datasets_file_dir : TYPE
        DESCRIPTION.
    database_name : TYPE
        DESCRIPTION.
    PerSubsystem: boolean
        If True, the function creates databases per subsystem and a general database.
        If False, the function only creates a general database in which the activities
        of each subsystem are all at the same level and only differentiate by their
        name (i.e. no subdivision).

    Returns
    -------
    my_db_list : TYPE
        DESCRIPTION.

    '''    
    import pathlib, os
            
    # DEFINE WORKING AND PROJECT DIRECTORIES
    pdir =  os.path.join(wdir,'projects')    
    pathlib.Path(pdir).mkdir(parents=True, exist_ok=True)
    os.environ['BRIGHTWAY2_DIR'] = pdir
    print('\nProject directory:', os.environ['BRIGHTWAY2_DIR'])

    from brightway2 import projects, databases, Database
    from brightway2 import bw2setup, SingleOutputEcospold2Importer
    from bw2io import BW2Package
    ## add option to export datasets as Excel file
    from bw2io.export.excel import CSVFormatter, create_valid_worksheet_name
    from bw2io.export.csv import reformat
    import xlsxwriter
    
    # CREATE/ACTIVATE NEW BW PROJECT
    if project_name not in projects:
        projects.create_project(project_name)
        projects.set_current(project_name)
    else: 
        print('\nThe project already exists; it was not changed, just activated!')
        projects.set_current(project_name)
    print('\nCurrent project: %s' % projects.current)
    
    # IMPORT BIOSPHERE 3
    if 'biosphere3' in databases:
        print('biosphere3 has already been imported in the project.')
    else:
       bw2setup()
    
    # IMPORT ECOINVENT
    if ei_name in databases:
        print('%s has already been imported' %ei_name)
    else:
        ei3x = SingleOutputEcospold2Importer(eidir,ei_name,use_mp=False) # Import Ecoinvent from a SPOLD file dowloaded from the website
        ei3x.apply_strategies()
        ei3x.statistics()
        ei3x.write_database() 
        
    ei = Database(ei_name)
    
    print('\nbiosphere3 and ecoinvent background databases imported.')
    
    # GET THE EI36 DATASETS FROM THE EXCEL FILE
    ds_dict = GetEcoinventDatasets(ei_datasets_file_dir)
        
    # GET THE BIOREFINERY DATASET WITH ALL THE SCENARIOS WITHOUT BIOMASS FLOWS
    biomass_names = ['fg_input','ref_flow','coproduct','losses', 'recirculated']
    
    my_db_list = []
    
    for scenario in comparison_dict.keys():

        # CREATE NEW FOREGROUND DATABASE
        my_db_name = str('db_' + database_name + str(scenario)) ### LINE WAS CHANGED
        if my_db_name in databases: 
            print('\nThe foreground database "%s" already exists; overwriting it!' %my_db_name)
            del databases[my_db_name]
        my_db = Database(my_db_name)
        data_dict = {}
        my_db.write(data_dict)
        
        ei_exc_list = [] # list of the ecoinvent activities that have already been retrieved
        
        for act_bioref in comparison_dict[scenario].keys():
            
            print('\nActivity: %s'%act_bioref)
            print('---------')
            
            # CREATE A NEW ACTIVITY IN THE FOREGROUND DB 
            for act_foreground in my_db:
                if act_bioref in act_foreground['name']:
                    print('The activity already exists => overwriting it!') 
            
            new_act = my_db.new_activity(
                code = str('code_' + act_bioref),
                name = act_bioref,
                unit = 'unit'
                )
            
            new_act.save()
            
            ## MAKE SURE THE ACTIVITY CONTAINS NO EXCHANGES
            for exc in new_act.exchanges():
                exc.delete()
                new_act.save()
            
            print('\nActivity %s created in the foreground database.' %act_bioref)
            
            
            ### CREATE A PRODUCTION EXCHANGE PER ACTIVITY
            print('\nExchange: Production')
            print('The production exchange is arbitrary. Each activity produces itself.')
            
            prod_exc = new_act.new_exchange(
                input = new_act.key,
                amount = 1,
                unit = 'unit',
                categories='',
                type = 'production'
                #formula = M
                )
            prod_exc.save()
            new_act.save()
            print('Done!')
            
            # ADD THE EXCHANGES TO THE ACTIVITY
        
            for exc in comparison_dict[scenario][act_bioref].keys():
                
                print('\nExchange: %s' %exc)
                
                if comparison_dict[scenario][act_bioref][exc]['type'] in biomass_names:
                    
                    print('Biomass flow: %s' %comparison_dict[scenario][act_bioref][exc]['type'])
                    print('Not included in the LCA model.')
                    print('Pass!')
                    pass
                
                elif comparison_dict[scenario][act_bioref][exc]['type'] == 'emission':
                    
                    print('Biosphere flow; ignored for now.')
                    print('Pass!')
                    pass
                
                else: 
                
                    # GET THE ACTIVITY IN ECOINVENT IF NOT ALREADY DONE
                    if exc not in ei_exc_list: # if the exchange is not in the list, get it 
                    
                        print('The activity %s is retrieved from the ecoinvent database.' %exc)
                        
                        name = ds_dict[exc]['dataset name']
                        print('Name: %s' %name)
                        location = ds_dict[exc]['location']
                        print('Location: %s' %location)
                        unit = ds_dict[exc]['unit']
                        print('Unit: %s' %unit)
                        db_name = ds_dict[exc]['database']
                        print('Database name: %s' %db_name)
                        
                        ei_act = [exc for exc in ei if name == exc['name'] and location == exc['location'] and unit == exc['unit']][0]
                        
                        ei_exc_list.append((exc, ei_act)) # the ecoinvent activity that was retrieved is added to the list in a tuple (short name, ei act)
                        print('Done!')
                        
                        # ADD THE EXCHANGE TO THE ACTIVITY
                        new_exc = new_act.new_exchange(
                            input = ei_act.key,
                            amount = comparison_dict[scenario][act_bioref][exc]['amount'],
                            unit = comparison_dict[scenario][act_bioref][exc]['unit'],
                            type = 'technosphere',
                            #formula = M
                            )
                        
                        new_exc.save()
                        new_act.save()
                    
                    # IF ALREADY DONE, GET THE INFO THAT WERE ALREADY RETRIEVED
                    elif exc in ei_exc_list: 
                        
                        print('\nThe exchange %s was already retrieved from the ecoinvent database.' %exc)
                        for i in range(len(ei_exc_list)):
                            if ei_exc_list[i][0] == exc:
                                ei_act = ei_exc_list[i][1]
                                
                        # ADD THE EXCHANGE TO THE ACTIVITY
                        new_exc = new_act.new_exchange(
                            input = ei_act.key,
                            amount = comparison_dict[scenario][act_bioref][exc]['amount'],
                            unit = comparison_dict[scenario][act_bioref][exc]['unit'],
                            type = 'technosphere',
                            #formula = M
                            )
                        
                        new_exc.save()
                        new_act.save()
        
        ## CREATE A MODEL ACTIVITY
        print('\nCreating the biorefinery model activity for LCA calculations..')
        
        act_name = str('model_'+ my_db_name)
        for act in my_db:
            if act_name in act['name']:
                print('The activity already exists => overwriting it!') 
                
        new_act = my_db.new_activity(
            code = str('code_' + act_name),
            name = act_name,
            unit = 'unit'
            )
        
        new_act.save()
        
        ## MAKE SURE THE MODEL ACTIVITY CONTAINS NO EXCHANGES
        for exc in new_act.exchanges():
            exc.delete()
            new_act.save()
        
        print('Done!')
        
        ### CREATE A PRODUCTION EXCHANGE IN THE MODEL ACTIVITY
        print('\nExchange: Production')
        print('The production exchange is arbitrary. Each activity produces itself.')
        
        prod_exc = new_act.new_exchange(
            input = new_act.key,
            amount = 1,
            unit = 'unit',
            categories='',
            type = 'production'
            #formula = M
            )
        prod_exc.save()
        new_act.save()
        print('Done!')
                
        ## CREATE ONE EXCHANGE PER BIOREF ACTIVITY IN THE MODEL
        for act in my_db:
            
            if act != new_act:
    
                new_exc = new_act.new_exchange(
                    input = act.key,
                    amount = 1,
                    unit = 'unit',
                    type = 'technosphere')
                
                new_exc.save()
                new_act.save()
       
            else:
                continue
            
        ## CHECK THE ACTIVITIES IN THE FOREGROUND DATABASE
        for act in my_db:
            print('\n')
            print(act)
            for exc in act.exchanges():
                print(exc)
                print('Type: %s' %exc['type'])
        
        print('\nBiorefinery model for LCA completed.')
        
        ## EXPORT THE DATBASE IN THE NATIVE BRIGHTWAY 2 FORMAT
        BW2Package.export_obj(obj = my_db, filename = my_db_name, folder = wdir + '/databases')
        #BW2Package.export_obj(obj = my_db, filename = my_db_name, folder = '/home/leabraud/Desktop/databases')
        print('\nDatabase %s exported as BW2Package file.'%my_db_name)
        print('Directory: %s'%(wdir + '/databases'))
        
        my_db_list.append(my_db)
                
    return my_db_list  
