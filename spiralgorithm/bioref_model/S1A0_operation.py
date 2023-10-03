# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 13:21:57 2022

@author: leabr
"""

def SodiumHypochlorite ():
    '''
    Amount of sodium hypochlorite used to clean the whole facility per day.
    The same data were used in 2019 and 2022 (i.e. does not depend in the 
    tech_period).
    '''
    
    ## DATA COLLECTED
    concentration_sc1 = 5 # concentration of the solution of sodium hypochorite [%] 
    volume_sodium_hypochlorite_sc1 = 150 / 1000 # volume of sodium hypochorite at 5% [L]
    ## DATA MODELLED
    concentration_ei36 = 100 # pure active substance in ei36 [%]
    volume_sodium_hypochlorite_ei36 = concentration_sc1 * volume_sodium_hypochlorite_sc1 / concentration_ei36 # equivalent volume of sodium hypochlorite at 100% [L]
    density_sodium_hypochlorite = 1.21
    amount_sodium_hypochlorite_ei36 = volume_sodium_hypochlorite_ei36 * density_sodium_hypochlorite
    sodium_hypochlorite = amount_sodium_hypochlorite_ei36
   
    return sodium_hypochlorite


def ElectricityFreezer (line):
    
    ''' Assumption: the freezer was used for the wet line only. There is a 
    78% difference in the electricity used by the freezer between the theoretical
    value indicated by the label and the value measured. This is due to the fact
    that the measured value does not account for the running time of the compressor 
    (i.e. in average, the compressor of a freezer is on 50% of the time). In addition, 
    the freezer could be an inverter one which uses less energy. At the end, the 
    theoretical electricity consumption was used in the LCA study.'''
        
    theoretical_electricity_use = 340 # amount of electricity used by the freezer according to the label [kWh/annum]
    intensity = (0.88 + 0.87  + 0.86) / 3 # average of the refregirator intensity over 3 days [A]
    instant_power = intensity * (0.9 * 234) / 1000 # average instant power between 3 values [kW]

    compressor_cycle = 50 # share of time during which the compressor is on [%]
    instant_power_with_compressor = instant_power * 50/100
    
    if line == 'dry':
        running_time = 0 # running time of the freezer [h]
        electricity = 0
        factor = 1
        
    if line == 'wet':
        running_time = 24 # running time of the freezer
        measured_electricity = instant_power * running_time # amount of electricity used [kWh]
        theoretical_electricity = theoretical_electricity_use / 365 # amount of electricity used per day [kWh/day]
        difference = (measured_electricity - theoretical_electricity) / measured_electricity * 100 # [%]
        factor = measured_electricity / theoretical_electricity # theoretical electricity used multiplied per the factor gives the measured value [-]
        electricity = theoretical_electricity
        
    return factor, electricity


def ElectricityRefregirator (factor):
    
    '''Assumption: the refregirator was used all year long, no matter the line
    or the period chosen. According to the values found with the freezer, it was 
    assumed that the electricity consumption of the refregirator could be 
    divided per the factor calculated for the freezer since there was no information
    on the theoretical electriicty consumption of the refregirator. By using the 
    same factor we ensure that the freezer consumed more than the refregirator 
    when both are used for 24h.'''
    
    intensity = (0.73 + 0.72  + 0.71) / 3 # average of the refregirator intensity over 3 days [A]
    instant_power = intensity * (0.9 * 234) / 1000 # average instant power between 3 values [kW]
    running_time = 24 # running time of the refregirator [h]
    electricity = running_time * instant_power / factor

    return electricity


def ElectricityBlastChiller (line, factor): ### NOT USED IN THE ASSESSMENT
    
    ''' Assumption: the blast chiller was only used in the wet line. Electricity used 
    by the blast chiller calculated from the measure of the instant power. The
    value of theoretical instant power seemed very high in comparison to the 
    measured vaue. Therefore, the measured value was used in the LCA.'''
    
    # dimensions
    lenght = 0.75 # length of the blast chiller [m]
    width = 0.75 # width of the blast chiller [m]
    height = 0.85 # height of the blast chiller [m]
    # electricity use
    measured_intensity = (0.03 + 0.56) / 2 # average intensity of the blast chiller
    measured_instant_power = measured_intensity * (0.9*234) / 1000 # instant power of the blast chiller [kW]
    theoretical_instant_power = 1.5 # theoretical instant power [kW]
    
    if line == 'dry':
        running_time = 0 # running time of the blast chiller [h]
        electricity = measured_instant_power * running_time
    
    if line == 'wet':
        running_time = 24 # running time of the blast chiller [h] ### VALUE TO CHANGE
        electricity = measured_instant_power * running_time / factor
    
    return electricity


def ElectricityAirConditioning (tech_period):
    
    '''The data regarding the AC are specific to summer and not representative 
    of the winter season. In summer, the AC is on from the morning to the evening.
Since in 2022, the start was ar 5:00AM, the running time is more important 
    in 2022 than 2019. The variability in the values measured between the 3 days
    shows that the intensity of the AC depends on the temperature set.'''
    
    from datetime import datetime 
    
    intensity_AC_office = (0.17 + 3.12 + 2.42) / 3 # average intensity of the AC in the office [A]
    instant_power_AC_office = intensity_AC_office * (0.9 * 234) / 1000 # instant power [kW]
    intensity_AC_lab = (8.59 + 8.5 + 8.55) / 3 # average intensity of the AC in the lab [A]
    instant_power_AC_lab = intensity_AC_lab * (0.9 * 234) / 1000 # instant power [kW]
   
    if tech_period == '1':
        start_time = '6:00:00' # AC started at 6:00AM
        end_time = '18:30:00' # AC stopped at 18:30PM
        t1 = datetime.strptime(start_time, "%H:%M:%S")
        t2 = datetime.strptime(end_time, "%H:%M:%S")
        delta = t2 - t1
        running_time = delta.total_seconds() / 60 / 60
        
    if tech_period == '2':
        start_time = '5:00:00' # AC started at 5:00AM
        end_time = '18:30:00' # AC stopped at 18:30PM
        t1 = datetime.strptime(start_time, "%H:%M:%S")
        t2 = datetime.strptime(end_time, "%H:%M:%S")
        delta = t2 - t1
        running_time = delta.total_seconds() / 60 / 60
   
    electricticty_AC_office = instant_power_AC_office * running_time
    electricity_AC_lab = instant_power_AC_lab * running_time
    total_electricity = electricticty_AC_office + electricity_AC_lab
        
    return total_electricity 


def ElectricityPlugs (tech_period):
    '''Assumption: the electricity used by the plugs is the same regarding the
    line. However the running time varies between periods 1 and 2.'''
    
    from datetime import datetime 
    
    intensity = (0.24 + 0.18 + 0.47) / 3 # average intensity of the plugs [A]
    instant_power = intensity * (0.9 * 234) /1000 # instant power of the plugs [kW]

    if tech_period == '1':
        start_time = '6:00:00' # AC started at 6:00AM
        end_time = '18:30:00' # AC stopped at 18:30PM
        t1 = datetime.strptime(start_time, "%H:%M:%S")
        t2 = datetime.strptime(end_time, "%H:%M:%S")
        delta = t2 - t1
        running_time = delta.total_seconds() / 60 / 60
        
    if tech_period == '2':
        start_time = '5:00:00' # AC started at 5:00AM
        end_time = '18:30:00' # AC stopped at 18:30PM
        t1 = datetime.strptime(start_time, "%H:%M:%S")
        t2 = datetime.strptime(end_time, "%H:%M:%S")
        delta = t2 - t1
        running_time = delta.total_seconds() / 60 / 60
   
    electricity = instant_power * running_time
    
    return electricity


def ElectricityLights (tech_period):
    '''Assumption: the electricity used by the lights is the same regarding the
    line. However the running time varies between periods 1 and 2. The electricity 
    consumption related to the lights is high but it was considered that they 
    were working the whole day. NO factor was appliedin the calculation. The 
    running time of the lights depends on the season.'''
    
    from datetime import datetime 
    
    intensity_office_lights = (1.2 + 1.2 + 0.7) / 3 # average intensity of the lights [A]
    instant_power_office_lights = intensity_office_lights * (0.9 * 234) /1000 # instant power of the lights [kW]
    intensity_lab_lights = (1.33 + 1.32 + 1.4) / 3 # average intensity of the lights [A]
    instant_power_lab_lights = intensity_lab_lights * (0.9 * 234) /1000 # instant power of the lights [kW]

    if tech_period == '1':
        start_time = '6:00:00' # AC started at 6:00AM
        end_time = '18:30:00' # AC stopped at 18:30PM
        t1 = datetime.strptime(start_time, "%H:%M:%S")
        t2 = datetime.strptime(end_time, "%H:%M:%S")
        delta = t2 - t1
        running_time = delta.total_seconds() / 60 / 60
        
    if tech_period == '2':
        start_time = '5:00:00' # AC started at 5:00AM
        end_time = '18:30:00' # AC stopped at 18:30PM
        t1 = datetime.strptime(start_time, "%H:%M:%S")
        t2 = datetime.strptime(end_time, "%H:%M:%S")
        delta = t2 - t1
        running_time = delta.total_seconds() / 60 / 60
   
    electricity_office_lights = instant_power_office_lights * running_time
    electricity_lab_lights = instant_power_lab_lights * running_time
    total_electricity = electricity_office_lights + electricity_lab_lights

    return total_electricity


def ElectricityOperation (tech_period, line):
    
    factor, electricity_freezer = ElectricityFreezer (line)
    electricity_refregirator = ElectricityRefregirator (factor)
    electricity_blast_chiller = ElectricityBlastChiller (line, factor)
    electricity_AC = ElectricityAirConditioning (tech_period)
    electricity_plugs = ElectricityPlugs (tech_period)
    electricity_lights = ElectricityLights (tech_period)
    
    electricity = electricity_blast_chiller + electricity_freezer + electricity_refregirator + electricity_AC + electricity_plugs + electricity_lights

    return electricity


def WaterOperation (volume_ORP, ORP_number, working_days):
    
    '''Assumption: the volumes of water used to clean and run the facility
    (e.g. bathroom) were measured in 2019 only. In 2019, the water used to clean
    the equipment was considered in S1A0Operation while in 2022, the volumes 
    used to clean each specific equipment was associated with each corresponding 
    acticity. The water used to initially fill in the ORPs was calculated from
    the theoretical volume of the ORPs.'''
 
    # water used in the facility
    water_cleaning = 1.18 * 1000 # volume of water used to clean the facility [L/day]
    water_facility = 2.28 * 1000 # volume of water used in the facility (e.g. bathroom) [L/day]
    # water used to initially fill in the ORPs
    water_ORPs = (volume_ORP * ORP_number / 1000) / working_days # water used to initially fill in the ORPs [L/day]
    total_water = water_cleaning + water_facility + water_ORPs
    
    return total_water


def SolidWastes (tech_period):
    ''' 
    The amounts of solid waste were measured for a week (either 5 or 6 days). The 
    values were then divided per the number of days during which the wastes were
    collected to obtain a daily value. The biomass waste was only measured in 2019
    and was limited. It was added to the general waste.
    '''
    
    if tech_period == '1':
        ## DATA COLLECTED
        plastic_waste = -0.22 # amount of plastic waste generated per day [kg]
        paperboard_waste = -0.08 # amount of paperboard waste generated per day [kg]
        general_waste = -0.19 -0.03 # amount of general waste generated per day [kg]    
    
    else: 
        ## DATA COLLECTED
        plastic_waste = -0.866 # amount of plastic waste generated per day [kg]
        paperboard_waste = -2.93 # amount of paperboard waste generated per day [kg]
        general_waste = -0.308 # amount of general waste generated per day [kg]      
     
    return plastic_waste, paperboard_waste, general_waste



def OperationDataDict (tech_period, line, volume_ORP, ORP_number, working_days):
    
    data_dict = {}
    
    ## ELECTRICITY
    data_dict['electricity_IT'] = {}
    data_dict['electricity_IT']['amount'] = ElectricityOperation (tech_period, line)
    data_dict['electricity_IT']['unit'] = 'kWh'
    data_dict['electricity_IT']['type'] = 'tech_input'
    
    ## WATER
    total_water = WaterOperation (volume_ORP, ORP_number, working_days)
    data_dict['ground_water'] = {}
    data_dict['ground_water']['amount'] = total_water
    data_dict['ground_water']['unit'] = 'kg'
    data_dict['ground_water']['type'] = 'tech_input'   
        
    plastic_waste, paperboard_waste, general_waste = SolidWastes (tech_period)
    ## PLASTIC WASTE
    data_dict['plastic_waste_IT'] = {}
    data_dict['plastic_waste_IT']['amount'] = plastic_waste
    data_dict['plastic_waste_IT']['unit'] = 'kg'
    data_dict['plastic_waste_IT']['type'] = 'tech_output'    
    
    ## PAPERBOARD WASTE
    data_dict['paperboard_waste_IT'] = {}
    data_dict['paperboard_waste_IT']['amount'] = paperboard_waste
    data_dict['paperboard_waste_IT']['unit'] = 'kg'
    data_dict['paperboard_waste_IT']['type'] = 'tech_output'       
    
    ## GENERAL WASTE
    data_dict['general_waste_IT'] = {}
    data_dict['general_waste_IT']['amount'] = general_waste
    data_dict['general_waste_IT']['unit'] = 'kg'
    data_dict['general_waste_IT']['type'] = 'tech_output'  
    
    ## SODIUM HYPOCHLORITE
    data_dict['sodium_hypochlorite'] = {}
    data_dict['sodium_hypochlorite']['amount'] = SodiumHypochlorite ()
    data_dict['sodium_hypochlorite']['unit'] = 'kg'
    data_dict['sodium_hypochlorite']['type'] = 'tech_input'  
 
    return data_dict