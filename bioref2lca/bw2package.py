# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 15:52:03 2022

@author: leabr
"""

def GetEcoinventDatasets (ei_datasets_file_dir):

    '''
    Function that get the name and location of the datasets to get from the 
    ecoinvent database based on a Excel file.
    
    :param dataset_file_name: DESCRIPTION, defaults to 'ecoinvent_datasets_test.xlsx'
    :type dataset_file_name: TYPE, optional
    :return: DESCRIPTION
    :rtype: TYPE

    '''
    import pandas as pd
            
    ds_dict = {} # create a new dictionary to store the ecoinvent datasets to get
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


def CreateForegroundDatabase (wdir, project_name, comparison_dict_per_FU, ei_datasets_file_dir, database_name):
    
    import pathlib, os
    from brightway2 import projects, databases, Database
    from brightway2 import bw2setup, SingleOutputEcospold2Importer
    from bw2io import BW2Package
        
    # DEFINE WORKING AND PROJECT DIRECTORIES
    pdir =  os.path.join(wdir,'projects')    
    pathlib.Path(pdir).mkdir(parents=True, exist_ok=True)
    os.environ['BRIGHTWAY2_DIR'] = pdir
    print('\nProject directory:', os.environ['BRIGHTWAY2_DIR'])
    
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
    ei36dir = os.path.join('/home/leabraud/Desktop/databases/ecoinvent_3.6_cut-off_ecoSpold02_complete/datasets')
    if 'ecoinvent_3.6_cutoff' in databases:
        print('ecoinvent_3.6_cutoff has already been imported')
    else:
        ei36 = SingleOutputEcospold2Importer(ei36dir, 'ecoinvent_3.6_cutoff',use_mp=False) # Import Ecoinvent from a SPOLD file dowloaded from the website
        ei36.apply_strategies()
        ei36.statistics()
        ei36.write_database() 
        
    ei = Database('ecoinvent_3.6_cutoff')
    
    print('\nbiosphere3 and ecoinvent background databases imported.')
    
    # GET THE EI36 DATASETS FROM THE EXCEL FILE
    ds_dict = GetEcoinventDatasets(ei_datasets_file_dir)
        
    # GET THE BIOREFINERY DATASET WITH ALL THE SCENARIOS WITHOUT BIOMASS FLOWS
    biomass_names = ['fg_input','ref_flow','coproduct','losses', 'recirculated']
    
    my_db_list = []
        
    for scenario in comparison_dict_per_FU.keys():

        # CREATE NEW FOREGROUND DATABASE
        my_db_name = database_name + str(scenario)
        if my_db_name in databases: 
            print('\nThe foreground database "%s" already exists; overwriting it!' %my_db_name)
            del databases[my_db_name]
        my_db = Database(my_db_name)
        data_dict = {}
        my_db.write(data_dict)
        
        ei_exc_list = [] # list of the ecoinvent activities that have already been retrieved
        
        for act_bioref in comparison_dict_per_FU[scenario].keys():
            
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
        
            for exc in comparison_dict_per_FU[scenario][act_bioref].keys():
                
                print('\nExchange: %s' %exc)
                
                if comparison_dict_per_FU[scenario][act_bioref][exc]['type'] in biomass_names:
                    
                    print('Biomass flow: %s' %comparison_dict_per_FU[scenario][act_bioref][exc]['type'])
                    print('Not included in the LCA model.')
                    print('Pass!')
                    pass
                
                elif comparison_dict_per_FU[scenario][act_bioref][exc]['type'] == 'emission':
                    
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
                            amount = comparison_dict_per_FU[scenario][act_bioref][exc]['amount'],
                            unit = comparison_dict_per_FU[scenario][act_bioref][exc]['unit'],
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
                            amount = comparison_dict_per_FU[scenario][act_bioref][exc]['amount'],
                            unit = comparison_dict_per_FU[scenario][act_bioref][exc]['unit'],
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