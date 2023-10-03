# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 10:42:57 2022

@author: leabr
"""

def BiomassPackagingWetLine(tech_period, paste_DW):
    '''
    Conservation of mass during packaging. Packaging wet line.
    '''
    biomass_balance_dict_sc1 = {}
    biomass_balance_dict = {}
    
    if tech_period == '1':
        ## DATA COLLECTED
        paste_sc1 = 91.45 # amount of paste [kg]
        DM_paste_sc1 = 33.07 # dry matter content of the paste [%]
        paste_DW_sc1 = paste_sc1 * DM_paste_sc1 /100
        paste_packaged_DW_sc1 = paste_DW_sc1
        biomass_balance_dict_sc1['paste'] = {'wet_mass':paste_sc1, 
                                             'DM_content' : DM_paste_sc1, 
                                             'dry_mass' :paste_DW_sc1}
        biomass_balance_dict_sc1['paste_packaged'] = {'wet_mass':paste_sc1, 
                                                      'DM_content' : DM_paste_sc1, 
                                                      'dry_mass' :paste_packaged_DW_sc1}
        # DATA MODELLED
        paste_packaged_DW = paste_DW * paste_packaged_DW_sc1 / paste_DW_sc1
        biomass_balance_dict['paste'] = paste_DW
        biomass_balance_dict['paste_packaged'] = paste_packaged_DW
    else: 
        ## DATA COLLECTED
        paste_sc1 = 77.38 # amount of dry spangles [kg]
        DM_paste_sc1 = 23.26 # dry matter content of the dry spangles [%]
        paste_DW_sc1 = paste_sc1 * DM_paste_sc1 /100
        paste_packaged_DW_sc1 = paste_DW_sc1
        biomass_balance_dict_sc1['paste'] = {'wet_mass':paste_sc1, 
                                             'DM_content' : DM_paste_sc1, 
                                             'dry_mass' :paste_DW_sc1}
        biomass_balance_dict_sc1['paste_packaged'] = {'wet_mass':paste_sc1, 
                                                      'DM_content' : DM_paste_sc1, 
                                                      'dry_mass' :paste_packaged_DW_sc1}
        # DATA MODELLED
        paste_packaged_DW = paste_DW * paste_packaged_DW_sc1 / paste_DW_sc1
        biomass_balance_dict['paste'] = paste_DW
        biomass_balance_dict['paste_packaged'] = paste_packaged_DW
    
    return biomass_balance_dict_sc1, biomass_balance_dict


def PlasticPackaging (tech_period, paste_DW):
 
    ## DATA COLLECTED
    paste_sc1 = 77.38 # amount of dry spangles [kg]
    DM_paste_sc1 = 23.26 # dry matter content of the dry spangles [%]
    paste_DW_sc1 = paste_sc1 * DM_paste_sc1 /100
    paste_packaged_DW_sc1 = paste_DW_sc1
    plastic_sc1 = 0.82 # amount of plastic used for packaging [kg]
    ## DATA MODELLED
    plastic = paste_DW * plastic_sc1 / paste_packaged_DW_sc1
 
    return plastic


def PackagingWetLineDataDict (tech_period, paste_DW):
    
    data_dict = {}
    
    biomass_balance_dict_sc1, biomass_balance_dict = BiomassPackagingWetLine (tech_period, 
                                                                              paste_DW)
    
    ## BIOMASS INPUT
    data_dict['paste'] = {}
    data_dict['paste']['amount'] = biomass_balance_dict['paste']
    data_dict['paste']['unit'] = 'kg DW-eq'
    data_dict['paste']['type'] = 'fg_input'
    
    ## BIOMASS OUTPUTS
    data_dict['paste_packaged'] = {}
    data_dict['paste_packaged']['amount'] = biomass_balance_dict['paste_packaged']
    data_dict['paste_packaged']['unit'] = 'kg DW-eq'
    data_dict['paste_packaged']['type'] = 'ref_flow'
    
    ## POLYETHYLENE
    data_dict['polyethylene'] = {}
    data_dict['polyethylene']['amount'] = PlasticPackaging (tech_period, paste_DW)
    data_dict['polyethylene']['unit'] = 'kg'
    data_dict['polyethylene']['type'] = 'tech_input'

    return data_dict
