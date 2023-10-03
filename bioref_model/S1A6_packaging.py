# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 13:34:29 2022

@author: leabr
"""

def BiomassPackagingDryLine (tech_period = '2', dry_spangles_DW = 14.81):
    '''
    Conservation of mass during packaging. Packaging dry line.
    '''
    biomass_balance_dict_sc1 = {}
    biomass_balance_dict = {}
    
    if tech_period == '1':
        ## DATA COLLECTED
        dry_spangles_sc1 = 27.53 # amount of dry spangles [kg]
        DM_dry_spangles_sc1 = 96.8 # dry matter content of the dry spangles [%]
        dry_spangles_DW_sc1 = dry_spangles_sc1 * DM_dry_spangles_sc1 /100    
        dry_spangles_packaged_DW_sc1 = dry_spangles_DW_sc1
        biomass_balance_dict_sc1['dry_spangles'] = {'wet_mass':dry_spangles_sc1, 
                                                    'DM_content' : DM_dry_spangles_sc1, 
                                                    'dry_mass' :dry_spangles_DW_sc1}
        biomass_balance_dict_sc1['dry_spangles_packaged'] = {'wet_mass':dry_spangles_sc1, 
                                                             'DM_content' : DM_dry_spangles_sc1, 
                                                             'dry_mass' :dry_spangles_DW_sc1}
        # DATA MODELLED
        dry_spangles_packaged_DW = (dry_spangles_DW * dry_spangles_packaged_DW_sc1 
                                    / dry_spangles_DW_sc1)
        biomass_balance_dict['dry_spangles'] = dry_spangles_DW
        biomass_balance_dict['dry_spangles_packaged'] = dry_spangles_packaged_DW
        biomass_balance_dict['losses'] = dry_spangles_DW - dry_spangles_packaged_DW
        
    if tech_period == '2': 
        ## DATA COLLECTED
        dry_spangles_sc1 = 15.59 # amount of dry spangles [kg]
        DM_dry_spangles_sc1 = 94.99 # dry matter content of the dry spangles [%]
        dry_spangles_DW_sc1 = dry_spangles_sc1 * DM_dry_spangles_sc1 /100    
        dry_spangles_packaged_DW_sc1 = dry_spangles_DW_sc1
        biomass_balance_dict_sc1['dry_spangles'] = {'wet_mass':dry_spangles_sc1, 
                                                    'DM_content' : DM_dry_spangles_sc1, 
                                                    'dry_mass' :dry_spangles_DW_sc1}
        biomass_balance_dict_sc1['dry_spangles_packaged'] = {'wet_mass':dry_spangles_sc1, 
                                                             'DM_content' : DM_dry_spangles_sc1, 
                                                             'dry_mass' :dry_spangles_DW_sc1}
        ## DATA MODELLED
        dry_spangles_packaged_DW = (dry_spangles_DW * dry_spangles_packaged_DW_sc1 
                                    / dry_spangles_DW_sc1)
        biomass_balance_dict['dry_spangles'] = dry_spangles_DW
        biomass_balance_dict['dry_spangles_packaged'] = dry_spangles_packaged_DW
        biomass_balance_dict['losses'] = dry_spangles_DW - dry_spangles_packaged_DW
       
    return biomass_balance_dict_sc1, biomass_balance_dict


def PlasticPackaging (tech_period, dry_spangles_DW):
    '''
    ADD THE PERIOD 1 HERE????
    '''
    ## DATA COLLECTED
    dry_spangles_sc1 = 15.59 # amount of dry spangles [kg]
    DM_dry_spangles_sc1 = 94.99 # dry matter content of the dry spangles [%]
    dry_spangles_DW_sc1 = dry_spangles_sc1 * DM_dry_spangles_sc1 /100 
    plastic_sc1 = 0.182 # amount of plastic used for packaging [kg]
    ## DATA MODELLED
    plastic = dry_spangles_DW * plastic_sc1 / dry_spangles_DW_sc1
 
    return plastic


def PackagingDryLineDataDict (tech_period, dry_spangles_DW):
    
    data_dict = {}
    
    biomass_balance_dict_sc1, biomass_balance_dict = BiomassPackagingDryLine (tech_period, 
                                                                              dry_spangles_DW)
    
    ## BIOMASS INPUT
    data_dict['dry_spangles'] = {}
    data_dict['dry_spangles']['amount'] = biomass_balance_dict['dry_spangles']
    data_dict['dry_spangles']['unit'] = 'kg DW-eq'
    data_dict['dry_spangles']['type'] = 'fg_input'
    
    ## BIOMASS OUTPUTS
    data_dict['dry_spangles_packaged'] = {}
    data_dict['dry_spangles_packaged']['amount'] = biomass_balance_dict['dry_spangles_packaged']
    data_dict['dry_spangles_packaged']['unit'] = 'kg DW-eq'
    data_dict['dry_spangles_packaged']['type'] = 'ref_flow'
    data_dict['losses'] = {}
    data_dict['losses']['amount'] = biomass_balance_dict['losses']
    data_dict['losses']['unit'] = 'kg DW-eq'
    data_dict['losses']['type'] = 'losses'
    
    ## POLYETHYLENE
    data_dict['polyethylene'] = {}
    data_dict['polyethylene']['amount'] = PlasticPackaging (tech_period, dry_spangles_DW)
    data_dict['polyethylene']['unit'] = 'kg'
    data_dict['polyethylene']['type'] = 'tech_input'

    return data_dict