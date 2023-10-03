# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 13:26:38 2022

@author: leabr
"""

def BiomassUltrafiltration2 (blue_extract_UF1_DW = 2.55629):
    
    biomass_balance_dict_sc1 = {}
    biomass_balance_dict = {}
    
    ## DATA COLLECTED
    blue_extract_UF1_DW_sc1 = 2.55629 # amount of blue extract from UF1 [kg DW-eq]
    CPD_sc1 = 140 # amount of supernatant from UF2 [kg]
    DM_CDP_sc1 = 0.1 # dry matter content of the CPD [% DW]
    CPD_DW_sc1 = CPD_sc1 * DM_CDP_sc1/100
    blue_extract_UF2_DW_sc1 = blue_extract_UF1_DW_sc1 - CPD_DW_sc1 # conservation of mass, no losses
    biomass_balance_dict_sc1['blue_extract_UF1'] = {'wet_mass':'NaN', 
                                                    'DM_content':'NaN', 
                                                    'dry_mass':blue_extract_UF1_DW_sc1}
    biomass_balance_dict_sc1['blue_extract_UF2'] = {'wet_mass':'NaN', 
                                                    'DM_content':'NaN', 
                                                    'dry_mass':blue_extract_UF2_DW_sc1}
    biomass_balance_dict_sc1['CPD'] = {'wet_mass':'NaN', 'DM_content':'NaN', 'dry_mass':CPD_DW_sc1}    
    ## DATA MODELLED
    CPD_DW = blue_extract_UF1_DW * CPD_DW_sc1 / blue_extract_UF1_DW_sc1
    blue_extract_UF2_DW = blue_extract_UF1_DW - CPD_DW
    biomass_balance_dict['blue_extract_UF1'] = blue_extract_UF1_DW
    biomass_balance_dict['blue_extract_UF2'] = blue_extract_UF2_DW
    biomass_balance_dict['CPD'] = CPD_DW
  
    return biomass_balance_dict_sc1, biomass_balance_dict


def ElectricityUltrafiltration2 (blue_extract_UF1_DW):
    
    ## DATA COLLECTED
    blue_extract_UF1_DW_sc1 = 2.55629 # amount of blue extract from UF1 [kg DW-eq]
    elec_UF2_sc1 = 12.2518
    ## DATA MODELLED
    elec_UF2 = blue_extract_UF1_DW * elec_UF2_sc1 / blue_extract_UF1_DW_sc1

    return elec_UF2


def WaterUltrafiltration2 (blue_extract_UF1_DW):
    
    ## DATA COLLECTED
    blue_extract_UF1_DW_sc1 = 2.55629 # amount of blue extract from UF1 [kg DW-eq]
    water_UF2_sc1 = 1086 + 30.45# volume of water [L]
    ## DATA MODELLED
    water_UF2 = blue_extract_UF1_DW * water_UF2_sc1 / blue_extract_UF1_DW_sc1

    return water_UF2


def WastewaterUltrafiltration2 (blue_extract_UF1_DW):
    
    ## DATA COLLECTED
    blue_extract_UF1_DW_sc1 = 2.55629 # amount of blue extract from UF1 [kg DW-eq]    
    wastewater_UF2_sc1 = -1 * 1086 / 1000 # volume of wastewater [m3]
    ## DATA MODELLED
    wastewater_UF2 = blue_extract_UF1_DW * wastewater_UF2_sc1 / blue_extract_UF1_DW_sc1
   
    return wastewater_UF2


def SodiumHydroxide (blue_extract_UF1_DW):
    
    NaOH_dict = {}
        
    ## DATA COLLECTED
    blue_extract_UF1_DW_sc1 = 2.55629 # amount of blue extract from UF1 [kg DW-eq]    
    volume_NaOH_sc1 = 1.4 # amount of NaOH in pearls (>99%) [kg]
    concentration_NaOH_sc1 = 30 # concentration of NaOH [%]
    density_NaOH = 1.36 # density of H2O2 at 35% and 20 °C [g/cm3] or [kg/L]
    ei36_concentration_NaOH = 100 # pure substances in ecoinvent 3.6 [%]
    volume_NaOH_ei36_sc1 = concentration_NaOH_sc1 * volume_NaOH_sc1 / ei36_concentration_NaOH # volume of NaOH [L]
    amount_NaOH_ei36_sc1 = volume_NaOH_ei36_sc1 * density_NaOH # amount of NaOH [kg]
    ## DATA MODELLED
    amount_NaOH_ei36 = blue_extract_UF1_DW * amount_NaOH_ei36_sc1 / blue_extract_UF1_DW_sc1
    volume_NaOH = blue_extract_UF1_DW * volume_NaOH_sc1 / blue_extract_UF1_DW_sc1
    volume_NaOH_ei36 = blue_extract_UF1_DW * volume_NaOH_ei36_sc1 / blue_extract_UF1_DW_sc1
    NaOH_dict['volume_NaOH_35%'] = volume_NaOH
    NaOH_dict['volume_NaOH_100%'] = volume_NaOH_ei36
    NaOH_dict['amount_NaOH_100%'] = amount_NaOH_ei36
    NaOH_dict['volume_ultrapure_water'] = volume_NaOH - volume_NaOH_ei36 
 
    return NaOH_dict


def NitricAcid (blue_extract_UF1_DW):
        
    HNO3_dict = {}
    
    ## DATA COLLECTED
    blue_extract_UF1_DW_sc1 = 2.55629 # amount of blue extract from UF1 [kg DW-eq]    
    volume_HNO3_sc1 = 1.4 # amount of hydrogen peroxide [L]
    concentration_HNO3_sc1 = 53 # concentration of H2O2 [%]
    density_HNO3 = 1.33 # density of HNO3 at 53%  [g/cm3] or [kg/L]
    ei36_concentration_HNO3 = 100 # pure substances in ecoinvent 3.6 [%]
    volume_HNO3_ei36_sc1 = concentration_HNO3_sc1 * volume_HNO3_sc1 / ei36_concentration_HNO3 
    amount_HNO3_ei36_sc1 = volume_HNO3_ei36_sc1 * density_HNO3 # amount of NaOH [kg]
    ## DATA MODELLED
    amount_HNO3_ei36 = blue_extract_UF1_DW * amount_HNO3_ei36_sc1 / blue_extract_UF1_DW_sc1
    volume_HNO3 = blue_extract_UF1_DW * volume_HNO3_sc1 / blue_extract_UF1_DW_sc1
    volume_HNO3_ei36 = blue_extract_UF1_DW * volume_HNO3_ei36_sc1 / blue_extract_UF1_DW_sc1
    HNO3_dict['volume_HNO3_53%'] = volume_HNO3
    HNO3_dict['volume_HNO3_100%'] = volume_HNO3_ei36
    HNO3_dict['amount_HNO3_100%'] = amount_HNO3_ei36
    HNO3_dict['volume_ultrapure_water'] = volume_HNO3 - volume_HNO3_ei36 
   
    return HNO3_dict


def Ultrafiltration2DataDict (blue_extract_UF1_DW):
    
    data_dict = {}
    
    ## BIOMASS INPUT
    data_dict['blue_extract_UF1'] = {}
    data_dict['blue_extract_UF1']['amount'] = blue_extract_UF1_DW
    data_dict['blue_extract_UF1']['unit'] = 'kg DW-eq'
    data_dict['blue_extract_UF1']['type'] = 'fg_input'
    
    ## BIOMASS OUTPUTS
    biomass_balance_dict_sc1, biomass_balance_dict = BiomassUltrafiltration2 (blue_extract_UF1_DW)
    data_dict['blue_extract_UF2'] = {}
    data_dict['blue_extract_UF2']['amount'] = biomass_balance_dict['blue_extract_UF2']
    data_dict['blue_extract_UF2']['unit'] = 'kg DW-eq'
    data_dict['blue_extract_UF2']['type'] = 'ref_flow'
    data_dict['CPD'] = {}
    data_dict['CPD']['amount'] = biomass_balance_dict['CPD']
    data_dict['CPD']['unit'] = 'kg DW-eq'
    data_dict['CPD']['type'] = 'coproduct'
    data_dict['losses'] = {}
    data_dict['losses']['amount'] = 0
    data_dict['losses']['unit'] = 'kg DW-eq'
    data_dict['losses']['type'] = 'losses'    
    
    ## ELECTRICITY
    data_dict['electricity_FR'] = {}
    data_dict['electricity_FR']['amount'] = ElectricityUltrafiltration2 (blue_extract_UF1_DW)
    data_dict['electricity_FR']['unit'] = 'kWh'
    data_dict['electricity_FR']['type'] = 'tech_input'
    
    ## SODIUM HYDROXIDE
    NaOH_dict = SodiumHydroxide (blue_extract_UF1_DW)
    data_dict['sodium_hydroxide'] = {}
    data_dict['sodium_hydroxide']['amount'] = NaOH_dict['amount_NaOH_100%']
    data_dict['sodium_hydroxide']['unit'] = 'kg'
    data_dict['sodium_hydroxide']['type'] = 'tech_input'    
    
    ## NITRIC ACID
    HNO3_dict = NitricAcid (blue_extract_UF1_DW)
    data_dict['nitric_acid'] = {}
    data_dict['nitric_acid']['amount'] = HNO3_dict['amount_HNO3_100%']
    data_dict['nitric_acid']['unit'] = 'kg'
    data_dict['nitric_acid']['type'] = 'tech_input'    
        
    ## ULTRAPURE WATER
    data_dict['ultrapure_water'] = {}
    data_dict['ultrapure_water']['amount'] = (NaOH_dict['volume_ultrapure_water'] 
                                              + HNO3_dict['volume_ultrapure_water'])
    data_dict['ultrapure_water']['unit'] = 'kg'
    data_dict['ultrapure_water']['type'] = 'tech_input'   
    
    ## TAP WATER
    data_dict['tap_water'] = {}
    data_dict['tap_water']['amount'] = WaterUltrafiltration2 (blue_extract_UF1_DW)
    data_dict['tap_water']['unit'] = 'L'
    data_dict['tap_water']['type'] = 'tech_input'
    
    ## WASTEWATER
    data_dict['wastewater'] = {}
    data_dict['wastewater']['amount'] = WastewaterUltrafiltration2 (blue_extract_UF1_DW)
    data_dict['wastewater']['unit'] = 'm3'
    data_dict['wastewater']['type'] = 'tech_output'    

    return data_dict
  