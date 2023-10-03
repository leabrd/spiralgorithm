# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 14:57:30 2022

@author: leabr
"""

def BiomassConcentration (retentate_UF_DW = 3.94):
    
    '''Upscaled the data; considered the DM target of 6% '''
    
    biomass_balance_dict_sc1 = {}
    biomass_balance_dict = {}
    
    ## DATA COLLECTED
    real_volume_retentate_sc1 = 165.76 # amount of retentate from UF (> 15 kDa) [kg]
    theoretical_volume_retentate_sc1 = 230.57 # theoretical amount of retentate from UF if the 370 L were ultrafiltered [kg]
    DM_retentate_UF_sc1 = 1.71 # dry matter content of the rententate [%]
    retentate_UF_DW_sc1 = theoretical_volume_retentate_sc1 * DM_retentate_UF_sc1 / 100
    biomass_balance_dict_sc1['retentate_UF'] = {'wet_mass': theoretical_volume_retentate_sc1, 
                                                'DM_content': DM_retentate_UF_sc1, 
                                                'dry_mass': retentate_UF_DW_sc1}   
    concentrate_DW_sc1 = retentate_UF_DW_sc1 # conservation of mass
    target_DM_concentrate = 6 # dry matter content targeted for concentration [%]
    concentrate_sc1 = theoretical_volume_retentate_sc1 / (target_DM_concentrate/DM_retentate_UF_sc1)
    biomass_balance_dict_sc1['concentrate'] = {'wet_mass': concentrate_sc1, 
                                               'DM_content': target_DM_concentrate, 
                                               'dry_mass': concentrate_DW_sc1}   
    ## DATA MODELLED
    biomass_balance_dict['retentate_UF'] = retentate_UF_DW
    concentrate_DW = retentate_UF_DW * concentrate_DW_sc1 / retentate_UF_DW_sc1
    biomass_balance_dict['concentrate'] = concentrate_DW
        
    return biomass_balance_dict_sc1, biomass_balance_dict

def ElectricityConcentration (retentate_UF_DW = 3.94):
    
    ## DATA COLLECTED
    retentate_UF_sc1 = 3.942747
    elec_concentration_sc1 = 226.30
    ## DATA MODELLED
    elec_concentration = retentate_UF_DW * elec_concentration_sc1 / retentate_UF_sc1
    
    return elec_concentration

def WaterConcentration (retentate_UF_DW = 3.94):
    
    ## DATA COLLECTED
    retentate_UF_sc1 = 3.942747
    water_concentration_sc1 = 462.07
    ## DATA MODELLED
    water_concentration = retentate_UF_DW * water_concentration_sc1 / retentate_UF_sc1
        
    return water_concentration

def WastewaterConcentration (retentate_UF_DW = 3.94):
    
    ## DATA COLLECTED
    retentate_UF_sc1 = 3.942747
    wastewater_concentration_sc1 = -1 * 462.07/1000
    ## DATA MODELLED
    wastewater_concentration = retentate_UF_DW * wastewater_concentration_sc1 / retentate_UF_sc1
    
    return wastewater_concentration

def ConcentrationCPADataDict (retentate_UF_DW = 3.94):
    
    data_dict = {}
    
    ## BIOMASS INPUT
    biomass_balance_dict_sc1, biomass_balance_dict = BiomassConcentration (retentate_UF_DW)
    data_dict['retentate_UF'] = {}
    data_dict['retentate_UF']['amount'] = biomass_balance_dict['retentate_UF']
    data_dict['retentate_UF']['unit'] = 'kg DW-eq'
    data_dict['retentate_UF']['type'] = 'fg_input'
    
    ## BIOMASS OUTPUTS
    data_dict['concentrate'] = {}
    data_dict['concentrate']['amount'] = biomass_balance_dict['concentrate']
    data_dict['concentrate']['unit'] = 'kg DW-eq'
    data_dict['concentrate']['type'] = 'ref_flow'
    data_dict['losses'] = {}
    data_dict['losses']['amount'] = 0
    data_dict['losses']['unit'] = 'kg DW-eq'
    data_dict['losses']['type'] = 'losses'  
    
    ## ELECTRICITY
    data_dict['electricity_FR'] = {}
    data_dict['electricity_FR']['amount'] = ElectricityConcentration(retentate_UF_DW)
    data_dict['electricity_FR']['unit'] = 'kWh'
    data_dict['electricity_FR']['type'] = 'tech_input'
    
    ## TAP WATER
    data_dict['tap_water'] = {}
    data_dict['tap_water']['amount'] =  WaterConcentration(retentate_UF_DW)
    data_dict['tap_water']['unit'] = 'L'
    data_dict['tap_water']['type'] = 'tech_input'
    
    ## WASTEWATER
    data_dict['wastewater'] = {}
    data_dict['wastewater']['amount'] = WastewaterConcentration(retentate_UF_DW)
    data_dict['wastewater']['unit'] = 'm3'
    data_dict['wastewater']['type'] = 'tech_output'   

    return data_dict
