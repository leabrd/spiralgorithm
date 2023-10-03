# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 14:14:18 2022

@author: leabr
"""

def BiomassDewatering (tech_period, slurry_DW):
    
    biomass_balance_dict_sc1 = {}
    biomass_balance_dict = {}
    
    if tech_period == '1':
        ## DATA COLLECTED
        slurry_sc1 = 257.71 # amount of slurry [kg]
        DM_slurry_sc1 = 14.75 # dry matter content of clurry [%]
        slurry_DW_sc1 = slurry_sc1 * DM_slurry_sc1 / 100  # amount of slurry [kg DW-eq]
        paste_sc1 = 91.45 # amount of paste [kg]
        DM_paste_sc1 = 33.07 # dry matter content of the paste [%]
        paste_DW_sc1 = paste_sc1 * DM_paste_sc1 /100
        biomass_balance_dict_sc1['slurry'] = {'wet_mass':slurry_sc1, 
                                              'DM_content' : DM_slurry_sc1, 
                                              'dry_mass' :slurry_DW_sc1}
        biomass_balance_dict_sc1['paste'] = {'wet_mass':paste_sc1, 
                                             'DM_content':DM_paste_sc1, 
                                             'dry_mass':paste_DW_sc1}
        ## DATA MODELLED 
        paste_DW = slurry_DW * paste_DW_sc1 / slurry_DW_sc1
        biomass_balance_dict['slurry'] = slurry_DW
        biomass_balance_dict['paste'] = paste_DW
        biomass_balance_dict['losses'] = slurry_DW - paste_DW
    
    if tech_period == '2':
        ## DATA COLLECTED
        slurry_sc1 = 198.99 # amount of slurry [kg]
        DM_slurry_sc1 = 10.39 # dry matter content of clurry [%]
        slurry_DW_sc1 = slurry_sc1 * DM_slurry_sc1 / 100  # amount of slurry [kg DW-eq]
        paste_sc1 = 77.38 # amount of paste [kg]
        DM_paste_sc1 = 23.26 # dry matter content of the paste [%]
        paste_DW_sc1 = paste_sc1 * DM_paste_sc1 /100
        biomass_balance_dict_sc1['slurry'] = {'wet_mass':slurry_sc1, 
                                              'DM_content' : DM_slurry_sc1, 
                                              'dry_mass' :slurry_DW_sc1}
        biomass_balance_dict_sc1['paste'] = {'wet_mass':paste_sc1, 
                                             'DM_content':DM_paste_sc1, 
                                             'dry_mass':paste_DW_sc1}
        ## DATA MODELLED 
        paste_DW = slurry_DW * paste_DW_sc1 / slurry_DW_sc1
        biomass_balance_dict['slurry'] = slurry_DW
        biomass_balance_dict['paste'] = paste_DW
        biomass_balance_dict['losses'] = slurry_DW - paste_DW
       
    return biomass_balance_dict_sc1, biomass_balance_dict


def ElectricityDewatering (tech_period, slurry_DW):

    # length_cycle = 50/60 # lenght of a dewatering cycle [h]
    # nb_batches = 11
    # intensity = (1.06 + 1.05)/2 # average intensity for the 3 pumps [A]
    # power = intensity * (0.9*234) # instant power of the pumps [W]
    # elec_waterPress = (power/1000) * length_cycle * nb_batches # electricity use [kWh]
    
    if tech_period == '1':
        ## DATA COLLECTED
        slurry_sc1 = 257.71 # amount of slurry [kg]
        DM_slurry_sc1 = 14.75 # dry matter content of clurry [%]
        slurry_DW_sc1 = slurry_sc1 * DM_slurry_sc1 / 100  # amount of slurry [kg DW-eq]
        elec_sc1 = 2.04
        ## DATA MODELLED
        elec = slurry_DW * elec_sc1 / slurry_DW_sc1
    else: 
        ## DATA COLLECTED
        slurry_sc1 = 198.99 # amount of slurry [kg]
        DM_slurry_sc1 = 10.39 # dry matter content of clurry [%]
        slurry_DW_sc1 = slurry_sc1 * DM_slurry_sc1 / 100  # amount of slurry [kg DW-eq]
        elec_sc1 = 1.99
        ## DATA MODELLED
        elec = slurry_DW * elec_sc1 / slurry_DW_sc1

    return elec


def WaterDewatering (tech_period, slurry_DW):
    ''' 
    The total water used corresponds to the water used to fill in the water presses
    and to clean them. In 2019, both volumes went to sewer system. In 2022, the 
    water used to fill in the water presses was recirculated in a closed loop
    => does not count as input of water and does not count as wastewater either.
    Ideally, should divide this volume of water per the number of times it is 
    refilled (assumed that the water is kept for months => can be ignored).
    '''

    # nb_batches0 = (12+9+11+10+11+13)/6 # average number of batches over a week
    # water_per_batch = 80 # volume of water used to fill in the water press for each batch
    # water_waterPress = nb_batches0 * water_per_batch # total volume of water [L]
    
    water_cleaning = 0.137*1000 # volume of water used to clean the WPs in 2022 [L]
    
    if tech_period == '1':
        ## DATA COLLECTED
        slurry_sc1 = 257.71 # amount of slurry [kg]
        DM_slurry_sc1 = 14.75 # dry matter content of clurry [%]
        slurry_DW_sc1 = slurry_sc1 * DM_slurry_sc1 / 100  # amount of slurry [kg DW-eq]
        water_WPs = 0.88 * 1000
        total_water_sc1 = water_cleaning + water_WPs
        ## DATA MODELLED
        water = slurry_DW * total_water_sc1 / slurry_DW_sc1
    else: 
        ## DATA COLLECTED
        slurry_sc1 = 198.99 # amount of slurry [kg]
        DM_slurry_sc1 = 10.39 # dry matter content of clurry [%]
        slurry_DW_sc1 = slurry_sc1 * DM_slurry_sc1 / 100  # amount of slurry [kg DW-eq]
        total_water_sc1 = water_cleaning
        ## DATA MODELLED
        water = slurry_DW * total_water_sc1 / slurry_DW_sc1

    return water


def WastewaterDewatering (tech_period, slurry_DW):
    
    water_from_cleaning = -0.137 # water used to clean the WPs in 2022 [m3]
    
    if tech_period == '1':
        ## DATA COLLECTED
        slurry_sc1 = 257.71 # amount of slurry [kg]
        DM_slurry_sc1 = 14.75 # dry matter content of clurry [%]
        slurry_DW_sc1 = slurry_sc1 * DM_slurry_sc1 / 100  # amount of slurry [kg DW-eq]
        wastewater_from_slurry = -167.88/1000 # water coming out of the slurry [m3]
        wastewater_WPs = -0.88 # water used to fill in the water presses [m3]
        total_ww_sc1 = water_from_cleaning + wastewater_from_slurry + wastewater_WPs
        ## DATA MODELLED
        wastewater = slurry_DW * total_ww_sc1 / slurry_DW_sc1
    else: 
        ## DATA COLLECTED
        slurry_sc1 = 198.99 # amount of slurry [kg]
        DM_slurry_sc1 = 10.39 # dry matter content of clurry [%]
        slurry_DW_sc1 = slurry_sc1 * DM_slurry_sc1 / 100  # amount of slurry [kg DW-eq]
        wastewater_sc1 = -0.237
        #water_recirculated = 832 # volume of water recirculated to the ORPs [L]
        ## DATA MODELLED
        wastewater = slurry_DW * wastewater_sc1 / slurry_DW_sc1

    return wastewater#, water_recirculated


def DewateringDataDict (tech_period, slurry_DW):
    
    data_dict = {}
    
    ## BIOMASS INPUT
    biomass_balance_dict_sc1, biomass_balance_dict = BiomassDewatering (tech_period, slurry_DW)
    data_dict['slurry'] = {}
    data_dict['slurry']['amount'] = biomass_balance_dict['slurry']
    data_dict['slurry']['unit'] = 'kg DW-eq'
    data_dict['slurry']['type'] = 'fg_input'
    
    ## BIOMASS OUTPUT
    data_dict['paste'] = {}
    data_dict['paste']['amount'] = biomass_balance_dict['paste']
    data_dict['paste']['unit'] = 'kg DW-eq'
    data_dict['paste']['type'] = 'ref_flow'
    data_dict['losses'] = {}
    data_dict['losses']['amount'] = biomass_balance_dict['losses']
    data_dict['losses']['unit'] = 'kg DW-eq'
    data_dict['losses']['type'] = 'losses' 
    
    ## ELECTRICITY
    data_dict['electricity_IT']  = {}
    data_dict['electricity_IT']['amount'] = ElectricityDewatering (tech_period, slurry_DW)
    data_dict['electricity_IT']['unit'] = 'kWh'
    data_dict['electricity_IT']['type'] = 'tech_input'
    
    ## GROUND WATER
    data_dict['ground_water']  = {}
    data_dict['ground_water']['amount'] = WaterDewatering (tech_period, slurry_DW)
    data_dict['ground_water']['unit'] = 'L' 
    data_dict['ground_water']['type'] = 'tech_input' 
    
    ## WASTEWATER
    data_dict['wastewater']  = {}
    data_dict['wastewater']['amount'] = WastewaterDewatering (tech_period, slurry_DW)
    data_dict['wastewater']['unit'] = 'm3'
    data_dict['wastewater']['type'] = 'tech_output'
    
    return data_dict