# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 08:51:22 2022

@author: leabr
"""

def ScenarioDataDictAllTogether (param_dict, lifetime_file_name):
    '''
    Function that generates a dictionary with the data for each scenario for 
    the complete system (i.e. no subsystems defined).

    Parameters
    ----------
    model_param_dict : TYPE
        DESCRIPTION.
    lifetime_file_name : TYPE
        DESCRIPTION.

    Returns
    -------
    comparison_dict : TYPE
        DESCRIPTION.

    '''
    from S0_spirulina_production import SpirulinaProductionDict, PasteToSpangles
    from S0_spirulina_processing import PCExtractionDict, CPATreatmentDataDict    
    
    comparison_dict = {}
    
    for scenario in param_dict.keys():
        
               
        print('\nScenario %s' %scenario)
        
        tech_period = str(param_dict[scenario]['tech_period'])
        line = param_dict[scenario]['line']
        productivity = param_dict[scenario]['productivity']
        PC_content = param_dict[scenario]['PC_content']
        PC_extraction_efficiency = param_dict[scenario]['PC_extraction_efficiency']
        working_days = param_dict[scenario]['working_days']
        number_ORP = param_dict[scenario]['number_ORP']
        surface_per_ORP = param_dict[scenario]['surface_per_ORP']
        VFS_number = param_dict[scenario]['VFS_number']
        harvesting_efficiency = param_dict[scenario]['harvesting_efficiency']
        distance_car = param_dict[scenario]['distance_car']
        distance_ship = param_dict[scenario]['distance_ship']
        distance_truck_S12 = param_dict[scenario]['distance_truck_S12']
        volume_ORP = param_dict[scenario]['volume_ORP']
        distance_truck_S23 = param_dict[scenario]['distance_truck_S23']
        print('All parameters imported.')
        
        production_data_dict = SpirulinaProductionDict (tech_period, productivity, 
                                                        working_days, harvesting_efficiency, line, 
                                                        distance_car, distance_ship, distance_truck_S12, number_ORP, 
                                                        surface_per_ORP, VFS_number, volume_ORP, 
                                                        lifetime_file_name)
        
        if line == 'dry':
            paste_DW = production_data_dict['S1A3Dewatering']['paste']['amount']
            dry_spangles_DW = production_data_dict['S1A5Drying']['dry_spangles']['amount']
            
        if line == 'wet':
            paste_DW = production_data_dict['S1A3Dewatering']['paste']['amount']
            dry_spangles_DW = PasteToSpangles (tech_period, paste_DW)
        
        print('paste: %s' %paste_DW)
        print('dry spangles: %s' %dry_spangles_DW)

        PC_extraction_data_dict = PCExtractionDict (tech_period, dry_spangles_DW, PC_content, PC_extraction_efficiency, distance_truck_S23)
        BE_DW = PC_extraction_data_dict['S2A5Ultrafiltration2']['blue_extract_UF2']['amount']
        print('blue extract: %s' %BE_DW)
        
        CPA_DW = PC_extraction_data_dict['S2A2Centrifugation']['CPA']['amount']
        
        CPA_treatment_data_dict = CPATreatmentDataDict (tech_period, CPA_DW)
        CPAc_DW = CPA_treatment_data_dict['S3A4Concentration']['concentrate']['amount']
        print('CPAc: %s' %CPAc_DW)
        
        # merge the three dictionaries
        comparison_dict[scenario] = {**production_data_dict, **PC_extraction_data_dict, **CPA_treatment_data_dict} 
        comparison_dict[scenario]['S12A8Transport'] = {}
        comparison_dict[scenario]['S12A8Transport']['transport_car'] = production_data_dict['S1A8Transport']['transport_car']
        
        if line == 'wet':
            comparison_dict[scenario]['S12A8Transport']['transport_ship_refrigerated'] = production_data_dict['S1A8Transport']['transport_ship_refrigerated']
            comparison_dict[scenario]['S12A8Transport']['transport_truck_refrigerated'] = production_data_dict['S1A8Transport']['transport_truck_refrigerated']
            
        if line == 'dry':
            comparison_dict[scenario]['S12A8Transport']['transport_ship'] = production_data_dict['S1A8Transport']['transport_ship']
            comparison_dict[scenario]['S12A8Transport']['transport_truck'] = production_data_dict['S1A8Transport']['transport_truck']
                     
        comparison_dict[scenario]['S23A8Transport'] = {}
        comparison_dict[scenario]['S23A8Transport']['transport_ref_truck'] = PC_extraction_data_dict['S2A8Transport']['transport_truck']

        comparison_dict[scenario]['S1A0Building'] = production_data_dict['S1A0Building'] 
        comparison_dict[scenario]['S1A0Operation'] = production_data_dict['S1A0Operation']    
    
    return comparison_dict



def ScenarioDataDict (model_param_dict, lifetime_file_name):
    '''
    Creates a dictionary with the data for each of the scenario defined. Data
    are for the total amount of products produced (e.g. if technical periods 
    1 and 2 are compared, the total amount of products produced in each of the
    periods).
    '''
    from S0_spirulina_production import SpirulinaProductionDict, PasteToSpangles
    from S0_spirulina_processing import PCExtractionDict, CPATreatmentDataDict
        
    comparison_dict = {}
    comparison_dict['S1'] = {}
    comparison_dict['S2'] = {}
    comparison_dict['S3'] = {}
    comparison_dict['transport_S12'] = {}
    comparison_dict['transport_S23'] = {}
    comparison_dict['infrastructures'] = {}
    comparison_dict['operation'] = {}
   
    
    print('\nCreation of the datasets for each scenario..')
        
    for scenario in model_param_dict.keys():
        
        print('\nScenario %s' %scenario)
        
        tech_period = str(model_param_dict[scenario]['tech_period'])
        line = model_param_dict[scenario]['line']
        #print(line)
        productivity = model_param_dict[scenario]['productivity']
        PC_content = model_param_dict[scenario]['PC_content']
        PC_extraction_efficiency = model_param_dict[scenario]['PC_extraction_efficiency']
        working_days = model_param_dict[scenario]['working_days']
        number_ORP = model_param_dict[scenario]['number_ORP']
        surface_per_ORP = model_param_dict[scenario]['surface_per_ORP']
        VFS_number = model_param_dict[scenario]['VFS_number']
        harvesting_efficiency = model_param_dict[scenario]['harvesting_efficiency']
        distance_car = model_param_dict[scenario]['distance_car']
        distance_ship = model_param_dict[scenario]['distance_ship']
        distance_truck_S12 = model_param_dict[scenario]['distance_truck_S12']
        volume_ORP = model_param_dict[scenario]['volume_ORP']
        distance_truck_S23 = model_param_dict[scenario]['distance_truck_S23']
        print('All parameters imported.')
        
        production_data_dict = SpirulinaProductionDict (tech_period, productivity, 
                                                        working_days, harvesting_efficiency, line, 
                                                        distance_car, distance_ship, distance_truck_S12, number_ORP, 
                                                        surface_per_ORP, VFS_number, volume_ORP, 
                                                        lifetime_file_name)
        
        if line == 'dry':
            paste_DW = production_data_dict['S1A3Dewatering']['paste']['amount']
            dry_spangles_DW = production_data_dict['S1A5Drying']['dry_spangles']['amount']
            
        if line == 'wet':
            paste_DW = production_data_dict['S1A3Dewatering']['paste']['amount']
            dry_spangles_DW = PasteToSpangles (tech_period, paste_DW)
        
        print('paste: %s' %paste_DW)
        print('dry spangles: %s' %dry_spangles_DW)

        PC_extraction_data_dict = PCExtractionDict (tech_period, dry_spangles_DW, PC_content, PC_extraction_efficiency, distance_truck_S23)
        BE_DW = PC_extraction_data_dict['S2A5Ultrafiltration2']['blue_extract_UF2']['amount']
        print('blue extract: %s' %BE_DW)
        
        CPA_DW = PC_extraction_data_dict['S2A2Centrifugation']['CPA']['amount']
        
        CPA_treatment_data_dict = CPATreatmentDataDict (tech_period, CPA_DW)
        CPAc_DW = CPA_treatment_data_dict['S3A4Concentration']['concentrate']['amount']
        print('CPAc: %s' %CPAc_DW)

        
        comparison_dict['S1'][scenario] = production_data_dict
        comparison_dict['S2'][scenario] = PC_extraction_data_dict
        comparison_dict['S3'][scenario] = CPA_treatment_data_dict
        
        comparison_dict['transport_S12'][scenario] = {}
        comparison_dict['transport_S12'][scenario]['S12A8Transport'] = {}
        comparison_dict['transport_S12'][scenario]['S12A8Transport']['transport_car'] = production_data_dict['S1A8Transport']['transport_car']
        
        if line == 'wet':
            comparison_dict['transport_S12'][scenario]['S12A8Transport']['transport_ship_refrigerated'] = production_data_dict['S1A8Transport']['transport_ship_refrigerated']        
            comparison_dict['transport_S12'][scenario]['S12A8Transport']['transport_truck_refrigerated'] = production_data_dict['S1A8Transport']['transport_truck_refrigerated']
        
        if line == 'dry':
          comparison_dict['transport_S12'][scenario]['S12A8Transport']['transport_ship'] = production_data_dict['S1A8Transport']['transport_ship']        
          comparison_dict['transport_S12'][scenario]['S12A8Transport']['transport_truck'] = production_data_dict['S1A8Transport']['transport_truck']
      
        
        comparison_dict['transport_S23'][scenario] = {}
        comparison_dict['transport_S23'][scenario]['S23A8Transport'] = {}
        comparison_dict['transport_S23'][scenario]['S23A8Transport']['transport_ref_truck'] = PC_extraction_data_dict['S2A8Transport']['transport_truck']
       
        comparison_dict['infrastructures'][scenario] = {}
        comparison_dict['infrastructures'][scenario]['S1A0Building'] = production_data_dict['S1A0Building']     
        
        comparison_dict['operation'][scenario] = {}
        comparison_dict['operation'][scenario]['S1A0Operation'] = production_data_dict['S1A0Operation']   
        
    return comparison_dict


def ScenarioDataDictPerProcess (comparison_dict):

    '''
    Creates a dictionary with the data for each of the scenario defined. Data
    are for the total amount of products produced divided per the main output of 
    each process, for each process. The activities S1A0Buidling and S1A0Operation
    do not have a reference flow (i.e. main output to be divided with). They 
    are not divided per process or FU as they represent the total amount of 
    inputs/outputs used to build and run the facilities i.e. it does not depend
    on the amount of biomass produced and the values are the same no matter the 
    amount of biomass produced.
    '''   
    bioref_dict_final = {}
    
    print('\nCreate the dataset dictionaries per process..')

    for scenario in comparison_dict.keys():
        
        print('\nScenario: %s' %scenario)
                    
        bioref_dict_final[scenario] = {}
        
        for act in comparison_dict[scenario].keys():
            
            print('\nActivity: %s' %act)
            bioref_dict_final[scenario][act] = {}
            
            if act == 'S1A0Building' or act == 'S1A0Operation':
                print('No main output to divide the exchange amounts by.\n>> Copy the exchanges!')
                
                # copy the amounts as they are in the original dataset
                i = 0
                for exc in comparison_dict[scenario][act].keys():
                    bioref_dict_final[scenario][act][exc] = {}
                    bioref_dict_final[scenario][act][exc]['amount'] = comparison_dict[scenario][act][exc]['amount']
                    bioref_dict_final[scenario][act][exc]['unit'] = comparison_dict[scenario][act][exc]['unit']
                    bioref_dict_final[scenario][act][exc]['type'] = comparison_dict[scenario][act][exc]['type']
                    i+=1
                    print('%s/%s'%(i,len(list(comparison_dict[scenario][act].keys()))))
                print('Done!')
            else:
                # get the amount of reference flow 
                for exc in comparison_dict[scenario][act].keys():
                    if comparison_dict[scenario][act][exc]['type'] == 'ref_flow':
                        value = comparison_dict[scenario][act][exc]['amount']
                    else: pass
                
                # add the amounts divided per the value of reference flow to the dict
                for exc in comparison_dict[scenario][act].keys():
                    exc_type =  comparison_dict[scenario][act][exc]['type']
                    amount = comparison_dict[scenario][act][exc]['amount']
                    unit = comparison_dict[scenario][act][exc]['unit']
                    print('\nExchange: %s \nType: %s \nAmount: %.2f %s => %.2f %s'%(exc, exc_type, amount, unit, amount/value, unit))
                    bioref_dict_final[scenario][act][exc] = {}
                    bioref_dict_final[scenario][act][exc]['amount'] = comparison_dict[scenario][act][exc]['amount'] / value
                    bioref_dict_final[scenario][act][exc]['unit'] = comparison_dict[scenario][act][exc]['unit']
                    bioref_dict_final[scenario][act][exc]['type'] = comparison_dict[scenario][act][exc]['type']
    
    print('Done!')
    
    return bioref_dict_final


def ScenarioDataDictPerMainOutput (comparison_dict_subsystem, act_name, exc_name, scaling_factor):
    '''
    Creates a dictionary with the data for each of the scenario defined. Data
    are for the total amount of products produced (e.g. if technical periods 
    1 and 2 are compared, the total amount of products produced in each of the
    periods).
    
    '''        
    comparison_dict_subsystem_per_main_output = {}
    

    for scenario in comparison_dict_subsystem.keys():
        
        comparison_dict_subsystem_per_main_output[scenario] = {}
    
        value = comparison_dict_subsystem[scenario][act_name][exc_name]['amount']
                    
        for act in comparison_dict_subsystem[scenario].keys():
            
            if act == 'S1A0Building' or act == 'S1A0Operation':
                continue
            
            if act == 'S1A8Transport' or act == 'S2A8Transport':
                continue
            
            if act != 'S1A0Building' and act != 'S1A0Operation' and act != 'S1A8Transport' and act != 'S2A8Transport':
            
                comparison_dict_subsystem_per_main_output[scenario][act] = {}
                
                for exc in comparison_dict_subsystem[scenario][act].keys():
                    
                    comparison_dict_subsystem_per_main_output[scenario][act][exc] = {}
                    
                    comparison_dict_subsystem_per_main_output[scenario][act][exc]['amount'] = comparison_dict_subsystem[scenario][act][exc]['amount'] / value * scaling_factor
                    comparison_dict_subsystem_per_main_output[scenario][act][exc]['unit'] = comparison_dict_subsystem[scenario][act][exc]['unit']
                    comparison_dict_subsystem_per_main_output[scenario][act][exc]['type'] = comparison_dict_subsystem[scenario][act][exc]['type']
            
    return comparison_dict_subsystem_per_main_output


def ScenarioDataExcel (result_dir, comparison_dict, filename):
    '''
    Creates a dictionary with the data for each of the scenario defined. Data
    are for the total amount of products produced (e.g. if technical periods 
    1 and 2 are compared, the total amount of products produced in each of the
    periods).
    '''
    import pandas as pd
    import numpy as np
       
    ## WRITE THE DATA INTO AN EXCEL FILE
    import os
    #print(os.getcwd())
    #directory = os.path.join(os.getcwd(),str('lci-datasets/' + filename + '.xlsx'))
    directory = os.path.join(result_dir + '/' + filename + '.xlsx')
    
    with pd.ExcelWriter(directory,mode = 'w') as writer:
        
        for scenario in comparison_dict.keys():
            
            for act in comparison_dict[scenario].keys():
                #print(act)
                
                df_data = []
                
                for scenario in comparison_dict.keys():
    
                    data_dict = comparison_dict[scenario][act]
                    data_dict = {key:comparison_dict[scenario][act][key]['amount'] for key in data_dict.keys()}
                    
                    scenario_name = str('scenario ' + str(scenario))
                    
                    index_names = [scenario_name,'unit','type']
                    
                    df_data_i = pd.DataFrame(data_dict,index = index_names).T
                    
                    df_data_i['unit'] = [comparison_dict[scenario][act][key]['unit'] for key in data_dict.keys()]
                    
                    df_data_i['type'] = [comparison_dict[scenario][act][key]['type'] for key in data_dict.keys()]
                    
                    df_data.append(df_data_i.T)
    
                df_data = pd.concat(df_data).T
                
                df_data= df_data.loc[:,~df_data.columns.duplicated()].copy()
                
                cols = np.sort(df_data.columns)
                df_data = df_data[cols]
                df_data.to_excel(writer, sheet_name=act) 
    
    return comparison_dict
