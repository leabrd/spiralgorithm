# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 14:30:29 2022

@author: leabr
"""

def BiomassFlowsToExcel (comparison_dict, result_dir_biomass):
    
    import pandas as pd
    import numpy as np
    import os
    import matplotlib.pyplot as plt
    
    biomass_dict = {}
    
    biomass_name_list = ['fg_input', 'ref_flow', 'coproduct', 'losses']
    
    for subsystem in comparison_dict.keys():
        
        if subsystem == 'transport': continue
        
        biomass_dict[subsystem] = {}
        
        for scenario in comparison_dict[subsystem].keys():
            
            biomass_dict[subsystem][scenario] = {}

            for activity in comparison_dict[subsystem][scenario].keys():
                                
                if activity == 'S1A0Building' or activity == 'S1A0Operation': 
                    continue
                
                else: 
                    
                    for exc in comparison_dict[subsystem][scenario][activity].keys():
                        
                        exc_type = comparison_dict[subsystem][scenario][activity][exc]['type']
                        
                        if exc_type in biomass_name_list:
                            
                            amount = comparison_dict[subsystem][scenario][activity][exc]['amount']
                            
                            if exc_type == 'losses':
                                exc = str('losses-' + activity)
                            
                            biomass_dict[subsystem][scenario][exc] = amount
                            
    ### PLOTING THE PIE CHART
                            
    subsystems = ['S2','S3']                     
    scenarios = ['tech_2', 'tech_2_S1', 'tech_2_S2', 'tech_2_S3', 'tech_2_S4']
    exc = ['blue_extract','CPD_concentrate','concentrate']
    
    #  Must be below 0.5
    bar_width = 0.35
    
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    
    scenario_spacing = dict(zip(scenarios ,0.5*bar_width*np.arange(-1,len(scenarios ))))
    
    colours = {'gold':'#FFDC3C','blue': '#08519c', 'medium red': '#CB3F2B', 'black': 'k', 'green': 'green'}
    
    #scenario_color = dict(zip(scenarios ,['r','g','b','k']))
    
    scenario_color = dict(zip(scenarios, colours.values()))    
    
    exc_spacing = dict(zip(exc, np.arange(0,len(exc ))))
    # Make plots for each subsystem 
    for ss in subsystems:
        for scenario in scenarios:
            if scenario not in biomass_dict[ss]: continue
            for e in exc:
                if e not in biomass_dict[ss][scenario]: continue
            
            
                ax1.bar(
                        exc_spacing[e]+scenario_spacing[scenario], 
                        biomass_dict[ss][scenario][e],
                        align='center', alpha=0.5,
                        width = bar_width/2,
                        color = scenario_color[scenario],
                        label = scenario)
                
                
                ax1.text(exc_spacing[e]+scenario_spacing[scenario],
                         biomass_dict[ss][scenario][e],
                         s = '%.2f' % biomass_dict[ss][scenario][e],
                         va = 'bottom',
                         ha = 'center',
                         fontsize = 7)
                
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    
    ax1.legend(by_label.values(), by_label.keys(),loc = 'upper right')
    
    labels = list(exc_spacing.keys())
    
    # labels = ['A','B','C']
    ax1.set_xticks(np.array(list(exc_spacing.values())),labels)
    right_side = ax1.spines["right"]
    right_side.set_visible(False)
    top = ax1.spines["top"]
    top.set_visible(False)
    
    plt.show()
    
    
    
    directory = os.path.join(result_dir_biomass, str('graph_sensitivity_biomass.pdf'))
    
    
    fig.savefig(directory,bbox_inches='tight')

    with pd.ExcelWriter(os.path.join(result_dir_biomass, str('biomass_flows.xlsx')),mode = 'w') as writer:
          
        for subsystem in biomass_dict.keys():
            #print(subsystem)
            
            df_data = []
              
            for scenario in biomass_dict[subsystem].keys():
                #print(scenario)
                
                data_dict = biomass_dict[subsystem][scenario]
                
                scenario_name = str('scenario_' + str(scenario))
                
                index_names = [scenario_name]
                
                df_data_i = pd.DataFrame(data_dict,index = index_names).T
                    
                df_data.append(df_data_i.T)
    
            df_data = pd.concat(df_data).T
                
            df_data= df_data.loc[:,~df_data.columns.duplicated()].copy()
                
            cols = np.sort(df_data.columns)
            df_data = df_data[cols]
            
            df_data.to_excel(writer, sheet_name = subsystem)          
            
    print('Biomass flows exported as an Excel file. \nDirectory: %s'%(os.path.join(result_dir_biomass, str('biomass_flows.xlsx'))))
    
    return biomass_dict



def PieChartCompo (biomass_dict):
    
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    
    subsystem_list = ['S2','S3']  # subsystems in which the biorefinery products are generated                   
    scenario_list = ['tech_1', 'tech_2']
    product_list = ['Blue extract','CPBc','CPAc']
    label_dict = {'Blue extract': 'blue_extract','CPBc':'CPD_concentrate','CPAc': 'concentrate'}
    
    bar_width = 0.35 #  Must be below 0.5
    
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    
    scenario_spacing = dict(zip(scenario_list, 0.5 * bar_width * np.arange(-1, len(scenario_list))))
    
    colours = {'gold':'#FFDC3C','blue': '#08519c', 'medium red': '#CB3F2B', 'black': 'k', 'green': 'green'}    
    scenario_color = dict(zip(scenario_list, colours.values()))    
    
    product_spacing = dict(zip(product_list, np.arange(0,len(product_list))))
    
    for subsystem in subsystem_list:
        
        for scenario in scenario_list:
            
            if scenario not in biomass_dict[subsystem]: continue
                
            for product in product_list:
                
                if product not in biomass_dict[subsystem][scenario]: continue
            
            
                ax1.bar(product_spacing[product] + scenario_spacing[scenario], 
                        biomass_dict[subsystem][scenario][product],
                        align =' center', alpha=0.5,
                        width = bar_width/2,
                        color = scenario_color[scenario],
                        label = label_dict[product])
                
                ax1.text(product_spacing[product] + scenario_spacing[scenario],
                         biomass_dict[subsystem][scenario][product],
                         s = '%.2f' % biomass_dict[subsystem][scenario][product],
                         va = 'bottom',
                         ha = 'center',
                         fontsize = 7)
                
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    
    ax1.legend(by_label.values(), by_label.keys(),loc = 'upper right')
    
    labels = list(product_spacing.keys())
    
    ax1.set_xticks(np.array(list(product_spacing.values())),labels)
    right_side = ax1.spines["right"]
    right_side.set_visible(False)
    top = ax1.spines["top"]
    top.set_visible(False)
    
    plt.show()
    
    return 









def SankeyBiorefineryScenarios (comparison_dict):
        
    import plotly.io as pio
    from plotly.offline import init_notebook_mode, iplot
    init_notebook_mode()
    # https://python.plainenglish.io/sankeying-with-plotly-90500b87d8cf
    
    source_dict = {}
    target_dict = {}
    amount_dict = {}
    
    for subsystem in comparison_dict.keys():
        
        source_dict[subsystem] = {}
        target_dict[subsystem] = {}
        amount_dict[subsystem] = {}
        
        for scenario in comparison_dict[subsystem].keys():
            
            source_list = []
            target_list = []
            amount_list = []
            
            for activity in comparison_dict[subsystem][scenario].keys():
                
                print('Activity: %s' %activity)
                
                for exc in comparison_dict[subsystem][scenario][activity].keys():
                    
                    input_i = [i for i in comparison_dict[subsystem][scenario][activity].keys() if comparison_dict[subsystem][scenario][activity][i]['type'] =='fg_input']
                    
                    if len(input_i)==0:
                        continue
                    else:
                        input_i = input_i[0]
                        
                    print('Foreground input: %s' %input_i)
                        
                    ref_flow_outputs =  [i for i in comparison_dict[subsystem][scenario][activity].keys()  if comparison_dict[subsystem][scenario][activity][i]['type'] =='ref_flow']
                    
                    for output in ref_flow_outputs:
                        print('Reference flow: %s' %output)
                        source_list.append(input_i)
                        target_list.append(output)
                        amount_list.append(comparison_dict[subsystem][scenario][activity][output]['amount'])
                    
                    coproducts_outputs =  [i for i in comparison_dict[subsystem][scenario][activity].keys()  if comparison_dict[subsystem][scenario][activity][i]['type'] =='coproduct']
                    
                    for output in coproducts_outputs:
                        print('Co-product: %s' %output)
                        source_list.append( input_i)
                        target_list.append(output)
                        amount_list.append(comparison_dict[subsystem][scenario][activity][output]['amount'])
                    
                    losses_outputs =  [i for i in comparison_dict[subsystem][scenario][activity].keys()  if comparison_dict[subsystem][scenario][activity][i]['type'] =='losses']
                    
                    for output in losses_outputs:
                        print('Losses: %s' %output)
                        source_list.append( input_i)
                        target_list.append(output)
                        amount_list.append(comparison_dict[subsystem][scenario][activity][output]['amount'])
                        
            source_dict[subsystem][scenario] = source_list   
            target_dict[subsystem][scenario] = target_list
            amount_dict[subsystem][scenario] = amount_list
    
    ## ADD THE VALUES OF S1, S2, S3 PER SCENARIO
    
    scenario_source_list = []
    for scenario in comparison_dict['S1'].keys():
        source_S1 = source_dict['S1'][scenario]
        source_S2 = source_dict['S2'][scenario]
        source_S3 = source_dict['S3'][scenario]
        scenario_source_list.append(source_S1 + source_S2 + source_S3)
    
    scenario_target_list = []
    for scenario in comparison_dict['S1'].keys():
        target_S1 = target_dict['S1'][scenario]
        target_S2 = target_dict['S2'][scenario]
        target_S3 = target_dict['S3'][scenario]
        scenario_target_list.append(target_S1 + target_S2 + target_S3)   
    
    scenario_value_list = []
    for scenario in comparison_dict['S1'].keys():
        value_S1 = amount_dict['S1'][scenario]
        value_S2 = amount_dict['S2'][scenario]
        value_S3 = amount_dict['S3'][scenario]
        scenario_value_list.append(value_S1 + value_S2 + value_S3)   

    ## CREATE A SANKEY DIAGRAM PER SCENARIO FOR THE WHOLE BIOREFINERY
    for i in range(len(scenario_source_list)):
        
        for j in range(len(scenario_source_list[i])):
            print('%s [%s] %s'%(scenario_source_list[i][j], scenario_value_list[i][j], scenario_target_list[i][j]))
        
        source_sankey = []
        target_sankey = []
        value_sankey = []
        
        ## list of unique names
        label_list = []
        for name in scenario_source_list[i]:
            if name not in label_list:
                label_list.append(name)
        for name in scenario_target_list[i]:
            if name not in label_list:
                label_list.append(name) 
        
        

        ## give a number to each label
        label_dict = {}
        for k in range(len(label_list)):
            label_dict[label_list[k]] = k
        
        # get a list of number corresonding to the names
        source_sankey = []
        for source in scenario_source_list[i]:
            source_sankey.append(label_dict[source])
            
        # get a list of number corresonding to the names        
        target_sankey = []
        for target in scenario_target_list[i]:
            target_sankey.append(label_dict[target])
        
        # get the list of values
        value_sankey = []
        for value in scenario_value_list[i]:
            value_sankey.append(value)
        
        # create the Sankey figure
        data = dict(type='sankey',
                    node = dict(pad = 15,
                                thickness = 5,
                                line = dict(color = "black",
                                            width = 0.5),
                                label = label_list,
                                color = ['grey' for i in range(len(label_list))]
                                ),
                    link = dict(source = source_sankey,
                                target = target_sankey,
                                value = value_sankey)
                                )
        
        layout =  dict(font = dict(size = 10))
            
        fig = dict(data=[data], layout=layout)
        pio.write_image(fig, 'sankey_diagram_scenario_%s.pdf' %(i))
        iplot(fig)
   
    return 
