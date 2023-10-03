# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 14:11:27 2022

@author: leabr
"""

def BiomassDiafiltration (tech_period = '2', hydrolysate_DW = 11.96):
    
    '''Assumption: the samples were taken before hte measurement of the biomass
    outputs. There are considered as losses in the biomass balance.'''
        
    biomass_balance_dict_sc1 = {}
    biomass_balance_dict = {}
        
    if tech_period == '1':
        ## DATA COLLECTED
        hydrolysate_DW_sc1 = 12.860926 # from the activity S2.A1.Extraction [kg DW-eq]
        DM_hydrolysate_sc1 = 8.81 # dry matter content of the hydrolysate [%]
        hydrolysate_sc1 = hydrolysate_DW_sc1 / (DM_hydrolysate_sc1 / 100) # amount of hydrolysate [kg]
        water_hydrolysate_sc1 = hydrolysate_sc1 - hydrolysate_DW_sc1
        biomass_balance_dict_sc1['hydrolysate'] = {'wet_mass': hydrolysate_sc1, 
                                                   'DM_content': DM_hydrolysate_sc1, 
                                                   'dry_mass': hydrolysate_DW_sc1}   
        amount_retentate_sc1 = 45.74 # amount of retentate from DF (> 0.2 μm) [kg]
        DM_retentate_sc1 = 9.97 # dry matter content of the rententate [%]
        retentate_DW_sc1 = amount_retentate_sc1 * DM_retentate_sc1 / 100
        water_retentate_sc1 = amount_retentate_sc1 - retentate_DW_sc1
        biomass_balance_dict_sc1['retentate_DF'] = {'wet_mass': amount_retentate_sc1, 
                                                    'DM_content': DM_retentate_sc1, 
                                                    'dry_mass': retentate_DW_sc1}   
        amount_permeate_sc1 = 386.04 # amount of retentate from DF (> 0.2 μm) [kg]
        DM_permeate_sc1 = 1.11 # dry matter content of the permeate [%]
        permeate_DW_sc1 = amount_permeate_sc1 * DM_permeate_sc1 / 100
        water_permeate_sc1 = amount_permeate_sc1 - permeate_DW_sc1
        biomass_balance_dict_sc1['permeate_DF'] = {'wet_mass': amount_permeate_sc1, 
                                                   'DM_content': DM_permeate_sc1, 
                                                   'dry_mass': permeate_DW_sc1}   
        sample_amount_sc1 = 0.2 # amount of one sample was set to 200g [kg]    
        DM_sample_retentate_sc1 = DM_retentate_sc1 # dry matter content of the sample0 [% DW]
        sample_retentate_DW_sc1 = sample_amount_sc1 * DM_sample_retentate_sc1 / 100 # amount of sample [kg DW-eq]
        DM_sample_permeate_sc1 = DM_permeate_sc1
        sample_permeate_DW_sc1 = sample_amount_sc1 * DM_sample_permeate_sc1 / 100
        total_sample_DW_sc1 = sample_retentate_DW_sc1 + sample_permeate_DW_sc1
        DM_average_sample_sc1 = (DM_sample_retentate_sc1 + DM_sample_permeate_sc1) / 2
        water_samples_sc1 = (sample_amount_sc1*2) - total_sample_DW_sc1
        biomass_balance_dict_sc1['samples'] = {'wet_mass': sample_amount_sc1*2, 
                                               'DM_content': DM_average_sample_sc1, 
                                               'dry_mass': total_sample_DW_sc1}
        ## BIOMASS BALANCE TO ESTIMATE THE LOSSES
        losses_DW_sc1 = hydrolysate_DW_sc1 - (retentate_DW_sc1 + permeate_DW_sc1 + total_sample_DW_sc1) # samples are already counted
        DM_losses = (DM_retentate_sc1 + DM_permeate_sc1) / 2 # average of the dry matter content of the outputs
        losses_sc1 = losses_DW_sc1 / (DM_losses/100)
        water_losses_sc1 = losses_sc1 - losses_DW_sc1
        biomass_balance_dict_sc1['losses'] = {'wet_mass': losses_sc1, 
                                              'DM_content': DM_losses, 
                                              'dry_mass': losses_DW_sc1}   
        water_added_to_product_sc1 = (water_retentate_sc1 + water_permeate_sc1 + water_samples_sc1 + water_losses_sc1) - water_hydrolysate_sc1        
        ## DATA MODELLED
        retentate_DW = hydrolysate_DW * retentate_DW_sc1 / hydrolysate_DW_sc1        
        permeate_DW = hydrolysate_DW * permeate_DW_sc1 / hydrolysate_DW_sc1 
        losses_DW = hydrolysate_DW - retentate_DW - permeate_DW
        water_added_to_product = hydrolysate_DW * water_added_to_product_sc1 / hydrolysate_DW_sc1
        biomass_balance_dict['hydrolysate'] = hydrolysate_DW
        biomass_balance_dict['retentate_DF'] = retentate_DW
        biomass_balance_dict['permeate_DF'] = permeate_DW
        biomass_balance_dict['losses'] = losses_DW
        
    if tech_period == '2':
        ## DATA COLLECTED
        hydrolysate_DW_sc1 = 11.96 # from the activity S2.A1.Extraction [kg DW-eq]
        DM_hydrolysate_sc1 = 7.58 # dry matter content of the hydrolysate [%]
        hydrolysate_sc1 = hydrolysate_DW_sc1 / (DM_hydrolysate_sc1 / 100) # amount of hydrolysate [kg]
        water_hydrolysate_sc1 = hydrolysate_sc1 - hydrolysate_DW_sc1
        biomass_balance_dict_sc1['hydrolysate'] = {'wet_mass': hydrolysate_sc1, 
                                                   'DM_content': DM_hydrolysate_sc1, 
                                                   'dry_mass': hydrolysate_DW_sc1}   
        
        volume_permeate_sc1 = 370 # volume of permeate from DF (< 0.2 μm) [L]
        losses_permeate_sc1 = 4.62 # volume of permeate losses [L]
        DM_permeate_sc1 = 1.54 # dry matter content of the permeate [%]
        permeate_DW_sc1 = volume_permeate_sc1 * DM_permeate_sc1 / 100 
        water_permeate_sc1 = volume_permeate_sc1 - permeate_DW_sc1
        biomass_balance_dict_sc1['permeate'] = {'wet_mass': volume_permeate_sc1, 
                                                'DM_content': DM_permeate_sc1, 
                                                'dry_mass': permeate_DW_sc1}   
        
        losses_permeate_DW_sc1 = losses_permeate_sc1 * DM_permeate_sc1 / 100 
        losses_permeate_sc1 = losses_permeate_DW_sc1 / (DM_permeate_sc1/100)
        water_losses_sc1 = losses_permeate_sc1 - losses_permeate_DW_sc1
        biomass_balance_dict_sc1['losses'] = {'wet_mass': losses_permeate_sc1, 
                                              'DM_content': DM_permeate_sc1, 
                                              'dry_mass': losses_permeate_DW_sc1} 
        
        sample_amount_sc1 = 0.2 # amount of one sample was set to 200g [kg]    
        DM_sample_retentate_sc1 = 10.09 # dry matter content of the sample0 [% DW]
        sample_retentate_DW_sc1 = sample_amount_sc1 * DM_sample_retentate_sc1 / 100 # amount of sample [kg DW-eq]
        DM_sample_permeate_sc1 = 1.54
        sample_permeate_DW_sc1 = sample_amount_sc1 * DM_sample_permeate_sc1 / 100
        total_sample_DW_sc1 = sample_retentate_DW_sc1 + sample_permeate_DW_sc1
        DM_average_sample_sc1 = (DM_sample_retentate_sc1 + DM_sample_permeate_sc1) / 2
        water_samples_sc1 = (sample_amount_sc1*2) - total_sample_DW_sc1
        biomass_balance_dict_sc1['samples'] = {'wet_mass': sample_amount_sc1*2, 
                                                'DM_content': DM_average_sample_sc1, 
                                                'dry_mass': total_sample_DW_sc1}
        
        retentate_DW_sc1 = hydrolysate_DW_sc1 - permeate_DW_sc1 - losses_permeate_DW_sc1 - total_sample_DW_sc1
        DM_retentate_sc1 = 10.09 # dry matter content of the rententate [%]
        retentate_sc1 = retentate_DW_sc1 / (DM_retentate_sc1 / 100)
        water_retentate_sc1 = retentate_sc1 - retentate_DW_sc1
        biomass_balance_dict_sc1['retentate'] = {'wet_mass': retentate_sc1, 
                                                 'DM_content': DM_retentate_sc1, 
                                                 'dry_mass': retentate_DW_sc1}    
        
        water_added_to_product_sc1 = (water_permeate_sc1 + water_retentate_sc1 + water_samples_sc1 + water_losses_sc1) - water_hydrolysate_sc1 
    
        ## DATA MODELLED
        retentate_DW = hydrolysate_DW * retentate_DW_sc1 / hydrolysate_DW_sc1        
        permeate_DW = hydrolysate_DW * permeate_DW_sc1 / hydrolysate_DW_sc1 
        losses_permeate_DW = hydrolysate_DW * losses_permeate_DW_sc1 / hydrolysate_DW_sc1
        water_added_to_product = hydrolysate_DW * water_added_to_product_sc1 / hydrolysate_DW_sc1
        biomass_balance_dict['hydrolysate'] = hydrolysate_DW
        biomass_balance_dict['retentate_DF'] = retentate_DW
        biomass_balance_dict['permeate_DF'] = permeate_DW
        biomass_balance_dict['losses'] = losses_permeate_DW
        ## UNBALANCED => CALCULATE AMOUNT OF RETENTATE FROM MASS BALANCE
        if biomass_balance_dict['hydrolysate'] != (biomass_balance_dict['retentate_DF'] 
                                                   + biomass_balance_dict['permeate_DF'] 
                                                   + biomass_balance_dict['losses'] ):
            retentate_DW = hydrolysate_DW - (permeate_DW + losses_permeate_DW)
            biomass_balance_dict['retentate_DF'] = retentate_DW
        
    return biomass_balance_dict_sc1, biomass_balance_dict, water_added_to_product


def ElectricityDiafiltration (tech_period = '2', hydrolysate_DW = 11.96):
    
    if tech_period == '1':
        ## DATA COLLECTED
        hydrolysate_DW_sc1 = 12.860926 # from the activity S2.A1.Extraction [kg DW-eq]
        elec_sc1 = 8.942
        ## DATA MODELLED
        elec = hydrolysate_DW * elec_sc1 / hydrolysate_DW_sc1
    else: 
        ## DATA COLLECTED
        hydrolysate_DW_sc1 = 11.962924 # from the activity S2.A1.Extraction [kg DW-eq]
        elec_sc1 = 18.63
        ## DATA MODELLED
        elec = hydrolysate_DW * elec_sc1 / hydrolysate_DW_sc1
   
    return elec


def WaterDiafiltration (tech_period = '2', hydrolysate_DW = 11.96):
    
    biomass_balance_dict_sc1, biomass_balance_dict, water_added_to_product = BiomassDiafiltration(tech_period, hydrolysate_DW)
    
    if tech_period == '1':
        ## DATA COLLECTED
        hydrolysate_DW_sc1 = 12.86 # from the activity S2.A1.Extraction [kg DW-eq]
        water_process_sc1 = 676.88
        total_water_sc1 = water_process_sc1 + water_added_to_product
        ## DATA MODELLED
        water = hydrolysate_DW * total_water_sc1 / hydrolysate_DW_sc1

    if tech_period == '2':
        ## DATA COLLECTED
        hydrolysate_DW_sc1 = 11.96 # from the activity S2.A1.Extraction [kg DW-eq]
        water_process_sc1 = 664.16
        total_water_sc1 = water_process_sc1 + water_added_to_product
        ## DATA MODELLED
        water = hydrolysate_DW * total_water_sc1 / hydrolysate_DW_sc1
   
    return water


def SodiumHydroxideDiafiltration (tech_period = '2', hydrolysate_DW = 11.96):
    
    NaOH_dict = {}
    
    if tech_period == '1':
        ## DATA COLLECTED
        hydrolysate_DW_sc1 = 12.860926 # from the activity S2.A1.Extraction [kg DW-eq]
        concentration_NaOH_sc1 = 30 # concentration of the solution of NaOH [%]
        volume_NaOH_sc1 = 1.5 # volume of NaOH used to clean the filtration machine [L]
        density_NaOH = 2.13 # density of sodium hydroxide [g/cm3] or [kg/L]
        ei36_conc_NaOH = 100 # pure substances in ecoinvent 3.6 [%]
        volume_NaOH_ei36_sc1 = concentration_NaOH_sc1 * volume_NaOH_sc1 / ei36_conc_NaOH # volume of NaOH [L]
        amount_NaOH_ei36_sc1 = volume_NaOH_ei36_sc1 * density_NaOH # amount of NaOH [kg]
        ## DATA MODELLED
        amount_NaOH_ei36 = hydrolysate_DW * amount_NaOH_ei36_sc1 / hydrolysate_DW_sc1 
        volume_NaOH = hydrolysate_DW * volume_NaOH_sc1 / hydrolysate_DW_sc1
        volume_NaOH_ei36 = hydrolysate_DW * volume_NaOH_ei36_sc1 / hydrolysate_DW_sc1
        NaOH_dict['volume_NaOH_30%'] = volume_NaOH
        NaOH_dict['volume_NaOH_100%'] = volume_NaOH_ei36
        NaOH_dict['amount_NaOH_100%'] = amount_NaOH_ei36
        NaOH_dict['volume_ultrapure_water'] = volume_NaOH - volume_NaOH_ei36_sc1
    else: 
        ## DATA COLLECTED
        hydrolysate_DW_sc1 = 11.962924 # from the activity S2.A1.Extraction [kg DW-eq]
        concentration_NaOH_sc1 = 30 # concentration of the solution of NaOH [%]
        volume_NaOH_sc1 = 1.5 # volume of NaOH used to clean the filtration machine [L]
        density_NaOH = 2.13 # density of sodium hydroxide [g/cm3] or [kg/L]
        ei36_conc_NaOH = 100 # pure substances in ecoinvent 3.6 [%]
        volume_NaOH_ei36_sc1 = concentration_NaOH_sc1 * volume_NaOH_sc1 / ei36_conc_NaOH # volume of NaOH [L]
        amount_NaOH_ei36_sc1 = volume_NaOH_ei36_sc1 * density_NaOH # amount of NaOH [kg]
        ## DATA MODELLED
        amount_NaOH_ei36 = hydrolysate_DW * amount_NaOH_ei36_sc1 / hydrolysate_DW_sc1 
        volume_NaOH = hydrolysate_DW * volume_NaOH_sc1 / hydrolysate_DW_sc1
        volume_NaOH_ei36 = hydrolysate_DW * volume_NaOH_ei36_sc1 / hydrolysate_DW_sc1
        NaOH_dict['volume_NaOH_30%'] = volume_NaOH
        NaOH_dict['volume_NaOH_100%'] = volume_NaOH_ei36
        NaOH_dict['amount_NaOH_100%'] = amount_NaOH_ei36
        NaOH_dict['volume_ultrapure_water'] = volume_NaOH - volume_NaOH_ei36_sc1
    
    return NaOH_dict 

    
def WastewaterDiafiltration (tech_period = '2', hydrolysate_DW = 11.96):
    
    if tech_period == '1':
        ## DATA COLLECTED
        hydrolysate_DW_sc1 = 12.860926 # from the activity S2.A1.Extraction [kg DW-eq]
        #biomass_balance_dict_sc1, biomass_balance_dict = BiomassDiafiltration (hydrolysate_DW, period)
        #losses_permeate = biomass_balance_dict['losses'] # the losses of permeate are discarded to the sewer system
        wastewater_sc1 = -1 * 676.88 / 1000 # does not account for losses as wastewater
        ## DATA MODELLED
        wastewater = hydrolysate_DW * wastewater_sc1 / hydrolysate_DW_sc1
    else: 
        ## DATA COLLECTED
        hydrolysate_DW_sc1 = 11.962924 # from the activity S2.A1.Extraction [kg DW-eq]
        #biomass_balance_dict_sc1, biomass_balance_dict = BiomassDiafiltration (hydrolysate_DW, period)
        #losses_permeate = biomass_balance_dict['losses'] # the losses of permeate are discarded to the sewer system
        #water = WaterDiafiltration (hydrolysate_DW, period)
        wastewater_sc1 = -1 * (4.62 + 664.16) / 1000 # wastewater to sewer system [m3] # the losses are treated in WWTP
        ## DATA MODELLED
        wastewater = hydrolysate_DW * wastewater_sc1 / hydrolysate_DW_sc1
    
    return wastewater
  
  
def DiafiltrationDataDict (tech_period = '2', hydrolysate_DW = 11.96):
    
    data_dict = {}
    
    biomass_balance_dict_sc1, biomass_balance_dict, water_added_to_product = BiomassDiafiltration(tech_period, hydrolysate_DW)
    
    ## BIOMASS INPUT
    data_dict['hydrolysate'] = {}
    data_dict['hydrolysate']['amount'] = hydrolysate_DW
    data_dict['hydrolysate']['unit'] = 'kg DW-eq'
    data_dict['hydrolysate']['type'] = 'fg_input'
    
    ## BIOMASS OUTPUTS
    data_dict['permeate_DF'] = {}
    data_dict['permeate_DF']['amount'] = biomass_balance_dict['permeate_DF']
    data_dict['permeate_DF']['unit'] = 'kg DW-eq'
    data_dict['permeate_DF']['type'] = 'ref_flow'
    data_dict['retentate_DF'] = {}
    data_dict['retentate_DF']['amount'] = biomass_balance_dict['retentate_DF']
    data_dict['retentate_DF']['unit'] = 'kg DW-eq'
    data_dict['retentate_DF']['type'] = 'coproduct'
    data_dict['losses'] = {}
    data_dict['losses']['amount'] = biomass_balance_dict['losses']
    data_dict['losses']['unit'] = 'kg DW-eq'
    data_dict['losses']['type'] = 'losses' # treated as wastewater??
    
    ## ELECTRICITY
    data_dict['electricity_FR'] = {}
    data_dict['electricity_FR']['amount'] = ElectricityDiafiltration(tech_period, hydrolysate_DW)
    data_dict['electricity_FR']['unit'] = 'kWh'
    data_dict['electricity_FR']['type'] = 'tech_input' 
    
    ## TAP WATER
    data_dict['tap_water'] = {}
    data_dict['tap_water']['amount'] = WaterDiafiltration(tech_period, hydrolysate_DW)
    data_dict['tap_water']['unit'] = 'kWh'
    data_dict['tap_water']['type'] = 'tech_input' 
    
    ## SODIUM HYDROXIDE
    NaOH_dict = SodiumHydroxideDiafiltration(tech_period, hydrolysate_DW)
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
    data_dict['wastewater']['amount'] = WastewaterDiafiltration(tech_period, hydrolysate_DW)
    data_dict['wastewater']['unit'] = 'm3'
    data_dict['wastewater']['type'] = 'tech_output'     
     
    return data_dict
