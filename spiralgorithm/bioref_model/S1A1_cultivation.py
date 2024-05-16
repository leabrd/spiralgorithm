# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 13:48:12 2022

@author: leabr
"""

def NutrientSupplyCultivation (tech_period, dry_spangles_DW):
    
    nutrient_supply_dict = {}
    time_period = 7 # the amount of nutrients used is divided per 7 days [day]
    
    if tech_period == '1': 
        ## DATA COLLECTED
        spangles_sc1 = 27.53 # amount of dry Spirulina spangles produced [kg]
        DM_spangles_sc1 = 96.8 # dry matter content of the spangles [%]
        spangles_DW_sc1 = spangles_sc1 * DM_spangles_sc1 / 100 # amount of dry spangles [kg DW-eq]
        sodium_bicarbonate_sc1 = 785.00 / time_period
        potassium_nitrate_sc1 = 135.53 / time_period
        TKPP_sc1 = 10.98 / time_period
        potassium_sulfate_sc1 = 6.28 / time_period
        magnesium_sulfate_sc1 = 3.14 / time_period
        chelated_iron_sc1 = 2.57 / time_period
        P2O5_content_TKPP = 0.43 # TKPP contains 43% of P2O5 (for ei36 proxy)
        ## DATA MODELLED 
        nutrient_supply_dict['sodium_bicarbonate'] = (dry_spangles_DW * sodium_bicarbonate_sc1 
                                                      / spangles_DW_sc1)
        nutrient_supply_dict['potassium_nitrate'] = (dry_spangles_DW * potassium_nitrate_sc1 
                                                     / spangles_DW_sc1)
        nutrient_supply_dict['TKPP'] = P2O5_content_TKPP*(dry_spangles_DW * TKPP_sc1 / 
                                        spangles_DW_sc1)
        nutrient_supply_dict['potassium_sulfate'] = (dry_spangles_DW * potassium_sulfate_sc1 
                                                     / spangles_DW_sc1)
        nutrient_supply_dict['magnesium_sulfate'] = (dry_spangles_DW * magnesium_sulfate_sc1 
                                                     / spangles_DW_sc1)
        nutrient_supply_dict['chelated_iron'] = (dry_spangles_DW * chelated_iron_sc1 
                                                 / spangles_DW_sc1)

    if tech_period == '2':
        ## DATA COLLECTED
        spangles_sc1 = 15.59 # amount of dry Spirulina spangles produced [kg]
        DM_spangles_sc1 = 94.99 # dry matter content of the spangles [%]
        spangles_DW_sc1 = spangles_sc1 * DM_spangles_sc1 / 100 # amount of dry spangles [kg DW-eq]
        sodium_bicarbonate_sc1 = 143.6 / time_period
        potassium_nitrate_sc1 = 164 / time_period
        ammonium_phosphate_sc1 = 1.84 / time_period
        magnesium_sulfate_sc1 = 2.44 / time_period
        chelated_iron_sc1 = 1.12 / time_period
        ## DATA MODELLED 
        nutrient_supply_dict['sodium_bicarbonate'] = (dry_spangles_DW * sodium_bicarbonate_sc1 
                                                      / spangles_DW_sc1)
        nutrient_supply_dict['potassium_nitrate'] = (dry_spangles_DW * potassium_nitrate_sc1 
                                                     / spangles_DW_sc1)
        nutrient_supply_dict['ammonium_phosphate'] = (dry_spangles_DW * ammonium_phosphate_sc1 
                                                      / spangles_DW_sc1)
        nutrient_supply_dict['magnesium_sulfate'] = (dry_spangles_DW * magnesium_sulfate_sc1 
                                                     / spangles_DW_sc1)
        nutrient_supply_dict['chelated_iron'] = (dry_spangles_DW * chelated_iron_sc1 
                                                 / spangles_DW_sc1)

    return nutrient_supply_dict


def WaterCultivation (broth_DW, tech_period, harvesting_efficiency, concentration):
    
    ''' 
    Only considers the water used to refill the ORPs. The water recirculated 
    does not appear in the bioreifnery/LCA model.
    '''
        
    from S1A2_filtration import BrothFiltered
    
    if tech_period == '1':
        
        ## DATA COLLECTED
        concentration_broth_sc1 = 1.07 # concentration of Spirulina in the broth [g/L]
        broth_sc1, broth_DW_sc1, water_recirculated_sc1 = BrothFiltered (tech_period, 
                                                                         harvesting_efficiency, 
                                                                         concentration)
        water_sc1 = 27720 # volume of water used to refill the OPRs (1 ORP/day) [L] 
        ## DATA MODELLED
        water = broth_DW * water_sc1 / broth_DW_sc1
        
    if tech_period == '2':
        ## DATA COLLECTED
        concentration_broth_sc1 = 0.64 # concentration of Spirulina in the broth [g/L]
        broth_sc1, broth_DW_sc1, water_recirculated_sc1 = BrothFiltered (tech_period, 
                                                                         harvesting_efficiency, 
                                                                         concentration)
        water_sc1 = 6612.80 # volume of water used to refill the OPRs (1 ORP/day) [L] 
        ## DATA MODELLED
        water = broth_DW * water_sc1 / broth_DW_sc1
   
    return water


def ElectricityPaddleWheels (running_time):
    '''
    Calculate the electricity used by the paddle wheels. Based on the data
    collected on site in 2019 in the frame of the SpiralG project.
    
    :param running_time: Running time of the control panel [h].
    :type running_time: float
    :param num_paddleWheels: Number of paddle wheel system in the greenhouse [-].
    :type num_paddleWheels: float
    :return: electricity used by the greenhouse fan [kWh].
    :rtype: float

    '''
    #running_time = 24 # running time of the paddle wheel [h]
    num_paddleWheels = 3 # number of paddle wheels
    intensity = 1.212 # average intensity of 3 paddlewheels over 3 days [A]
    power = intensity * (1.7320508*0.85*380) # instant power of the paddle wheel [W]
    elec_paddleWheels = (power/1000) * running_time * num_paddleWheels # electricity use [kWh]
    
    return elec_paddleWheels


def ElectricityGreenhouseFan (tech_period, running_time):
    '''
    Calculate the electricity used by the greenhouse fan. Based on the data
    collected on site in 2019 in the frame of the SpiralG project.
    
    :param running_time: Running time of the control panel [h].
    :type running_time: float
    :return: electricity used by the greenhouse fan [kWh].
    :rtype: float

    '''
    if tech_period == '1':
        #running_time = 12 # running time of the greenhouse fan [h]
        intensity = 3.32 # intensity of the fan [A]
        power = intensity * (0.9*234) # instant power of the greenhouse fan [W]
        elec_greenhouseFan = (power/1000) * running_time # electricity use [kWh]
    else: 
        elec_greenhouseFan = 0
        
    return elec_greenhouseFan


def ElectricityControlPanel (running_time):
    '''
    Calculate the electricity used by the control panel in the greenhouse. Based 
    on the data collected on site in 2019 in the frame of the SpiralG project.
    
    :param running_time: Running time of the control panel [h].
    :type running_time: float
    :return: electricity used by the control panel [kWh].
    :rtype: float

    '''
    #running_time = 5/60 # running time of the control panel [h]
    intensity = 1 # average intensity of the fan over 3 days [A]
    power = intensity * (0.9*234) # instant power of the paddle wheel [W]
    elec_controlPanel = (power/1000) * running_time # electricity use [kWh]
    
    return elec_controlPanel


def PlasticWasteCultivation (tech_period, spangles_DW):
    '''
    Calculate the amount of plastic waste generated from the use of sodium
    bicarbonate. Based on the data collected on site in 2019 in the frame of 
    the SpiralG project.
    
    :param nutrient_recipe_dict: Nutrient recipe including the name and amount
    of nutrient used for a week. 
    :type nutrient_recipe_dict: dict
    :return: Amount of plastic waste discarded to the general bin [kg].
    :rtype: float

    '''
    ## DATA COLLECTED
    sodium_bicarbonate_sc1 = 785.00 # total amount for 6 ORPs for 1 week
    plastic_waste_sc1 = -2.452
    ## DATA MODELLED
    nutrient_supply_dict = NutrientSupplyCultivation (tech_period, spangles_DW)
    sodium_bicarbonate = nutrient_supply_dict['sodium_bicarbonate']
    plastic_waste_IT = sodium_bicarbonate * plastic_waste_sc1 / sodium_bicarbonate_sc1
    
    return plastic_waste_IT


def CultivationDataDict (tech_period, harvesting_efficiency, concentration, 
                         dry_spangles_DW, broth_DW):
    '''
    Create the process-level aggregated dictionary with the data expressed for 
    the total amount of broth in the ORP: TO WHAT SHOULD THE VALUES BE DIVIDED???
    :param nutrient_recipe_dict: DESCRIPTION
    :type nutrient_recipe_dict: TYPE
    :param period: DESCRIPTION
    :type period: TYPE
    :return: DESCRIPTION
    :rtype: TYPE

    '''
    from S1A2_filtration import BrothFiltered
    
    data_dict = {}
    
    ## BIOMASS OUTPUT
    broth, broth_DW, water_recirculated = BrothFiltered (tech_period, 
                                                         harvesting_efficiency, 
                                                         concentration)
    data_dict['broth'] = {}
    data_dict['broth']['amount'] = broth_DW
    data_dict['broth']['unit'] = 'kg DW-eq'
    data_dict['broth']['type'] = 'ref_flow'
        
    ## NUTRIENT SUPPLY
    nutrient_supply_dict = NutrientSupplyCultivation (tech_period, dry_spangles_DW)
    for nutrient in nutrient_supply_dict.keys():
        data_dict[nutrient] = {}
        data_dict[nutrient]['amount'] = nutrient_supply_dict[nutrient]
        data_dict[nutrient]['unit'] = 'kg'
        data_dict[nutrient]['type'] = 'tech_input'
    
    ## ELECTRICITY
    elec_paddleWheels = ElectricityPaddleWheels (running_time =24)
    elec_greenhouseFan = ElectricityGreenhouseFan (tech_period, running_time = 12)
    elec_controlPanel = ElectricityControlPanel (running_time = 5/60)
    data_dict['electricity_IT'] = {}
    data_dict['electricity_IT']['amount'] = (elec_paddleWheels + elec_greenhouseFan 
                                             + elec_controlPanel)
    data_dict['electricity_IT']['unit'] = 'kWh'
    data_dict['electricity_IT']['type'] = 'tech_input'
    
    ## GROUND WATER
    data_dict['ground_water'] = {}
    data_dict['ground_water']['amount'] = WaterCultivation (broth_DW, tech_period, 
                                                            harvesting_efficiency, 
                                                            concentration)
    data_dict['ground_water']['unit'] = 'L'
    data_dict['ground_water']['type'] = 'tech_input'
    
    ## PASTIC WASTE
    data_dict['plastic_waste_IT'] = {}
    data_dict['plastic_waste_IT']['amount'] = PlasticWasteCultivation (tech_period, 
                                                                       dry_spangles_DW)
    data_dict['plastic_waste_IT']['unit'] = 'kg'
    data_dict['plastic_waste_IT']['type'] = 'tech_output'
    
    return data_dict
