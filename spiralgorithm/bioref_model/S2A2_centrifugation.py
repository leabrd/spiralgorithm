# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 11:11:47 2022

@author: leabr
"""

def BiomassCentrifugation (tech_period, mix_DW, PC_content, PC_extraction_eff):
    
    '''The amount of supernantant was calculated from the biomass balance.
    Assumed that there was no losses in the centrifugation process.'''
    
    from S0_set_parameters import InitialPCContent
    
    biomass_balance_dict_sc1 = {}
    biomass_balance_dict = {}
    
    if tech_period == '1':
        ## DATA COLLECTED
        PC_data_dict = InitialPCContent (tech_period)
        PC_content_sc1 = PC_data_dict['PC_content_biomass']
        PC_extraction_eff_sc1 = PC_data_dict['PC_extraction_efficiency']
        dry_spangles_sc1 = 50 # amount of the dry spangles [kg]
        mix_sc1 = 2050 # amount of mix [kg]
        DM_mix_sc1 = 96.8 # dry matter content of the dry spangles [% DM]
        mix_DW_sc1 = dry_spangles_sc1 * DM_mix_sc1 / 100 # amount of mix [kg DW-eq] (biomass conservation)
        CPA_sc1 = 200 # amount of CPA obtained [kg]
        DM_CPA_sc1 = 6.5 # dry matter content of the CPA [% DM]
        CPA_DW_sc1 = CPA_sc1 * DM_CPA_sc1 /100 # amount of CPA [kg DW-eq]
        ## DATA CALCULATED
        supernatant_DW_sc1 = mix_DW_sc1 - CPA_DW_sc1 # amount of supernatant [kg DW-eq]
        biomass_balance_dict_sc1['mix'] = {'wet_mass':mix_sc1, 
                                           'DM_content':DM_mix_sc1, 
                                           'dry_mass':mix_DW_sc1}
        biomass_balance_dict_sc1['CPA'] = {'wet_mass':CPA_sc1, 
                                           'DM_content':DM_CPA_sc1, 
                                           'dry_mass':CPA_DW_sc1}
        biomass_balance_dict_sc1['supernatant'] = {'wet_mass':'n/a', 
                                                   'DM_content':'n/a', 
                                                   'dry_mass':supernatant_DW_sc1}
        ## DATA MODELLED
        PC_content_factor = PC_content / PC_content_sc1 # factor that is either superior or inferior to 1
        PC_extraction_eff_factor = PC_extraction_eff / PC_extraction_eff_sc1
        supernatant_DW = (mix_DW * supernatant_DW_sc1 / mix_DW_sc1) * PC_content_factor * PC_extraction_eff_factor # amount of supernatant [kg DW-eq]
        CPA_DW = mix_DW - supernatant_DW # CPA calculated from the biomass balance [kg DW-eq]
        biomass_balance_dict['mix'] = mix_DW
        biomass_balance_dict['CPA'] = CPA_DW
        biomass_balance_dict['supernatant'] = supernatant_DW  
        
    if tech_period == '2': 
        ## DATA COLLECTED
        PC_data_dict = InitialPCContent (tech_period)
        PC_content_sc1 = PC_data_dict['PC_content_biomass']
        PC_extraction_eff_sc1 = PC_data_dict['PC_extraction_efficiency']
        dry_spangles_sc1 = 12.84 # amount of dry spangles [kg]
        mix_sc1 = 512.84 # amount of mix [kg]
        DM_mix_sc1 = 94.99 # dry matter content of the dry spangles [% DM]
        mix_DW_sc1 = dry_spangles_sc1 * DM_mix_sc1 / 100 # amount of mix [kg DW-eq] (biomass conservation)
        CPA_sc1 = 105.37 # amount of CPA obtained [kg]
        DM_CPA_sc1 = 4.25 # dry matter content of the CPA [% DM]
        CPA_DW_sc1 = CPA_sc1 * DM_CPA_sc1 /100 # amount of CPA [kg DW-eq]
        ## DATA CALCULATED
        supernatant_DW_sc1 = mix_DW_sc1 - CPA_DW_sc1 # amount of supernatant [kg DW-eq]
        biomass_balance_dict_sc1['mix'] = {'wet_mass':mix_sc1, 
                                           'DM_content':DM_mix_sc1, 
                                           'dry_mass':mix_DW_sc1}
        biomass_balance_dict_sc1['CPA'] = {'wet_mass':CPA_sc1, 
                                           'DM_content':DM_CPA_sc1, 
                                           'dry_mass':CPA_DW_sc1}
        biomass_balance_dict_sc1['supernatant'] = {'wet_mass':'n/a', 
                                                   'DM_content':'n/a', 
                                                   'dry_mass':supernatant_DW_sc1}
        ## DATA MODELLED
        PC_content_factor = PC_content / PC_content_sc1 # factor that is either superior or inferior to 1
        PC_extraction_eff_factor = PC_extraction_eff / PC_extraction_eff_sc1
        supernatant_DW = (mix_DW * supernatant_DW_sc1 / mix_DW_sc1) * PC_content_factor * PC_extraction_eff_factor # amount of supernatant [kg DW-eq]
        CPA_DW = mix_DW - supernatant_DW # CPA calculated from the biomass balance [kg DW-eq]
        biomass_balance_dict['mix'] = mix_DW
        biomass_balance_dict['CPA'] = CPA_DW
        biomass_balance_dict['supernatant'] = supernatant_DW
    
    return biomass_balance_dict_sc1, biomass_balance_dict


def ElectricityRefrigeratedTank (mix_DW):
    
    '''Value measured in 2022 only i.e. does not depend on the tech_period. '''
    
    ## DATA COLLECTED
    dry_spangles_sc1 = 12.84 # amount of dry spangles [kg]
    mix_sc1 = 512.84 # amount of mix [kg]
    DM_mix_sc1 = 94.99 # dry matter content of the dry spangles [% DM]
    mix_DW_sc1 = dry_spangles_sc1 * DM_mix_sc1 / 100 # amount of mix [kg DW-eq] (biomass conservation)
    instant_power = 1 # instant power of the refregirated tank [kW]
    running_time_sc1 = 25.83 # running time of the refregirated tank [h]
    elec_sc1 = instant_power * running_time_sc1
    ## DATA MODELLED
    elec = mix_DW * elec_sc1 / mix_DW_sc1

    return elec


def ElectricityCentrifuge (tech_period, mix_DW):
    
    if tech_period == '1':
        ## DATA COLLECTED
        dry_spangles_sc1 = 50 # amount of the dry spangles [kg]
        mix_sc1 = 2050 # amount of mix [kg]
        DM_mix_sc1 = 96.8 # dry matter content of the dry spangles [% DM]
        mix_DW_sc1 = dry_spangles_sc1 * DM_mix_sc1 / 100 # amount of mix [kg DW-eq] (biomass conservation)
        elec_process_sc1 = 39 # electricity in the process [kWh]
        elec_cleaning_sc1 = 25.8 # electricity used for cleaning [kWh]
        elec_sc1 = elec_process_sc1 + elec_cleaning_sc1 # total electricity used [kWh]
        ## MODELLED DATA
        elec = mix_DW * elec_sc1 / mix_DW_sc1
    
    if tech_period == '2':
        ## DATA COLLECTED
        dry_spangles_sc1 = 12.84 # amount of dry spangles [kg]
        mix_sc1 = 512.84 # amount of mix [kg]
        DM_mix_sc1 = 94.99 # dry matter content of the dry spangles [% DM]
        mix_DW_sc1 = dry_spangles_sc1 * DM_mix_sc1 / 100 # amount of mix [kg DW-eq] (biomass conservation)
        elec_process_sc1 = 7.237 # electricity in the process [kWh]
        elec_cleaning_sc1 = 12.664 # electricity used for cleaning [kWh]
        elec_sc1 = elec_process_sc1 + elec_cleaning_sc1 # total electricity used [kWh]
        ## MODELLED DATA
        elec = mix_DW * elec_sc1 / mix_DW_sc1
    
    return elec


def WaterCentrifugation (tech_period, mix_DW):
    
    
    if tech_period == '1':
        ## DATA COLLECTED
        dry_spangles_sc1 = 50 # amount of the dry spangles [kg]
        mix_sc1 = 2050 # amount of mix [kg]
        DM_mix_sc1 = 96.8 # dry matter content of the dry spangles [% DM]
        mix_DW_sc1 = dry_spangles_sc1 * DM_mix_sc1 / 100 # amount of mix [kg DW-eq] (biomass conservation)
        water_sc1 = 3405 + 71.55 # volume of water used [L] + volume to adjust the water balance [L]
        ## MODELLED DATA
        water = mix_DW * water_sc1 / mix_DW_sc1     
        
    if tech_period == '2':
        ## DATA COLLECTED
        dry_spangles_sc1 = 12.84 # amount of dry spangles [kg]
        mix_sc1 = 512.84 # amount of mix [kg]
        DM_mix_sc1 = 94.99 # dry matter content of the dry spangles [% DM]
        mix_DW_sc1 = dry_spangles_sc1 * DM_mix_sc1 / 100 # amount of mix [kg DW-eq] (biomass conservation)
        water_sc1 = 1563 # volume of water used [L]
        ## MODELLED DATA
        water = mix_DW * water_sc1 / mix_DW_sc1

    return water


def WastewaterCentrifugation (tech_period, mix_DW):
    
    if tech_period == '1':
        ## DATA COLLECTED
        dry_spangles_sc1 = 50 # amount of the dry spangles [kg]
        mix_sc1 = 2050 # amount of mix [kg]
        DM_mix_sc1 = 96.8 # dry matter content of the dry spangles [% DM]
        mix_DW_sc1 = dry_spangles_sc1 * DM_mix_sc1 / 100 # amount of mix [kg DW-eq] (biomass conservation)
        wastewater_sc1 = - 1 * 3355 /1000 # volume of water used [L]
        ## MODELLED DATA
        wastewater = mix_DW * wastewater_sc1 / mix_DW_sc1    
        
    if tech_period == '2':
        ## DATA COLLECTED
        dry_spangles_sc1 = 12.84 # amount of dry spangles [kg]
        mix_sc1 = 512.84 # amount of mix [kg]
        DM_mix_sc1 = 96.5 # dry matter content of the dry spangles [% DM]
        mix_DW_sc1 = dry_spangles_sc1 * DM_mix_sc1 / 100 # amount of mix [kg DW-eq] (biomass conservation)
        wastewater_sc1 = - 1 * 1470/1000 # volume of wastewater [m3]
        ## MODELLED DATA
        wastewater = mix_DW * wastewater_sc1 / mix_DW_sc1
 
    return wastewater


def SodiumHydroxide (tech_period, mix_DW):
    
    '''Sodium hydroxide was used in 2021 and 2022.'''
    
    if tech_period == '1':
        ## DATA COLLECTED
        dry_spangles_sc1 = 50 # amount of the dry spangles [kg]
        mix_sc1 = 2050 # amount of mix [kg]
        DM_mix_sc1 = 96.8 # dry matter content of the dry spangles [% DM]
        mix_DW_sc1 = dry_spangles_sc1 * DM_mix_sc1 / 100 # amount of mix [kg DW-eq] (biomass conservation)
        amount_NaOH_sc1 = 2.9 # amount of NaOH in pearls (>99%) [kg]
        amount_NaOH_ei36_sc1 = amount_NaOH_sc1 # considered as pure [kg]
        ## DATA MODELLED
        amount_NaOH_ei36 = mix_DW * amount_NaOH_ei36_sc1 / mix_DW_sc1
        
    if tech_period == '2':
        ## DATA COLLECTED
        dry_spangles_sc1 = 12.84 # amount of dry spangles [kg]
        mix_sc1 = 512.84 # amount of mix [kg]
        DM_mix_sc1 = 94.99 # dry matter content of the dry spangles [% DM]
        mix_DW_sc1 = dry_spangles_sc1 * DM_mix_sc1 / 100 # amount of mix [kg DW-eq] (biomass conservation)
        amount_NaOH_sc1 = 1.2 # amount of NaOH in pearls (>99%) [kg]
        amount_NaOH_ei36_sc1 = amount_NaOH_sc1 # considered as pure [kg]
        ## DATA MODELLED
        amount_NaOH_ei36 = mix_DW * amount_NaOH_ei36_sc1 / mix_DW_sc1
 
    return amount_NaOH_ei36


def HydrogenPeroxide (tech_period, mix_DW):
    
    '''Hydrogen peroxide was only used in 2021. In 2022 nitric acid was used 
    instead.'''    
    
    H2O2_dict = {}
    
    if tech_period == '1':
        ## DATA COLLECTED
        dry_spangles_sc1 = 50 # amount of the dry spangles [kg]
        mix_sc1 = 2050 # amount of mix [kg]
        DM_mix_sc1 = 96.8 # dry matter content of the dry spangles [% DM]
        mix_DW_sc1 = dry_spangles_sc1 * DM_mix_sc1 / 100 # amount of mix [kg DW-eq] (biomass conservation)
        volume_H2O2_sc1 = 240/1000 # amount of hydrogen peroxide [L]
        concentration_H2O2_sc1 = 35 # concentration of H2O2 [%]
        density_H2O2 = 1.13 # density of H2O2 at 35% and 20 °C [g/cm3] or [kg/L]
        ei36_concentration_H2O2 = 100 # pure substances in ecoinvent 3.6 [%]
        volume_H2O2_ei36_sc1 = concentration_H2O2_sc1 * volume_H2O2_sc1 / ei36_concentration_H2O2 # volume of NaOH [L]
        amount_H2O2_ei36_sc1 = volume_H2O2_ei36_sc1 * density_H2O2 # amount of NaOH [kg]
        ## DATA MODELLED
        amount_H2O2_ei36 = mix_DW * amount_H2O2_ei36_sc1 / mix_DW_sc1
        volume_H2O2 = mix_DW * volume_H2O2_sc1 / mix_DW_sc1
        volume_H2O2_ei36 = mix_DW * volume_H2O2_ei36_sc1 / mix_DW_sc1
        H2O2_dict['volume_H2O2_35%'] = volume_H2O2
        H2O2_dict['volume_H2O2_100%'] = volume_H2O2_ei36
        H2O2_dict['amount_H2O2_100%'] = amount_H2O2_ei36
        H2O2_dict['volume_ultrapure_water'] = volume_H2O2 - volume_H2O2_ei36 
        
    if tech_period == '2':
        H2O2_dict['volume_H2O2_35%'] = 0
        H2O2_dict['volume_H2O2_100%'] = 0
        H2O2_dict['amount_H2O2_100%'] = 0
        H2O2_dict['volume_ultrapure_water'] = 0
        
    return H2O2_dict


def NitricAcid (tech_period, mix_DW):
    
    '''Nitric acid was used in 2022 only. In 2021, hydrogen peroxide was used instead. '''
    
    HNO3_dict = {}
    
    if tech_period == '1':
        HNO3_dict['volume_HNO3_53%'] = 0 
        HNO3_dict['volume_HNO3_100%'] = 0
        HNO3_dict['amount_HNO3_100%'] = 0
        HNO3_dict['volume_ultrapure_water'] = 0
        
    if tech_period == '2':
        ## DATA COLLECTED
        dry_spangles_sc1 = 12.84 # amount of dry spangles [kg]
        mix_sc1 = 512.84 # amount of mix [kg]
        DM_mix_sc1 = 94.99 # dry matter content of the dry spangles [% DM]
        mix_DW_sc1 = dry_spangles_sc1 * DM_mix_sc1 / 100 # amount of mix [kg DW-eq] (biomass conservation)
        volume_HNO3_sc1 = 1.2 # amount of hydrogen peroxide [L]
        concentration_HNO3_sc1 = 53 # concentration of H2O2 [%]
        density_HNO3 = 1.33 # density of HNO3 at 53%  [g/cm3] or [kg/L]
        ei36_concentration_HNO3 = 100 # pure substances in ecoinvent 3.6 [%]
        volume_HNO3_ei36_sc1 = concentration_HNO3_sc1 * volume_HNO3_sc1 / ei36_concentration_HNO3 
        amount_HNO3_ei36_sc1 = volume_HNO3_ei36_sc1 * density_HNO3 # amount of NaOH [kg]
        ## DATA MODELLED
        amount_HNO3_ei36 = mix_DW * amount_HNO3_ei36_sc1 / mix_DW_sc1
        volume_HNO3 = mix_DW * volume_HNO3_sc1 / mix_DW_sc1
        volume_HNO3_ei36 = mix_DW * volume_HNO3_ei36_sc1 / mix_DW_sc1
        HNO3_dict['volume_HNO3_53%'] = volume_HNO3
        HNO3_dict['volume_HNO3_100%'] = volume_HNO3_ei36
        HNO3_dict['amount_HNO3_100%'] = amount_HNO3_ei36
        HNO3_dict['volume_ultrapure_water'] = volume_HNO3 - volume_HNO3_ei36 
   
    return HNO3_dict


def CentrifugationDataDict (tech_period, mix_DW, PC_content, PC_extraction_eff):
    
    data_dict = {}
    
    ## BIOMASS INPUT
    data_dict['mix'] = {}
    data_dict['mix']['amount'] = mix_DW
    data_dict['mix']['unit'] = 'kg DW-eq'
    data_dict['mix']['type'] = 'fg_input'
    
    ## BIOMASS OUTPUTS
    biomass_balance_dict_sc1, biomass_balance_dict = BiomassCentrifugation (tech_period, 
                                                                            mix_DW, PC_content,
                                                                            PC_extraction_eff)
    data_dict['supernatant'] = {}
    data_dict['supernatant']['amount'] = biomass_balance_dict['supernatant']
    data_dict['supernatant']['unit'] = 'kg DW-eq'
    data_dict['supernatant']['type'] = 'ref_flow'
    data_dict['CPA'] = {}
    data_dict['CPA']['amount'] = biomass_balance_dict['CPA']
    data_dict['CPA']['unit'] = 'kg DW-eq'
    data_dict['CPA']['type'] = 'coproduct'    
    data_dict['losses'] = {}
    data_dict['losses']['amount'] = 0
    data_dict['losses']['unit'] = 'kg DW-eq'
    data_dict['losses']['type'] = 'losses'
    
    ## ELECTRICITY
    data_dict['electricity_FR'] = {}
    data_dict['electricity_FR']['amount'] = (ElectricityRefrigeratedTank (mix_DW) 
                                             + ElectricityCentrifuge (tech_period, mix_DW))
    data_dict['electricity_FR']['unit'] = 'kWh'
    data_dict['electricity_FR']['type'] = 'tech_input'
    
    ## TAP WATER
    data_dict['tap_water'] = {}
    data_dict['tap_water']['amount'] = WaterCentrifugation (tech_period, mix_DW)
    data_dict['tap_water']['unit'] = 'L'
    data_dict['tap_water']['type'] = 'tech_input'
    
    ## SODIUM HYDROXIDE
    data_dict['sodium_hydroxide'] = {}
    data_dict['sodium_hydroxide']['amount'] = SodiumHydroxide (tech_period, mix_DW)
    data_dict['sodium_hydroxide']['unit'] = 'kg'
    data_dict['sodium_hydroxide']['type'] = 'tech_input'    
    
    ## HYDROGEN PEROXIDE 
    H2O2_dict = HydrogenPeroxide (tech_period, mix_DW)
    data_dict['hydrogen_peroxide'] = {}
    data_dict['hydrogen_peroxide']['amount'] = H2O2_dict['amount_H2O2_100%']
    data_dict['hydrogen_peroxide']['unit'] = 'kg'
    data_dict['hydrogen_peroxide']['type'] = 'tech_input'    
    
    ## NITRIC ACID
    HNO3_dict = NitricAcid (tech_period, mix_DW)
    data_dict['nitric_acid'] = {}
    data_dict['nitric_acid']['amount'] = HNO3_dict['amount_HNO3_100%']
    data_dict['nitric_acid']['unit'] = 'kg'
    data_dict['nitric_acid']['type'] = 'tech_input'    
        
    ## ULTRAPURE WATER
    data_dict['ultrapure_water'] = {}
    data_dict['ultrapure_water']['amount'] = (H2O2_dict['volume_ultrapure_water'] 
                                              + HNO3_dict['volume_ultrapure_water'])
    data_dict['ultrapure_water']['unit'] = 'kg'
    data_dict['ultrapure_water']['type'] = 'tech_input'    
    
    ## WASTEWATER
    data_dict['wastewater'] = {}
    data_dict['wastewater']['amount'] =  WastewaterCentrifugation (tech_period, mix_DW)
    data_dict['wastewater']['unit'] = 'm3'
    data_dict['wastewater']['type'] = 'tech_output'

    return data_dict
