# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 16:38:06 2022

@author: leabr
"""

def BiomassMaceration (dry_spangles_DW):
    '''
    Assumed conservation of mass for periods 1 and 2. 
    '''
    
    mix_DW = dry_spangles_DW # conservation of mass, no losses
    
    return mix_DW


def WaterMaceration (tech_period, dry_spangles_DW): 
    ''' 
    The volume of water is calculated in order to reach the concentration of 
    2.5% Spirulina in water. In 2021 and 2022, the volumes of water used
    were slightly different i.e. 12.84 kg instead of 12.5 exactly. Considered
    as negligibe.
    '''
    if tech_period == '1':
        ## DATA COLLECTED 
        dry_spangles_sc1 = 50 # amount of dry spangles [kg]
        DW_dry_spangles_sc1 = 96.8 # dry matter content of the dry spangles [% DM]
        dry_spangles_DW_sc1 = dry_spangles_sc1 * DW_dry_spangles_sc1 / 100 # amount of dry spangles [kg DW-eq]
        water_maceration_sc1 = 2000 # volume of water [L]
        water_flow_hose = 18.56 # average water flow of the hose [L/min]
        water_cleaning_sc1 = (4 + 3) * water_flow_hose # volume of water [L]
        total_water_sc1 = water_maceration_sc1 + water_cleaning_sc1
        ## DATA MODELLED
        water_maceration = dry_spangles_DW / (2.5/100) # volume of water to reach a concentration of 2.5% spirulina [L]
        water_cleaning = dry_spangles_DW * water_cleaning_sc1 / dry_spangles_DW_sc1 # volume of water [L]
        total_water = water_maceration + water_cleaning
        
    if tech_period == '2':
        ## DATA COLLECTED 
        dry_spangles_sc1 = 12.84 # amount of dry spangles [kg]
        DW_dry_spangles_sc1 = 94.99 # dry matter content of the dry spangles [% DM]
        dry_spangles_DW_sc1 = dry_spangles_sc1 * DW_dry_spangles_sc1 / 100 # amount of dry spangles [kg DW-eq]
        water_maceration_sc1 = 500 # volume of water [L]
        water_flow_hose = 11.94 # average water flow of the hose [L/min]
        water_cleaning_sc1 = 46/60*water_flow_hose # volume of water [L]
        total_water_sc1 = water_maceration_sc1 + water_cleaning_sc1
        ## DATA MODELLED
        water_maceration = dry_spangles_DW / (2.5/100) # volume of water to reach a concentration of 2.5% spirulina [L]
        water_cleaning = dry_spangles_DW * water_cleaning_sc1 / dry_spangles_DW_sc1 # volume of water [L]
        total_water = water_maceration + water_cleaning

    return total_water


def ElectricityMaceration (tech_period, dry_spangles_DW):
    '''The running time of the mixing was reduced from 24h to 1h approx. '''
    
    if tech_period == '1':
        ## DATA COLLECTED 
        running_time= 25.33
        dry_spangles_sc1 = 50 # amount of dry spangles [kg]
        DW_dry_spangles_sc1 = 96.8 # dry matter content of the dry spangles [% DM]
        dry_spangles_DW_sc1 = dry_spangles_sc1 * DW_dry_spangles_sc1 / 100 # amount of dry spangles [kg DW-eq]
        elec_sc1 = 4.445 # amount of electricity used [kWh]
        ## DATA MODELLED
        elec = dry_spangles_DW * elec_sc1 / dry_spangles_DW_sc1
        
    else:
        ## DATA COLLECTED
        running_time = 46/60 # running time reduced to less than 1 h [h]
        dry_spangles_sc1 = 12.84 # amount of dry spangles [kg]
        DW_dry_spangles_sc1 = 94.99 # dry matter content of the dry spangles [% DM]
        dry_spangles_DW_sc1 = dry_spangles_sc1 * DW_dry_spangles_sc1 / 100 # amount of dry spangles [kg DW-eq]
        elec_sc1 = 0.138 # amount of electricity used [kWh]
        ## DATA MODELLED
        elec = dry_spangles_DW * elec_sc1 / dry_spangles_DW_sc1
    
    return elec


def WastewaterMaceration (tech_period, dry_spangles_DW):
    
    '''The wastewater corresponds to the water used for cleaning only. 
    The water used for maceration was added into the product.'''
    
    if tech_period == '1':
        ## DATA COLLECTED 
        dry_spangles_sc1 = 50 # amount of dry spangles [kg]
        DW_dry_spangles_sc1 = 96.8 # dry matter content of the dry spangles [% DM]
        dry_spangles_DW_sc1 = dry_spangles_sc1 * DW_dry_spangles_sc1 / 100 # amount of dry spangles [kg DW-eq]
        wastewater_sc1 = -1 * 129.92/1000 # amount of wastewater [m3]  
        ## DATA MODELLED
        wastewater = dry_spangles_DW * wastewater_sc1 / dry_spangles_DW_sc1
        
    else: 
        ## DATA COLLECTED
        dry_spangles_sc1 = 12.84 # amount of dry spangles [kg]
        DW_dry_spangles_sc1 = 94.99 # dry matter content of the dry spangles [% DM]
        dry_spangles_DW_sc1 = dry_spangles_sc1 * DW_dry_spangles_sc1 / 100 # amount of dry spangles [kg DW-eq]
        wastewater_sc1 = -1 * 9.154/1000 # amount of wastewater [m3]
        ## DATA MODELLED
        wastewater = dry_spangles_DW * wastewater_sc1 / dry_spangles_DW_sc1
    
    return wastewater


def PlasticWaste (dry_spangles_DW):
    
    '''The value was not measured but calculated from the values obtained
    from the packaging processes in S1.'''
    
    dry_spangles_sc1 = 12.84 # amount of dry spangles [kg]
    DW_dry_spangles_sc1 = 94.99 # dry matter content of the dry spangles [% DM]
    dry_spangles_DW_sc1 = dry_spangles_sc1 * DW_dry_spangles_sc1 / 100 # amount of dry spangles [kg DW-eq]
    plastic_sc1 = 0.089 # amount of plastic calculated from S1 [kg]
    plastic_waste = -1 * dry_spangles_DW * plastic_sc1 / dry_spangles_DW_sc1

    return plastic_waste


def MacerationDataDict (tech_period, dry_spangles_DW):
   
    data_dict = {}
    
    ## BIOMASS INPUT
    data_dict['dry_spangles'] = {}
    data_dict['dry_spangles']['amount'] = dry_spangles_DW
    data_dict['dry_spangles']['unit'] = 'kg DW-eq'
    data_dict['dry_spangles']['type'] = 'fg_input'
    
    ## BIOMASS OUTPUTS
    data_dict['mix'] = {}
    data_dict['mix']['amount'] = BiomassMaceration (dry_spangles_DW)
    data_dict['mix']['unit'] = 'kg DW-eq'
    data_dict['mix']['type'] = 'ref_flow'
    data_dict['losses'] = {}
    data_dict['losses']['amount'] = 0
    data_dict['losses']['unit'] = 'kg DW-eq'
    data_dict['losses']['type'] = 'losses'
    
    ## ELECTRICITY
    data_dict['electricity_FR'] = {}
    data_dict['electricity_FR']['amount'] = ElectricityMaceration (tech_period, 
                                                                   dry_spangles_DW)
    data_dict['electricity_FR']['unit'] = 'kWh'
    data_dict['electricity_FR']['type'] = 'tech_input'
    
    ## TAP WATER
    data_dict['tap_water'] = {}
    data_dict['tap_water']['amount'] = WaterMaceration (tech_period, 
                                                        dry_spangles_DW)
    data_dict['tap_water']['unit'] = 'L'
    data_dict['tap_water']['type'] = 'tech_input'
    
    ## PLASTIC WASTE
    data_dict['plastic_waste_FR'] = {}
    data_dict['plastic_waste_FR']['amount'] = PlasticWaste (dry_spangles_DW)
    data_dict['plastic_waste_FR']['unit'] = 'kg'
    data_dict['plastic_waste_FR']['type'] = 'tech_output'
    
    ## WASTEWATER 
    data_dict['wastewater'] = {}
    data_dict['wastewater']['amount'] = WastewaterMaceration (tech_period, 
                                                              dry_spangles_DW)
    data_dict['wastewater']['unit'] = 'm3'
    data_dict['wastewater']['type'] = 'tech_output'
  
    return data_dict