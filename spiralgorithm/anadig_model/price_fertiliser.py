#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 13:20:26 2023

@author: leabraud
"""

def FertiliserPrices (csv_files, ddir, resdir):
    '''
    Function that plots the price of urea, muriate of potash, and diammonium 
    phosphate for the period January 2016 - December 2023. The data were extracted
    from the graph presented on the following website, using WebPlotDigitizer:
    https://blogs.worldbank.org/opendata/fertilizer-prices-ease-affordability-and-availability-issues-linger.
    The prices are expressed in USD per metric ton of fertiliser.
    '''
    import os
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy import interpolate
    
    # save the data into a new DataFrame
    df_fertilisers = pd.DataFrame()
    
    # Create a figure and axis
    fig, ax = plt.subplots()

    # Iterate over the CSV files and plot the curves
    for i, csv_file in enumerate(csv_files):
        
        # get the name of the fertiliser
        name = csv_file.split('data_')[1].split('.csv')[0]
        
        # Read the CSV file into a pandas DataFrame
        csv_file_dir = os.path.join(ddir, csv_file)
        print(csv_file_dir)
        df = pd.read_csv(csv_file_dir)
        df.columns = ['month', 'price']
        print('Number of rows, columns for %s: %s' %(name, df.shape))
        
        # Extract the x and y data from the DataFrame
        x = df['month']
        y = df['price']
        
        # interpolate the data 
        f = interpolate.interp1d(x, y)
        x_new = x
        y_new = f(x_new)
        
        # add the interpolated data to the DataFrame
        df_fertilisers['month'] = x_new
        df_fertilisers[name] = pd.Series(y_new) # adds "NaN"s to meet the required length
        print(df_fertilisers.shape)

        df_fertilisers.to_excel(str(resdir + '/fertiliser_price_excel.xlsx'), engine='xlsxwriter') 

        
        # Plot the curve
        ax.plot(x_new, y_new, label=f'Curve {i+1}')
        #ax.plot(x, y, 'x', x_new, y_new, '-', label=f'Curve {i+1}')
        
    # Set labels and title
    ax.set_xlabel('Time period from January 2016 to December 2022 [month]')
    ax.set_ylabel('Fertiliser price [USD/mt]')
    
    # Add legend
    ax.legend(['Urea', 'Muriate of potash', 'Diammonium phosphate'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.savefig(str(resdir + '/fertiliser_price.pdf'))
    
    # Show the plot
    plt.show()
    
    
    return df_fertilisers




def NPKPrices (df_fertilisers, resdir):
    
    # calculate the price of N from the price of urea
    # extract values  (i.e. in table or figure)
    # get the minium and maximum
    # how much does the price vary => how much do the allocation factors vary
    # the values are in USD/T (short ton) and would require to be converted
    # since all the economic values are in USD/T, we keed them in that unit
    
    # calculate the price per m3 of digestate based on the composition given
    #  by the mass balance and energy code.
    
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    
    # store the data in a new dataframe
    df_NPK = pd.DataFrame()
    df_NPK['month'] = df_fertilisers['month']
    
    '''
    https://extension.wvu.edu/agriculture/pasture-hay-forage/soil-water/calculating-the-value-of-nutrients-in-fertilizers
    '''
           
    # calculate the N content of urea (46-0-0)
    M_C = 12.011 # molecular weight of carbon [g/mol]
    M_H = 1.00797 # molecular weight of hydrogen [g/mol]
    M_N = 14.0067 # molecular weight of nitrogent [g/mol]
    M_O = 15.9994 # molecular weight of oxygen [g/mol]
    M_CH4N2O = M_C + M_H*4 + M_N*2 + M_O # molecular weight of urea [g/mol]
    N_CH4N2O = (M_N*2) / M_CH4N2O * 100 # percentage of N in urea [%]
    N_CH4N2O = 46 # assumed for now
    '''
    On commercial websites, the value of 46% N in urea is common.
    '''

    # calculate the P205 content of DAP (18-46-0)
    M_P = 30.974 # molecular weight of phosphorus [g/mol]
    M_NH42HPO4 = M_N*2 + M_H*8 + M_H + M_P + M_O*4 
    P205_NH42HPO4 = (M_P*2 + M_O*5) / M_NH42HPO4 * 100
    N_NH42HPO4 = M_N*2 / M_NH42HPO4 * 100 
    P205_NH42HPO4 = 46 # assumed for now
    '''
    ACcording to commercial websites, the P2O5 composition of DAP is 46% (and
    18% of N). These values are far from the one found when performing the 
    molar mass calculations. 
    '''
    
    # calculate the K20 content of muriate of potash (MOP) = potassium chloride
    M_K = 39.0983 # molecular weight of K [g/mol]
    M_Cl = 35.453 # molecular weight of Cl [g/mol] 
    M_KCl = M_K + M_Cl # molecular weight of KCl [g/mol]
    K_KCl = M_K / M_KCl * 100 # percentage of K in KCl [%]
    K20_KCl = 60
    '''
    Here we find that there is 52% of K in KCl while on commercial websites, 
    the value of 60% K in MOP is common:
    https://www.eurochem-na.com/product/mop-60k-muriate-of-potash/    
    https://www.cropnutrition.com/resource-library/what-is-potash
    '''
    
    # Calculate the price of N, P205, and K20 and store the values in the dataframe
    df_NPK['N'] = df_fertilisers['urea'].div(100/N_CH4N2O)
    df_NPK['P205'] = df_fertilisers['DAP'].div(100/P205_NH42HPO4)
    df_NPK['K20'] = df_fertilisers['muriate'].div(100/K20_KCl)
    
    # plot the prices of NPK (USD/mt) for N, P205, K20
    df_NPK_plot = df_NPK
    df_NPK_plot = df_NPK_plot.drop(['month'], axis = 1)

    df_NPK_plot.to_excel(str(resdir + '/NPK_price_excel.xlsx'), engine='xlsxwriter') 

    
    # Create a figure and axis
    fig, ax = plt.subplots()
    x = df_NPK['month']
    
    for i in range(len(df_NPK_plot.columns)): 
        
        nutrient = df_NPK_plot.columns[i]
        
        y = df_NPK_plot[nutrient]
        # Plot the curve
        ax.plot(x, y, label=f'Curve {i+1}')
    
    # Set labels and title
    ax.set_xlabel('Time period from January 2016 to December 2022 [month]')
    ax.set_ylabel('NPK price [USD/mt]')
    
    # Add legend
    ax.legend(df_NPK_plot.columns)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.savefig(str(resdir + '/NPK_price.pdf'))

    # Show the plot
    plt.show()

    return df_NPK

    
 
def DigestatePrice (df_NPK, data_dict, resdir):
    
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
      
    ''' 
    In the fertiliser industry, the nutrient content is often reported as NPK.
    N is expressed as %N, P as %P2O5 (phosphate != phosphorous), and K as %K2O
    (potash != potassium). P2O5 and K20 need to be converted into P and K. 
    The most common form of P fertiliser is monoammonium phosphate (NH4H2PO4) in
    which P is present in the form PO4. 
    '''
    
    # create a dataframe to store the data
    df_digestate = pd.DataFrame()
    
    # get the NPK content of the digestate from the data dict
    N = data_dict['total']['N']['amount'] # amount of N [kg/day]
    P2O5 = data_dict['total']['P2O5']['amount'] # amount of P2O5 [kg/day]
    K2O = data_dict['total']['K2O']['amount'] # amount of K2O [kg/day]
    
    # build a dataframe in which the column columns correspond to the economic 
    # value of the daily production of N, P205, and K20
    df_digestate['month'] = df_NPK['month']
    df_digestate['N'] = df_NPK['N'].div(1000)*N # price of total N produced [USD/day]
    df_digestate['P205'] = df_NPK['P205'].div(1000)*P2O5 # price of total P205 produced [USD/day]
    df_digestate['K20'] = df_NPK['K20'].div(1000)*K2O # price of total P205 produced [USD/day]
    df_digestate['total_100%'] = df_digestate[['N', 'P205', 'K20']].sum(axis = 1)
    df_digestate['total_50%'] = df_digestate[['N', 'P205', 'K20']].sum(axis = 1) / 2
    df_digestate['total_10%'] = df_digestate[['N', 'P205', 'K20']].sum(axis = 1) * (10/100)
    df_digestate['total_0%'] = df_digestate[['N', 'P205', 'K20']].sum(axis = 1) * (0/100)

    
    # Create a figure and axis
    fig, ax = plt.subplots()
    x = df_digestate['month']
    df_digestate_plot = df_digestate.drop(['month'], axis = 1)

    df_digestate_plot.to_excel(str(resdir + '/digestate_price_excel.xlsx'), engine='xlsxwriter') 
    
    for i in range(len(df_digestate_plot.columns)): 
        
        item = df_digestate_plot.columns[i]
        
        y = df_digestate_plot[item]
        # Plot the curve
        ax.plot(x, y, label=f'Curve {i+1}')
    
    # Set labels and title
    ax.set_xlabel('Time period from January 2016 to December 2022 [month]')
    ax.set_ylabel('Economic value of digestate [USD/day]')
    
    # Add legend
    ax.legend(df_digestate_plot.columns)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.savefig(str(resdir + '/digestate_price.pdf'))

    # Show the plot
    plt.show()
    
    # plot pie chart composition of the digestate (assumed constant)
    sizes = np.array([N, P2O5, K2O])
    labels = ['N', 'P205', 'K20']
    
    plt.pie(sizes, labels = labels, autopct = '%1.1f%%')
    
    plt.savefig(str(resdir + '/digestate_compo.pdf'))

    #plt.legend(title = 'Digestate composition: [kg/day]', loc = 'best')
    plt.show() 
    
    return df_digestate



def absolute_value(val, sizes):
    
    import numpy as np
    
    a  = np.round(val/100.*sizes.sum(), 0)
    
    return a