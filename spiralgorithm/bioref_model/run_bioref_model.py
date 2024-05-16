#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 11:34:23 2023

@author: leabraud
"""

def RunBiorefineryModel (wdir, rdir, ddir, recipe_name, param_file_name, ei_file_name, lifetime_file_name):
     
    from S0_set_parameters import InitialParametersDict, SetParameters
    from S0_set_parameters import DatasetScaling
    from S0_scenario_datasets import ScenarioDataDict
    from S0_scenario_datasets import ScenarioDataDictPerProcess
    from S0_scenario_datasets import ScenarioDataDictPerMainOutput
    from S0_scenario_datasets import ScenarioDataExcel
    from S0_biomass_flows import BiomassFlowsToExcel
    from S0_elec_water_analysis import ElecWaterBiorefineryScenarios
    from S0_bw2package import CreateForegroundDatabase

    import os
    import yaml
    import pathlib
    from shutil import copyfile
    

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    
    InitialParametersDict (param_file_name)
    
    
    # create a 'results' directory   
    result_dir = os.path.join(wdir,'results')   
    if os.path.exists(result_dir) == False:
        pathlib.Path(result_dir).mkdir(parents=True, exist_ok=True)
    
    # -------------------------------------------------------------------------
    # OPEN, READ, AND WRITE IN THE RECIPE COPIED TO THE WORKING DIRECTORY
    
    # the recipe directory should be entered
    if not rdir:
        rdir = input('Please enter recipe directory: ')
    print('Recipe directory:', rdir)
    
    # load default recipe, this location shouldn't change
    default_recipe_dir = os.path.join(rdir, recipe_name)
    
    # new directory for the copy of default_recipe, in the working directory
    new_recipe_dir = os.path.join(wdir,recipe_name)
    
    # copy to work directory and return new loaction
    copyfile(default_recipe_dir, new_recipe_dir)
    
    with open(new_recipe_dir) as file:
        recipe = yaml.load(file, Loader=yaml.FullLoader)
    
    # write the directories in the recipe          
    recipe['input']['wdir'] = wdir
    #recipe['input']['pdir'] = pdir
    #recipe['input']['rdir'] = result_dir
    recipe['input']['recipe_dir'] = new_recipe_dir
    
    # open the file and make it readable
    with open(new_recipe_dir,'w') as file:
        yaml.dump(recipe,file)
    
    # remove the 'input' from the recipe dictionary
    recipe = recipe['input']
    
    
    # -------------------------------------------------------------------------
    # SET THE PARAMETERS AND GET THE DATA DICTIONARY FOR THE BIOREFINERY 
    
    # get the files directory
    param_file_dir = os.path.join(ddir, param_file_name)
    lifetime_file_dir = os.path.join(ddir, lifetime_file_name)
    
    # import the model parameters
    model_param_dict = SetParameters(param_file_dir)
    
    # create the comparison dictionary
    comparison_dict = ScenarioDataDict (model_param_dict, lifetime_file_dir)
    
    # -------------------------------------------------------------------------
    # EXPORT THE DATASETS IN EXCEL FILES  
    
    for subsystem in comparison_dict.keys():
        
        filename = str('raw_dataset_per_subsystem_'+ subsystem)

        ScenarioDataExcel (result_dir, comparison_dict[subsystem], filename)
        
        
    #-------------------------------------------------------------------------
    # get comparison dict per subsystems adjusted with scaling factors
    #-------------------------------------------------------------------------
    
    main_output = recipe['main_output']
    
    
    comparison_dict_per_main_output = {}

    for subsystem in comparison_dict.keys():
        
        print(subsystem)
        
        comparison_dict_per_main_output[subsystem] = {}
        
        if subsystem == 'transport_S12': # proportional to S1
            
            for scenario in comparison_dict['transport_S12'].keys():
                
                print(scenario)
                
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
        ScenarioDataExcel (result_dir, comparison_dict_per_main_output[subsystem], filename)    
        
    
        #-------------------------------------------------------------------------
        # export the datasets into the BW format if stated in recipe
        #-------------------------------------------------------------------------    
        
        if recipe['export_to_BW']: 
            
            ei_datasets_file_dir = os.path.join(ddir, ei_file_name)
            project_name = recipe['databases']['project_name']
            database_name = str('db_'+subsystem)
            my_db_list = CreateForegroundDatabase (wdir, project_name, 
                                                   comparison_dict_per_main_output[subsystem], 
                                                   ei_datasets_file_dir, database_name)
            
    # -------------------------------------------------------------------------
    # LOCAL SENSITIVITY ANALYSIS (ONE AT A TIME)
    # -------------------------------------------------------------------------        
            
    if recipe['sensitivity']:
        
        # create a directory to store the results of the water/electricity use analysis 
        results_dir_sensitivity = os.path.join(wdir,'results/sensitivity')  
        if os.path.exists(results_dir_sensitivity) == False:
            pathlib.Path(results_dir_sensitivity).mkdir(parents=True, exist_ok=True)
        
        
        for pi in recipe['p']:
            
            ### SENSITIVITY TO THE PC CONTENT
            
            PC = np.arange(5,15,.1) # PC content varies from 5 to 15%
            elec_PC = []
            water_PC = []
            
            for PC_i in PC:
                
                # value of the parameter "PC_content" changes
                for tech in model_param_dict.keys():
                    model_param_dict[tech]['PC_content'] = PC_i
                
                comparison_dict = ScenarioDataDict (model_param_dict, lifetime_file_dir)
                
                elec_PC_i = 0
                water_PC_i = 0
                
                for subsystem in comparison_dict.keys():
                    for scenarios in comparison_dict[subsystem].keys():
                        if scenarios == 'tech_1': continue
                    
                        for activity in comparison_dict[subsystem][scenarios]:
                            div_value =comparison_dict[pi[0]][scenarios][pi[1]][pi[2]]['amount']
                            for product in comparison_dict[subsystem][scenarios][activity]:
                                if 'electricity' in product.lower():
                                    #print(product)
                                    elec_PC_i+=comparison_dict[subsystem][scenarios][activity][product]['amount']/div_value
                                    
                                if 'tap_water' in product.lower() or 'ground_water' in product.lower():
                                    #print('water = ',product)
                                    water_PC_i+=comparison_dict[subsystem][scenarios][activity][product]['amount']/div_value
                                        
                elec_PC.append([PC_i,elec_PC_i])
                water_PC.append([PC_i,water_PC_i])
            
            elec_PC = np.array(elec_PC)
            water_PC = np.array(water_PC)
           
            
            ### SENSITIVITY TO THE PC EXTRACTION EFFICIENCY
           
            PC_extr_eff = np.arange(50,100,.1) # PC extraction efficicency varies from 50 to 100%
            elec = []
            water = []
           
            for PC_extr_eff_i in PC_extr_eff:
                
                for tech in model_param_dict.keys():
                    
                    model_param_dict[tech]['PC_extraction_efficiency'] = PC_extr_eff_i
                
                comparison_dict = ScenarioDataDict (model_param_dict, lifetime_file_dir)
               
                elec_i = 0
                water_i= 0
       
                for subsystem in comparison_dict.keys():
                    for scenarios in comparison_dict[subsystem].keys():
                        if scenarios == 'tech_1': continue
                   
                        for activity in comparison_dict[subsystem][scenarios]:
                            div_value =comparison_dict[pi[0]][scenarios][pi[1]][pi[2]]['amount']
                            for product in comparison_dict[subsystem][scenarios][activity]:
                                if 'electricity' in product.lower():
                                   #print(product)
                                   elec_i+=comparison_dict[subsystem][scenarios][activity][product]['amount']/div_value
                                   
                                if 'tap_water' in product.lower() or 'ground_water' in product.lower():
                                   #print('water = ',product)
                                   water_i+=comparison_dict[subsystem][scenarios][activity][product]['amount']/div_value
                                       
                elec.append([PC_extr_eff_i,elec_i])
                water.append([PC_extr_eff_i,water_i])
               
            elec = np.array(elec)
            water = np.array(water)
           
        
            ### SENSITIVITY TO THE BIOMASS PRODUCTIVITY
            
            prod = np.arange(1,10,.1)
        
            elec_prod = []
            water_prod = []
            
            for  prod_i in prod:
                
                # get the parameter values for the different scenarios
                model_param_dict = SetParameters(param_file_dir)
                for tech in model_param_dict.keys():
                    model_param_dict[tech]['productivity'] = prod_i
                    
                comparison_dict = ScenarioDataDict (model_param_dict, lifetime_file_dir)
                
                elec_i = 0
                water_i= 0
                for subsystem in comparison_dict.keys():
                    for scenarios in comparison_dict[subsystem].keys():
                        if scenarios == 'tech_1': continue
                    
                        for activity in comparison_dict[subsystem][scenarios]:
                            div_value =comparison_dict[pi[0]][scenarios][pi[1]][pi[2]]['amount']
                            for product in comparison_dict[subsystem][scenarios][activity]:
                                if 'electricity' in product.lower():
                                    # print(product)
                                    elec_i+=comparison_dict[subsystem][scenarios][activity][product]['amount']/div_value
                                    
                                if 'tap_water' in product.lower() or 'ground_water' in product.lower():
                                    # print('water = ',product)
                                    water_i+=comparison_dict[subsystem][scenarios][activity][product]['amount']/div_value
                                        
                elec_prod.append([ prod_i,elec_i])
                water_prod.append([ prod_i,water_i])
                
            elec_prod = np.array(elec_prod)
            water_prod = np.array(water_prod)
            
            
            ### PLOT FIGURE 
            
            fig = plt.figure()
            
            # ax1 = fig.add_subplot(331)
            # ax2 = fig.add_subplot(332,sharey = ax1)
            # ax3 = fig.add_subplot(333,sharey = ax1)
            
            # ax4 = fig.add_subplot(334)
            # ax5 = fig.add_subplot(335,sharey = ax3)
            # ax6 = fig.add_subplot(336,sharey = ax3)
            
            # # plot productivity
            # ax1.plot(elec_prod[:,0],elec_prod[:,1],label = 'Electricity',c = '#CB3F2B')
            # ax4.plot(water_prod[:,0],water_prod[:,1],label = 'Water',c = '#CB3F2B')
            
            # ## plot PC content
            # ax2.plot(elec_PC[:,0],elec_PC[:,1],label = 'Electricity',c = '#08519c')
            # ax5.plot(water_PC[:,0],water_PC[:,1],label = 'Water',c = '#08519c')
            
            # ## plot PC extr eff
            # ax3.plot(elec[:,0],elec[:,1],label = 'Electricity',c = '#08519c')
            # ax6.plot(water[:,0],water[:,1],label = 'Water',c = '#08519c')
    
            
            # ax1.set_xticklabels([])
            # ax4.set_xticklabels([])
            
            # ax4.set_xlabel('Prod. [g/m2/day]')
            # ax5.set_xlabel('PC content [%]')
            # ax6.set_xlabel('PC extr. eff. [%]')
            
            # ax1.set_ylabel('Electricity [kWh]')
            # ax4.set_ylabel('Water [m3]')
            
            ax1 = fig.add_subplot(221)
            ax2 = fig.add_subplot(222,sharey = ax1)
            
            ax3 = fig.add_subplot(223)
            ax4 = fig.add_subplot(224,sharey = ax3)
            
            ## plot relation to PC content
            ax2.plot(elec[:,0],elec[:,1],label = 'Electricity',c = '#08519c')
            ax4.plot(water[:,0],water[:,1],label = 'Water',c = '#08519c')
            
            ax1.plot(elec_prod[:,0],elec_prod[:,1],label = 'Electricity',c = '#CB3F2B')
            ax3.plot(water_prod[:,0],water_prod[:,1],label = 'Water',c = '#CB3F2B')
    
            ax1.set_xticklabels([])
            ax2.set_xticklabels([])
            
            ax4.set_xlabel('PC content [%]')
            
            ax3.set_xlabel('Productivity [g/m2/day]')
            
            ax1.set_ylabel('Electricity [kWh]')
            
            ax3.set_ylabel('Water [m3]')
            
            fig.suptitle('%s-%s-%s'% (pi[0],pi[1],pi[2]))
            
            plt.tight_layout()
            plt.show()    
            
            
            #fig.savefig('/home/leabraud/OneDrive/UCD/paper2_bioref/python_code/results/sensitivity/sensitivity_elec_water_%s.pdf'%(pi[0]))
            fig.savefig(str(wdir + '/results/sensitivity/sensitivity_elec_water_%s.pdf'%(pi[0])))
            
            #plot_name =  str('/sensitivity_elec_water_%s.pdf' %(pi[0]))
            #fig.savefig(str(results_dir_sensitivity + plot_name))
            
            plt.close()            
            
            
            
            ### SENSITIVITY OF THE COMPOSITION OF THE BOP TO THE PC CONTENT
            
            PC = np.arange(5,15,.1)
            dry_spangles = []
            blue_extract = []
            CPAc = []
            CPDc = []
            transport_car = []
            transport_ship = []
            transport_truck = []
            transport_ref_truck = []
            
            for PC_i in PC:
                 
                for tech in model_param_dict.keys():
                    model_param_dict[tech]['PC_content'] = PC_i
        
                for subsystem in comparison_dict.keys():
                    for scenarios in comparison_dict[subsystem].keys():
                        if scenarios == 'tech_1': continue
                        for activity in comparison_dict[subsystem][scenarios]:
                            print(activity)
                            
                            if activity == recipe['p'][0][1]: 
                                dry_spangles_i = comparison_dict[subsystem][scenarios][activity]['dry_spangles']['amount']
                                print('dry spangles after S1A5: ', dry_spangles)
                            
                            if activity == recipe['p'][1][1]: 
                                blue_extract_i = comparison_dict[subsystem][scenarios][activity]['blue_extract_UF2']['amount']
                                print('blue extract after S2A5: ', blue_extract)
                                
                            if activity == 'S2A6Concentration': 
                                CPDc_i = comparison_dict[subsystem][scenarios][activity]['CPD_concentrate']['amount']
                                print('CPDc after S2A6: ', CPDc)                        
                                
                            if activity == recipe['p'][2][1]: 
                                CPAc_i = comparison_dict[subsystem][scenarios][activity]['concentrate']['amount']
                                print('CPAc after S3A4: ', CPAc)     
                            
                            # if activity == 'S123A8Transport':
                            #     transport_car_i = comparison_dict[subsystem][scenarios][activity]['transport_car']['amount']
                            #     transport_ship_i = comparison_dict[subsystem][scenarios][activity]['transport_ship']['amount']
                            #     transport_truck_i = comparison_dict[subsystem][scenarios][activity]['transport_truck']['amount']
                            #     transport_ref_truck_i = comparison_dict[subsystem][scenarios][activity]['transport_ref_truck']['amount']
                                                           
                                    
                dry_spangles.append([PC_i,dry_spangles_i])
                blue_extract.append([PC_i,blue_extract_i])
                CPAc.append([PC_i,CPAc_i])
                CPDc.append([PC_i,CPDc_i])
                # transport_car.append([PC_i,transport_car_i])
                # transport_ship.append([PC_i,transport_ship_i])
                # transport_truck.append([PC_i,transport_truck_i])
                # transport_ref_truck.append([PC_i,transport_ref_truck_i])            
                
                
            dry_spangles = np.array(dry_spangles)
            blue_extract = np.array(blue_extract)
            CPAc = np.array(CPAc)
            CPDc = np.array(CPDc)
            # transport_car = np.array(transport_car)
            # transport_ship = np.array(transport_ship)
            # transport_truck = np.array(transport_truck)
            # transport_ref_truck = np.array(transport_ref_truck)   
        
        
        ### SENSITIVITY OF THE COMPOSITION OF THE BOP TO BIOMASS PRODUCTIVITY
        
        prod = np.arange(1,10,.1)
        
        dry_spangles_prod = []
        blue_extract_prod = []
        CPAc_prod = []
        CPDc_prod = []
        transport_car_prod = []
        transport_ship_prod = []
        transport_truck_prod = []
        transport_ref_truck_prod = []
        
        for prod_i in prod:
            
            # get the parameter values for the different scenarios
            model_param_dict = SetParameters(param_file_dir)
            
            for tech in model_param_dict.keys():
                model_param_dict[tech]['productivity'] = prod_i
            
            comparison_dict = ScenarioDataDict (model_param_dict, lifetime_file_dir)

    
            for subsystem in comparison_dict.keys():
                for scenarios in comparison_dict[subsystem].keys():
                    if scenarios == 'tech_1': continue
                    for activity in comparison_dict[subsystem][scenarios]:
                        
                        if activity == recipe['p'][0][1]: 
                            dry_spangles_prod_i = comparison_dict[subsystem][scenarios][activity]['dry_spangles']['amount']
                            print('dry spangles after S1A5: ', dry_spangles)
                        
                        if activity == recipe['p'][1][1]: 
                            blue_extract_prod_i = comparison_dict[subsystem][scenarios][activity]['blue_extract_UF2']['amount']
                            print('blue extract after S2A5: ', blue_extract)
                            
                        if activity == 'S2A6Concentration': 
                            CPDc_prod_i = comparison_dict[subsystem][scenarios][activity]['CPD_concentrate']['amount']
                            print('CPDc after S2A6: ', CPDc)                        
                            
                        if activity == recipe['p'][2][1]: 
                            CPAc_prod_i = comparison_dict[subsystem][scenarios][activity]['concentrate']['amount']
                            print('CPAc after S3A4: ', CPAc)   
                            
                        # if activity == 'S123A8Transport':
                        #     transport_car_prod_i = comparison_dict[subsystem][scenarios][activity]['transport_car']['amount']
                        #     transport_ship_prod_i = comparison_dict[subsystem][scenarios][activity]['transport_ship']['amount']
                        #     transport_truck_prod_i = comparison_dict[subsystem][scenarios][activity]['transport_truck']['amount']
                        #     transport_ref_truck_prod_i = comparison_dict[subsystem][scenarios][activity]['transport_ref_truck']['amount']
                                      
                            
            dry_spangles_prod.append([prod_i,dry_spangles_prod_i])
            blue_extract_prod.append([prod_i,blue_extract_prod_i])
            CPAc_prod.append([prod_i,CPAc_prod_i])
            CPDc_prod.append([prod_i,CPDc_prod_i])
            # transport_car_prod.append([prod_i,transport_car_prod_i])
            # transport_ship_prod.append([prod_i,transport_ship_prod_i])
            # transport_truck_prod.append([prod_i,transport_truck_prod_i])
            # transport_ref_truck_prod.append([prod_i,transport_ref_truck_prod_i])                
            
        dry_spangles_prod = np.array(dry_spangles_prod)
        blue_extract_prod = np.array(blue_extract_prod)
        CPAc_prod = np.array(CPAc_prod)
        CPDc_prod = np.array(CPDc_prod)        
        # transport_car_prod = np.array(transport_car_prod)
        # transport_ship_prod = np.array(transport_ship_prod)
        # transport_truck_prod = np.array(transport_truck_prod)
        # transport_ref_truck_prod = np.array(transport_ref_truck_prod)   
        
        import matplotlib.pyplot as plt
        fig = plt.figure()
        
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122,sharey = ax1)
        
        #ax3 = fig.add_subplot(223)
        #ax4 = fig.add_subplot(224,sharey = ax3)
        
        ## plot relation to PC content
        ax2.plot(dry_spangles[:,0],dry_spangles[:,1],label = 'Dry spangles',c = 'green')
        ax2.plot(blue_extract[:,0],blue_extract[:,1],'--', label = 'Blue extract',c = '#08519c')
        ax2.plot(CPAc[:,0],CPAc[:,1],'-.', label = 'CPAc',c = 'red')
        ax2.plot(CPDc[:,0],CPDc[:,1],':', label = 'CPDc',c = 'orange')
        
        ## plot productivity
        #ax1.plot(dry_spangles_prod[:,0],dry_spangles_prod[:,1],label = 'Dry spangles',c = '#08519c')
        ax1.plot(blue_extract_prod[:,0],blue_extract_prod[:,1],'--', label = 'Blue extract',c = '#08519c')
        ax1.plot(CPAc_prod[:,0],CPAc_prod[:,1],'-.', label = 'CPAc',c = 'red')
        ax1.plot(CPDc_prod[:,0],CPDc_prod[:,1],':', label = 'CPDc',c = 'orange')
        
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys())
        
        
        # ax1.set_xticklabels([])
        # ax2.set_xticklabels([])
        
        ax2.set_xlabel('PC content [%]')
        
        ax1.set_xlabel('Productivity [g/m2/day]')
        
        ax1.set_ylabel('Amount [kg DW-eq]')
       
        
        #ax3.set_ylabel('Water [m3]')
        
        #fig.suptitle('%s-%s-%s'% (pi[0],pi[1],pi[2]))
        
        plt.tight_layout()
        plt.show()    
        
        fig.savefig(wdir + '/results/sensitivity/sensitivity_BoP.pdf')
    
        plt.close()    
        
        
        # fig = plt.figure()
        
        # ax1 = fig.add_subplot(121)
        # ax2 = fig.add_subplot(122,sharey = ax1)
        
        # #ax3 = fig.add_subplot(223)
        # #ax4 = fig.add_subplot(224,sharey = ax3)
        
        # ## plot relation to PC content
        # ax2.plot(transport_car[:,0],transport_car[:,1],label = 'transport_car',c = 'green')
        # ax2.plot(transport_ship[:,0],transport_ship[:,1],'--', label = 'transport_ship',c = '#08519c')
        # ax2.plot(transport_truck[:,0],transport_truck[:,1],'-.', label = 'transport_truck',c = 'red')
        # ax2.plot(transport_ref_truck[:,0],transport_ref_truck[:,1],':', label = 'transport_ref_truck',c = 'orange')
        
        # ## plot productivity
        # #ax1.plot(dry_spangles_prod[:,0],dry_spangles_prod[:,1],label = 'Dry spangles',c = '#08519c')
        # ax1.plot(transport_car_prod[:,0],transport_car_prod[:,1],label = 'transport_car',c = 'green')
        # ax1.plot(transport_ship_prod[:,0],transport_ship_prod[:,1],'--', label = 'transport_ship',c = '#08519c')
        # ax1.plot(transport_truck_prod[:,0],transport_truck_prod[:,1],'-.', label = 'transport_truck',c = 'red')
        # ax1.plot(transport_ref_truck_prod[:,0],transport_ref_truck_prod[:,1],':', label = 'transport_ref_truck',c = 'orange')
        

        # handles, labels = plt.gca().get_legend_handles_labels()
        # by_label = dict(zip(labels, handles))
        # plt.legend(by_label.values(), by_label.keys())
        
        
        # # ax1.set_xticklabels([])
        # # ax2.set_xticklabels([])
        
        # ax2.set_xlabel('PC content [%]')
        
        # ax1.set_xlabel('Productivity [g/m2/day]')
        
        # ax1.set_ylabel('Transport [ton*km]')
       
        
        # #ax3.set_ylabel('Water [m3]')
        
        # #fig.suptitle('%s-%s-%s'% (pi[0],pi[1],pi[2]))
        
        # plt.tight_layout()
        # plt.show()    
        # fig.savefig(str(wdir + ''))
       
        
        # fig.savefig(wdir + '/results/sensitivity/sensitivity_transport.pdf')

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
            
            
            
            
            
            
            
            
            
            
    return comparison_dict_per_main_output





def WaterElecAnalysis (comparison_dict_per_main_output, wdir):
    
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import pathlib
    import os
    
    from S0_elec_water_analysis import ElecWaterBiorefineryScenarios
    
    # create a directory to store the results of the water/electricity use analysis 
    result_dir_water_elec = os.path.join(wdir,'results/elec&water')  
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
        
            plotData_elec[subsystem], plotData_water[subsystem] = ElecWaterBiorefineryScenarios (wdir, new_comparison_dict[subsystem], file_name, subsystem)
            
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
    fig.savefig(str(wdir + '/results/elec&water/total_electricity.pdf'))
    
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
    
    fig.savefig(str(wdir + '/results/elec&water/total_water.pdf'))
        
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
    directory = os.path.join(wdir, str('results/elec&water/' + file_name))
    

    with pd.ExcelWriter(directory, mode = 'w') as writer:
        df_elec.to_excel(writer, sheet_name='electricity') 
        df_water.to_excel(writer, sheet_name='water')        
            
    df_elec = pd.DataFrame.from_dict(data_dict_plot_elec, orient = 'columns')
        
    
    return comparison_dict_per_main_output








