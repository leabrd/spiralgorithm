# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 09:17:55 2022

@author: leabr
"""

import os

# This is where this file(master_test) is located ...this doesn't change
fpath = os.path.dirname(os.path.abspath(__file__))


def prep_dir(wdir = None, rdir = None, recipe_name = 'default_recipe.yml'):
    
    '''
    Set up the working and project directories, copy the default_recipe to 
    the working directory, create a new "results" file in the working directory.
    
    :param wdir: working directory, defaults to None
    :type wdir: Str, optional
    :param result_directory_name: name of the results folder, defaults to 'results'
    :type result_directory_name: Str, optional
    :return: updated recipe
    :rtype: yaml file

    '''
    
    print('\n --------------\n| SPIRALGORITHM |\n --------------\n')

    print('\n> PREPARATION:\n  ------------')
    
    from shutil import copyfile
    import yaml
    import pathlib
    
    #-------------------------------------------------------------------------
    # DEFINE THE WORKING DIRECTORY IF NOT ALREADY DONE
    
    # the working directory should be entered in the spiralgorithm.py file
    if not wdir:   
        wdir = input('Please enter working directory: ')
    print('Working directory:', wdir)    
        
    #-------------------------------------------------------------------------       
    # DEFINE THE PROJECT DIRECTORY
        
    # the project directory has to be the same as the working directory
    # the directory has to be changed before importing the BW2 module
    # If not, the installation of the BW2 module sets a default dir that cannot be changed later on
    pdir =  os.path.join(wdir,'projects')    
    
    pathlib.Path(pdir).mkdir(parents=True, exist_ok=True)
    os.environ['BRIGHTWAY2_DIR'] = pdir
    
    print('Project directory:', os.environ['BRIGHTWAY2_DIR'])
        
    #-------------------------------------------------------------------------
    # COPY DEFAULT_RECIPE TO THE WORKING DIRECTORY    
    
    # the recipe directory should be entered in the spiralgorithm.py file
    if not rdir:
        rdir = input('Please enter recipe directory: ')
    print('Recipe directory:', rdir)    
        
    # load default recipe, this location shouldn't change
    default_recipe_dir = os.path.join(rdir, recipe_name)
    
    # new directory for the copy of default_recipe, in the working directory
    new_recipe_dir = os.path.join(wdir,recipe_name)
    
    # copy to work directory and return new loaction
    copyfile(default_recipe_dir, new_recipe_dir)
        
    #-------------------------------------------------------------------------    
    # CREATE A RESULTS FOLDER IN THE WORKING DIRECTORY
    
    # create a 'results' directory   
    result_dir = os.path.join(wdir,'results')   
    if os.path.exists(result_dir) == False:
    	pathlib.Path(result_dir).mkdir(parents=True, exist_ok=True)
    
    # create sub-folders for each type of analysis (if they do not already exist)
 
    result_dir_CA_subsystem = os.path.join(result_dir,'CA_subsystem')  
    if os.path.exists(result_dir_CA_subsystem) == False:
    	pathlib.Path(result_dir_CA_subsystem).mkdir(parents=True, exist_ok=True)

    result_dir_CA_activity = os.path.join(result_dir,'CA_activity')
    if os.path.exists(result_dir_CA_activity) == False: 
    	pathlib.Path(result_dir_CA_activity).mkdir(parents=True, exist_ok=True)
    
    result_dir_CA_input_category = os.path.join(result_dir,'CA_input_category')  
    if os.path.exists(result_dir_CA_input_category) == False: 
    	pathlib.Path(result_dir_CA_input_category).mkdir(parents=True, exist_ok=True)
    
    #-------------------------------------------------------------------------    
    # OPEN, READ, AND WRITE IN THE RECIPE COPIED TO THE WORKING DIRECTORY
    
    with open(new_recipe_dir) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        recipe = yaml.load(file, Loader=yaml.FullLoader)
    
    # write the directories in the recipe          
    recipe['input']['wdir'] = wdir
    recipe['input']['pdir'] = pdir
    recipe['input']['rdir'] = result_dir
    recipe['input']['recipe_dir'] = new_recipe_dir
    
    # open the file and make it readable
    with open(new_recipe_dir,'w') as file:
        yaml.dump(recipe,file)
    
    # remove the 'input' from the recipe dictionary
    recipe = recipe['input']
    
    return recipe



def import_databases(recipe, wdir):
      
    '''
    Import the databases in the brightway project.
    
    :param recipe: YAML file containing all the information to conduct the LCA analysis
    :type recipe: yaml file
    :param wdir: working directory
    :type wdir: working directory
    :return: updated recipe
    :rtype: yaml file

    '''
    print('\n\n> INITIATE LCA ANALYSIS:\n  ----------------------')
    
    #-------------------------------------------------------------------------    
    # CHOOSE OR CREATE A NEW WORKING PROJECT
    
    from project import project  
    recipe = project(recipe)
    
    #-------------------------------------------------------------------------    
    # IMPORT BIOSPHERE 3 AND ECOINVENT 3.6 IF NOT ALREADY IMPORTED
    
    from databases import background_db
    recipe = background_db(recipe,wdir)
    
    #-------------------------------------------------------------------------    
    # IMPORT FOREGROUND DATABASE
    
    from databases import foreground_db
    recipe = foreground_db(recipe, wdir)
    
    return recipe
    


def run (recipe, wdir, dataset_file_directory):
    
    ## CALCULATE THE LCA SCORES PER SUBSYSTEM   
    from lca_scores_per_subsystem import dict_LCA_score_per_subsystem
    from CA_subsystems import relative_stacked_bar_plot_CA_subsystem
    from CA_subsystems import bar_chart_CA_subsystems_specific_IC,diff_LCA_scores_CA_subsystem
    
    # create the nested dictionary with the LCA results 
    LCA_scores_dict_subsystem, recipe = dict_LCA_score_per_subsystem (recipe)
 
    
    # plot relative stacked bar plot to show contribution of each subsystem
    relative_stacked_bar_plot_CA_subsystem (recipe, LCA_scores_dict_subsystem)
    diff_LCA_scores_CA_subsystem(recipe)
    # plot bar chart to show contribution of each subsystem to specific IC 
    bar_chart_CA_subsystems_specific_IC (recipe, LCA_scores_dict_subsystem)
    
    ## CALCULATE THE LCA SCORES PER PROCESS
    from lca_scores_per_process import dict_LCA_score_per_process
    from CA_processes import relative_stacked_bar_plot_CA_process
    from CA_processes import pie_chart_stacked_bar_plot
    from CA_activity import stacked_bar_plot_comparison

    LCA_scores_dict_processes, recipe = dict_LCA_score_per_process (recipe)
    
    relative_stacked_bar_plot_CA_process (recipe, LCA_scores_dict_processes)
    
    pie_chart_stacked_bar_plot (LCA_scores_dict_processes, recipe)
    
    stacked_bar_plot_comparison (recipe, LCA_scores_dict_processes)
    
    ### CALCULATE THE LCA SCORES PER INPUT CATEGORY
    from lca_scores_per_input_category import dict_LCA_score_per_input_category
    from CA_input_category import stacked_bar_plot_input_category
    from CA_input_category import heatmap_input_category
    
    LCA_scores_dict_category = dict_LCA_score_per_input_category(recipe, dataset_file_directory)
    stacked_bar_plot_input_category (recipe, LCA_scores_dict_category)
    heatmap_input_category (recipe, LCA_scores_dict_category)
    
    
    ### ALLOCATION
    from lca_scores_allocation import dict_LCA_score_allocation
    LCA_scores_dict_allocation = dict_LCA_score_allocation(recipe)
    
        
    return recipe



def write_recipe(recipe,reset = False):
    
    '''Rewrite the recipe with the most recent data. If reset = True, it puts the 
    input back at the top of the file.
    Save the last version of the recipe'''
    
    import yaml
    
    recipe_dir = recipe['recipe_dir']
                  
    if reset:
        new_recipe = {}
        new_recipe['input'] = recipe
    else:
        new_recipe = recipe
    
    with open(recipe_dir,'w') as file:
        yaml.dump(new_recipe,file)
    print('\nUpdated recipe saved to %s.' % recipe['recipe_dir'])
    
    
