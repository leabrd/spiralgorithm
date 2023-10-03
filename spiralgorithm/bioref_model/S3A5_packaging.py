# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 17:59:38 2022

@author: leabr
"""

def BiomassPackaging (concentrate_DW = 3.94):
    
    plastic = PlasticPackaging (concentrate_DW)
    concentrate_packaged_DW = concentrate_DW # conservation of mass
    lca_amount = concentrate_packaged_DW + plastic

    return concentrate_packaged_DW, lca_amount


def PlasticPackaging (concentrate_DW = 3.94):
    
    target_DM_concentrate = 6 # dry matter content targeted for concentration [%]
    theoretical_volume_retentate_sc1 = 230.57
    DM_retentate_UF_sc1 = 1.71
    concentrate_sc1 = theoretical_volume_retentate_sc1 / (target_DM_concentrate/DM_retentate_UF_sc1)
    container_weight = 0.409 # weight of one 10 L HDPE container with lid
    number_containers_needed = round(concentrate_sc1 / 10)
    plastic = container_weight * number_containers_needed
    
    return plastic


def PackagingDataDict (concentrate_DW = 3.94):
    
    data_dict = {}
    
    ## BIOMASS INPUT
    data_dict['concentrate'] = {}
    data_dict['concentrate']['amount'] = concentrate_DW
    data_dict['concentrate']['unit'] = 'kg DW-eq'
    data_dict['concentrate']['type'] = 'fg_input'
    
    ## BIOMASS OUTPUTS
    concentrate_packaged_DW, lca_amount = BiomassPackaging(concentrate_DW)
    data_dict['concentrate_packaged'] = {}
    data_dict['concentrate_packaged']['amount'] = concentrate_packaged_DW
    data_dict['concentrate_packaged']['unit'] = 'kg DW-eq'
    data_dict['concentrate_packaged']['type'] = 'ref_flow'
    
    ## PLASTIC PACKAGING
    data_dict['polyethylene'] = {}
    data_dict['polyethylene']['amount'] = PlasticPackaging (concentrate_DW)
    data_dict['polyethylene']['unit'] = 'kg'
    data_dict['polyethylene']['type'] = 'tech_input'
    
    return data_dict





