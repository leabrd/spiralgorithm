# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 14:11:36 2022

@author: leabr
"""

def ElecWaterBiorefineryScenarios (wdir, comparison_dict_subsystem, file_name, subsystem):
    
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import os
    
    ## ELECTRICITY CONSUMPTION DATA
    data_dict_plot_elec = {}
    
    for scenario in comparison_dict_subsystem.keys():
        
        print('\nScenario: %s'%scenario)
        
        data_dict_plot_elec[scenario] = {}
        
        for activity in comparison_dict_subsystem[scenario].keys():  
            
            print('Activity: %s'%activity)
            
            if 'electricity_IT' in comparison_dict_subsystem[scenario][activity].keys():
                elec = comparison_dict_subsystem[scenario][activity]['electricity_IT']['amount']
                
            elif 'electricity_FR' in comparison_dict_subsystem[scenario][activity].keys():
                elec = comparison_dict_subsystem[scenario][activity]['electricity_FR']['amount']
            
            else: 
                elec = 0
            
            data_dict_plot_elec[scenario][activity] = elec
  
    df_elec = pd.DataFrame.from_dict(data_dict_plot_elec, orient = 'columns')
    
    ## WATER CONSUMPTION DATA
    data_dict_plot_water = {}
    
    for scenario in comparison_dict_subsystem.keys():
        
        print('\nScenario: %s'%scenario)
        
        data_dict_plot_water[scenario] = {}
        
        for activity in comparison_dict_subsystem[scenario].keys():  
            
            water = 0
            
            print('Activity: %s'%activity)
            
            if 'ground_water' in comparison_dict_subsystem[scenario][activity].keys():
                water += comparison_dict_subsystem[scenario][activity]['ground_water']['amount']
                
            elif 'tap_water' in comparison_dict_subsystem[scenario][activity].keys():
                water += comparison_dict_subsystem[scenario][activity]['tap_water']['amount']
                
            elif 'ultrapure_water' in comparison_dict_subsystem[scenario][activity].keys():
                water += comparison_dict_subsystem[scenario][activity]['ultrapure_water']['amount']            
            
            else: 
                water += 0
            
            data_dict_plot_water[scenario][activity] = water
  
    df_water = pd.DataFrame.from_dict(data_dict_plot_water, orient = 'columns')
    
    #chap_name = file_name[0][:5]
    
    directory = os.path.join(wdir, str('results/elec&water/elec-water-use-act-' + subsystem + '.xlsx'))
        
    with pd.ExcelWriter(directory,mode = 'w') as writer:
        df_elec.to_excel(writer, sheet_name='electricity') 
        df_water.to_excel(writer, sheet_name='water')   

    
    ### PLOT TWO GRAHS: ELECTRICITY AND WATER
    list_df_to_plot = [df_elec.T, df_water.T]
    
    labels = []
    for period in data_dict_plot_elec.keys():
        for activity in data_dict_plot_elec[period].keys():
            if activity[0:5] not in labels:
                labels.append(activity[0:5])               
    labels = list(labels)
    print(labels)
    
    Ylabel = ['Electricty Use [kWh/kg FU]', 'Water Use [L/kg FU]']
    Ylabel2 = ['Cumulative Electricty Use [kWh/kg FU]', 'Cumulative Water Use [L/kg FU]']
    
    for i in range(len(list_df_to_plot)):        

        Y_list = []
        
        df = list_df_to_plot[i]
        
        for j in range(len(comparison_dict_subsystem.keys())):
            Y_list.append(df.iloc[j].values)
        
        X = np.arange(len(labels))
        print(X,Y_list)
        
    
        c = ['#08519c', '#CB3F2B']
        c = ['#1c9099', '#a6bddb'] # dark teal, light blue
        #c = ['#2c7fb8', '#7fcdbb'] # light teal, dark blue
        c = ['#444979', '#10A794'] # teal, blue grey
     
        fig = plt.figure(figsize= (4.566210045662101, 7.388283053652488))
    
        ax1 = fig.add_subplot(111)
        
        ax11 = ax1.twinx()
        
        ax1.bar(X-0.2,Y_list[0],0.4,label ='Period 1',color = c[0])
        ax1.bar(X+0.2,Y_list[1],0.4,label ='Period 2',color = c[1])
        
        ax1.set_xlim(ax1.get_xlim()[0],ax1.get_xlim()[1])
        
        ax11.plot(X-0.2,np.cumsum(Y_list[0]),marker = 'o',ls = '--',color = c[0])
        ax11.plot(X+0.2,np.cumsum(Y_list[1]),marker = 's',ls = ':',color = c[-1])
        
        ax11.text((X+0.2)[-1],np.cumsum(Y_list[1])[-1]+5,'Total:\n%.1f'%np.cumsum(Y_list[1])[-1],va = 'bottom',ha = 'center')
        ax11.text((X-0.2)[-1],np.cumsum(Y_list[0])[-1]+5,'Total:\n%.1f'%np.cumsum(Y_list[0])[-1],va = 'bottom',ha = 'center')
 
        ax1.set_xticks(X,labels)
        ax1.set_xticklabels(labels, rotation = 45)
        ax1.set_xlabel('Subsystem activity')
        ax1.set_ylabel(Ylabel[i])
        ax11.set_ylabel(Ylabel2[i])
        
        ax11.set_ylim(None,max(np.cumsum(Y_list[1])[-1], np.cumsum(Y_list[0])[-1])+max(np.cumsum(Y_list[1])[-1], np.cumsum(Y_list[0])[-1])/3) ####
        
        ax1.legend(loc = 'best')
        
        fig.tight_layout()
        
        fig.savefig(str(wdir + '/results/elec&water/'+file_name[i]))
        
        plt.close()

    return data_dict_plot_elec, data_dict_plot_water



colours_per_topic = {'biofuel': 'blue', 'biomass': 'medium red', 'biogas':'orange',
                    'pigment': 'gold', 'lactic acid': 'dark red',
                    'lipids': 'light orange', 'proteins': 'apricot',
                    'terpene': 'blue grey', 'biofertiliser': 'turquoise',
                    'WT': 'indigo', 'MWF': 'dark teal'}
           

colours = {'blue-grey':'#444979', 'indigo': '#444557', 'gold':'#FFDC3C',
           'dark-blue': '#006EBD', 'turquoise': '#1D9BC5', 'dark-green': '#4A6958',
           'dark-teal': '#10A794', 'green': '#4DBC64', 'yellow': '#F5E447',
           'orange':'#FF9428', 'red':'#FF561D', 'lavender':'#dcbeff', 'white':'#ffffff',
           'pink':'#fabed4', 'cyan':'#42d4f4','beige':'#fffac8','lime':'#bfef45'}


colours = {'blue': '#08519c', 'turquoise': '#1D9BC5','dark red': '#750B05', 'medium red': '#CB3F2B',
           'orange':'#FF9428','light orange': '#F1AE7A', 'beige':'#FEF7EC','gold':'#FFDC3C',
           'blue grey':'#444979','indigo': '#444557','cyan':'#42d4f4','green': '#4DBC64','dark teal': '#10A794',
           'dark blue': '#006EBD','apricot':'#ffd8b1'}
