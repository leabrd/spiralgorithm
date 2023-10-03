# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 14:15:14 2022

@author: leabr
"""

def BiomassShaping (tech_period, paste_DW):
    
    biomass_balance_dict_sc1 = {}
    biomass_balance_dict = {}
    
    if tech_period == '1':
        ## DATA COLLECTED
        paste_sc1 = 91.45 # amount of slurry [kg]
        DM_paste_sc1 = 33.07 # dry matter content of clurry [%]
        paste_DW_sc1 = paste_sc1 * DM_paste_sc1 / 100  # amount of slurry [kg DW-eq]
        wet_spangles_sc1 = 80.14 # amount of wet spangles [kg]
        DM_wet_spangles_sc1 = DM_paste_sc1 # dry matter content of the paste [%]
        wet_spangles_DW_sc1 = wet_spangles_sc1 * DM_wet_spangles_sc1 /100
        biomass_balance_dict_sc1['paste'] = {'wet_mass':paste_sc1, 
                                             'DM_content' : DM_paste_sc1, 
                                             'dry_mass' :paste_DW_sc1}
        biomass_balance_dict_sc1['wet_spangles'] = {'wet_mass':wet_spangles_sc1, 
                                                    'DM_content':DM_wet_spangles_sc1, 
                                                    'dry_mass':wet_spangles_DW_sc1}
        ## DATA MODELLED 
        wet_spangles_DW = paste_DW * wet_spangles_DW_sc1 / paste_DW_sc1
        biomass_balance_dict['paste'] = paste_DW
        biomass_balance_dict['wet_spangles'] = wet_spangles_DW
        biomass_balance_dict['losses'] = paste_DW - wet_spangles_DW
    
    if tech_period == '2':
        ## DATA COLLECTED
        paste_sc1 = 77.38 # amount of slurry [kg]
        DM_paste_sc1 = 23.26 # dry matter content of clurry [%]
        paste_DW_sc1 = paste_sc1 * DM_paste_sc1 / 100  # amount of slurry [kg DW-eq]
        wet_spangles_sc1 = 64.03 # amount of paste [kg]
        DM_wet_spangles_sc1 = DM_paste_sc1 # dry matter content of the paste [%]
        wet_spangles_DW_sc1 = wet_spangles_sc1 * DM_wet_spangles_sc1 /100
        biomass_balance_dict_sc1['paste'] = {'wet_mass':paste_sc1, 
                                             'DM_content' : DM_paste_sc1, 
                                             'dry_mass' :paste_DW_sc1}
        biomass_balance_dict_sc1['wet_spangles'] = {'wet_mass':wet_spangles_sc1, 
                                                    'DM_content':DM_wet_spangles_sc1, 
                                                    'dry_mass':wet_spangles_DW_sc1}
        ## DATA MODELLED 
        wet_spangles_DW = paste_DW * wet_spangles_DW_sc1 / paste_DW_sc1
        biomass_balance_dict['paste'] = paste_DW
        biomass_balance_dict['wet_spangles'] = wet_spangles_DW
        biomass_balance_dict['losses'] = paste_DW - wet_spangles_DW
    
    return biomass_balance_dict_sc1, biomass_balance_dict


def ElectricityShaping (tech_period, paste_DW):
  
    # running_time = 5 # running time of the shaping machine in 2019 [h] ### VARIABLE
    # intensity = 0.7 # intensity of the shaping machine [A]
    # power = intensity * (1.7320508*0.85*380) # instant power of the pumps [W]
    # elec_shaping = (power/1000) * running_time # electricity use [kWh]  
    
    if tech_period == '1':
        ## DATA COLLECTED
        paste_sc1 = 91.45 # amount of slurry [kg]
        DM_paste_sc1 = 33.07 # dry matter content of clurry [%]
        paste_DW_sc1 = paste_sc1 * DM_paste_sc1 / 100  # amount of slurry [kg DW-eq]
        elec_sc1 = 0.508
        ## DATA MODELLED
        elec = paste_DW * elec_sc1 / paste_sc1
    else: 
        ## DATA COLLECTED
        paste_sc1 = 77.38 # amount of slurry [kg]
        DM_paste_sc1 = 23.26 # dry matter content of clurry [%]
        paste_DW_sc1 = paste_sc1 * DM_paste_sc1 / 100  # amount of slurry [kg DW-eq]
        elec_sc1 = 0.508
        ## DATA MODELLED
        elec = paste_DW * elec_sc1 / paste_DW_sc1

    return elec


def WaterShaping (tech_period, paste_DW):
    
    if tech_period == '1':
        ## DATA COLLECTED
        paste_sc1 = 91.45 # amount of slurry [kg]
        DM_paste_sc1 = 33.07 # dry matter content of clurry [%]
        paste_DW_sc1 = paste_sc1 * DM_paste_sc1 / 100  # amount of slurry [kg DW-eq]
        water_sc1 = 194.50
        ## DATA MODELLED
        water = paste_DW * water_sc1 / paste_sc1
    else: 
        ## DATA COLLECTED
        paste_sc1 = 77.38 # amount of slurry [kg]
        DM_paste_sc1 = 23.26 # dry matter content of clurry [%]
        paste_DW_sc1 = paste_sc1 * DM_paste_sc1 / 100  # amount of slurry [kg DW-eq]
        water_sc1 = 194.50
        ## DATA MODELLED
        water = paste_DW * water_sc1 / paste_DW_sc1

    return water


def WastewaterShaping (tech_period, paste_DW):
    
    if tech_period == '1':
        ## DATA COLLECTED
        paste_sc1 = 91.45 # amount of slurry [kg]
        DM_paste_sc1 = 33.07 # dry matter content of clurry [%]
        paste_DW_sc1 = paste_sc1 * DM_paste_sc1 / 100  # amount of slurry [kg DW-eq]
        wastewater_sc1 = -1 * 194.50 / 1000
        ## DATA MODELLED
        wastewater = paste_DW * wastewater_sc1 / paste_sc1
    else: 
        ## DATA COLLECTED
        paste_sc1 = 77.38 # amount of slurry [kg]
        DM_paste_sc1 = 23.26 # dry matter content of clurry [%]
        paste_DW_sc1 = paste_sc1 * DM_paste_sc1 / 100  # amount of slurry [kg DW-eq]
        wastewater_sc1 = -1 * 194.50 / 1000
        ## DATA MODELLED
        wastewater = paste_DW * wastewater_sc1 / paste_DW_sc1

    return wastewater


def ShapingDataDict (tech_period, paste_DW):
    
    data_dict = {}
    
    biomass_balance_dict_sc1, biomass_balance_dict = BiomassShaping (tech_period, paste_DW)

    ## BIOMASS INPUT
    data_dict['paste'] = {}
    data_dict['paste']['amount'] = biomass_balance_dict['paste']
    data_dict['paste']['unit'] = 'kg'
    data_dict['paste']['type'] = 'fg_input'
    
    ## BIOMASS OUTPUTS
    data_dict['wet_spangles'] = {}
    data_dict['wet_spangles']['amount'] = biomass_balance_dict['wet_spangles']
    data_dict['wet_spangles']['unit'] = 'kg DW-eq'
    data_dict['wet_spangles']['type'] = 'ref_flow'
    data_dict['losses'] = {}
    data_dict['losses']['amount'] = biomass_balance_dict['losses']
    data_dict['losses']['unit'] = 'kg DW-eq'
    data_dict['losses']['type'] = 'losses'
    
    ## ELECTRICITY
    data_dict['electricity_IT'] = {}
    data_dict['electricity_IT']['amount'] = ElectricityShaping(tech_period, paste_DW)
    data_dict['electricity_IT']['unit'] = 'kWh'
    data_dict['electricity_IT']['type'] = 'tech_input'
    
    ## GROUND WATER
    data_dict['ground_water'] = {}
    data_dict['ground_water']['amount'] = WaterShaping(tech_period, paste_DW)
    data_dict['ground_water']['unit'] = 'L'
    data_dict['ground_water']['type'] = 'tech_input'
    
    ## WASTEWATER
    data_dict['wastewater'] = {}
    data_dict['wastewater']['amount'] = WastewaterShaping(tech_period, paste_DW)
    data_dict['wastewater']['unit'] = 'm3'
    data_dict['wastewater']['type'] = 'tech_output'
 
    return data_dict