#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 10:14:45 2023

@author: leabraud
"""

def BiomassPackaging (blue_extract_DW):
    '''
    Packaging of the blue extract from UF2.
    Conservation of mass during packaging.
    Measured in 2022 only => no technical period.
    '''
    biomass_balance_dict_sc1 = {}
    biomass_balance_dict = {}
    
    ## DATA COLLECTED
    blue_extract_sc1 = 43.85 # amount of blue extract packaged [kg]
    DM_blue_extract_sc1 = 6.55 # dry matter content of the blue extract [%]
    blue_extract_DW_sc1 = blue_extract_sc1 * DM_blue_extract_sc1 /100    
    blue_extract_packaged_DW_sc1 = blue_extract_DW_sc1 # conservation of mass 
    
    # for the biomass balance, the weight of the packaging is not accounted for
    biomass_balance_dict_sc1['blue_extract'] = {'wet_mass':blue_extract_sc1, 
                                                'DM_content' : DM_blue_extract_sc1, 
                                                'dry_mass' :blue_extract_DW_sc1}
    
    # wet weight of blue extract package = weight blue extract + packaging
    biomass_balance_dict_sc1['blue_extract_packaged'] = {'wet_mass':'NaN', 
                                                         'DM_content' : DM_blue_extract_sc1, 
                                                         'dry_mass' :blue_extract_packaged_DW_sc1}
    
    
    ## DATA MODELLED
    blue_extract_packaged_DW = (blue_extract_DW * blue_extract_packaged_DW_sc1 
                                / blue_extract_DW_sc1)
    biomass_balance_dict['blue_extract'] = blue_extract_DW
    biomass_balance_dict['blue_extract_packaged'] = blue_extract_packaged_DW
    biomass_balance_dict['losses'] = abs(blue_extract_DW - blue_extract_packaged_DW)
       
    return biomass_balance_dict_sc1, biomass_balance_dict


def PlasticPackaging (blue_extract_DW):
    '''
    The data regarding the amount of packaging used were measured in 2022 only.
    '''
    ## DATA COLLECTED
    blue_extract_sc1 = 43.85 # amount of blue extract packaged [kg]
    DM_blue_extract_sc1 = 6.55 # dry matter content of the blue extract [%]
    blue_extract_DW_sc1 = blue_extract_sc1 * DM_blue_extract_sc1 /100    
    plastic_sc1 = 2.57 # amount of plastic used for packaging [kg]
    ## DATA MODELLED
    plastic = blue_extract_DW * plastic_sc1 / blue_extract_DW_sc1
 
    return plastic


def PackagingBlueExtractDataDict (blue_extract_DW):
    
    data_dict = {}
    
    biomass_balance_dict_sc1, biomass_balance_dict = BiomassPackaging (blue_extract_DW)
    
    ## BIOMASS INPUT
    data_dict['blue_extract'] = {}
    data_dict['blue_extract']['amount'] = biomass_balance_dict['blue_extract']
    data_dict['blue_extract']['unit'] = 'kg DW-eq'
    data_dict['blue_extract']['type'] = 'fg_input'
    
    ## BIOMASS OUTPUTS
    data_dict['blue_extract_packaged'] = {}
    data_dict['blue_extract_packaged']['amount'] = biomass_balance_dict['blue_extract_packaged']
    data_dict['blue_extract_packaged']['unit'] = 'kg DW-eq'
    data_dict['blue_extract_packaged']['type'] = 'ref_flow'
    data_dict['losses'] = {}
    data_dict['losses']['amount'] = biomass_balance_dict['losses']
    data_dict['losses']['unit'] = 'kg DW-eq'
    data_dict['losses']['type'] = 'losses'
    
    ## POLYETHYLENE
    data_dict['polyethylene'] = {}
    data_dict['polyethylene']['amount'] = PlasticPackaging (blue_extract_DW)
    data_dict['polyethylene']['unit'] = 'kg'
    data_dict['polyethylene']['type'] = 'tech_input'

    return data_dict