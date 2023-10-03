# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 13:57:10 2022

@author: leabr
"""

def BiomassExtraction (tech_period = '2', CPA_DW = 12.03):
    
    biomass_balance_dict_sc1 = {} # store details of the baseline scenario
    biomass_balance_dict = {} # store details of the scenario modelled
    
    if tech_period == '1':
        ## DATA COLLECTED
        CPA_sc1 = 201.02 # amount of CPA received thawed [kg]
        DM_CPA_sc1 = 6.43 # dry matter content of the CPA [%]
        CPA_DW_sc1 = CPA_sc1 * DM_CPA_sc1 / 100 # amount of CPA treated [kg DW-eq]
        biomass_balance_dict_sc1['CPA'] = {'wet_mass': CPA_sc1, 
                                           'DM_content': DM_CPA_sc1, 
                                           'dry_mass': CPA_DW_sc1}
        sample_amount_sc1 = 0.2 # amount of one sample was set to 200g [kg]    
        DM_sample0_sc1 = 6.43 # dry matter content of the sample0 [% DW]
        DM_sample1_sc1 = 8.38 # dry matter content of the sample1 [% DW]
        DM_sample2_sc1 = 8.71 # dry matter content of the sample2 [% DW]
        DM_sample3_sc1 = 8.81 # dry matter content of the sample3 [% DW]
        average_DM_sample = (DM_sample0_sc1 + DM_sample1_sc1 + DM_sample2_sc1 + DM_sample3_sc1) / 4
        sample0_DW_sc1 = sample_amount_sc1 * DM_sample0_sc1 /100 # amount of sample0 [kg DW-eq]
        sample1_DW_sc1 = sample_amount_sc1 * DM_sample1_sc1 /100 # amount of sample1 [kg DW-eq]
        sample2_DW_sc1 = sample_amount_sc1 * DM_sample2_sc1 /100 # amount of sample2 [kg DW-eq]
        sample3_DW_sc1 = sample_amount_sc1 * DM_sample3_sc1 /100 # amount of sample3 [kg DW-eq]
        total_sample_DW_sc1 = sample0_DW_sc1 + sample1_DW_sc1 + sample2_DW_sc1 + sample3_DW_sc1
        biomass_balance_dict_sc1['samples'] = {'wet_mass': sample_amount_sc1*5, 
                                               'DM_content': average_DM_sample, 
                                               'dry_mass': total_sample_DW_sc1}
        ## CONSERVATION OF MASS OUTPUT = INPUT - SAMPLES TO CALCULATE AMOUNT OF HYDROLYSATE
        process_losses = 0 # assumption implied by the conservation of mass
        hydrolysate_DW_sc1 = CPA_DW_sc1 - total_sample_DW_sc1 - process_losses # amount of hydrolysate [kg DW-eq]
        DM_hydrolysate_sc1 = DM_sample3_sc1 # dry matter content of the hydrolysate is the same as the last sample [% DW]
        hydrolysate_sc1 = hydrolysate_DW_sc1 / (DM_hydrolysate_sc1/100)
        biomass_balance_dict_sc1['hydrolysate'] = {'wet_mass': hydrolysate_sc1, 
                                                   'DM_content': DM_hydrolysate_sc1, 
                                                   'dry_mass': hydrolysate_DW_sc1}
        ## DATA MODELLED
        hydrolysate_DW = CPA_DW * hydrolysate_DW_sc1 / CPA_DW_sc1
        biomass_balance_dict['CPA'] = CPA_DW
        biomass_balance_dict['hydrolysate'] = hydrolysate_DW
        biomass_balance_dict['losses'] = CPA_DW - hydrolysate_DW # samples considered as biomass losses in the balance
        ## CHECK THE MASS BALANCE
        if biomass_balance_dict['CPA'] != (biomass_balance_dict['hydrolysate'] + 
                                           biomass_balance_dict['losses']):
            raise Exception('The activity S3.A1.Extraction is unbalanced!')
            
    if tech_period == '2':
        ## DATA COLLECTED
        CPA_sc1 = 192.24 # amount of CPA received thawed [kg]
        DM_CPA_sc1 = 6.26 # dry matter content of the CPA [%]
        CPA_DW_sc1 = CPA_sc1 * DM_CPA_sc1 / 100 # amount of CPA treated [kg DW-eq]
        biomass_balance_dict_sc1['CPA'] = {'wet_mass': CPA_sc1, 
                                           'DM_content': DM_CPA_sc1, 
                                           'dry_mass': CPA_DW_sc1}
        sample_amount_sc1 = 0.2 # amount of one sample was set to 200g [kg]    
        DM_sample0_sc1 = 6.26 # dry matter content of the sample0 [% DW]
        DM_sample1_sc1 = 7.12 # dry matter content of the sample1 [% DW]
        DM_sample2_sc1 = 7.35 # dry matter content of the sample2 [% DW]
        DM_sample3_sc1 = 7.34 # dry matter content of the sample3 [% DW]
        DM_sample4_sc1 = 7.58 # dry matter content of the sample4 [% DW]
        average_DM_sample = (DM_sample0_sc1 + DM_sample1_sc1 + DM_sample2_sc1 + DM_sample3_sc1 + DM_sample4_sc1) / 5
        sample0_DW_sc1 = sample_amount_sc1 * DM_sample0_sc1 /100 # amount of sample0 [kg DW-eq]
        sample1_DW_sc1 = sample_amount_sc1 * DM_sample1_sc1 /100 # amount of sample1 [kg DW-eq]
        sample2_DW_sc1 = sample_amount_sc1 * DM_sample2_sc1 /100 # amount of sample2 [kg DW-eq]
        sample3_DW_sc1 = sample_amount_sc1 * DM_sample3_sc1 /100 # amount of sample3 [kg DW-eq]
        sample4_DW_sc1 = sample_amount_sc1 * DM_sample4_sc1 /100 # amount of sample4 [kg DW-eq]
        total_sample_DW_sc1 = sample0_DW_sc1 + sample1_DW_sc1 + sample2_DW_sc1 + sample3_DW_sc1 + sample4_DW_sc1 
        biomass_balance_dict_sc1['samples'] = {'wet_mass': sample_amount_sc1*5, 
                                               'DM_content': average_DM_sample, 
                                               'dry_mass': total_sample_DW_sc1}
        ## CONSERVATION OF MASS OUTPUT = INPUT - SAMPLES TO CALCULATE AMOUNT OF HYDROLYSATE
        process_losses = 0 # assumption implied by the conservation of mass
        hydrolysate_DW_sc1 = CPA_DW_sc1 - total_sample_DW_sc1 - process_losses # amount of hydrolysate [kg DW-eq]
        DM_hydrolysate_sc1 = DM_sample4_sc1 # dry matter content of the hydrolysate is the same as the last sample [% DW]
        hydrolysate_sc1 = hydrolysate_DW_sc1 / (DM_hydrolysate_sc1/100)
        biomass_balance_dict_sc1['hydrolysate'] = {'wet_mass': hydrolysate_sc1, 
                                                   'DM_content': DM_hydrolysate_sc1, 
                                                   'dry_mass': hydrolysate_DW_sc1}
       ## DATA MODELLED
        hydrolysate_DW = CPA_DW * hydrolysate_DW_sc1 / CPA_DW_sc1
        biomass_balance_dict['CPA'] = CPA_DW
        biomass_balance_dict['hydrolysate'] = hydrolysate_DW
        biomass_balance_dict['losses'] = CPA_DW - hydrolysate_DW # samples considered as biomass losses in the balance
        ## CHECK THE MASS BALANCE
        if biomass_balance_dict['CPA'] != (biomass_balance_dict['hydrolysate'] 
                                           + biomass_balance_dict['losses']):
            raise Exception('The activity S3.A1.Extraction is unbalanced!')
      
    return biomass_balance_dict_sc1, biomass_balance_dict


def SulfuricAcidExtraction (tech_period = '2', CPA_DW = 12.03):
    
    H2SO4_dict = {}
    
    if tech_period == '1': 
        ## DATA COLLECTED
        CPA_sc1 = 201.02 # amount of CPA received thawed [kg]
        DM_CPA_sc1 = 6.43 # dry matter content of the CPA [%]
        CPA_DW_sc1 = CPA_sc1 * DM_CPA_sc1 / 100 # amount of CPA treated [kg DW-eq]
        concentration_H2SO4_sc1 = 96 # concentration of the solution used [%]
        initial_concentration_H2SO4 = 18 # solution at 18M used [M]
        diluted_concentration_H2SO4 = 6 # diluted solution at 6M [M]
        volume_H2SO4_sc1 = 1.57
        ### CALCULATION OF THE VOLUME OF WATER NEEDED
        volume_water_sc1 = (initial_concentration_H2SO4 * volume_H2SO4_sc1 / diluted_concentration_H2SO4 
                            - volume_H2SO4_sc1)
        ## ADAPTION TO ECOINVENT 3.6 DATASET
        density_H2SO4 = 1.83 # density of H2SO4 (96%) at 20°C [g/cm3] = [kg/L]
        ei36_conc_H2SO4 = 100 # pure substances in ecoinvent 3.6 [%]
        # calculation of the equivalent volume of H2SO4 at 100% (V2 = C1 x V1 / C2)
        volume_H2SO4_ei36_sc1 = concentration_H2SO4_sc1 * volume_H2SO4_sc1 / ei36_conc_H2SO4 # volume of H2SO2 [L]
        amount_H2SO4_ei36_sc1 = volume_H2SO4_ei36_sc1 * density_H2SO4 # amount of H2SO4 [kg]
        volume_water_ei36_sc1 = volume_water_sc1 # volume of water used for dilution [L]
        ## DATA MODELLED
        amount_H2SO4_ei36 = CPA_DW * amount_H2SO4_ei36_sc1 / CPA_DW_sc1 
        volume_H2SO4 = CPA_DW * volume_H2SO4_sc1 / CPA_DW_sc1 
        volume_water = CPA_DW * volume_water_ei36_sc1 / CPA_DW_sc1
        H2SO4_dict['amount_H2SO4_100%'] = amount_H2SO4_ei36
        H2SO4_dict['volume_H2SO4_96%'] = volume_H2SO4
        H2SO4_dict['volume_ultrapure_water'] = abs(volume_H2SO4 - volume_H2SO4_ei36_sc1)
        H2SO4_dict['volume_water'] = volume_water
    
    if tech_period == '2':
        ## DATA COLLECTED
        CPA_sc1 = 192.24 # amount of CPA received thawed [kg]
        DM_CPA_sc1 = 6.26 # dry matter content of the CPA [%]
        CPA_DW_sc1 = CPA_sc1 * DM_CPA_sc1 / 100 # amount of CPA treated [kg DW-eq]
        concentration_H2SO4_sc1 = 96 # concentration of the solution used [%]
        initial_concentration_H2SO4 = 18 # solution at 18M used [M]
        diluted_concentration_H2SO4 = 6 # diluted solution at 6M [M]
        volume_H2SO4_sc1 = 1.5
        ### CALCULATION OF THE VOLUME OF WATER NEEDED TO REACH THE 6M CONCENTRATION
        volume_water_sc1 = (initial_concentration_H2SO4 * volume_H2SO4_sc1 / diluted_concentration_H2SO4 
                            - volume_H2SO4_sc1)
        ## ADAPTION TO ECOINVENT 3.6 DATASET
        density_H2SO4 = 1.83 # density of H2SO4 (96%) at 20°C [g/cm3] = [kg/L]
        ei36_conc_H2SO4 = 100 # pure substances in ecoinvent 3.6 [%]
        # calculation of the equivalent volume of H2SO4 at 100% (V2 = C1 x V1 / C2)
        volume_H2SO4_ei36_sc1 = concentration_H2SO4_sc1 * volume_H2SO4_sc1 / ei36_conc_H2SO4 # volume of H2SO2 [L]
        amount_H2SO4_ei36_sc1 = volume_H2SO4_ei36_sc1 * density_H2SO4 # amount of H2SO4 [kg]
        volume_water_ei36_sc1 = volume_water_sc1 # volume of water used for dilution [L]
        ## DATA MODELLED
        amount_H2SO4_ei36 = CPA_DW * amount_H2SO4_ei36_sc1 / CPA_DW_sc1 
        volume_H2SO4 = CPA_DW * volume_H2SO4_sc1 / CPA_DW_sc1 
        volume_water = CPA_DW * volume_water_ei36_sc1 / CPA_DW_sc1
        H2SO4_dict['amount_H2SO4_100%'] = amount_H2SO4_ei36
        H2SO4_dict['volume_H2SO4_96%'] = volume_H2SO4
        H2SO4_dict['volume_ultrapure_water'] = abs(volume_H2SO4 - volume_H2SO4_ei36_sc1)
        H2SO4_dict['volume_water'] = volume_water

    return H2SO4_dict


def WaterExtraction (tech_period = '2', CPA_DW = 12.03):
    
    if tech_period == '1': 
        ## DATA COLLECTED
        water_process_sc1 = 627.71 # total volume of water used in the process [L]
        CPA_sc1 = 201.02 # amount of CPA received thawed [kg]
        DM_CPA_sc1 = 6.43 # dry matter content of the CPA [%]
        CPA_DW_sc1 = CPA_sc1 * DM_CPA_sc1 / 100 # amount of CPA treated [kg DW-eq] 
        water_CPA_sc1 = CPA_sc1 - CPA_DW_sc1      
        ## WATER BALANCE TO CALCULATE WATER LOSSES PER EVAPORATION
        H2SO4_dict = SulfuricAcidExtraction (tech_period, CPA_DW)
        water_H2SO4 = H2SO4_dict['volume_water'] # volume of water used to prepare the solution of H2SO4 [L]
        biomass_balance_dict_sc1, biomass_balance_dict = BiomassExtraction (tech_period, CPA_DW)
        water_samples = (biomass_balance_dict_sc1['samples']['wet_mass'] 
                         - biomass_balance_dict_sc1['samples']['dry_mass'])
        water_hydrolysate_sc1 = (biomass_balance_dict_sc1['hydrolysate']['wet_mass'] 
                                 - biomass_balance_dict_sc1['hydrolysate']['dry_mass']) # volume of water in the hydrolysate [L]
        water_evaporation_sc1 = (water_CPA_sc1 + water_H2SO4) - (water_hydrolysate_sc1 + water_samples)
        ## DATA MODELLED
        water_process = CPA_DW * water_process_sc1 / CPA_DW_sc1
        water_evaporation = CPA_DW * water_evaporation_sc1 / CPA_DW_sc1
    
    if tech_period == '2':
        ## DATA COLLECTED
        water_process_sc1 = 575.94 # total volume of water used in the process [L]
        CPA_sc1 = 192.24 # amount of CPA received thawed [kg]
        DM_CPA_sc1 = 6.26 # dry matter content of the CPA [%]
        CPA_DW_sc1 = CPA_sc1 * DM_CPA_sc1 / 100 # amount of CPA treated [kg DW-eq] 
        water_CPA_sc1 = CPA_sc1 - CPA_DW_sc1      
        ## WATER BALANCE TO CALCULATE WATER LOSSES PER EVAPORATION
        H2SO4_dict = SulfuricAcidExtraction (tech_period, CPA_DW)
        water_H2SO4 = H2SO4_dict['volume_water'] # volume of water used to prepare the solution of H2SO4 [L]
        biomass_balance_dict_sc1, biomass_balance_dict = BiomassExtraction (tech_period, CPA_DW)
        water_samples = (biomass_balance_dict_sc1['samples']['wet_mass'] 
                         - biomass_balance_dict_sc1['samples']['dry_mass'])
        water_hydrolysate_sc1 = (biomass_balance_dict_sc1['hydrolysate']['wet_mass'] 
                                 - biomass_balance_dict_sc1['hydrolysate']['dry_mass']) # volume of water in the hydrolysate [L]
        water_evaporation_sc1 = (water_CPA_sc1 + water_H2SO4) - (water_hydrolysate_sc1 + water_samples)
        ## DATA MODELLED
        water_process = CPA_DW * water_process_sc1 / CPA_DW_sc1
        water_evaporation = CPA_DW * water_evaporation_sc1 / CPA_DW_sc1
        
    return water_process, water_evaporation


def ElectricityExtraction (tech_period = '2', CPA_DW = 12.03):
    
    if tech_period == '1': # period set to 2019/2021 i.e. baseline scenario
        ## DATA COLLECTED
        elec_sc1 = 197.26
        CPA_sc1 = 201.02 # amount of CPA received thawed [kg]
        DM_CPA_sc1 = 6.43 # dry matter content of the CPA [%]
        CPA_DW_sc1 = CPA_sc1 * DM_CPA_sc1 / 100 # amount of CPA treated [kg DW-eq]  
        ## DATA MODELLED
        elec = CPA_DW * elec_sc1 / CPA_DW_sc1  
    
    if tech_period == '2': 
        ## DATA COLLECTED
        elec_sc1 = 37.72 # amont of electricity directly measured [kWh]
        CPA_sc1 = 192.24 # amount of CPA received thawed [kg]
        DM_CPA_sc1 = 6.26 # dry matter content of the CPA [%]
        CPA_DW_sc1 = CPA_sc1 * DM_CPA_sc1 / 100 # amount of CPA treated [kg DW-eq]  
        ## DATA MODELLED
        elec = CPA_DW * elec_sc1 / CPA_DW_sc1        
    
    return elec


def WastewaterExtraction (tech_period = '2', CPA_DW = 12.03):
    
    if tech_period == '1': # period set to 2019/2021 i.e. baseline scenario
        ## DATA COLLECTED
        wastewater_sc1 = -1 * 624.58 / 1000 # wastewater discarded to sewer system [m3]
        CPA_sc1 = 201.02 # amount of CPA received thawed [kg]
        DM_CPA_sc1 = 6.43 # dry matter content of the CPA [%]
        CPA_DW_sc1 = CPA_sc1 * DM_CPA_sc1 / 100 # amount of CPA treated [kg DW-eq]     
        ## DATA MODELLED
        wastewater = CPA_DW * wastewater_sc1 / CPA_DW_sc1        
    
    if tech_period == '2':
        ## DATA COLLECTED
        wastewater_sc1 = -1 * 572.94 / 1000 # wastewater discarded to sewer system [m3]
        CPA_sc1 = 192.24 # amount of CPA received thawed [kg]
        DM_CPA_sc1 = 6.26 # dry matter content of the CPA [%]
        CPA_DW_sc1 = CPA_sc1 * DM_CPA_sc1 / 100 # amount of CPA treated [kg DW-eq]      
        ## DATA MODELLED
        wastewater = CPA_DW * wastewater_sc1 / CPA_DW_sc1        
    
    return wastewater


def ExtractionDataDict (tech_period = '2', CPA_DW = 12.03):
    
    data_dict = {}
    
    biomass_balance_dict_sc1, biomass_balance_dict = BiomassExtraction(tech_period, CPA_DW)
    
    ## BIOMASS INPUT
    data_dict['CPA'] = {}
    data_dict['CPA']['amount'] = biomass_balance_dict['CPA']
    data_dict['CPA']['unit'] = 'kg DW-eq'
    data_dict['CPA']['type'] = 'fg_input'
    
    ## BIOMASS OUTPUTS
    data_dict['hydrolysate'] = {}
    data_dict['hydrolysate']['amount'] = biomass_balance_dict['hydrolysate']
    data_dict['hydrolysate']['unit'] = 'kg DW-eq'
    data_dict['hydrolysate']['type'] = 'ref_flow'
    data_dict['losses'] = {}
    data_dict['losses']['amount'] = biomass_balance_dict['losses']
    data_dict['losses']['unit'] = 'kg DW-eq'
    data_dict['losses']['type'] = 'losses'   
    
    ## ELECTRICITY
    data_dict['electricity_FR'] = {}
    data_dict['electricity_FR']['amount'] = ElectricityExtraction (tech_period, CPA_DW)
    data_dict['electricity_FR']['unit'] = 'kWh'
    data_dict['electricity_FR']['type'] = 'tech_input'
    
    ## TAP WATER
    water_process, water_evaporation = WaterExtraction (tech_period, CPA_DW)
    data_dict['tap_water'] = {}
    data_dict['tap_water']['amount'] = water_process
    data_dict['tap_water']['unit'] = 'L'
    data_dict['tap_water']['type'] = 'tech_input'    
    
    ## SULFURIC ACID
    H2SO4_dict = SulfuricAcidExtraction (tech_period, CPA_DW)
    data_dict['sulfuric_acid'] = {}
    data_dict['sulfuric_acid']['amount'] = H2SO4_dict['amount_H2SO4_100%']
    data_dict['sulfuric_acid']['unit'] = 'kg'
    data_dict['sulfuric_acid']['type'] = 'tech_input'
    
    ## ULTRAPURE WATER
    data_dict['ultrapure_water'] = {}
    data_dict['ultrapure_water']['amount'] = H2SO4_dict['volume_ultrapure_water']
    data_dict['ultrapure_water']['unit'] = 'L'
    data_dict['ultrapure_water']['type'] = 'tech_input'
    
    ## WASTEWATER
    data_dict['wastewater'] = {}
    data_dict['wastewater']['amount'] = WastewaterExtraction(tech_period, CPA_DW)
    data_dict['wastewater']['unit'] = 'm3'
    data_dict['wastewater']['type'] = 'tech_output'
    
    ## WATER VAPOR
    data_dict['water_vapor'] = {}
    data_dict['water_vapor']['amount'] = water_evaporation
    data_dict['water_vapor']['unit'] = 'L'
    data_dict['water_vapor']['type'] = 'emission'
      
    return data_dict
