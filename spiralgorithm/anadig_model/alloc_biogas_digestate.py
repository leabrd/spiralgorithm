#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 13:16:29 2023

@author: leabraud
"""

import os
import sys

# Set up the directory in which the modules to be loaded are saved
mdir1 = '/home/leabraud/OneDrive/UCD/spiralgorithm/lca_calc'
mdir2 = '/home/leabraud/OneDrive/UCD/spiralgorithm/anadig_model'

for mdir in [mdir1, mdir2]:
    if mdir not in sys.path:
        sys.path.insert(0,mdir)

def AllocationBiogasDigestate (allocation_type, data_dict, ddir):
    
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    
    from price_fertiliser import FertiliserPrices, NPKPrices, DigestatePrice
    from price_biogas import NaturalGasPrice, BiogasPrice
    
    ## PERFORM ECONOMIC ALLOCATION
    if allocation_type == 'economic': 
        
        # calculate the economic value of the daily produced digestate
        csv_files = ['data_urea.csv', 'data_muriate.csv', 'data_DAP.csv']
        
        df_fertilisers = FertiliserPrices (csv_files, ddir)
        df_NPK = NPKPrices (df_fertilisers)
        df_digestate = DigestatePrice (df_NPK, data_dict)
        
        # calculate the economic value of the daily produced biogas
        csv_file = 'data_natural_gas.csv'
        df_natural_gas = NaturalGasPrice (csv_file, ddir)
        df_biogas = BiogasPrice (df_natural_gas, data_dict)
        
        strategy_list = ['total_100%', 'total_50%', 'total_10%', 'total_0%']
        
        
        df_alloc_biogas = pd.DataFrame()
        df_alloc_digestate = pd.DataFrame()
            
        fig, ax = plt.subplots()
        
        for i in range(len(strategy_list)): 
         
            df = pd.DataFrame()
            df['month'] = df_biogas['month']
            df['biogas'] = df_biogas['biogas']
            df['digestate'] = df_digestate[strategy_list[i]]
            df[str('alloc_biogas_' + strategy_list[i])] =df['biogas'].div(df['biogas'] + df['digestate'])
            df[str('alloc_dig_' + strategy_list[i])] = df['digestate'].div(df['biogas'] + df['digestate'])
            
            
            df_alloc_biogas[str('alloc_biogas_' + strategy_list[i])] = df[str('alloc_biogas_' + strategy_list[i])]
            df_alloc_digestate[str('alloc_dig_' + strategy_list[i])] = df['digestate'].div(df['biogas'] + df['digestate'])
            
            months = np.array(df['month'])
            
            alloc_biogas = np.array(df[str('alloc_biogas_' + strategy_list[i])])
            
            ax.plot(months, alloc_biogas, label=strategy_list[i])
            
        # Set labels and title
        ax.set_xlabel('Time period from January 2016 to December 2022 [month]')
        ax.set_ylabel('Allocation factor for biogas')
        
        # Add legend
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend(loc = "lower left")
        
        plt.savefig(str('allocation_factors_biogas.pdf'))

        plt.show()
  
    return df_alloc_biogas
