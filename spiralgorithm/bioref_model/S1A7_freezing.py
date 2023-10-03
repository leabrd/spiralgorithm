# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 15:27:57 2022

@author: leabr
"""

def ElectricityFreezing (tech_period, paste_packaged_DW):
    
    ## DATA COLLECTED
    volume = 342 # volume capacity of the freezer [L]
    elec_freezer_per_year_sc1 = 340 # electricity consumption [kWh/year] A+ freezer
    elec_freezer_per_day_sc1 = elec_freezer_per_year_sc1 / 365 
    paste_packaged_sc1 = 77.38 # amount of dry spangles [kg]
    DM_paste_packaged_sc1 = 23.26 # dry matter content of the dry spangles [%]
    paste_packaged_DW_sc1 = paste_packaged_sc1 * DM_paste_packaged_sc1 /100
    elec_sc1 = elec_freezer_per_day_sc1
    ## DATA MODELLED 
    elec = elec_freezer_per_day_sc1
    
    return elec


def FreezingDataDict (tech_period, paste_packaged_DW):
    
    data_dict = {}
    
    ## BIOMASS INPUT
    data_dict['paste_packaged'] = {}
    data_dict['paste_packaged']['amount'] = paste_packaged_DW
    data_dict['paste_packaged']['unit'] = 'kg' 
    data_dict['paste_packaged']['type'] = 'fg_input'
    
    ## BIOMASS OUTPUT
    data_dict['paste_packaged_frozen'] = {}
    data_dict['paste_packaged_frozen']['amount'] = paste_packaged_DW
    data_dict['paste_packaged_frozen']['unit'] = 'kg' 
    data_dict['paste_packaged_frozen']['type'] = 'ref_flow'
    
    ## ELECTRICITY
    data_dict['electricity_IT'] = {}
    data_dict['electricity_IT']['amount'] = ElectricityFreezing (tech_period, 
                                                                 paste_packaged_DW)
    data_dict['electricity_IT']['unit'] = 'kWh' 
    data_dict['electricity_IT']['type'] = 'tech_input'

    return data_dict