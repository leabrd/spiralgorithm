#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 17:55:22 2023

@author: leabraud
"""

def BiomassPackaging (CPA_DW):
    '''
    Packaging of the CPA from centrifugation.
    Conservation of mass during packaging.
    No data measured in 2021 or 2022 => assumed from S3 based on the data from 2021
    since the CPA produced in 2021 was processed in S3 te week after (i.e. same
                                                                      biomass).
    '''
    biomass_balance_dict_sc1 = {}
    biomass_balance_dict = {}
    
    ## DATA COLLECTED
    CPA_sc1 = 200 # amount of CPA obtained after centrifugation [kg]
    DM_CPA_sc1 = 6.5 # dry matter content of the CPA [% DW]
    CPA_DW_sc1 = CPA_sc1 * DM_CPA_sc1 /100    
    CPA_packaged_DW_sc1 = CPA_DW_sc1 # conservation of mass 
        
    # for the biomass balance, the weight of the packaging is not accounted for
    biomass_balance_dict_sc1['CPA'] = {'wet_mass':CPA_sc1, 
                                                'DM_content' : DM_CPA_sc1, 
                                                'dry_mass' :CPA_DW_sc1}
    
    # wet weight of blue extract package = weight blue extract + packaging
    biomass_balance_dict_sc1['CPA_packaged'] = {'wet_mass':'NaN', 
                                                         'DM_content' : DM_CPA_sc1, 
                                                         'dry_mass' : CPA_packaged_DW_sc1}
    
    ## DATA MODELLED
    CPA_packaged_DW = (CPA_DW * CPA_packaged_DW_sc1 / CPA_DW_sc1)
    biomass_balance_dict['CPA'] = CPA_DW
    biomass_balance_dict['CPA_packaged'] = CPA_packaged_DW
    biomass_balance_dict['losses'] = abs(CPA_DW - CPA_packaged_DW)
       
    return biomass_balance_dict_sc1, biomass_balance_dict


def PlasticPackaging (CPA_DW):
    '''
    The data regarding the amount of packaging used were measured in 2022 only.
    Considered that the 200 L container weighs 10 kg. 
    '''
    ## DATA COLLECTED
    CPA_sc1 = 200 # amount of CPA obtained after centrifugation [kg]
    DM_CPA_sc1 = 6.5 # dry matter content of the CPA [% DW]
    CPA_DW_sc1 = CPA_sc1 * DM_CPA_sc1 /100    
    plastic_sc1 = 10 # amount of plastic used for packaging [kg]
    
    ## DATA MODELLED
    plastic = CPA_DW * plastic_sc1 / CPA_DW_sc1
 
    return plastic


def PackagingCPADataDict (CPA_DW):
    
    data_dict = {}
    
    biomass_balance_dict_sc1, biomass_balance_dict = BiomassPackaging (CPA_DW)
    
    ## BIOMASS INPUT
    data_dict['CPA'] = {}
    data_dict['CPA']['amount'] = biomass_balance_dict['CPA']
    data_dict['CPA']['unit'] = 'kg DW-eq'
    data_dict['CPA']['type'] = 'fg_input'
    
    ## BIOMASS OUTPUTS
    data_dict['CPA_packaged'] = {}
    data_dict['CPA_packaged']['amount'] = biomass_balance_dict['CPA_packaged']
    data_dict['CPA_packaged']['unit'] = 'kg DW-eq'
    data_dict['CPA_packaged']['type'] = 'ref_flow'
    data_dict['losses'] = {}
    data_dict['losses']['amount'] = biomass_balance_dict['losses']
    data_dict['losses']['unit'] = 'kg DW-eq'
    data_dict['losses']['type'] = 'losses'
    
    ## POLYETHYLENE
    data_dict['polyethylene'] = {}
    data_dict['polyethylene']['amount'] = PlasticPackaging (CPA_DW)
    data_dict['polyethylene']['unit'] = 'kg'
    data_dict['polyethylene']['type'] = 'tech_input'

    return data_dict
