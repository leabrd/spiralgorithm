# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 14:35:23 2022

@author: leabr
"""

def BiomassUltrafiltration (tech_period = '2', permeate_DF_DW = 4.1):
    
    biomass_balance_dict_sc1 = {}
    biomass_balance_dict = {}
    
    if tech_period == '1':
        ## DATA COLLECTED
        permeate_DF_DW_sc1 = 4.285044 # from the activity S2.A1.Extraction [kg DW-eq]
        amount_retentate_sc1 = 141.62 # amount of retentate from UF (> 15 kDa) [kg]
        DM_retentate_sc1 = 2.63 # dry matter content of the rententate [%]
        retentate_DW_sc1 = amount_retentate_sc1 * DM_retentate_sc1 / 100
        amount_permeate_sc1 = 214.60 # amount of retentate from UF (> 15 kDa) [kg]
        DM_permeate_sc1 = 1.55 # dry matter content of the permeate [%]
        permeate_DW_sc1 = amount_permeate_sc1 * DM_permeate_sc1 / 100 
        ## UNBALANCED => CALCULATE AMOUNT OF RETENTATE FROM MASS BALANCE (NO LOSSES)
        '''For now, scaled the flows down to meet the total input of permeate from DF.'''
        total_unbalanced = retentate_DW_sc1 + permeate_DW_sc1
        retentate_DW_sc1_balanced = permeate_DF_DW_sc1 * retentate_DW_sc1 / total_unbalanced
        permeate_DW_sc1_balanced = permeate_DF_DW_sc1 * permeate_DW_sc1 / total_unbalanced
        ## BIOMASS BALANCE TO ESTIMATE THE LOSSES
        losses_DW_sc1 = 0
        biomass_balance_dict_sc1['permeate_DF'] = {'wet_mass': 'NaN', 
                                                   'DM_content': 'NaN', 
                                                   'dry_mass': permeate_DF_DW_sc1}   
        biomass_balance_dict_sc1['retentate_UF'] = {'wet_mass': 'NaN', 
                                                    'DM_content': DM_retentate_sc1, 
                                                    'dry_mass': retentate_DW_sc1_balanced}   
        biomass_balance_dict_sc1['permeate_UF'] = {'wet_mass': 'NaN', 
                                                   'DM_content': DM_permeate_sc1, 
                                                   'dry_mass': permeate_DW_sc1_balanced}   
        biomass_balance_dict_sc1['losses'] = {'wet_mass': 'NaN', 
                                              'DM_content': 'NaN', 
                                              'dry_mass': losses_DW_sc1}   
        ## DATA MODELLED
        retentate_UF_DW = permeate_DF_DW * retentate_DW_sc1_balanced / permeate_DF_DW_sc1        
        permeate_UF_DW = permeate_DF_DW * permeate_DW_sc1_balanced / permeate_DF_DW_sc1  
        losses_DW = permeate_DF_DW - retentate_UF_DW - permeate_UF_DW
        biomass_balance_dict['permeate_DF'] = permeate_DF_DW
        biomass_balance_dict['retentate_UF'] = retentate_UF_DW
        biomass_balance_dict['permeate_UF'] = permeate_UF_DW
        biomass_balance_dict['losses'] = losses_DW 
        
    if tech_period == '2': 
        ## DATA COLLECTED
        vol_perm_sc1 = 370 # volume of permeate from DF (< 0.2 μm) [L]
        vol_perm_not_ultraf_sc1 = 104 # volume of permeate that was not ultrafiltered; values measured [L]
        vol_perm_ultraf_sc1 = vol_perm_sc1 - vol_perm_not_ultraf_sc1
        DM_permeate_DF_sc1 = 1.54 # dry matter content of the permeate [%]
        permeate_ultrafiltered_DW_sc1 = vol_perm_ultraf_sc1 * DM_permeate_DF_sc1 / 100 
        permeate_theoretical_DW_sc1 = vol_perm_sc1 * DM_permeate_DF_sc1 / 100 
        ## REAL VALUES MEASURED TO THEORETICAL VALUES CALCULATED
        amount_ret_meas_sc1 = 165.76 # amount of retentate from UF (> 15 kDa) [kg]
        amount_ret_theo_sc1 = vol_perm_sc1 * amount_ret_meas_sc1 / vol_perm_ultraf_sc1
        DM_retentate_sc1 = 1.71 # dry matter content of the rententate [%]
        retentate_DW_sc1 = amount_ret_theo_sc1 * DM_retentate_sc1 / 100
        amount_perm_meas_sc1 = 90.62 # amount of retentate from UF (> 15 kDa) [kg]
        amount_perm_theo_sc1 = vol_perm_sc1 * amount_perm_meas_sc1 / vol_perm_ultraf_sc1
        DM_permeate_sc1 = 1.32 # dry matter content of the permeate [%]
        permeate_DW_sc1 = amount_perm_theo_sc1 * DM_permeate_sc1 / 100 
        ## BIOMASS BALANCE TO ESTIMATE THE LOSSES
        losses_DW_sc1 = permeate_theoretical_DW_sc1 - (retentate_DW_sc1 + permeate_DW_sc1)
        biomass_balance_dict_sc1['permeate_DF'] = {'wet_mass': vol_perm_sc1, 
                                                   'DM_content': DM_permeate_DF_sc1, 
                                                   'dry_mass': permeate_theoretical_DW_sc1}   
        biomass_balance_dict_sc1['retentate_UF'] = {'wet_mass': amount_ret_theo_sc1, 
                                                    'DM_content': DM_retentate_sc1, 
                                                    'dry_mass': retentate_DW_sc1}   
        biomass_balance_dict_sc1['permeate_UF'] = {'wet_mass': amount_perm_theo_sc1, 
                                                   'DM_content': DM_permeate_sc1, 
                                                   'dry_mass': permeate_DW_sc1}   
        biomass_balance_dict_sc1['losses'] = {'wet_mass': 'NaN', 
                                              'DM_content': 'NaN', 
                                              'dry_mass': losses_DW_sc1}   
        ## DATA MODELLED
        retentate_UF_DW = permeate_DF_DW * retentate_DW_sc1 / permeate_theoretical_DW_sc1        
        permeate_UF_DW = permeate_DF_DW * permeate_DW_sc1 / permeate_theoretical_DW_sc1  
        losses_DW = permeate_DF_DW - (retentate_UF_DW + permeate_UF_DW)
        biomass_balance_dict['permeate_DF'] = permeate_DF_DW
        biomass_balance_dict['retentate_UF'] = retentate_UF_DW
        biomass_balance_dict['permeate_UF'] = permeate_UF_DW
        biomass_balance_dict['losses'] = losses_DW

    return biomass_balance_dict_sc1, biomass_balance_dict


def ElectricityUltrafiltration (tech_period = '2', permeate_DF_DW = 4.1):
    
    if tech_period == '1':
        ## DATA COLLECTED
        permeate_DF_DW_sc1 = 4.285044 # from the activity S2.A1.Extraction [kg DW-eq]
        elec_UF_sc1 = 23.818 # amount of electricity used [kWh]
        ## DATA MODELLED
        elec_UF = permeate_DF_DW * elec_UF_sc1 / permeate_DF_DW_sc1
    else: 
        ## DATA COLLECTED
        permeate_DF_DW_sc1 = 4.1 # from the activity S2.A1.Extraction [kg DW-eq]
        elec_UF_sc1 = 17.54 # amount of electricity used [kWh] - upscaled to 370L
        ## DATA MODELLED
        elec_UF = permeate_DF_DW * elec_UF_sc1 / permeate_DF_DW_sc1

    return elec_UF


def WaterUltrafiltration (tech_period = '2', permeate_DF_DW = 4.1):
    
    if tech_period == '1':
        ## DATA COLLECTED
        permeate_DF_DW_sc1 = 4.285044 # from the activity S2.A1.Extraction [kg DW-eq]
        water_UF_sc1 = 800
        ## DATA MODELLED
        water_UF = permeate_DF_DW * water_UF_sc1 / permeate_DF_DW_sc1
    else: 
        ## DATA COLLECTED
        permeate_DF_DW_sc1 = 4.1  # from the activity S2.A1.Extraction [kg DW-eq]
        water_UF_sc1 = 419.45
        ## DATA MODELLED
        water_UF = permeate_DF_DW * water_UF_sc1 / permeate_DF_DW_sc1

    return water_UF


def SodiumHydroxideUltrafiltration (tech_period = '2', permeate_DF_DW = 4.1):
    
    NaOH_dict = {}
    
    if tech_period == '1':
        ## DATA COLLECTED
        permeate_DF_DW_sc1 = 4.285044 # from the activity S2.A1.Extraction [kg DW-eq]
        concentration_NaOH_sc1 = 30 # concentration of the solution of NaOH [%]
        volume_NaOH_sc1 = 1.1 # volume of NaOH used to clean the filtration machine [L]
        density_NaOH = 2.13 # density of sodium hydroxide [g/cm3] or [kg/L]
        ei36_conc_NaOH = 100 # pure substances in ecoinvent 3.6 [%]
        volume_NaOH_ei36_sc1 = concentration_NaOH_sc1 * volume_NaOH_sc1 / ei36_conc_NaOH # volume of NaOH [L]
        amount_NaOH_ei36_sc1 = volume_NaOH_ei36_sc1 * density_NaOH # amount of NaOH [kg]
        ## DATA MODELLED
        amount_NaOH_ei36 = permeate_DF_DW * amount_NaOH_ei36_sc1 / permeate_DF_DW_sc1 
        volume_NaOH = permeate_DF_DW * volume_NaOH_sc1 / permeate_DF_DW_sc1
        volume_NaOH_ei36 = permeate_DF_DW * volume_NaOH_ei36_sc1 / permeate_DF_DW_sc1
        NaOH_dict['volume_NaOH_30%'] = volume_NaOH
        NaOH_dict['volume_NaOH_100%'] = volume_NaOH_ei36
        NaOH_dict['amount_NaOH_100%'] = amount_NaOH_ei36
        NaOH_dict['volume_ultrapure_water'] = volume_NaOH - volume_NaOH_ei36 ## replaced volume_NaOH_ei36_sc1 by volume_NaOH_ei36
    else: 
        ## DATA COLLECTED
        permeate_DF_DW_sc1 = 4.1 # from the activity S2.A1.Extraction [kg DW-eq]
        concentration_NaOH_sc1 = 30 # concentration of the solution of NaOH [%]
        volume_NaOH_sc1 = 1.1 # volume of NaOH used to clean the filtration machine [L]
        density_NaOH = 2.13 # density of sodium hydroxide [g/cm3] or [kg/L]
        ei36_conc_NaOH = 100 # pure substances in ecoinvent 3.6 [%]
        volume_NaOH_ei36_sc1 = concentration_NaOH_sc1 * volume_NaOH_sc1 / ei36_conc_NaOH # volume of NaOH [L]
        amount_NaOH_ei36_sc1 = volume_NaOH_ei36_sc1 * density_NaOH # amount of NaOH [kg]
        ## DATA MODELLED
        amount_NaOH_ei36 = permeate_DF_DW * amount_NaOH_ei36_sc1 / permeate_DF_DW_sc1 
        volume_NaOH = permeate_DF_DW * volume_NaOH_sc1 / permeate_DF_DW_sc1
        volume_NaOH_ei36 = permeate_DF_DW * volume_NaOH_ei36_sc1 / permeate_DF_DW_sc1
        NaOH_dict['volume_NaOH_30%'] = volume_NaOH
        NaOH_dict['volume_NaOH_100%'] = volume_NaOH_ei36
        NaOH_dict['amount_NaOH_100%'] = amount_NaOH_ei36
        NaOH_dict['volume_ultrapure_water'] = volume_NaOH - volume_NaOH_ei36
    
    return NaOH_dict 


def WastewaterUltrafiltration (tech_period = '2', permeate_DF_DW = 4.1):
    
    if tech_period == '1':
        ## DATA COLLECTED
        permeate_DF_sc1 = 4.285044 
        wastewater_UF_sc1 = -1 * (800+169.40)/1000
        ## DATA MODELLED
        wastewater_UF = permeate_DF_DW * wastewater_UF_sc1 / permeate_DF_sc1
    else: 
        ## DATA COLLECTED
        permeate_DF_sc1 = 4.10 
        wastewater_UF_sc1 = -1 * (419.45+10.32)/1000
        ## DATA MODELLED
        wastewater_UF = permeate_DF_DW * wastewater_UF_sc1 / permeate_DF_sc1

    return wastewater_UF


def UltafiltrationDataDict (tech_period = '2', permeate_DF_DW = 4.1):
    
    data_dict = {}
    
    biomass_balance_dict_sc1, biomass_balance_dict = BiomassUltrafiltration(tech_period, permeate_DF_DW)
    
    ## BIOMASS INPUT
    data_dict['permeate_DF'] = {}
    data_dict['permeate_DF']['amount'] = permeate_DF_DW
    data_dict['permeate_DF']['unit'] = 'kg DW-eq'
    data_dict['permeate_DF']['type'] = 'fg_input'
    
    ## BIOMASS OUTPUTS
    data_dict['retentate_UF'] = {}
    data_dict['retentate_UF']['amount'] = biomass_balance_dict['retentate_UF']
    data_dict['retentate_UF']['unit'] = 'kg DW-eq'
    data_dict['retentate_UF']['type'] = 'ref_flow'
    data_dict['permeate_UF'] = {}
    data_dict['permeate_UF']['amount'] = biomass_balance_dict['permeate_UF']
    data_dict['permeate_UF']['unit'] = 'kg DW-eq'
    data_dict['permeate_UF']['type'] = 'coproduct'
    data_dict['losses'] = {}
    data_dict['losses']['amount'] = biomass_balance_dict['losses']
    data_dict['losses']['unit'] = 'kg DW-eq'
    data_dict['losses']['type'] = 'losses'
    
    ## ELECTRICITY
    data_dict['electricity_FR'] = {}
    data_dict['electricity_FR']['amount'] = ElectricityUltrafiltration(tech_period, permeate_DF_DW)
    data_dict['electricity_FR']['unit'] = 'kWh'
    data_dict['electricity_FR']['type'] = 'tech_input'
    
    ## TAP WATER
    data_dict['tap_water'] = {}
    data_dict['tap_water']['amount'] = WaterUltrafiltration(tech_period, permeate_DF_DW)
    data_dict['tap_water']['unit'] = 'L'
    data_dict['tap_water']['type'] = 'tech_input'    
        
    ## SODIUM HYDROXIDE
    NaOH_dict = SodiumHydroxideUltrafiltration(tech_period, permeate_DF_DW)
    data_dict['sodium_hydroxide'] = {}
    data_dict['sodium_hydroxide']['amount'] = NaOH_dict['amount_NaOH_100%']
    data_dict['sodium_hydroxide']['unit'] = 'kg'
    data_dict['sodium_hydroxide']['type'] = 'tech_input'
    
    ## ULTRAPURE WATER
    data_dict['ultrapure_water'] = {}
    data_dict['ultrapure_water']['amount'] = NaOH_dict['volume_ultrapure_water']
    data_dict['ultrapure_water']['unit'] = 'L'
    data_dict['ultrapure_water']['type'] = 'tech_input'
    
    ## WASTEWATER
    data_dict['wastewater'] = {}
    data_dict['wastewater']['amount'] = WastewaterUltrafiltration(tech_period, permeate_DF_DW)
    data_dict['wastewater']['unit'] = 'm3'
    data_dict['wastewater']['type'] = 'tech_output'
        
    return data_dict
