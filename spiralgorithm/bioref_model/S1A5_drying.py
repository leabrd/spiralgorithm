# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 14:42:22 2022

@author: leabr
"""

def BiomassDrying (tech_period, wet_spangles_DW):
    
    biomass_balance_dict_sc1 = {}
    biomass_balance_dict = {}
    
    if tech_period == '1':
        ## DATA COLLECTED
        wet_spangles_sc1 = 80.14 # amount of slurry [kg]
        DM_wet_spangles_sc1 = 33.07 # dry matter content of clurry [%]
        wet_spangles_DW_sc1 = wet_spangles_sc1 * DM_wet_spangles_sc1 / 100  # amount of slurry [kg DW-eq]
        water_content_wet_spangles_sc1 = wet_spangles_sc1 - wet_spangles_DW_sc1
        dry_spangles_sc1 = 27.53 # amount of the dry spangles [kg]
        DM_dry_spangles_sc1 = 96.8 # dry matter content of the dry spangles [% DW]
        dry_spangles_DW_sc1 = dry_spangles_sc1 * DM_dry_spangles_sc1 /100
        water_content_dry_spangles_sc1 = dry_spangles_sc1 - dry_spangles_DW_sc1
        water_evaporated_sc1 = water_content_wet_spangles_sc1 - water_content_dry_spangles_sc1
        if wet_spangles_DW_sc1 < dry_spangles_DW_sc1:
            dry_spangles_DW_sc1 = wet_spangles_DW_sc1
        else: 
            losses = wet_spangles_DW_sc1 - dry_spangles_DW_sc1
        biomass_balance_dict_sc1['wet_spangles'] = {'wet_mass':wet_spangles_sc1, 
                                                    'DM_content' : DM_wet_spangles_sc1, 
                                                    'dry_mass' :wet_spangles_DW_sc1}
        biomass_balance_dict_sc1['dry_spangles'] = {'wet_mass':dry_spangles_sc1, 
                                                    'DM_content':DM_dry_spangles_sc1, 
                                                    'dry_mass':dry_spangles_DW_sc1}
        biomass_balance_dict_sc1['water_evaporated'] : water_evaporated_sc1
        ## DATA MODELLED 
        dry_spangles_DW = wet_spangles_DW * dry_spangles_DW_sc1 / wet_spangles_DW_sc1
        if wet_spangles_DW < dry_spangles_DW:
            dry_spangles_DW = wet_spangles_DW
            losses =0
        else: 
            losses = wet_spangles_DW - dry_spangles_DW 
        biomass_balance_dict['losses'] = losses             
        biomass_balance_dict['wet_spangles'] = wet_spangles_DW
        biomass_balance_dict['dry_spangles'] = dry_spangles_DW
        biomass_balance_dict['water_evaporated'] = (wet_spangles_DW * water_evaporated_sc1 
                                                    / wet_spangles_DW_sc1)
    
    if tech_period == '2':
        ## DATA COLLECTED
        wet_spangles_sc1 = 64.03 # amount of slurry [kg]
        DM_wet_spangles_sc1 = 23.26 # dry matter content of clurry [%]
        wet_spangles_DW_sc1 = wet_spangles_sc1 * DM_wet_spangles_sc1 / 100  # amount of slurry [kg DW-eq]
        water_content_wet_spangles_sc1 = wet_spangles_sc1 - wet_spangles_DW_sc1
        dry_spangles_sc1 = 15.59 # amount of paste [kg]
        DM_dry_spangles_sc1 = 94.99 # dry matter content of the paste [%]
        dry_spangles_DW_sc1 = dry_spangles_sc1 * DM_dry_spangles_sc1 /100
        water_content_dry_spangles_sc1 = dry_spangles_sc1 - dry_spangles_DW_sc1
        water_evaporated_sc1 = water_content_wet_spangles_sc1 - water_content_dry_spangles_sc1
        if wet_spangles_DW_sc1 < dry_spangles_DW_sc1:
            dry_spangles_DW_sc1 = wet_spangles_DW_sc1
            losses=0
        else: 
            losses = wet_spangles_DW_sc1 - dry_spangles_DW_sc1       
        biomass_balance_dict_sc1['wet_spangles'] = {'wet_mass':wet_spangles_sc1, 
                                                    'DM_content' : DM_wet_spangles_sc1, 
                                                    'dry_mass' :wet_spangles_DW_sc1}
        biomass_balance_dict_sc1['dry_spangles'] = {'wet_mass':dry_spangles_sc1, 
                                                    'DM_content':DM_dry_spangles_sc1, 
                                                    'dry_mass':dry_spangles_DW_sc1}
        biomass_balance_dict_sc1['water_evaporated'] : (water_content_wet_spangles_sc1 
                                                        - water_content_dry_spangles_sc1)
        ## DATA MODELLED 
        dry_spangles_DW = wet_spangles_DW * dry_spangles_DW_sc1 / wet_spangles_DW_sc1
        if wet_spangles_DW < dry_spangles_DW:
            dry_spangles_DW = wet_spangles_DW
            losses=0
        else: 
            losses = wet_spangles_DW - dry_spangles_DW 
        biomass_balance_dict['losses'] = losses             
        biomass_balance_dict['wet_spangles'] = wet_spangles_DW
        biomass_balance_dict['dry_spangles'] = dry_spangles_DW
        biomass_balance_dict['water_evaporated'] = (wet_spangles_DW * water_evaporated_sc1 
                                                    / wet_spangles_DW_sc1)
          
    return biomass_balance_dict_sc1, biomass_balance_dict


def ElectrictyDryingFan (tech_period):

    nb_dc = 2 # number of drying chambers   
    running_time = 20 # running time of the drying chambers in 2019 [h] ### VARIABLE
    intensity = (1.93 + 1.92 + 1.3 + 1.3 + 1.36 + 1.40)/6 # average intensity for the 3 pumps [A]
    power = intensity * (1.7320508*0.85*380) # instant power of the pumps [W]
    elec_fans = (power/1000) * running_time * nb_dc # electricity use [kWh]

    return elec_fans


def ElectrictyDryingBatteries (tech_period):

    if tech_period == '1':
        running_time = 20 # running time of the drying chambers in 2019 [h] ### VARIABLE
    else: 
        running_time = 0 # running time of the drying chambers in 2019 [h] ### VARIABLE

    nb_dc = 2 # number of drying chambers   
    intensity = (12 + 11.9 + 11.71 + 12.18 + 11.7)/5 # average intensity for the 3 pumps [A]
    power = intensity * (1.7320508*0.85*380) # instant power of the pumps [W]
    elec_batteries = (power/1000) * running_time * nb_dc # electricity use [kWh]

    return elec_batteries


def ElectricityDrying (tech_period, wet_spangles_DW):
    
    if tech_period == '1':
        ## DATA COLLECTED
        wet_spangles_sc1 = 80.14 # amount of slurry [kg]
        DM_wet_spangles_sc1 = 33.07 # dry matter content of clurry [%]
        wet_spangles_DW_sc1 = wet_spangles_sc1 * DM_wet_spangles_sc1 / 100  # amount of slurry [kg DW-eq]
        elec_sc1 = ElectrictyDryingBatteries (tech_period) + ElectrictyDryingFan (tech_period)
        ## DATA MODELLED
        elec = wet_spangles_DW * elec_sc1 / wet_spangles_DW_sc1
    else: 
        ## DATA COLLECTED
        wet_spangles_sc1 = 64.03 # amount of slurry [kg]
        DM_wet_spangles_sc1 = 23.26 # dry matter content of clurry [%]
        wet_spangles_DW_sc1 = wet_spangles_sc1 * DM_wet_spangles_sc1 / 100  # amount of slurry [kg DW-eq]
        elec_sc1 = ElectrictyDryingBatteries (tech_period) + ElectrictyDryingFan (tech_period)
        ## DATA MODELLED
        elec = wet_spangles_DW * elec_sc1 / wet_spangles_DW_sc1

    return elec


def HeatADDrying (tech_period, wet_spangles_DW):
    
    '''
    If we want to consider the amount of heat from AD that would be required
    to dry the biomass. Based on the conversion of kWh to Meha Joules.
    '''

    ## DATA COLLECTED
    wet_spangles_sc1 = 80.14 # amount of slurry [kg]
    DM_wet_spangles_sc1 = 33.07 # dry matter content of clurry [%]
    wet_spangles_DW_sc1 = wet_spangles_sc1 * DM_wet_spangles_sc1 / 100  # amount of slurry [kg DW-eq]
    elec_batteries_sc1 = ElectrictyDryingBatteries (tech_period = '1') # amount of electricity used to dry the biomass in 2019 [kWh]
    heat_AD_sc1 = elec_batteries_sc1 * 3.6
    ## DATA MODELLED
    heat_AD = wet_spangles_DW * heat_AD_sc1 / wet_spangles_DW_sc1
    
    return heat_AD


def DryingDataDict (tech_period, wet_spangles_DW):
    
    data_dict = {}
    
    biomass_balance_dict_sc1, biomass_balance_dict = BiomassDrying (tech_period, 
                                                                    wet_spangles_DW)

    ## BIOMASS INPUT
    data_dict['wet_spangles'] = {}
    data_dict['wet_spangles']['amount'] = biomass_balance_dict['wet_spangles']
    data_dict['wet_spangles']['unit'] = 'kg DW-eq'
    data_dict['wet_spangles']['type'] = 'fg_input'
    
    ## BIOMASS OUTPUTS
    data_dict['dry_spangles'] = {}
    data_dict['dry_spangles']['amount'] = biomass_balance_dict['dry_spangles']
    data_dict['dry_spangles']['unit'] = 'kg DW-eq'
    data_dict['dry_spangles']['type'] = 'ref_flow'
    data_dict['losses'] = {}
    data_dict['losses']['amount'] = biomass_balance_dict['losses']
    data_dict['losses']['unit'] = 'kg DW-eq'
    data_dict['losses']['type'] = 'losses'    
    
    ## ELECTRICITY
    data_dict['electricity_IT'] = {}
    data_dict['electricity_IT']['amount'] = ElectricityDrying (tech_period, 
                                                               wet_spangles_DW)
    data_dict['electricity_IT']['unit'] = 'kWh'
    data_dict['electricity_IT']['type'] = 'tech_input'

    ## WATER VAPOR
    data_dict['water_vapor'] = {}
    data_dict['water_vapor']['amount'] = biomass_balance_dict['water_evaporated']
    data_dict['water_vapor']['unit'] = 'L'
    data_dict['water_vapor']['type'] = 'emission'
   
    return data_dict

