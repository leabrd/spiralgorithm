# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 09:28:13 2022

@author: leabr
"""

'''
Function to set up the working project i.e. directory.
'''


def project(recipe):
    
    '''
    Choose a project to work in among existing projects or create a new project.
    Write the name of the chosen project into the recipe.
    Returns the updated recipe.
    
    :param recipe: YAML file containing all the information to conduct the LCA analysis
    :type recipe: yml file
    :raises Exception: DESCRIPTION
    :return: updated recipe
    :rtype: yml file

    '''    
    
    from brightway2 import projects

    print('\n>>> BW2 PROJECT:')
    
    print('\nCurrent project directory: %s \n%s' % (projects.dir,projects))

    answer = input('Create a new project? y/[n]: ') or 'n'
    
    if answer == 'y':
        
        project_name = str(input ('Name of the new project: '))
        
        if project_name in projects:
           
            # Quick fix - put in while loop here to loop back to input
            raise Exception('This project already exist, choose another name!')
        
        else:
            projects.create_project(project_name)
            projects.set_current(project_name)
            #bw.config.p['lockable'] = True
            print('Current project: %s  \nLocation: %s' %  (projects.current,projects.output_dir))
    
    else:
        default_name = 'default'
        project_name = input ('Choose a working project [%s]: ' % default_name) or default_name 
        
        if project_name in projects:
            projects.set_current(project_name)
            print('\nCurrent project: %s' % projects.current)
       
        else: 
            raise Exception('The name does not correspond to any existing projects.')
        
        
    recipe['project'] = projects.current
    
    return recipe