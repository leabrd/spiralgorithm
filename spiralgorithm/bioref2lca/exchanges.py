#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 13:46:27 2023

@author: leabraud
"""

def AddExchangeNames (db_name, ei_name):
    
    import brightway2 as bw
    import lca_algebraic as alg
    from tqdm import tqdm
    
        
    act_list = [act for act in bw.Database(db_name)]
    
    for i in tqdm(range(len(act_list))):
    
    
    #for act in bw.Database(db_name):
    
    #print('\nActivity: %s' %act)
    
        for exc in act_list[i].exchanges():
            
            # for "production" exchanges, the name corresponds to the one of the FG activity (i.e. S1A1Cultivation)
            if exc['type'] == 'production':
    
                exc_name = str(exc.input['name']).split('_PARAM')[0]
                
            if exc['type'] == 'technosphere':
                
                # exception for monoammonium phosphate for which activity name != reference product
                if exc.input['name'] == 'monoammonium phosphate production':
                  
                    # get the activity from the ecoinvent database
                    exc2act = [act for act in bw.Database(ei_name) if exc.input['name'] in act['name'] and act['location'] == exc.input['location'] and act['reference product'] == 'nitrogen fertiliser, as N'][0]
                    #print('\n %s' %exc2act)
                    
                    # look into the exchanges of the activity retrieved to find the name
                    for exc2act_exc in exc2act.exchanges():
                        
                        if exc2act_exc['type'] == 'production':
                            exc_name_temp = exc2act_exc['name']
                        else: 
                            'WARNING: The production exchange was not found.'
                            
                    exc_name = exc_name_temp
      
                else: 
                    
                    exc2act = alg.findTechAct(name = exc.input['name'], loc = exc.input['location'])
                    exc_name = [exc['name'] for exc in exc2act.exchanges() if exc['name'] in exc2act['name']][0]
                    
            exc_dataset = exc._document   
            exc_dataset.data.update(name = exc_name)
            exc.save()
            #print('Exchange name: %s' %exc_name)
    
    return 
