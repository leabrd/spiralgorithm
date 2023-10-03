#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 17:40:20 2023

@author: leabraud
"""

def BiomassPackaging (CPD_concentrate_DW):
    '''
    Packaging of the CPD_concentrate from centrifugation.
    Conservation of mass during packaging.
    No data measured in 2021 or 2022 => assumed from S3 based on the data from 2021
    since the CPD_concentrate produced in 2021 was processed in S3 te week after (i.e. same
                                                                      biomass).
    '''
    biomass_balance_dict_sc1 = {}
    biomass_balance_dict = {}
    
    ## DATA COLLECTED
    CPD_concentrate_sc1 = 55.5 # amount of CPD_concentrate obtained after centrifugation [kg]
    DM_CPD_concentrate_sc1 = 6.3 # dry matter content of the CPD_concentrate [% DW]
    CPD_concentrate_DW_sc1 = CPD_concentrate_sc1 * DM_CPD_concentrate_sc1 /100    
    CPD_concentrate_packaged_DW_sc1 = CPD_concentrate_DW_sc1 # conservation of mass 
        
    # for the biomass balance, the weight of the packaging is not accounted for
    biomass_balance_dict_sc1['CPD_concentrate'] = {'wet_mass':CPD_concentrate_sc1, 
                                                'DM_content' : DM_CPD_concentrate_sc1, 
                                                'dry_mass' :CPD_concentrate_DW_sc1}
    
    # wet weight of blue extract package = weight blue extract + packaging
    biomass_balance_dict_sc1['CPD_concentrate_packaged'] = {'wet_mass':'NaN', 
                                                         'DM_content' : DM_CPD_concentrate_sc1, 
                                                         'dry_mass' : CPD_concentrate_packaged_DW_sc1}
    
    ## DATA MODELLED
    CPD_concentrate_packaged_DW = (CPD_concentrate_DW * CPD_concentrate_packaged_DW_sc1 / CPD_concentrate_DW_sc1)
    biomass_balance_dict['CPD_concentrate'] = CPD_concentrate_DW
    biomass_balance_dict['CPD_concentrate_packaged'] = CPD_concentrate_packaged_DW
    biomass_balance_dict['losses'] = abs(CPD_concentrate_DW - CPD_concentrate_packaged_DW)
       
    return biomass_balance_dict_sc1, biomass_balance_dict


def PlasticPackaging (CPD_concentrate_DW):
    '''
    The data regarding the amount of packaging used were measured in 2022 only.
    Considered that the 200 L container weighs 10 kg. 
    '''
    ## DATA COLLECTED
    CPD_concentrate_sc1 = 55.5 # amount of CPD_concentrate obtained after centrifugation [kg]
    DM_CPD_concentrate_sc1 = 6.3 # dry matter content of the CPD_concentrate [% DW]
    CPD_concentrate_DW_sc1 = CPD_concentrate_sc1 * DM_CPD_concentrate_sc1 /100    
    plastic_sc1 = 2.44 # amount of plastic used for packaging [kg]
    
    ## DATA MODELLED
    plastic = CPD_concentrate_DW * plastic_sc1 / CPD_concentrate_DW_sc1
 
    return plastic


def PackagingCPDConcentrateDataDict (CPD_concentrate_DW):
    
    data_dict = {}
    
    biomass_balance_dict_sc1, biomass_balance_dict = BiomassPackaging (CPD_concentrate_DW)
    
    ## BIOMASS INPUT
    data_dict['CPD_concentrate'] = {}
    data_dict['CPD_concentrate']['amount'] = biomass_balance_dict['CPD_concentrate']
    data_dict['CPD_concentrate']['unit'] = 'kg DW-eq'
    data_dict['CPD_concentrate']['type'] = 'fg_input'
    
    ## BIOMASS OUTPUTS
    data_dict['CPD_concentrate_packaged'] = {}
    data_dict['CPD_concentrate_packaged']['amount'] = biomass_balance_dict['CPD_concentrate_packaged']
    data_dict['CPD_concentrate_packaged']['unit'] = 'kg DW-eq'
    data_dict['CPD_concentrate_packaged']['type'] = 'ref_flow'
    data_dict['losses'] = {}
    data_dict['losses']['amount'] = biomass_balance_dict['losses']
    data_dict['losses']['unit'] = 'kg DW-eq'
    data_dict['losses']['type'] = 'losses'
    
    ## POLYETHYLENE
    data_dict['polyethylene'] = {}
    data_dict['polyethylene']['amount'] = PlasticPackaging (CPD_concentrate_DW)
    data_dict['polyethylene']['unit'] = 'kg'
    data_dict['polyethylene']['type'] = 'tech_input'

    return data_dict