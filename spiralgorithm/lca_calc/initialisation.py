# -*- coding: utf-8 -*-

"""
Created on Mon Feb 21 09:07:19 2022

@author: leabr
"""

'''
Run this file to do a LCA study of an algae system. The foreground databases
are imported as BW2Package files according to the information from the recipe
(YAML file).
'''


# the "master" is the main code which calls the functions in the slave files
from master import prep_dir, import_databases, run

# Set the working directory (this needs to be changed manually)
wdir = '/home/leabraud/lca_spiralg/lca'

# Set the directory for the Excel file containing the ecoinvent 3.6 datasets and input categories
ddir = '/home/leabraud/lca_spiralg/ecoinvent_datasets.xlsx'


# Prepare the recipe i.e. instructions to do the analysis, create a new results folder
recipe = prep_dir (wdir = wdir, result_directory_name = 'results')
recipe = import_databases (recipe, wdir)

# Do the LCA analysis and save the results into the results folder
recipe = run (recipe, wdir, ddir)
