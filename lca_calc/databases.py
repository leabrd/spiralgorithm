# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 09:33:20 2022

@author: leabr
"""

'''
This file contains the functions to import foreground and background databases 
into the working project. The foreground database includes the system directly 
studied i.e. for which data were collected. The backrgound databases includes
 ecoinvent or biosphere3.
'''

def foreground_db(recipe, wdir):
    
    '''
    This function imports the foreground database(s) if not already imported in 
    the working project. It returns the recipe
    
    :param recipe: YAML file containing all the information to conduct the LCA analysis.
    :type recipe: yml
    :param wdir: Working directory
    :type wdir: str
    :param db_name: Name of the foreground database
    :type db_name: str
    :return: recipe
    :rtype: yml

    '''
        
    import os
    from brightway2 import BW2Package, databases
       
    for db_name in recipe['all_databases'].keys():
        
        print('\n>>> IMPORT FOREGROUND DATABASE: %s \n' %db_name.upper())
        
        foreground_db_dir = os.path.join(wdir.strip('lca'),'databases/%s.bw2package' %db_name) #databases in Desktop directly
        
        print(foreground_db_dir)
        
        BW2Package.import_file(foreground_db_dir)
    
    
    print('\n\n All the background and foreground databases were imported. \n\n', databases)   

    
#    if db_name in databases:
        
        #print('%s has already been imported in the project.' %db_name)
    
    #else: 
    
#        #foreground_db_dir = os.path.join(wdir,'databases\\%s.bw2package' %db_name) #databases inside the results folder...
#        foreground_db_dir = os.path.join(wdir.strip('lca'),'databases\\%s.bw2package' %db_name) #databases in Desktop directly
#        BW2Package.import_file(foreground_db_dir)
        
    return recipe



def background_db(recipe, wdir):
    '''
    This function imports the background databases ecoinvent and biosphere3
    if there are not already imported in the working project.
    
    :param recipe: YAML file containing all the information to conduct the LCA analysis.
    :type recipe: yml
    :param wdir: Working directory
    :type wdir: str
    :return: recipe
    :rtype: yml

    '''
    
    import os
    from brightway2 import databases
    from bw2io import bw2setup
    
    #-----------------------------------------------------------------   
    '''Checking for biosphere3 and import it if not in the project'''
     
    print('\n>>> IMPORT BIOSPHERE 3:\n')


    if 'biosphere3' in databases:
        print('biosphere3 has already been imported in the project.')
    
    else:
       # Import and write the biosphere3 database  
       bw2setup()
       
    #-----------------------------------------------------------------   
    '''Checking if ecoinvent 3.6 cutoff in the project and import it if not.'''
    
    from  bw2io import SingleOutputEcospold2Importer
        
    print('\n>>> IMPORT ECOINVENT 3.6:\n')
   
    #ei36dir = os.path.join(wdir,'databases\\ecoinvent_3.6_cut-off_ecoSpold02_complete\\datasets')
    #ei36dir = os.path.join(os.path.dirname(wdir),'databases/ecoinvent_3.6_cut-off_ecoSpold02_complete/datasets')
    ei36dir = os.path.join(wdir,'databases/ecoinvent_3.6_cut-off_ecoSpold02_complete/datasets')
    print(ei36dir)

    if 'ecoinvent_3.6_cutoff' in databases:
        print("ecoinvent_3.6_cutoff has already been imported")
    
    else:
        ei36 = SingleOutputEcospold2Importer(ei36dir, 'ecoinvent_3.6_cutoff',use_mp=False) # Import Ecoinvent from a SPOLD file dowloaded from the website
         #added use_mp=False to avoid the use of multiprocessing
        ei36.apply_strategies()
        ei36.statistics()
        ei36.write_database() # Write the database in the project
    
    return recipe
