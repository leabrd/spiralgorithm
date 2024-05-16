# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 11:52:38 2022

@author: leabr
"""

def BiomassFiltration (tech_period, supernatant_DW):
    
    '''The amount of filtrate obtained was not measured but calculated from the
    biomass balance.'''
    
    biomass_balance_dict_sc1 = {}
    biomass_balance_dict = {}
    
    if tech_period == '1':
        ## DATA COLLECTED
        supernatant_DW_sc1 = 35.4 # amount of supernatant calculated from mass balance [kg DW-eq]
        biomass_on_filters_sc1 = 5.87 # amount of biomass accumulated on the 42 filters [kg DW-eq]
        filtrate_DW_sc1 = supernatant_DW_sc1 - biomass_on_filters_sc1 # amount of filtrate [kg DW-eq]
        losses_sc1 = 0 # amount of supernatant lost during filtration [kg]
        DM_losses_sc1 = 1.80 # dry matter content of the supernatant [%] ## CHECK VALUE
        losses_DW_sc1 = losses_sc1 * DM_losses_sc1/100
        ## DATA MODELLED
        biomass_on_filters_DW = supernatant_DW * biomass_on_filters_sc1 / supernatant_DW_sc1
        losses_DW = supernatant_DW * losses_DW_sc1 / supernatant_DW_sc1
        filtrate_DW = supernatant_DW - biomass_on_filters_DW - losses_DW
        biomass_balance_dict_sc1['supernatant'] = {'wet_mass':'NaN', 
                                                   'DM_content':'NaN', 
                                                   'dry_mass':supernatant_DW_sc1}
        biomass_balance_dict_sc1['filtrate'] = {'wet_mass':'NaN', 
                                                'DM_content':'NaN', 
                                                'dry_mass':filtrate_DW_sc1}
        biomass_balance_dict_sc1['biomass_on_filters'] = {'wet_mass':'NaN', 
                                                          'DM_content':'NaN', 
                                                          'dry_mass':biomass_on_filters_sc1}
        biomass_balance_dict_sc1['losses'] = {'wet_mass':'', 
                                              'DM_content':'NaN', 
                                              'dry_mass':losses_DW_sc1}
        biomass_balance_dict['supernatant'] = supernatant_DW
        biomass_balance_dict['filtrate'] = filtrate_DW
        # biomass_balance_dict['biomass_on_filters'] = biomass_on_filters_DW
        biomass_balance_dict['losses'] = losses_DW + biomass_on_filters_DW
        
    if tech_period == '2':
        ## DATA COLLECTED
        supernatant_DW_sc1 = 7.71849 # amount of supernatant calculated from mass balance [kg DW-eq]
        biomass_on_filters_sc1 = 0.53 # amount of biomass accumulated on the 42 filters [kg DW-eq]
        losses_sc1 = 6.87 # amount of supernatant lost during filtration [kg]
        DM_losses_sc1 = 1.54 # dry matter content of the supernatant [%]
        losses_DW_sc1 = losses_sc1 * DM_losses_sc1/100
        filtrate_DW_sc1 = supernatant_DW_sc1 - biomass_on_filters_sc1 - losses_DW_sc1# amount of filtrate [kg DW-eq]
        ## DATA MODELLED
        biomass_on_filters_DW = supernatant_DW * biomass_on_filters_sc1 / supernatant_DW_sc1
        losses_DW = supernatant_DW * losses_DW_sc1 / supernatant_DW_sc1
        filtrate_DW = supernatant_DW - biomass_on_filters_DW - losses_DW
        biomass_balance_dict_sc1['supernatant'] = {'wet_mass':'NaN', 
                                                   'DM_content':'NaN', 
                                                   'dry_mass':supernatant_DW_sc1}
        biomass_balance_dict_sc1['filtrate'] = {'wet_mass':'NaN', 
                                                'DM_content':'NaN', 
                                                'dry_mass':filtrate_DW_sc1}
        biomass_balance_dict_sc1['biomass_on_filters'] = {'wet_mass':'NaN', 
                                                          'DM_content':'NaN', 
                                                          'dry_mass':biomass_on_filters_sc1}
        biomass_balance_dict_sc1['losses'] = {'wet_mass':'', 
                                              'DM_content':'NaN', 
                                              'dry_mass':losses_DW_sc1}
        biomass_balance_dict['supernatant'] = supernatant_DW
        biomass_balance_dict['filtrate'] = filtrate_DW
        # biomass_balance_dict['biomass_on_filters'] = biomass_on_filters_DW
        biomass_balance_dict['losses'] = losses_DW + biomass_on_filters_DW

    return biomass_balance_dict_sc1, biomass_balance_dict


def ElectricityFiltration (tech_period, supernatant_DW):
    '''Electricity was only used in 2021. In 2022 the pump used compressed
    air.'''
       
    if tech_period == '1':
        ## DATA COLLECTED
        supernatant_DW_sc1 = 35.4 # amount of supernatant calculated from mass balance [kg DW-eq]
        elec_filtration_sc1 = 2.15
        ## DATA MODELLED
        elec_filtration = supernatant_DW * elec_filtration_sc1 / supernatant_DW_sc1
    else: 
        elec_filtration = 0 # no electricity used for filtration in 2022 (compressed air pump instead)
    
    return elec_filtration


def CelluloseFilters (tech_period, supernatant_DW):
    '''
    Calculate the amount of cellulose filters needed to filtrate the supernatant
    obtained from centrifugation.
    '''
    if tech_period == '1': #  period set to 2019/2021 i.e. baseline scenario
        ## DATA COLLECTED
        supernatant_DW_sc1 = 35.4
        cellulose_sc1 = 80.27
        ## DATA MODELLED
        cellulose_filters = supernatant_DW * cellulose_sc1 / supernatant_DW_sc1  
        
    if tech_period == '2': 
        ## DATA COLLECTED
        supernatant_DW_sc1 = 7.71849 # amount of supernatant calculated from mass balance [kg DW-eq]       
        cellulose_sc1 = 9.53 # amount of cellulose filters used [kg DW-eq]
        ## DATA MODELLED
        cellulose_filters = supernatant_DW * cellulose_sc1 / supernatant_DW_sc1
           
    return cellulose_filters


def CardboardWaste (tech_period, supernatant_DW):
    '''
    Calculate the amount of cellulose filters discarded to carboard waste.
    In 2021 (period 1), all cellulose filters were discared to cardboard waste.
    In 2022 (period 2), trials were conducted to use the filters as feedstock 
    for AD but were still discarded to the sewer system.
    In 2030/50 (period 3) 100% of the cellulose filters were used as feedstock 
    for AD.

    '''
    if tech_period == '1': 
        ## DATA COLLECTED
        supernatant_DW_sc1 = 35.4
        cellulose_sc1 = 80.27
        ## DATA MODELLED
        cardboard_waste = -1 * supernatant_DW * cellulose_sc1 / supernatant_DW_sc1
    
    if tech_period == '2': 
        ## DATA COLLECTED
        supernatant_DW_sc1 = 7.71849 # amount of supernatant calculated from mass balance [kg DW-eq]       
        cellulose_sc1 = 9.53 # amount of cellulose filters used [kg DW-eq]
        ## DATA MODELLED
        cardboard_waste = -1 * supernatant_DW * cellulose_sc1 / supernatant_DW_sc1

    return cardboard_waste


def WaterFiltration (tech_period, supernatant_DW):
    
    if tech_period == '1': 
        ## DATA COLLECTED
        supernatant_DW_sc1 = 35.4 # amount of supernatant calculated from mass balance [kg DW-eq]               
        water_filtration_sc1 = 1082 # volume of water used for cleaning of added to the product [L]
        ## DATA MODELLED
        water_filtration = supernatant_DW * water_filtration_sc1 / supernatant_DW_sc1
    
    if tech_period == '2': 
        ## DATA COLLECTED 
        supernatant_DW_sc1 = 7.71849 # amount of supernatant calculated from mass balance [kg DW-eq]        
        water_filtration_sc1 = 329.56
        ## DATA MODELLED
        water_filtration = supernatant_DW * water_filtration_sc1 / supernatant_DW_sc1
    
    return water_filtration


def WastewaterFiltration (tech_period, supernatant_DW):
    
    if tech_period == '1': 
        ## DATA COLLECTED
        supernatant_DW_sc1 = 35.4 # amount of supernatant calculated from mass balance [kg DW-eq]               
        wastewater_filtration_sc1 = -1 * 890/1000 # volume of wastewater [m3]
        ## DATA MODELLED
        wastewater_filtration = supernatant_DW * wastewater_filtration_sc1 / supernatant_DW_sc1
    
    if tech_period == '2': 
        ## DATA COLLECTED 
        supernatant_DW_sc1 = 7.71849 # amount of supernatant calculated from mass balance [kg DW-eq]        
        wastewater_filtration_sc1 = -1 * 298/1000 # volume of wastewater [m3]
        ## DATA MODELLED
        wastewater_filtration = supernatant_DW * wastewater_filtration_sc1 / supernatant_DW_sc1
    
    return wastewater_filtration


def FiltrationDataDict (tech_period, supernatant_DW):
 
    data_dict = {}
    
    ## BIOMASS INPUT
    data_dict['supernatant'] = {}
    data_dict['supernatant']['amount'] = supernatant_DW
    data_dict['supernatant']['unit'] = 'kg DW-eq'
    data_dict['supernatant']['type'] = 'fg_input'
    
    ## BIOMASS OUTPUTS
    biomass_balance_dict_sc1, biomass_balance_dict = BiomassFiltration (tech_period, 
                                                                        supernatant_DW)
    data_dict['filtrate'] = {}
    data_dict['filtrate']['amount'] = biomass_balance_dict['filtrate']
    data_dict['filtrate']['unit'] = 'kg DW-eq'
    data_dict['filtrate']['type'] = 'ref_flow'
    data_dict['losses'] = {}
    data_dict['losses']['amount'] = biomass_balance_dict['losses']
    data_dict['losses']['unit'] = 'kg DW-eq'
    data_dict['losses']['type'] = 'losses'
    # data_dict['biomass_filters'] = {}
    # data_dict['biomass_filters']['amount'] = biomass_balance_dict['biomass_on_filters']
    # # data_dict['biomass_filters']['unit'] = 'kg DW-eq'
    # data_dict['biomass_filters']['type'] = 'biomass_filters'
    
    ## ELECTRICITY
    data_dict['electricity_FR'] = {}
    data_dict['electricity_FR']['amount'] = ElectricityFiltration (tech_period, 
                                                                   supernatant_DW)
    data_dict['electricity_FR']['unit'] = 'kWh'
    data_dict['electricity_FR']['type'] = 'tech_input'
    
    ## CELLULOSE
    data_dict['cellulose'] = {}
    data_dict['cellulose']['amount'] = CelluloseFilters (tech_period, 
                                                         supernatant_DW)
    data_dict['cellulose']['unit'] = 'kg'
    data_dict['cellulose']['type'] = 'tech_input'
    
    ## TAP WATER
    data_dict['tap_water'] = {}
    data_dict['tap_water']['amount'] = WaterFiltration (tech_period, 
                                                        supernatant_DW)
    data_dict['tap_water']['unit'] = 'L'
    data_dict['tap_water']['type'] = 'tech_input'
    
    ## CARDBOARD WASTE
    data_dict['paperboard_waste_FR'] = {}
    data_dict['paperboard_waste_FR']['amount'] = CardboardWaste (tech_period, 
                                                                 supernatant_DW)
    data_dict['paperboard_waste_FR']['unit'] = 'kg'
    data_dict['paperboard_waste_FR']['type'] = 'tech_output'    

    ## WASTEWATER
    data_dict['wastewater'] = {}
    data_dict['wastewater']['amount'] = WastewaterFiltration (tech_period, 
                                                              supernatant_DW)
    data_dict['wastewater']['unit'] = 'kg'
    data_dict['wastewater']['type'] = 'tech_output'  
    
    
    return data_dict