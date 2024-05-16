#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 13:23:45 2023

@author: leabraud
"""

def NaturalGasPrice (csv_file, ddir, resdir):
    
    '''
    Data extracted from:
    https://tradingeconomics.com/commodity/eu-natural-gas
    '''
    import os
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy import interpolate
    
    # save the data into a new DataFrame
    df_natural_gas = pd.DataFrame()
    
    # get the name of the fertiliser
    name = csv_file.split('data_')[1].split('.csv')[0]
    
    # Read the CSV file into a pandas DataFrame
    csv_file_dir = os.path.join(ddir, csv_file)
    df = pd.read_csv(csv_file_dir)
    df.columns = ['month', 'price']
    df.sort_values(by = 'month', ascending=True)
    df.sort_values(by = 'price', ascending=True)
    print('Number of rows, columns for %s: %s' %(name, df.shape))
    
    fig, ax = plt.subplots()
    
    # Extract the x and y data from the DataFrame
    x = df['month']
    y = df['price']
    
    # interpolate the data 
    f = interpolate.interp1d(x, y)
    x_new = x
    y_new = f(x_new)
    
    idx = np.argsort(x_new)
    x_new_sorted = x_new[idx]
    
    # add the interpolated data to the DataFrame
    df_natural_gas['month'] = x_new
    df_natural_gas[name] = pd.Series(y_new) # adds "NaN"s to meet the required length
    print(df_natural_gas.shape)

    df_natural_gas.to_excel(str(resdir + '/natural_gas_price_excel.xlsx'), engine='xlsxwriter') 
    
    # Plot the curve
    ax.plot(x_new_sorted, y_new)
    #ax.plot(x, y, 'x', x_new, y_new, '-', label=f'Curve {i+1}')
    
    # Set labels and title
    ax.set_xlabel('Time period from January 2016 to December 2022 [month]')
    ax.set_ylabel('Natural gas price (EU Dutch TTF) [EUR/MWh]')
    
    # Add legend
    #ax.legend(name)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.savefig(str(resdir + '/natural_gas_price.pdf'))
    
    # Show the plot
    plt.show()
    
    
    return df_natural_gas



def BiogasPrice (df_natural_gas, data_dict, resdir):
    
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    
    df_biogas = pd.DataFrame()
    
    # amount of energy produced daily (CH4 in biogas) [kWh/day]
    energy = data_dict['total']['energy']['amount']
    
    df_biogas['month'] = df_natural_gas['month']
    df_biogas['biogas'] = df_natural_gas['natural_gas'].div(1000) * energy

    df_biogas.to_excel(str(resdir + '/biogas_price_excel.xlsx'), engine='xlsxwriter') 
    
    fig, ax = plt.subplots()
    
    x = df_biogas['month']
    y = df_biogas['biogas']
    
    # Plot the curve
    ax.plot(x, y)
    
    # Set labels and title
    ax.set_xlabel('Time period from January 2016 to December 2022 [month]')
    ax.set_ylabel('Economic value of biogas [EUR/day]') # economic value??
    
    # Add legend
    #ax.legend(name)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.savefig(str(resdir + '/biogas_price.pdf'))
    
    # Show the plot
    plt.show()
    
    
    return df_biogas
