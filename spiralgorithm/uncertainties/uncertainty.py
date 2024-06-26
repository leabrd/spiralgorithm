#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 11:47:25 2023

@author: leabraud
"""


def UpdateUncertaintyPerDb (db_name, act_list, xlsx_dir):
    '''
    Function that updates the uncertainty information for each exchange in the 
    foreground database based on the data retrieved from the Excel file.
    The loc and scale are calculated from the data entered by the LCA practitioner
    in the Excel file and added to the database. The pedigree matrix scores are
    not added to the exchange dictionary. The information added are limited to 
    the loc, scale, and negative parameters. 
   
    Parameters
    ----------
    db_name : str
        Name of the database.
    act_list : list
        List of activities for which the uncertainty information needs to be
        updated. Typicall, the list of activities excluded the model activity.
    xlsx_dir : str
        Directory in which the Excel files are stored.
    as_geometric_sigma : boolean
        Add the uncertainty value as standard deviation (sigma) or geometric
        standard deviation (GSD).

    Returns
    -------
    None.

    '''
    import stats_arrays
    import pandas as pd
    import brightway2 as bw
    from pedigree import CalculateLoc, CalculateScale
    from pedigree import BasicUncertainty, AdditionalUncertainty, TotalUncertainty
    
    db = bw.Database(db_name)
    
    # copy the foreground database 
    if str(db_name + '_uncert') in bw.databases: 
        print('The database already exists. Deleleting it.')
        del bw.databases[str(db_name + '_uncert')]
    db_uncert = db.copy(str(db_name + '_uncert'))
    
    
    for act_name in act_list: 
        
        print('\nActivity name: %s' %act_name)
        
        # open the Excel file sheet per sheet i.e. for each activity
        df = pd.read_excel(xlsx_dir, sheet_name = act_name)
        
        # get the activity in the copied database (i.e. the db in which the uncertainty info will be added)
        get_act = [act for act in db_uncert if act['name'] == act_name][0]
        print('Got the activity %s' %get_act)
        # for each row (i.e. for each exchange in the activity)
        for i in range(df.shape[0]):
            
            # get the identifier of the exchange from the Excel file
            exc_id = df.loc[i]['identifier']
            #print('\n>> %s' %exc_id)
            
            # get the exchange
            get_exc_list = [exc for exc in get_act.exchanges() if exc_id in exc.input.key]
            #print('\n%s' %get_exc_list)
            
            if len(get_exc_list)>0: 
                get_exc = get_exc_list[0]
            else: 
                ### TO CHANGE!!
                print('The activity could not be found using the exchange ID. Searching with the name and location.')
                for exc in get_act.exchanges():
                    #print(exc)
                    print('\n')
                    print(exc.input)
                    print(exc.input.key)
                    print(exc['input'])
                get_exc_list = [exc for exc in get_act.exchanges() if str(df.loc[i]['name']) in str(exc.input)]
                print('\n%s' %get_exc_list)
                get_exc = get_exc_list[0]
            
            print('\n%s\n'%get_exc)
            
            # add the uncertainty values
            if df.loc[i]['uncertainty type'] == 2:
                get_exc['uncertainty type'] = stats_arrays.distributions.lognormal.LognormalUncertainty.id
            else:
                print('The uncertainty type was not set to 2 (lognormal)! Check the value in the Excel file!')
                # NEXT LINE TO CHANGE!!
                get_exc['uncertainty type'] = stats_arrays.distributions.lognormal.LognormalUncertainty.id
                
            
            # calculate the loc as ln of the amount
            # the absolute amount was used here to handle the negative values for waste exchanges
            #get_exc['loc'] = np.log(abs(get_exc['amount']))
            get_exc['loc'] = CalculateLoc (get_exc['amount'])
                                    
            # get the pedigree matrix scores for each exchange 
            pg_str = str(df.loc[i]['pedigree'])
            #pg_num = [int(i) for i in pg_str.split(',')]
            basic_uncertainty = BasicUncertainty ()
            additional_uncertainty = AdditionalUncertainty (pg_str)
            total_uncertainty = TotalUncertainty (basic_uncertainty, additional_uncertainty)
            get_exc['scale'] = CalculateScale (total_uncertainty)
        
            # the scale is calculated with the pedigree matrix uncertainty factors
            #get_exc['scale'] = CalculateGSD (pg_num, as_geometric_sigma)
            
            # add the information about negative/positive amount values
            get_exc['negative'] = df.loc[i]['negative']
            
            # check that the modification occured
            print('\nInformation added: \n- uncertainty type: %s \n- loc: %s \n- scale: %s' %(get_exc['uncertainty type'], get_exc['loc'], get_exc['scale']))
            
            # save the exchange
            get_exc.save()

    return


def UpdateUncertainty (rdir, recipe_name, dbdir):
    '''
    Function that updates the uncertainty information for all the foreground
    databases based on the recipe file. 
    
    Parameters
    ----------
    recipe : yml
        YAML file containing the informartion about the databases and activities
        to include in the uncertainty analysis.

    Returns
    -------
    None.

    '''
    import yaml
    import os   
    
    recipe_dir = os.path.join(rdir, recipe_name)
        
    with open(recipe_dir) as file:
       recipe = yaml.load(file, Loader=yaml.FullLoader)
       
    recipe = recipe['input']
    
    for db_name in recipe['databases'].keys(): 
        
        xlsx_dir = os.path.join(dbdir, str('fg_db_uncert/' + db_name + '_uncert.xlsx'))
        
        print('\nUpdating uncertainty information in the database %s' %db_name)
        
        act_list = recipe['databases'][db_name]
        
        UpdateUncertaintyPerDb (db_name, act_list, xlsx_dir)
        
        print('Done!')
    
    
    return