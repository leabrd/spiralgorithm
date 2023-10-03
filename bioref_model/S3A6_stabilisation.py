# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 17:03:32 2022

@author: leabr
"""


def BiomassStabilisation (concentrate_packaged_DW = 3.94):
    
    concentrate_stabilised_DW = concentrate_packaged_DW # conservation of mass
    
    return concentrate_stabilised_DW



def PotassiumSorbate (concentrate_packaged_DW = 3.94):
    
    ## DATA COLLECTED
    concentrate_packaged_DW_sc1 = 3.94 # conservation of mass
    target_DM_concentrate = 6 # dry matter content targeted for concentration [%]
    theoretical_volume_retentate_sc1 = 230.57
    DM_retentate_UF_sc1 = 1.71
    concentrate_sc1 = theoretical_volume_retentate_sc1 / (target_DM_concentrate/DM_retentate_UF_sc1)
    potassium_sorbate_per_10L_sc1 = 0.2 # amount of potassium sorbate to be added per 10 L of condensate [kg] 
    potassium_sorbate_sc1 = concentrate_sc1 * potassium_sorbate_per_10L_sc1 / 10
    ## DATA MODELLED
    concentrate = concentrate_packaged_DW * concentrate_sc1 / concentrate_packaged_DW_sc1
    potassium_sorbate = concentrate * potassium_sorbate_per_10L_sc1 / 10
        
    return potassium_sorbate


def StabilisationDataDict (concentrate_packaged_DW = 3.94):
    
    data_dict = {}
        
    ## BIOMASS INPUT
    data_dict['concentrate_packaged'] = {}
    data_dict['concentrate_packaged']['amount'] = concentrate_packaged_DW
    data_dict['concentrate_packaged']['unit'] = 'kg DW-eq'
    data_dict['concentrate_packaged']['type'] = 'fg_input'
    
    ## BIOMASS OUTPUTS
    data_dict['concentrate_packaged_stabilised'] = {}
    data_dict['concentrate_packaged_stabilised']['amount'] = BiomassStabilisation (concentrate_packaged_DW)
    data_dict['concentrate_packaged_stabilised']['unit'] = 'kg DW-eq'
    data_dict['concentrate_packaged_stabilised']['type'] = 'ref_flow'
    
    ## POTASSIUM SORBATE
    data_dict['potassium_sorbate'] = {}
    data_dict['potassium_sorbate']['amount'] = PotassiumSorbate (concentrate_packaged_DW)
    data_dict['potassium_sorbate']['unit'] = 'kg'
    data_dict['potassium_sorbate']['type'] = 'tech_input'
    
    return data_dict
