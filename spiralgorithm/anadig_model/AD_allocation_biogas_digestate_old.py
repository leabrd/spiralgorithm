#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 11:16:48 2023

@author: leabraud
"""

import yaml
import io

# open and read the recipe of the AD model
with open('/home/leabraud/Desktop/spiralgorithm/recipes/recipe_allocation.yml', 'r') as stream:
    recipe_allocation = yaml.safe_load(stream)    


def AllocationBiogasDigestate (recipe_allocation, data_dict):
    
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    
    from AD_fertiliser_prices import FertiliserPrices, NPKPrices, DigestatePrice
    from AD_biogas_prices import NaturalGasPrice, BiogasPrice
    
    
    ## PERFORM ECONOMIC ALLOCATION
    if recipe_allocation['input']['biogas/digestate'] == 'economic': 
        
        # calculate the economic value of the daily produced digestate
        csv_files = ['data_urea.csv', 'data_muriate.csv', 'data_DAP.csv']
        
        df_fertilisers = FertiliserPrices (csv_files)
        df_NPK = NPKPrices (df_fertilisers)
        df_digestate = DigestatePrice (df_NPK, data_dict)
        
        # calculate the economic value of the daily produced biogas
        csv_file = 'data_natural_gas.csv'
        df_natural_gas = NaturalGasPrice (csv_file)
        df_biogas = BiogasPrice (df_natural_gas, data_dict)
        
        strategy_list = ['total_100%', 'total_50%', 'total_10%', 'total_0%']
        
        for i in range(len(strategy_list)): 
         
            df = pd.DataFrame()
            df['month'] = df_biogas['month']
            df['biogas'] = df_biogas['biogas']
            df['digestate'] = df_digestate[strategy_list[i]]
            df['alloc_biogas'] =df['biogas'].div(df['biogas'] + df['digestate'])
            df['alloc_digestate'] = df['digestate'].div(df['biogas'] + df['digestate'])
            
            df_plot = df.drop(['biogas', 'digestate'], axis = 1)
            print(df_plot)     
            
            months = np.array(df['month'])
            data_biogas = np.array(df['alloc_biogas'])
            data_digestate = np.array(df['alloc_digestate'])
            
            width = 0.5
            
            fig, ax = plt.subplots()
            
            ax.bar(months, data_biogas, width = width)
            ax.bar(months, data_digestate, bottom = data_biogas, width = width)
            
            ax.set_title("blablabal")
            ax.legend(loc="upper right")
            
            plt.show()
            
            ### save the figures
            ### return the allocation factors for each strategy as function of time 
            # => select the values to use in the LCA calculation
        
        
    return



