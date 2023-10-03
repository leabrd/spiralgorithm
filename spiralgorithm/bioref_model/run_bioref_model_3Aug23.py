#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 14:05:27 2023

@author: leabraud
"""


def RunBiorefModel (wdir, recdir, ddir, recipe_name, param_file_name, lifetime_file_name, PerSubsystem = True):
       
    import os
    import yaml
    import pathlib
    from shutil import copyfile
    import pandas as pd
    
    from S0_set_parameters import SetParameters
    from S0_scenario_datasets import ScenarioDataDict, ScenarioDataDictAllTogether
    from S0_scenario_datasets import ScenarioDataExcel
    
    
    print('\n --------------\n| SPIRALGORITHM |\n --------------\n')

    print('\n> PREPARATION:\n  ------------')
       
    # -------------------------------------------------------------------------
    # SET DIRECTORIES AND LOAD THE RECIPE FOR BIOREFINERY MODEL CALCULATIONS 
    
    # create the file directories from their names
    param_file_dir = os.path.join(ddir, param_file_name)
    lifetime_file_dir = os.path.join(ddir, lifetime_file_name)
    
    # create a directory/folder to store the results
    result_dir = os.path.join(wdir,'results')   
    if os.path.exists(result_dir) == False:
        pathlib.Path(result_dir).mkdir(parents=True, exist_ok=True)
    
    # get the directory of the recipe file
    recipe_dir = os.path.join(recdir, recipe_name)
    
    # create a new directory for the copy of the recipe
    new_recipe_dir = os.path.join(recdir, str(recipe_name[:-4] + '_copy.yml'))
    
    # copy the recipe to the new directory
    copyfile(recipe_dir, new_recipe_dir)
    
    # load the copied recipe  
    with open(new_recipe_dir) as file:
        recipe = yaml.load(file, Loader = yaml.FullLoader)
        
    # write the directories in the recipe          
    recipe['input']['wdir'] = wdir
    recipe['input']['resdir'] = result_dir
    recipe['input']['recdir'] = new_recipe_dir
    
    # open the file and make it readable
    with open(new_recipe_dir,'w') as file:
        yaml.dump(recipe,file)
    
    # remove the 'input' from the recipe dictionary
    recipe = recipe['input']
    
    print('\nDirectories set up.')
    print('\nRecipe loaded.')
        
    # -------------------------------------------------------------------------
    # CALCULATE INPUTS/OUTPUTS OF THE BIOREFINERY BASED ON THE PARAMETERS
    
    print('\n> CALCULATION:\n  -----------')
    
    # import the model parameters
    model_param_dict = SetParameters(param_file_dir)
    print('\nBiorefinery model parameters imported.')
    
    if PerSubsystem == True:
        # create the comparison dictionary
        comparison_dict = ScenarioDataDict (model_param_dict, lifetime_file_dir)
        print('\nAll calculations performed. Data stored in a nested dictionary. Subdivision per subsystem.')
        
    else: 
        comparison_dict = ScenarioDataDictAllTogether (model_param_dict, lifetime_file_dir)
        print('\nAll calculations performed. Data stored in a nested dictionary. NO subdivision')

    
    return comparison_dict, recipe



def ScaleBiorefModelAllTogether (comparison_dict, scaling_factors_dict, recipe):
    '''
    Function that scales a data dictionary built for all the subsystem together
    (i.e. no subdivision).

    Parameters
    ----------
    comparison_dict : TYPE
        DESCRIPTION.
    recipe : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    
    import pandas as pd
    
    from S0_scenario_datasets import ScenarioDataDictPerMainOutput
    from S0_scenario_datasets import ScenarioDataExcel
    
    # -------------------------------------------------------------------------
    # SCALE THE DATASET BASED ON THE SCALING FACTORS AND MAIN OUTPUT    
        
    print('\n> SCALING:\n  -------')

    # get the main outputs for each subsystem from the recipe
    main_output = recipe['main_output']
    
    df = pd.DataFrame()
    
    for subsystem in main_output.keys():
        df_subs = pd.DataFrame.from_dict(main_output[subsystem], orient = 'index')
        df[subsystem] = df_subs
        
    print(df)
    
    # create a new dictionary
    comparison_dict_per_main_output = {}
    
    for scenario in comparison_dict.keys():
        
        comparison_dict_per_main_output[scenario] = {}
        
        value_dict = {'S1': comparison_dict[scenario]['S1A5Drying']['dry_spangles']['amount'],
                      'S2': comparison_dict[scenario]['S2A5Ultrafiltration2']['blue_extract_UF2']['amount'],
                      'S3': comparison_dict[scenario]['S3A4Concentration']['concentrate']['amount']}
        
        for act in comparison_dict[scenario].keys():
            
            if act == 'S12A8Transport': # transport is proportional to S1
                
                comparison_dict_per_main_output[scenario]['S12A8Transport'] = {}
                                
                comparison_dict_per_main_output[scenario]['S12A8Transport']['transport_car'] = {}
                comparison_dict_per_main_output[scenario]['S12A8Transport']['transport_car']['amount'] = main_output['S1']['scaling_factor'] * comparison_dict[scenario]['S12A8Transport']['transport_car']['amount'] / value_dict['S1']     
                comparison_dict_per_main_output[scenario]['S12A8Transport']['transport_car']['unit'] = comparison_dict[scenario]['S12A8Transport']['transport_car']['unit']
                comparison_dict_per_main_output[scenario]['S12A8Transport']['transport_car']['type'] = comparison_dict[scenario]['S12A8Transport']['transport_car']['type']
            
                comparison_dict_per_main_output[scenario]['S12A8Transport']['transport_ship'] = {}
                comparison_dict_per_main_output[scenario]['S12A8Transport']['transport_ship']['amount'] = main_output['S1']['scaling_factor'] * comparison_dict[scenario]['S12A8Transport']['transport_ship']['amount'] / value_dict['S1']     
                comparison_dict_per_main_output[scenario]['S12A8Transport']['transport_ship']['unit'] = comparison_dict[scenario]['S12A8Transport']['transport_ship']['unit']
                comparison_dict_per_main_output[scenario]['S12A8Transport']['transport_ship']['type'] = comparison_dict[scenario]['S12A8Transport']['transport_ship']['type']
               
                comparison_dict_per_main_output[scenario]['S12A8Transport']['transport_truck'] = {}
                comparison_dict_per_main_output[scenario]['S12A8Transport']['transport_truck']['amount'] = main_output['S1']['scaling_factor'] * comparison_dict[scenario]['S12A8Transport']['transport_truck']['amount'] / value_dict['S1']     
                comparison_dict_per_main_output[scenario]['S12A8Transport']['transport_truck']['unit'] = comparison_dict[scenario]['S12A8Transport']['transport_truck']['unit']
                comparison_dict_per_main_output[scenario]['S12A8Transport']['transport_truck']['type'] = comparison_dict[scenario]['S12A8Transport']['transport_truck']['type']
            
    
            if act == 'S23A8Transport': # transport is proportional to S2
                
                comparison_dict_per_main_output[scenario]['S23A8Transport'] = {}
         
                
                comparison_dict_per_main_output[scenario]['S23A8Transport']['transport_ref_truck'] = {}
                comparison_dict_per_main_output[scenario]['S23A8Transport']['transport_ref_truck']['amount'] = main_output['S2']['scaling_factor'] * comparison_dict[scenario]['S23A8Transport']['transport_ref_truck']['amount'] / value_dict['S2']    
                comparison_dict_per_main_output[scenario]['S23A8Transport']['transport_ref_truck']['unit'] = comparison_dict[scenario]['S23A8Transport']['transport_ref_truck']['unit']
                comparison_dict_per_main_output[scenario]['S23A8Transport']['transport_ref_truck']['type'] = comparison_dict[scenario]['S23A8Transport']['transport_ref_truck']['type']
       
     
            if act == 'S1A0Building': # bulding/infrastructures is not scaled
            
                comparison_dict_per_main_output[scenario]['S1A0Building'] = comparison_dict[scenario]['S1A0Building']
        
                
            if act == 'S1A0Operation': # operation is not scaled
            
                comparison_dict_per_main_output[scenario]['S1A0Operation'] = comparison_dict[scenario]['S1A0Operation']  
                
                
            for subsystem in ['S1', 'S2', 'S3']:
                
                if subsystem in act and act not in ['S12A8Transport', 'S23A8Transport', 'S1A0Building', 'S1A0Operation']:
                    
                    comparison_dict_per_main_output[scenario][act] = {}
                    
                    for exc in comparison_dict[scenario][act].keys():
                        
                        comparison_dict_per_main_output[scenario][act][exc] = {}
                        comparison_dict_per_main_output[scenario][act][exc]['amount'] = comparison_dict[scenario][act][exc]['amount'] / value_dict[subsystem] * scaling_factors_dict[subsystem]
                        comparison_dict_per_main_output[scenario][act][exc]['unit'] = comparison_dict[scenario][act][exc]['unit']
                        comparison_dict_per_main_output[scenario][act][exc]['type'] = comparison_dict[scenario][act][exc]['type']
                    
        filename = str('scaled_dataset_S123')
        ScenarioDataExcel (recipe['resdir'], comparison_dict_per_main_output, filename)    
        
    
    print('\nData scaled to the main output and exported as Excel files.')  
    print('Location of the files: %s' %recipe['resdir'])
    
    
    return comparison_dict_per_main_output, recipe


def ScaleBiorefModel (comparison_dict, recipe):
    
    import pandas as pd
    
    from S0_scenario_datasets import ScenarioDataDictPerMainOutput
    from S0_scenario_datasets import ScenarioDataExcel
    
    # -------------------------------------------------------------------------
    # SCALE THE DATASET BASED ON THE SCALING FACTORS AND MAIN OUTPUT    
        
    print('\n> SCALING:\n  -------')

    # get the main outputs for each subsystem from the recipe
    main_output = recipe['main_output']
    
    df = pd.DataFrame()
    
    for subsystem in main_output.keys():
        df_subs = pd.DataFrame.from_dict(main_output[subsystem], orient = 'index')
        df[subsystem] = df_subs
        
    print(df)
    
    # create a new dictionary
    comparison_dict_per_main_output = {}

    for subsystem in comparison_dict.keys():
        
        #print(subsystem)
        
        comparison_dict_per_main_output[subsystem] = {}
        
        if subsystem == 'transport_S12': # proportional to S1
            
            for scenario in comparison_dict['transport_S12'].keys():
                
                #print(scenario)
                
                comparison_dict_per_main_output[subsystem][scenario] = {}
                comparison_dict_per_main_output[subsystem][scenario]['S12A8Transport'] = {}
                
                value_S1 = comparison_dict['S1'][scenario]['S1A5Drying']['dry_spangles']['amount']
          
                comparison_dict_per_main_output[subsystem][scenario]['S12A8Transport']['transport_car'] = {}
                comparison_dict_per_main_output[subsystem][scenario]['S12A8Transport']['transport_car']['amount'] = main_output['S1']['scaling_factor'] * comparison_dict['transport_S12'][scenario]['S12A8Transport']['transport_car']['amount'] / value_S1                
                comparison_dict_per_main_output[subsystem][scenario]['S12A8Transport']['transport_car']['unit'] = comparison_dict['transport_S12'][scenario]['S12A8Transport']['transport_car']['unit']
                comparison_dict_per_main_output[subsystem][scenario]['S12A8Transport']['transport_car']['type'] = comparison_dict['transport_S12'][scenario]['S12A8Transport']['transport_car']['type']
                
                comparison_dict_per_main_output[subsystem][scenario]['S12A8Transport']['transport_ship'] = {}
                comparison_dict_per_main_output[subsystem][scenario]['S12A8Transport']['transport_ship']['amount'] = main_output['S1']['scaling_factor'] * comparison_dict['transport_S12'][scenario]['S12A8Transport']['transport_ship']['amount'] / value_S1
                comparison_dict_per_main_output[subsystem][scenario]['S12A8Transport']['transport_ship']['unit'] = comparison_dict['transport_S12'][scenario]['S12A8Transport']['transport_ship']['unit']
                comparison_dict_per_main_output[subsystem][scenario]['S12A8Transport']['transport_ship']['type'] = comparison_dict['transport_S12'][scenario]['S12A8Transport']['transport_ship']['type']
                
                comparison_dict_per_main_output[subsystem][scenario]['S12A8Transport']['transport_truck'] = {}
                comparison_dict_per_main_output[subsystem][scenario]['S12A8Transport']['transport_truck']['amount'] = main_output['S1']['scaling_factor'] * comparison_dict['transport_S12'][scenario]['S12A8Transport']['transport_truck']['amount'] / value_S1
                comparison_dict_per_main_output[subsystem][scenario]['S12A8Transport']['transport_truck']['unit'] = comparison_dict['transport_S12'][scenario]['S12A8Transport']['transport_truck']['unit']
                comparison_dict_per_main_output[subsystem][scenario]['S12A8Transport']['transport_truck']['type'] = comparison_dict['transport_S12'][scenario]['S12A8Transport']['transport_truck']['type']
            
        if subsystem == 'transport_S23': # proportional to S2
                
            for scenario in comparison_dict['transport_S23'].keys():
                
                comparison_dict_per_main_output[subsystem][scenario] = {}
                comparison_dict_per_main_output[subsystem][scenario]['S23A8Transport'] = {}
                
                value_S2 = comparison_dict['S2'][scenario]['S2A5Ultrafiltration2']['blue_extract_UF2']['amount']              
                
                comparison_dict_per_main_output[subsystem][scenario]['S23A8Transport']['transport_ref_truck'] = {}
                comparison_dict_per_main_output[subsystem][scenario]['S23A8Transport']['transport_ref_truck']['amount'] = main_output['S2']['scaling_factor'] * comparison_dict['transport_S23'][scenario]['S23A8Transport']['transport_ref_truck']['amount'] / value_S2
                comparison_dict_per_main_output[subsystem][scenario]['S23A8Transport']['transport_ref_truck']['unit'] = comparison_dict['transport_S23'][scenario]['S23A8Transport']['transport_ref_truck']['unit']
                comparison_dict_per_main_output[subsystem][scenario]['S23A8Transport']['transport_ref_truck']['type'] = comparison_dict['transport_S23'][scenario]['S23A8Transport']['transport_ref_truck']['type']
       
        
        if subsystem == 'infrastructures': # always 1 (independent from amount of biomass produced)
            
            for scenario in comparison_dict['infrastructures'].keys():
                
                comparison_dict_per_main_output[subsystem][scenario] = {}              
                comparison_dict_per_main_output[subsystem][scenario]['S1A0Building'] = comparison_dict['infrastructures'][scenario]['S1A0Building']
        
        if subsystem == 'operation': # always 1 (independent from amount of biomass produced)
            
            for scenario in comparison_dict['operation'].keys():
                
                comparison_dict_per_main_output[subsystem][scenario] = {}              
                comparison_dict_per_main_output[subsystem][scenario]['S1A0Operation'] = comparison_dict['operation'][scenario]['S1A0Operation']
               
        if subsystem != 'transport_S12' and subsystem != 'transport_S23' and subsystem != 'infrastructures' and subsystem != 'operation':
            
            act_name = main_output[subsystem]['act_name']
            exc_name = main_output[subsystem]['exc_name']
            scaling_factor = main_output[subsystem]['scaling_factor']
            comparison_dict_per_main_output[subsystem] = ScenarioDataDictPerMainOutput (comparison_dict[subsystem], act_name, exc_name, scaling_factor)
            
        filename = str('scaled_dataset_per_subsystem_'+ subsystem)
        ScenarioDataExcel (recipe['resdir'], comparison_dict_per_main_output[subsystem], filename)    
        
    
    print('\nData scaled to the main output and exported as Excel files.')  
    print('Location of the files: %s' %recipe['resdir'])
    
    
    return comparison_dict_per_main_output, recipe

    


def WaterElecAnalysis (comparison_dict_per_main_output, recipe):
    
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import pathlib
    import os
    
    from S0_elec_water_analysis import ElecWaterBiorefineryScenarios
    
    # create a directory to store the results of the water/electricity use analysis 
    result_dir_water_elec = os.path.join(recipe['wdir'],'results/elec&water')  
    if os.path.exists(result_dir_water_elec) == False:
        pathlib.Path(result_dir_water_elec).mkdir(parents=True, exist_ok=True)

    
  
    # remove the double activities to avoid double counting
    # building, operation, transport present in S1, S2, S3 and individual activities
    new_comparison_dict = {}
    
    for subsystem in comparison_dict_per_main_output.keys(): 
        new_comparison_dict[subsystem] ={}
        
        for scenario in comparison_dict_per_main_output[subsystem].keys(): 
            new_comparison_dict[subsystem][scenario] ={}
            
            for activity in comparison_dict_per_main_output[subsystem][scenario].keys(): 
                
                # avoid double counting the electricity/water consumption
                if subsystem == 'S1' and activity == 'S1A0Building': continue
                if subsystem == 'S1' and activity == 'S1A0Operation': continue
                if subsystem == 'S1' and activity == 'S1A8Transport': continue
                if subsystem == 'S2' and activity == 'S2A8Transport': continue
                
                new_comparison_dict[subsystem][scenario][activity] = comparison_dict_per_main_output[subsystem][scenario][activity]
            
    plotData_elec = {}
    plotData_water = {}
    
    for subsystem in new_comparison_dict.keys(): 
        
        # do not plot transport and infrastructure (no water and electricity used)
        if subsystem == 'S1' or subsystem == 'S2' or subsystem == 'S3' or subsystem == 'operation':
            
            file_name = ['electricity_' + subsystem + '.pdf', 'water_' + subsystem + '.pdf']
        
            plotData_elec[subsystem], plotData_water[subsystem] = ElecWaterBiorefineryScenarios (recipe['wdir'], new_comparison_dict[subsystem], file_name, subsystem)
            
        else: continue
    
    
    
    #  Get the data in the correct laytout for plott
    plotData_cleanup = {}
    
    # Setup initial dictionary structiure
    for ss in plotData_elec.keys():
        for scen in plotData_elec[ss]:
            plotData_cleanup[scen] = []
     
            
    #  Go through and add up all the values for each scenario
    for ss in plotData_elec.keys():
        for scen in plotData_elec[ss]:
            total=0
            for act in plotData_elec[ss][scen]:
                total += plotData_elec[ss][scen][act] 
                
            plotData_cleanup[scen].append(total)  

    labels  = list(plotData_elec.keys())
    
    c = ['#444979', '#10A794'] # teal, blue grey
                    
    fig = plt.figure(figsize= (4.566210045662101, 3.694141526826244))
    ax1 = fig.add_subplot(111)
    
    
    ind = np.arange(len(labels))  # the x locations for the groups
    width = 0.35       # the width of the bars
    
    
    i = 0
    for scen in plotData_cleanup:
       
        ax1.bar(ind + i*width,plotData_cleanup[scen],width = width,label = scen.replace('tech_','Period '),color = c[i])
        
        i+=1
    
    ax1.set_xticks(ind + width/2,labels)
    ax1.set_ylabel('Electricity use [kWh/kg FU]')
    
    ax1.legend()
    plt.show()
    
    fig.tight_layout()
    fig.savefig(str(recipe['wdir'] + '/results/elec&water/total_electricity.pdf'))
    
    plt.close()
        
    ## PLOT WATER USE
    
    #  Get the data in the correct laytout for plott
    plotData_cleanup = {}
    
    # Setup initial dictionary structiure
    for ss in plotData_water.keys():
        for scen in plotData_elec[ss]:
            plotData_cleanup[scen] = []
     
            
     #  Go through and add up all the values for each scenario
    for ss in plotData_water.keys():
        for scen in plotData_water[ss]:
            total=0
            for act in plotData_water[ss][scen]:
                total += plotData_water[ss][scen][act] 
                
            plotData_cleanup[scen].append(total)  

    labels  = list(plotData_water.keys())

                    
    fig = plt.figure(figsize= (4.566210045662101, 3.694141526826244))
    ax1 = fig.add_subplot(111)
    
    
    ind = np.arange(len(labels))  # the x locations for the groups
    width = 0.35       # the width of the bars
    
    
    i = 0
    for scen in plotData_cleanup:
        ax1.bar(ind + i*width,plotData_cleanup[scen],width = width,label = scen.replace('tech_','Period '),color = c[i])
        i+=1
        
        
    ax1.set_xticks(ind + width/2,labels)
    ax1.set_ylabel('Water use [L/kg FU]')
    
    ax1.legend()
    plt.show()
    
    fig.tight_layout()
    
    fig.savefig(str(recipe['wdir'] + '/results/elec&water/total_water.pdf'))
        
    plt.close()
    
    
   #-------------------------------------------------------------------------
   # contribution of the subsystems to the overall electricity/water use
   #-------------------------------------------------------------------------

    data_dict_plot_elec = {}
    
    for subsystem in new_comparison_dict.keys(): 

        data_dict_plot_elec[subsystem] = {}
        
        for scenario in new_comparison_dict[subsystem].keys(): 
            
            elec = 0
        
            data_dict_plot_elec[subsystem][scenario] = {}
            
            for activity in new_comparison_dict[subsystem][scenario].keys(): 

                if 'electricity_IT' in new_comparison_dict[subsystem][scenario][activity].keys():
                    elec += new_comparison_dict[subsystem][scenario][activity]['electricity_IT']['amount']
                    
                elif 'electricity_FR' in new_comparison_dict[subsystem][scenario][activity].keys():
                    elec += new_comparison_dict[subsystem][scenario][activity]['electricity_FR']['amount']
                    
                else:
                    elec +=0
                        
            data_dict_plot_elec[subsystem][scenario] = elec
            
    df_elec = pd.DataFrame.from_dict(data_dict_plot_elec)
    
    # contribution of the subsystems to the overall water use
    data_dict_plot_water = {}
    
    for subsystem in new_comparison_dict.keys(): 
        
        data_dict_plot_water[subsystem] = {}
        
        for scenario in new_comparison_dict[subsystem].keys(): 

            water = 0
            
            data_dict_plot_water[subsystem][scenario] = {}
            
            for activity in new_comparison_dict[subsystem][scenario].keys(): 
                
                if 'ground_water' in new_comparison_dict[subsystem][scenario][activity].keys():
                    water += new_comparison_dict[subsystem][scenario][activity]['ground_water']['amount']
                    
                elif 'tap_water' in new_comparison_dict[subsystem][scenario][activity].keys():
                    water += new_comparison_dict[subsystem][scenario][activity]['tap_water']['amount']
                    
                elif 'ultrapure_water' in new_comparison_dict[subsystem][scenario][activity].keys():
                    water += new_comparison_dict[subsystem][scenario][activity]['ultrapure_water']['amount']  
                    
                else: 
                    water +=0
                        
            data_dict_plot_water[subsystem][scenario] = water
            
    df_water = pd.DataFrame.from_dict(data_dict_plot_water)
    
    file_name = 'elec-water-use-whole-bioref.xlsx'
    directory = os.path.join(recipe['wdir'], str('results/elec&water/' + file_name))
    

    with pd.ExcelWriter(directory, mode = 'w') as writer:
        df_elec.to_excel(writer, sheet_name='electricity') 
        df_water.to_excel(writer, sheet_name='water')        
            
    df_elec = pd.DataFrame.from_dict(data_dict_plot_elec, orient = 'columns')
    
    return recipe




def BiomassFlows (comparison_dict_per_main_output, recipe):
    
    import os
    import pathlib
    from S0_biomass_flows import BiomassFlowsToExcel, SankeyBiorefineryScenarios
    
    # create a directory to store the results of the biomass balance analysis 
    result_dir_biomass = os.path.join(recipe['wdir'],'results/biomass')  
    if os.path.exists(result_dir_biomass) == False:
        pathlib.Path(result_dir_biomass).mkdir(parents=True, exist_ok=True)


    BiomassFlowsToExcel(comparison_dict_per_main_output, result_dir_biomass)

    SankeyBiorefineryScenarios (comparison_dict_per_main_output)
    
    return recipe