# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 12:47:39 2022

@author: leabr
"""

def BiomassUltrafiltration1 (tech_period = '2', filtrate_DW = 7.08):
    
    biomass_balance_dict_sc1 = {}
    biomass_balance_dict = {}
    
    '''In 2022, the dry matter content of the blue extract obtained after UF1
    was not measured since it was directly put into the UF2.'''
        
    if tech_period == '1':
        ## DATA COLLECTED
        filtrate_DW_sc1 = 29.53 # amount of filtrate [kg DW-eq]
        blue_extract_UF1_sc1 = 148 # amount of blue extract [kg]
        DM_blue_extract_UF1_sc1 = 5.84 # dry matter content of the blue extract [%]
        blue_extract_UF1_DW_sc1 = blue_extract_UF1_sc1 * DM_blue_extract_UF1_sc1/100 # amount of blue extract [kg DW-eq] 
        CDP_sc1 = 2118 # amount of CPD [kg]
        DM_CPD_sc1 = 0.8 # dry matter content of the CPD [%]
        CPD_DW_sc1 = CDP_sc1 * DM_CPD_sc1/100 # amount of CPD [kg DW-eq]
        losses_DW_sc1 = abs(filtrate_DW_sc1 - CPD_DW_sc1 - blue_extract_UF1_DW_sc1)
        biomass_balance_dict_sc1['filtrate'] = {'wet_mass':'NaN', 
                                                'DM_content':'NaN', 
                                                'dry_mass':filtrate_DW_sc1}
        biomass_balance_dict_sc1['CPD'] = {'wet_mass':CDP_sc1, 
                                           'DM_content':DM_CPD_sc1, 
                                           'dry_mass':CPD_DW_sc1}
        biomass_balance_dict_sc1['blue_extract_UF1'] = {'wet_mass':'NaN', 
                                                        'DM_content':'NaN', 
                                                        'dry_mass':blue_extract_UF1_DW_sc1}
        biomass_balance_dict_sc1['losses'] = {'wet_mass':'NaN', 
                                              'DM_content':'NaN', 
                                              'dry_mass':losses_DW_sc1}
        ## DATA MODELLED
        blue_extract_UF1 = filtrate_DW * blue_extract_UF1_DW_sc1 / filtrate_DW_sc1        
        CPD = filtrate_DW * CPD_DW_sc1 / filtrate_DW_sc1
        losses = abs(filtrate_DW - CPD - blue_extract_UF1)
        biomass_balance_dict['filtrate'] = filtrate_DW
        biomass_balance_dict['blue_extract_UF1'] = blue_extract_UF1
        biomass_balance_dict['CPD'] = CPD
        biomass_balance_dict['losses'] = losses
      

    if tech_period == '2':
        ## DATA COLLECTED
        filtrate_DW_sc1 = 7.082692 # amount of filtrate [kg DW-eq]
        blue_extract_UF1_sc1 = 146.5 # amount of blue extract [kg]
        CDP_sc1 = 1968 # amount of CPD [kg]
        DM_CPD_sc1 = 0.23 # dry matter content of the CPD [%]
        CPD_DW_sc1 = CDP_sc1 * DM_CPD_sc1/100 # amount of CPD [kg DW-eq]
        blue_extract_UF1_DW_sc1 = filtrate_DW_sc1 - CPD_DW_sc1
        losses_DW_sc1 = 0 # assumed no losses to calculate the amount of blue extract
        biomass_balance_dict_sc1['filtrate'] = {'wet_mass':'NaN', 
                                                'DM_content':'NaN', 
                                                'dry_mass':filtrate_DW_sc1}
        biomass_balance_dict_sc1['CPD'] = {'wet_mass':CDP_sc1, 
                                           'DM_content':DM_CPD_sc1, 
                                           'dry_mass':CPD_DW_sc1}
        biomass_balance_dict_sc1['blue_extract_UF1'] = {'wet_mass':'NaN', 
                                                        'DM_content':'NaN', 
                                                        'dry_mass':blue_extract_UF1_DW_sc1}
        biomass_balance_dict_sc1['losses'] = {'wet_mass':'NaN', 
                                              'DM_content':'NaN', 
                                              'dry_mass':losses_DW_sc1}
        ## DATA MODELLED
        blue_extract_UF1 = filtrate_DW * blue_extract_UF1_DW_sc1 / filtrate_DW_sc1        
        CPD = filtrate_DW * CPD_DW_sc1 / filtrate_DW_sc1
        losses = abs(filtrate_DW - CPD - blue_extract_UF1)
        biomass_balance_dict['filtrate'] = filtrate_DW
        biomass_balance_dict['blue_extract_UF1'] = blue_extract_UF1
        biomass_balance_dict['CPD'] = CPD
        biomass_balance_dict['losses'] = abs(losses)

    return biomass_balance_dict_sc1, biomass_balance_dict


def ElectricityUltrafiltration1 (tech_period, filtrate_DW):
    
    if tech_period == '1': 
        ## DATA COLLECTED
        filtrate_DW_sc1 = 29.53 # amount of supernatant filtrated [kg DW-eq]
        elec_UF1_sc1 = 144.28
        ## DATA MODELLED
        elec_UF1 = filtrate_DW * elec_UF1_sc1 / filtrate_DW_sc1
        
    else: 
        ## DATA COLLECTED
        filtrate_DW_sc1 = 7.082692 # amount of filtrate [kg DW-eq]
        elec_UF1_sc1 = 87.73
        ## DATA MODELLED
        elec_UF1 = filtrate_DW * elec_UF1_sc1 / filtrate_DW_sc1
    
    return elec_UF1


def WaterUltrafiltration1 (tech_period, filtrate_DW):
    
    if tech_period == '1': 
        ## DATA COLLECTED
        filtrate_DW_sc1 = 29.53 # amount of supernatant filtrated [kg DW-eq]
        water_UF1_sc1 = 3522.19
        ## DATA MODELLED
        water_UF1 = filtrate_DW * water_UF1_sc1 / filtrate_DW_sc1
        
    else: 
        ## DATA COLLECTED
        filtrate_DW_sc1 = 7.082692 # amount of filtrate [kg DW-eq]
        water_UF1_sc1 = 1387 + 1600 # volume water from cleaning + water balance [L]
        ## DATA MODELLED
        water_UF1 = filtrate_DW * water_UF1_sc1 / filtrate_DW_sc1
    
    return water_UF1


def WastewaterUltrafiltration1 (tech_period, filtrate_DW):
    
    if tech_period == '1': # period set to 2019/2021 i.e. baseline scenario
        ## DATA COLLECTED
        filtrate_DW_sc1 = 29.53 # amount of supernatant filtrated [kg DW-eq]
        wastewater_UF1_sc1 = -1 * (3159.19+33.98)/1000 # volume of wastewater [m3]
        ## DATA MODELLED
        wastewater_UF1 = filtrate_DW * wastewater_UF1_sc1 / filtrate_DW_sc1
        
    else: 
        ## DATA COLLECTED
        filtrate_DW_sc1 = 7.082692 # amount of filtrate [kg DW-eq]
        wastewater_UF1_sc1 = -1 * 1387/1000 # volume of wastewater [m3]
        ## DATA MODELLED
        wastewater_UF1 = filtrate_DW * wastewater_UF1_sc1 / filtrate_DW_sc1
    
    return wastewater_UF1


def SodiumHydroxide (tech_period, filtrate_DW):
    
    NaOH_dict = {}
        
    if tech_period == '1':
        ## DATA COLLECTED
        filtrate_DW_sc1 = 29.53 # amount of supernatant filtrated [kg DW-eq]
        volume_NaOH_sc1 = 9.9 # amount of NaOH in pearls (>99%) [kg]
        concentration_NaOH_sc1 = 30 # concentration of NaOH [%]
        density_NaOH = 1.36 # density of H2O2 at 35% and 20 °C [g/cm3] or [kg/L]
        ei36_conc_NaOH = 100 # pure substances in ecoinvent 3.6 [%]
        volume_NaOH_ei36_sc1 = concentration_NaOH_sc1 * volume_NaOH_sc1 / ei36_conc_NaOH # volume of NaOH [L]
        amount_NaOH_ei36_sc1 = volume_NaOH_ei36_sc1 * density_NaOH # amount of NaOH [kg]
        ## DATA MODELLED
        amount_NaOH_ei36 = filtrate_DW * amount_NaOH_ei36_sc1 / filtrate_DW_sc1
        volume_NaOH = filtrate_DW * volume_NaOH_sc1 / filtrate_DW_sc1
        volume_NaOH_ei36 = filtrate_DW * volume_NaOH_ei36_sc1 / filtrate_DW_sc1
        NaOH_dict['volume_NaOH_35%'] = volume_NaOH
        NaOH_dict['volume_NaOH_100%'] = volume_NaOH_ei36
        NaOH_dict['amount_NaOH_100%'] = amount_NaOH_ei36
        NaOH_dict['volume_ultrapure_water'] = volume_NaOH - volume_NaOH_ei36 
        
    else: 
        ## DATA COLLECTED
        filtrate_DW_sc1 = 7.082692 # amount of filtrate [kg DW-eq]
        volume_NaOH_sc1 = 9.9 # amount of NaOH in pearls (>99%) [kg]
        concentration_NaOH_sc1 = 30 # concentration of NaOH [%]
        density_NaOH = 1.36 # density of H2O2 at 35% and 20 °C [g/cm3] or [kg/L]
        ei36_conc_NaOH = 100 # pure substances in ecoinvent 3.6 [%]
        volume_NaOH_ei36_sc1 = concentration_NaOH_sc1 * volume_NaOH_sc1 / ei36_conc_NaOH # volume of NaOH [L]
        amount_NaOH_ei36_sc1 = volume_NaOH_ei36_sc1 * density_NaOH # amount of NaOH [kg]
        ## DATA MODELLED
        amount_NaOH_ei36 = filtrate_DW * amount_NaOH_ei36_sc1 / filtrate_DW_sc1
        volume_NaOH = filtrate_DW * volume_NaOH_sc1 / filtrate_DW_sc1
        volume_NaOH_ei36 = filtrate_DW * volume_NaOH_ei36_sc1 / filtrate_DW_sc1
        NaOH_dict['volume_NaOH_35%'] = volume_NaOH
        NaOH_dict['volume_NaOH_100%'] = volume_NaOH_ei36
        NaOH_dict['amount_NaOH_100%'] = amount_NaOH_ei36
        NaOH_dict['volume_ultrapure_water'] = volume_NaOH - volume_NaOH_ei36 
 
    return NaOH_dict


def HydrogenPeroxide (tech_period, filtrate_DW):
    
    H2O2_dict = {}
    
    if tech_period == '1':
        ## DATA COLLECTED
        filtrate_DW_sc1 = 29.53 # amount of supernatant filtrated [kg DW-eq]
        volume_H2O2_sc1 = 1.7 # amount of hydrogen peroxide [L]
        concentration_H2O2_sc1 = 4 # concentration of H2O2 [%]
        density_H2O2 = 1.04 # density of H2O2 at 4% and 20 °C [g/cm3] or [kg/L]
        ei36_conc_H2O2 = 100 # pure substances in ecoinvent 3.6 [%]
        volume_H2O2_ei36_sc1 = concentration_H2O2_sc1 * volume_H2O2_sc1 / ei36_conc_H2O2 # volume of NaOH [L]
        amount_H2O2_ei36_sc1 = volume_H2O2_ei36_sc1 * density_H2O2 # amount of NaOH [kg]
        ## DATA MODELLED
        amount_H2O2_ei36 = filtrate_DW * amount_H2O2_ei36_sc1 / filtrate_DW_sc1
        volume_H2O2 = filtrate_DW * volume_H2O2_sc1 / filtrate_DW_sc1
        volume_H2O2_ei36 = filtrate_DW * volume_H2O2_ei36_sc1 / filtrate_DW_sc1
        H2O2_dict['volume_H2O2_35%'] = volume_H2O2
        H2O2_dict['volume_H2O2_100%'] = volume_H2O2_ei36
        H2O2_dict['amount_H2O2_100%'] = amount_H2O2_ei36
        H2O2_dict['volume_ultrapure_water'] = volume_H2O2 - volume_H2O2_ei36 
    else: 
        ## DATA COLLECTED
        filtrate_DW_sc1 = 7.082692 # amount of filtrate [kg DW-eq]
        volume_H2O2_sc1 = 1.7 # amount of hydrogen peroxide [L]
        concentration_H2O2_sc1 = 4 # concentration of H2O2 [%]
        density_H2O2 = 1.04 # density of H2O2 at 4% and 20 °C [g/cm3] or [kg/L]
        ei36_conc_H2O2 = 100 # pure substances in ecoinvent 3.6 [%]
        volume_H2O2_ei36_sc1 = concentration_H2O2_sc1 * volume_H2O2_sc1 / ei36_conc_H2O2 # volume of NaOH [L]
        amount_H2O2_ei36_sc1 = volume_H2O2_ei36_sc1 * density_H2O2 # amount of NaOH [kg]
        ## DATA MODELLED
        amount_H2O2_ei36 = filtrate_DW * amount_H2O2_ei36_sc1 / filtrate_DW_sc1
        volume_H2O2 = filtrate_DW * volume_H2O2_sc1 / filtrate_DW_sc1
        volume_H2O2_ei36 = filtrate_DW * volume_H2O2_ei36_sc1 / filtrate_DW_sc1
        H2O2_dict['volume_H2O2_35%'] = volume_H2O2
        H2O2_dict['volume_H2O2_100%'] = volume_H2O2_ei36
        H2O2_dict['amount_H2O2_100%'] = amount_H2O2_ei36
        H2O2_dict['volume_ultrapure_water'] = volume_H2O2 - volume_H2O2_ei36 
       
        
    return H2O2_dict


def PhosphoricAcid (tech_period, filtrate_DW):
    
    H3PO4_dict = {}
    
    if tech_period == '1':
        ## DATA COLLECTED
        filtrate_DW_sc1 = 29.53 # amount of supernatant filtrated [kg DW-eq]
        volume_H3PO4_sc1 = 3.9 # amount of hydrogen peroxide [L]
        concentration_H3PO4_sc1 = 20 # concentration of H2O2 [%]
        density_H3PO4 = 1.11 # density of H2O2 at 35% and 20 °C [g/cm3] or [kg/L]
        ei36_conc_H3PO4 = 100 # pure substances in ecoinvent 3.6 [%]
        volume_H3PO4_ei36_sc1 = concentration_H3PO4_sc1 * volume_H3PO4_sc1 / ei36_conc_H3PO4 # volume of NaOH [L]
        amount_H3PO4_ei36_sc1 = volume_H3PO4_ei36_sc1 * density_H3PO4 # amount of NaOH [kg]
        ## DATA MODELLED
        amount_H3PO4_ei36 = filtrate_DW * amount_H3PO4_ei36_sc1 / filtrate_DW_sc1
        volume_H3PO4 = filtrate_DW * volume_H3PO4_sc1 / filtrate_DW_sc1
        volume_H3PO4_ei36 = filtrate_DW * volume_H3PO4_ei36_sc1 / filtrate_DW_sc1
        H3PO4_dict['volume_H3PO4_20%'] = volume_H3PO4
        H3PO4_dict['volume_H3PO4_100%'] = volume_H3PO4_ei36
        H3PO4_dict['amount_H3PO4_100%'] = amount_H3PO4_ei36
        H3PO4_dict['volume_ultrapure_water'] = volume_H3PO4 - volume_H3PO4_ei36 
    else: 
        ## DATA COLLECTED
        filtrate_DW_sc1 = 7.082692 # amount of filtrate [kg DW-eq]
        volume_H3PO4_sc1 = 2 # amount of hydrogen peroxide [L]
        concentration_H3PO4_sc1 = 75 # concentration of H2O2 [%]
        density_H3PO4 = 1.58 # density of H2O2 at 35% and 20 °C [g/cm3] or [kg/L]
        ei36_conc_H3PO4 = 100 # pure substances in ecoinvent 3.6 [%]
        volume_H3PO4_ei36_sc1 = concentration_H3PO4_sc1 * volume_H3PO4_sc1 / ei36_conc_H3PO4 # volume of NaOH [L]
        amount_H3PO4_ei36_sc1 = volume_H3PO4_ei36_sc1 * density_H3PO4 # amount of NaOH [kg]
        ## DATA MODELLED
        amount_H3PO4_ei36 = filtrate_DW * amount_H3PO4_ei36_sc1 / filtrate_DW_sc1
        volume_H3PO4 = filtrate_DW * volume_H3PO4_sc1 / filtrate_DW_sc1
        volume_H3PO4_ei36 = filtrate_DW * volume_H3PO4_ei36_sc1 / filtrate_DW_sc1
        H3PO4_dict['volume_H3PO4_75%'] = volume_H3PO4
        H3PO4_dict['volume_H3PO4_100%'] = volume_H3PO4_ei36
        H3PO4_dict['amount_H3PO4_100%'] = amount_H3PO4_ei36
        H3PO4_dict['volume_ultrapure_water'] = volume_H3PO4 - volume_H3PO4_ei36 
        
    return H3PO4_dict



def Ultrafiltration1DataDict (tech_period, filtrate_DW):
    
    data_dict = {}
    
    ## BIOMASS INPUT
    data_dict['filtrate'] = {}
    data_dict['filtrate']['amount'] = filtrate_DW
    data_dict['filtrate']['unit'] = 'kg DW-eq'
    data_dict['filtrate']['type'] = 'fg_input'
    
    ## BIOMASS OUTPUTS
    biomass_balance_dict_sc1, biomass_balance_dict = BiomassUltrafiltration1 (tech_period, 
                                                                              filtrate_DW)
    data_dict['blue_extract_UF1'] = {}
    data_dict['blue_extract_UF1']['amount'] = biomass_balance_dict['blue_extract_UF1']
    data_dict['blue_extract_UF1']['unit'] = 'kg DW-eq'
    data_dict['blue_extract_UF1']['type'] = 'ref_flow'
    data_dict['CPD'] = {}
    data_dict['CPD']['amount'] = biomass_balance_dict['CPD']
    data_dict['CPD']['unit'] = 'kg DW-eq'
    data_dict['CPD']['type'] = 'coproduct'
    data_dict['losses'] = {}
    data_dict['losses']['amount'] = biomass_balance_dict['losses']
    data_dict['losses']['unit'] = 'kg DW-eq'
    data_dict['losses']['type'] = 'losses'  
    
    ## ELECTRICITY
    data_dict['electricity_FR'] = {}
    data_dict['electricity_FR']['amount'] = ElectricityUltrafiltration1 (tech_period, 
                                                                         filtrate_DW)
    data_dict['electricity_FR']['unit'] = 'kWh'
    data_dict['electricity_FR']['type'] = 'tech_input'
    
    ## TAP WATER
    data_dict['tap_water'] = {}
    data_dict['tap_water']['amount'] = WaterUltrafiltration1 (tech_period, 
                                                              filtrate_DW)
    data_dict['tap_water']['unit'] = 'L'
    data_dict['tap_water']['type'] = 'tech_input'    
    
    ## SODIUM HYDROXIDE
    NaOH_dict = SodiumHydroxide (tech_period, filtrate_DW)
    data_dict['sodium_hydroxide'] = {}
    data_dict['sodium_hydroxide']['amount'] = NaOH_dict['amount_NaOH_100%']
    data_dict['sodium_hydroxide']['unit'] = 'kg'
    data_dict['sodium_hydroxide']['type'] = 'tech_input'    
    
    ## HYDROGEN PEROXIDE 
    H2O2_dict = HydrogenPeroxide (tech_period, filtrate_DW)
    data_dict['hydrogen_peroxide'] = {}
    data_dict['hydrogen_peroxide']['amount'] = H2O2_dict['amount_H2O2_100%']
    data_dict['hydrogen_peroxide']['unit'] = 'kg'
    data_dict['hydrogen_peroxide']['type'] = 'tech_input'    
    
    ## NITRIC ACID
    H3PO4_dict = PhosphoricAcid (tech_period, filtrate_DW)
    data_dict['nitric_acid'] = {}
    data_dict['nitric_acid']['amount'] = H3PO4_dict['amount_H3PO4_100%']
    data_dict['nitric_acid']['unit'] = 'kg'
    data_dict['nitric_acid']['type'] = 'tech_input'    
        
    ## ULTRAPURE WATER
    data_dict['ultrapure_water'] = {}
    data_dict['ultrapure_water']['amount'] = (NaOH_dict['volume_ultrapure_water'] 
                                              + H2O2_dict['volume_ultrapure_water'] 
                                              + H3PO4_dict['volume_ultrapure_water'])
    data_dict['ultrapure_water']['unit'] = 'kg'
    data_dict['ultrapure_water']['type'] = 'tech_input' 

    ## WASTEWATER
    data_dict['wastewater'] = {}
    data_dict['wastewater']['amount'] = WastewaterUltrafiltration1 (tech_period, 
                                                                    filtrate_DW)
    data_dict['wastewater']['unit'] = 'm3'
    data_dict['wastewater']['type'] = 'tech_output'

    return data_dict