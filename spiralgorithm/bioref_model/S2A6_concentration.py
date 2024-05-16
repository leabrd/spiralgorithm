# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 13:44:06 2022

@author: leabr
"""

def BiomassConcentration (CPD_DW = 4.53):
    
    '''Only the CPD from UF1 was concentrated. But in the model it should be the 
    CPD from UF1 and from UF2. The data for the period 2 were used.'''
    
    biomass_balance_dict_sc1 = {}
    biomass_balance_dict = {}
    
    ## DATA COLLECTED 
    ### CPD from UF1
    CDP_UF1_sc1 = 1968 # amount of CPD [kg]
    DM_CPD_UF1_sc1 = 0.23 # dry matter content of the CPD [%]
    CPD_DW_UF1_sc1 = CDP_UF1_sc1 * DM_CPD_UF1_sc1/100 # amount of CPD [kg DW-eq]
    # ### CPD from UF2; the DM content was calculated from the mass balance
    # CPD_UF2_sc1 = 140 # amount of supernatant from UF2 [kg]
    # DM_CDP_UF2_sc1 = 0.1 # dry matter content of the CPD [% DW]
    # CPD_DW_UF2_sc1 = CPD_UF2_sc1 * DM_CDP_UF2_sc1/100
    # ### Total CPD for theoretical concentration
    # total_CDP_DW_sc1 = CPD_DW_UF1_sc1 + CPD_DW_UF2_sc1
    ### concentrate obtained from the concentration of CPD form UF1 only 
    CPD_concentrate_sc1 = 55.5 # amoumt of CPD concentrate [kg]
    DM_CPD_concentrate_sc1 = 6.3 # dry matter content of the CPD concentrate [%]
    CPD_concentrate_DW_sc1 = CPD_concentrate_sc1 * DM_CPD_concentrate_sc1 / 100 # amount of CPD concentrate [kg DW-eq]
    losses_sc1 = CPD_DW_UF1_sc1 - CPD_concentrate_DW_sc1 # biomass in distillate [kg DW-eq]
    biomass_balance_dict_sc1['CPD_UF1'] = {'wet_mass':CDP_UF1_sc1, 
                                           'DM_content':DM_CPD_UF1_sc1, 
                                           'dry_mass':CPD_DW_UF1_sc1}
    biomass_balance_dict_sc1['CPD_concentrate'] = {'wet_mass':CPD_concentrate_sc1, 
                                                   'DM_content':DM_CPD_concentrate_sc1, 
                                                   'dry_mass':CPD_concentrate_DW_sc1}
    biomass_balance_dict_sc1['losses'] = {'wet_mass':'NaN', 
                                          'DM_content':'NaN', 
                                          'dry_mass':losses_sc1}   
    ## DATA MODELLED
    CPD_concentrate_DW = CPD_DW * CPD_concentrate_DW_sc1 / CPD_DW_UF1_sc1
    losses_DW = CPD_DW - CPD_concentrate_DW
    biomass_balance_dict['CPD'] = CPD_DW
    biomass_balance_dict['CPD_concentrate'] = CPD_concentrate_DW
    biomass_balance_dict['losses'] = losses_DW
   
    return biomass_balance_dict_sc1, biomass_balance_dict


def ElectricityConcentration (CPD_DW):
    
    ## DATA COLLECTED
    CDP_sc1 = 1968 # amount of CPD [kg]
    DM_CPD_sc1 = 0.23  # dry matter content of the CPD [%]
    CPD_DW_sc1 = CDP_sc1 * DM_CPD_sc1/100 # amount of CPD [kg DW-eq]
    elec_concentration_sc1 = 162.42
    ## DATA MODELLED
    elec_concentration = CPD_DW * elec_concentration_sc1 / CPD_DW_sc1

    return elec_concentration


def WaterConcentration (CPD_DW):
    
    ## DATA COLLECTED
    CDP_sc1 = 1968 # amount of CPD [kg]
    DM_CPD_sc1 = 0.23 # dry matter content of the CPD [%]
    CPD_DW_sc1 = CDP_sc1 * DM_CPD_sc1/100 # amount of CPD [kg DW-eq]
    water_concentration_sc1 = 41.4 + 38.5  # amount of water used [L]
    ## DATA MODELLED
    water_concentration = CPD_DW * water_concentration_sc1 / CPD_DW_sc1

    return water_concentration


def NaturalGasConcentration (CPD_DW):
    
    ## DATA COLLECTED
    CDP_sc1 = 1968 # amount of CPD [kg]
    DM_CPD_sc1 = 0.23 # dry matter content of the CPD [%]
    CPD_DW_sc1 = CDP_sc1 * DM_CPD_sc1/100 # amount of CPD [kg DW-eq]    
    gas_concentration_sc1 = 170.5 # amount of natural gas [m3]
    ## DATA MODELLED
    gas_concentration = CPD_DW * gas_concentration_sc1 / CPD_DW_sc1

    return gas_concentration


def WastewaterConcentration (CPD_DW):
    
    ## DATA COLLECTED
    CDP_sc1 = 1968 # amount of CPD [kg]
    DM_CPD_sc1 = 0.23 # dry matter content of the CPD [%]
    CPD_DW_sc1 = CDP_sc1 * DM_CPD_sc1/100 # amount of CPD [kg DW-eq]    
    wastewater_concentration_sc1 = -1 * 41.4/1000 # [L]
    ## DATA MODELLED
    wastewater_concentration = CPD_DW * wastewater_concentration_sc1 / CPD_DW_sc1

    return wastewater_concentration


def ConcentrationCPDDataDict (CPD_DW):

    data_dict = {}
    
    ## BIOMASS INPUT
    data_dict['CPD'] = {}
    data_dict['CPD']['amount'] = CPD_DW
    data_dict['CPD']['unit'] = 'kg DW-eq'
    data_dict['CPD']['type'] = 'fg_input'
    
    ## BIOMASS OUTPUTS
    biomass_balance_dict_sc1, biomass_balance_dict =  BiomassConcentration (CPD_DW)
    data_dict['CPD_concentrate'] = {}
    data_dict['CPD_concentrate']['amount'] = biomass_balance_dict['CPD_concentrate']
    data_dict['CPD_concentrate']['unit'] = 'kg DW-eq'
    data_dict['CPD_concentrate']['type'] = 'ref_flow'
    data_dict['losses'] = {}
    data_dict['losses']['amount'] = biomass_balance_dict['losses']
    data_dict['losses']['unit'] = 'kg DW-eq'
    data_dict['losses']['type'] = 'losses'    
    
    ## ELECTRICITY
    data_dict['electricity_FR'] = {}
    data_dict['electricity_FR']['amount'] = ElectricityConcentration (CPD_DW)
    data_dict['electricity_FR']['unit'] = 'kWh'
    data_dict['electricity_FR']['type'] = 'tech_input'
    
    ## TAP WATER
    data_dict['tap_water'] = {}
    data_dict['tap_water']['amount'] = WaterConcentration (CPD_DW)
    data_dict['tap_water']['unit'] = 'L'
    data_dict['tap_water']['type'] = 'tech_input'
    
    ## NATURAL GAS
    data_dict['natural_gas_FR'] = {}
    data_dict['natural_gas_FR']['amount'] = NaturalGasConcentration (CPD_DW)
    data_dict['natural_gas_FR']['unit'] = 'm3'
    data_dict['natural_gas_FR']['type'] = 'tech_input'
    
    ## WASTEWATER
    data_dict['wastewater'] = {}
    data_dict['wastewater']['amount'] = WastewaterConcentration (CPD_DW)
    data_dict['wastewater']['unit'] = 'm3'
    data_dict['wastewater']['type'] = 'tech_output'
    
    return data_dict

