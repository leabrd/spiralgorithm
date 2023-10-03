# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 19:44:27 2022

@author: leabr
"""

def InitialSpangleProductivity (tech_period):
    
    '''Returns the initial dry spangle productivity for the periods 1 and 2.
    These values should be used to obtain the initial 2019 and 2022 datasets
    for Spirulina cultivation. The initial spangles productivity is calculated
    for the specific layout of the cultivation facility which was the same 
    for period 1 and 2'''
    
    number_ORP = 6 # number of ORPs harvested [unit]
    surface_per_ORP = 705 # surface of one ORP [m2]

    if tech_period == '1':
        ## DATA COLLECTED
        dry_spangles_sc1 = 27.53 # amount of dry spangles [kg]
        DM_dry_spangles_sc1 = 96.8 # dry matter content of the paste [%]
        dry_spangles_DW_sc1 = dry_spangles_sc1 * DM_dry_spangles_sc1 / 100 # dry spangles daily productivity [kg DW-eq/day]
        spangle_daily_areal_productivity = dry_spangles_DW_sc1 * 1000 / (surface_per_ORP * number_ORP) # dry spangles daily areal productivity [g DW-eq/m2/day]
        
    if tech_period == '2':
        ## DATA COLLECTED
        dry_spangles_sc1 = 15.59 # amount of paste [kg]
        DM_dry_spangles_sc1 = 94.99 # dry matter content of the paste [%]
        dry_spangles_DW_sc1 = dry_spangles_sc1 * DM_dry_spangles_sc1 / 100 # dry spangles daily productivity [kg DW-eq/day]
        spangle_daily_areal_productivity = dry_spangles_DW_sc1 * 1000 / (surface_per_ORP * number_ORP) # dry spangles daily areal productivity [g DW-eq/m2/day]
    
    return spangle_daily_areal_productivity



def InitialPCExtractionEfficiency ():
    
    '''The efficiency of the extraction process at pilot scale was calculated 
    from the measurement of the concentration obtained by extracting PC at lab 
    and pilot scale. These measurements were conducted for period 2 only. '''
    
    # Amount of dry spangles used
    dry_spangles_sc1 = 12.84 # amount of dry spangles [kg]
    DM_dry_spangles_sc1 = 94.99 # dry matter content of the dry spangles [% DM]
    dry_spangles_DW_sc1 = dry_spangles_sc1 * DM_dry_spangles_sc1 / 100 # amount of dry spangles [kg DW-eq]
    
    # Amount of blue extract produced
    blue_extract_UF2_sc1 = 43.01 # amount of blue extract from UF2 [kg]
    DM_blue_extract_UF2_sc1 = 6.55 # dry matter content of the blue extract [%]
    blue_extract_UF2_DW_sc1 = blue_extract_UF2_sc1 * DM_blue_extract_UF2_sc1 / 100
    
    # Amount PC before extraction (in the mix before centrifugation)
    PC_concentration_lab = 2.78 # concentration of PC obtained from extraction in lab on the mix sampled before centrifugation [g/L]
    water_maceration_sc1 = 500 # volume of water [L]
    volume_mix = dry_spangles_DW_sc1 + water_maceration_sc1 # volume of mix with assumption on density [L] or [kg]
    amount_PC_mix = volume_mix * PC_concentration_lab / 1000 # amount of PC in the mix after lab extraction [kg]
    
    # Amount PC recovered after pilot extraction (in the blue extract after UF2)
    PC_concentration = 30.09 # PC concentration in the blue extract from UF2 [g/L]
    density_blue_extract_UF2 = 1.014 # density of the blue extract from UF2 [kg/L]
    volume_blue_extract_UF2 = blue_extract_UF2_sc1 * density_blue_extract_UF2 # volume of blue extract from UF2 calculated from density [L]
    amount_PC_blue_extract_UF2 = volume_blue_extract_UF2 * PC_concentration / 1000 # amout of pure PC in the blue extract [kg]

    # Pilot extraction efficiency
    pilot_extraction_efficiency = amount_PC_blue_extract_UF2 / amount_PC_mix * 100  
    
    return pilot_extraction_efficiency



def InitialPCContent (tech_period):
    
    '''Returns the initial PC content of the Spirulina biomass. The PC content
    of the biomass was not measured in the specific Spirulina biomass used for 
    the extraction. The value was calculated from the blue extract obtained at
    the end and the concentration in pure PC. The pilot extraction efficiency
    value from tech_period 2 was used in pilot 1. It was therefore assumed that 
    the efficiency of the extraction does not depend on the load which is an 
    assumption. The biggest the load, the lowest the extraction effiency.'''
    
    PC_data_dict = {}    
    
    pilot_extraction_efficiency = InitialPCExtractionEfficiency ()
       
    if tech_period == '1':
        ## DATA COLLECTED 
        dry_spangles_sc1 = 27.53 # amount of the dry spangles [kg]
        DM_dry_spangles_sc1 = 96.8 # dry matter content of the dry spangles [% DW]
        dry_spangles_DW_sc1 = dry_spangles_sc1 * DM_dry_spangles_sc1 /100
        PC_data_dict['dry spangles'] = {'wet mass':dry_spangles_sc1, 'DM content':DM_dry_spangles_sc1, 'dry mass': dry_spangles_DW_sc1}
        # amount of blue extract from UF1
        blue_extract_UF1_sc1 = 148 # amount of blue extract [kg]
        DM_blue_extract_UF1_sc1 = 5.84 # dry matter content of the blue extract [%]
        blue_extract_UF1_DW_sc1 = blue_extract_UF1_sc1 * DM_blue_extract_UF1_sc1/100 # amount of blue extract [kg DW-eq] 
        PC_data_dict['blue extract'] = {'wet mass':blue_extract_UF1_sc1, 'DM content':DM_blue_extract_UF1_sc1, 'dry mass': blue_extract_UF1_DW_sc1}
        # amount of pure PC in the blue extract from UF1
        PC_concentration = 20.95 # concentration of PC in the blue extract from UF1 [g/L]
        volume_blue_extract_UF1 = blue_extract_UF1_sc1 # assumed that the density was 1 (not measured)
        amount_PC_blue_extract_UF1 = volume_blue_extract_UF1 * PC_concentration / 1000
        PC_data_dict['amount_PC'] = amount_PC_blue_extract_UF1
        # PC content in the blue extract from UF1
        PC_content_blue_extract_UF1 = amount_PC_blue_extract_UF1 / blue_extract_UF1_DW_sc1 * 100
        other_molecules_blue_extract_UF1 = 100 - PC_content_blue_extract_UF1
        PC_data_dict['PC_content_blue_extract'] = PC_content_blue_extract_UF1
        # PC content biomass
        PC_content_biomass = amount_PC_blue_extract_UF1 / dry_spangles_DW_sc1 * 100 * 100 / pilot_extraction_efficiency
        PC_data_dict['PC_extraction_efficiency'] = pilot_extraction_efficiency
        PC_data_dict['PC_content_biomass'] = PC_content_biomass  
        
    if tech_period == '2':
        ## DATA COLLECTED
        dry_spangles_sc1 = 12.84 # amount of dry spangles [kg]
        DW_dry_spangles_sc1 = 94.99 # dry matter content of the dry spangles [% DM] # was 96.5 changed it to 94.99
        dry_spangles_DW_sc1 = dry_spangles_sc1 * DW_dry_spangles_sc1 / 100 # amount of dry spangles [kg DW-eq]
        PC_data_dict['dry spangles'] = {'wet mass':dry_spangles_sc1, 'DM content':DW_dry_spangles_sc1, 'dry mass': dry_spangles_DW_sc1}
        # amount of blue extract from UF2
        blue_extract_UF2_sc1 = 43.01 # amount of blue extract from UF2 [kg]
        DM_blue_extract_UF2_sc1 = 6.55 # dry matter content of the blue extract [%]
        blue_extract_UF2_DW_sc1 = blue_extract_UF2_sc1 * DM_blue_extract_UF2_sc1/100
        PC_data_dict['blue extract'] = {'wet mass':blue_extract_UF2_sc1, 'DM content':DM_blue_extract_UF2_sc1, 'dry mass': blue_extract_UF2_DW_sc1}
        # amount of PC in blue extract from UF2 (and other molecules)
        PC_concentration = 30.09 # PC concentration in the blue extract from UF2 [g/L]
        density_blue_extract_UF2 = 1.014 # density of the blue extract from UF2 [kg/L]
        volume_blue_extract_UF2 = blue_extract_UF2_sc1 * density_blue_extract_UF2 # volume of blue extract from UF2 calculated from density [L]
        amount_PC_blue_extract_UF2 = volume_blue_extract_UF2 * PC_concentration / 1000 # amout of pure PC in the blue extract [kg]
        PC_data_dict['amount_PC'] = amount_PC_blue_extract_UF2
        # PC content in the blue extract from UF2
        PC_content_blue_extract_UF2 = amount_PC_blue_extract_UF2 / blue_extract_UF2_DW_sc1 * 100
        other_molecules_blue_extract_UF2 = 100 - PC_content_blue_extract_UF2
        PC_data_dict['PC_content_blue_extract'] = PC_content_blue_extract_UF2
        # PC content in the total biomass according to the extraction efficiency
        PC_content_biomass = amount_PC_blue_extract_UF2 / dry_spangles_DW_sc1 * 100 * 100 / pilot_extraction_efficiency
        PC_data_dict['PC_extraction_efficiency'] = pilot_extraction_efficiency
        PC_data_dict['PC_content_biomass'] = PC_content_biomass  

    return PC_data_dict


def InitialParametersDict (ddir, param_file_name):
    
    '''Creates an Excel file with the initial parameters of tech 1 and tech 2
    based on the data collected. The parameter values are exported as an Excel 
    file and the file can be completed for other scenarios calculations (used
    as a template).'''
    
    import os
    import pandas as pd
    
    param_file_dir = os.path.join(ddir, param_file_name)
        
    dict_list = []
    parameter_dict = {}
    tech_period_list = ['1', '2']
    harvesting_eff = {'1':52.13,
                      '2':75.36}
    
    ## CREATE AN EXCEL FILE WITH THE INITIAL VALUES OF PARAMETERS
    for tech_period in tech_period_list:
        
        productivity = InitialSpangleProductivity (tech_period)
        PC_data_dict = InitialPCContent (tech_period)
        working_days = 365
        production_capacity = PC_data_dict['dry spangles']['dry mass'] * working_days / 1000

        parameter_dict['tech_period'] = tech_period 
        parameter_dict['line'] = 'dry'
        parameter_dict['productivity'] = round(productivity,2)
        parameter_dict['PC_content'] = round(PC_data_dict['PC_content_biomass'],2)
        parameter_dict['PC_extraction_efficiency'] = round(PC_data_dict['PC_extraction_efficiency'],2)
        parameter_dict['dry_spangles'] = round(PC_data_dict['dry spangles']['dry mass'],2)
        parameter_dict['blue_extract']  = round(PC_data_dict['blue extract']['dry mass'], 2)
        parameter_dict['pure_PC'] = round(PC_data_dict['amount_PC'], 2)
        parameter_dict['working_days'] = 365
        parameter_dict['spangles_production_capacity'] = round(production_capacity, 2)
        parameter_dict['number_ORP'] = 6
        parameter_dict['surface_per_ORP'] = 705
        parameter_dict['harvesting_efficiency'] = harvesting_eff[tech_period]
        parameter_dict['distance_car'] = 12.7
        parameter_dict['distance_ship'] = 562
        parameter_dict['distance_truck_S12'] = 21
        parameter_dict['distance_truck_S23'] = 985       
        parameter_dict['VFS_number'] = 3
        parameter_dict['volume_ORP'] = 200

        df = pd.DataFrame(parameter_dict, index=[str('tech_' + tech_period)]).T
        dict_list.append(df)
    
    parameter_df = pd.concat(dict_list, axis =1)
    
    parameter_df.to_excel(param_file_dir)
    
    print('Location of the parameter file: %s' %param_file_dir)

    return parameter_df


def SetParameters (parameters_file_name):
    
    import pandas as pd
    
    param_dict = {}
            
    df = pd.read_excel(parameters_file_name, index_col = 0) # convert the Excel file into a dataframe
    temp_param_dict = df.to_dict() # convert the dataframe into a temporary dictionary
    
    for item in temp_param_dict.keys():
                    
        param_dict[item] = temp_param_dict[item]
    
    return param_dict


def DatasetScaling (scaling_dict, parameters_file_name):
    
    '''The scaling can only be done for dry_spangles or 'blue_extract'.
    Complete the parameters excel file from the info given.'''
    
    import pandas as pd
                
    df = pd.read_excel(parameters_file_name, index_col = 0) # convert the Excel file into a dataframe
    param_dict = df.to_dict() # convert the dataframe into a temporary dictionary
    
    initial_blue_extract = param_dict['tech_2']['blue_extract']
    initial_dry_spangles = param_dict['tech_2']['dry_spangles']
    number_ORP = param_dict['tech_2']['number_ORP']
    surface_per_ORP = param_dict['tech_2']['surface_per_ORP']
    working_days = param_dict['tech_2']['working_days']
        
    param_dict['tech_2a'] = param_dict['tech_2'].copy()
    param_dict['tech_2a']['dry_spangles'] = scaling_dict['dry_spangles']
    param_dict['tech_2a']['productivity'] = scaling_dict['dry_spangles'] / (number_ORP*surface_per_ORP) *1000
    param_dict['tech_2a']['spangles_production_capacity'] = scaling_dict['dry_spangles'] * working_days / 1000
    param_dict['tech_2a']['blue_extract'] = '-'
    param_dict['tech_2a']['pure_PC'] = '-'
    
    param_dict['tech_2b'] = param_dict['tech_2'].copy()
    param_dict['tech_2b']['blue_extract'] = scaling_dict['blue_extract_UF2']
    param_dict['tech_2b']['pure_PC'] = '-'
    dry_spangles = scaling_dict['blue_extract_UF2'] * initial_dry_spangles / initial_blue_extract
    param_dict['tech_2b']['dry_spangles'] = dry_spangles
    param_dict['tech_2b']['productivity'] = dry_spangles / (number_ORP*surface_per_ORP) *1000
    param_dict['tech_2b']['spangles_production_capacity'] = dry_spangles * working_days / 1000

    df2 = pd.DataFrame(param_dict)
        
    df2.to_excel(parameters_file_name)  
    
    
    return param_dict