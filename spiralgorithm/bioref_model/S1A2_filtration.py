# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 12:36:39 2022

@author: leabr
"""

# def PlotConcentrationBroth(concentration):
    
#     import numpy as np
#     import pandas as pd
#     import matplotlib.pyplot as plt
#     from scipy import stats

    
#     tech_period = '2'
#     harvesting_efficiency = 75.36
    
#     data = []
    
#     for concentration in np.arange(0,5,0.1):
#         broth, broth_DW, water_recirculated = BrothFiltered (tech_period, harvesting_efficiency, concentration)
#         data.append([concentration,broth])
     
#     df = pd.DataFrame(data, columns = ['concentration (g/L)', 'broth filtered (kg DW-eq/day)'])
#     x = df['broth filtered (kg DW-eq/day)']
#     y = df['concentration (g/L)']
    
#     slope, intercept, r, p, std_err = stats.linregress(x, y)
        
#     def myfunc(x):
#         return slope * x + intercept
    
#     mymodel = list(map(myfunc, x))

#     plt.scatter(x, y)
#     plt.plot(x, mymodel)
#     plt.show()
    

#     return broth



def BrothFiltered (tech_period, harvesting_efficiency, concentration):
    ''' 
    Calculation of the amount of broth filtered from the amount of slurry produced.
    Values depends on the concentration at harvesting and the harvesting efficicency.
    The value obtained are also used in the activity S1A1Cultivation.
    '''
    if tech_period == '1':
        ## DATA COLLECTED
        slurry_sc1 = 257.71 # amount of slurry [kg]
        DM_slurry_sc1 = 14.75 # dry matter content of the slurry[% DM]
        slurry_DW_sc1 = slurry_sc1 * DM_slurry_sc1 /100 # amount of slurry [kg DW-eq]
        water_in_slurry_sc1 = slurry_sc1 - slurry_DW_sc1 # volume of water in the slurry [L]
        concentration_sc1 = 1.07 # concentration of Spirulina in broth [g/L]
        broth_sc1 = (100 / harvesting_efficiency) * (slurry_DW_sc1 / concentration_sc1) # volume of broth [m3]
        broth_DW_sc1 = concentration_sc1 * broth_sc1
        water_in_broth_sc1 = broth_sc1*1000 - broth_DW_sc1
        water_recirculated_sc1 = water_in_broth_sc1 - water_in_slurry_sc1 # volume of water recirculated to the ORPs [L]
        ## DATA MODELLED
        broth = concentration * broth_sc1 / concentration_sc1 # volume of broth filtered [m3]
        broth_DW = concentration * broth # amount of broth [kg DW-eq]
        water_recirculated = broth * water_recirculated_sc1 / broth_sc1        
    else: 
        ## DATA COLLECTED
        slurry_sc1 = 198.99 # amount of slurry [kg]
        DM_slurry_sc1 = 10.39 # dry matter content of the slurry [% DM]
        slurry_DW_sc1 = slurry_sc1 * DM_slurry_sc1/100 # amount of slurry [kg DW-eq]
        water_in_slurry_sc1 = slurry_sc1 - slurry_DW_sc1 # volume of water in the slurry [L]
        concentration_sc1 = 0.64 # concentration of Spirulina in broth [g/L]
        broth_sc1 = (100 / harvesting_efficiency) * (slurry_DW_sc1 / concentration_sc1) # volume of broth [m3]
        broth_DW_sc1 = concentration_sc1 * broth_sc1        
        water_in_broth_sc1 = broth_sc1*1000 - broth_DW_sc1
        water_recirculated_sc1 = water_in_broth_sc1 - water_in_slurry_sc1 # volume of water recirculated to the ORPs [L]
        ## DATA MODELLED
        broth = concentration * broth_sc1 / concentration_sc1 # volume of broth filtered [m3]
        broth_DW = concentration * broth # amount of broth [kg DW-eq]
        water_recirculated = broth * water_recirculated_sc1 / broth_sc1

    return broth, broth_DW, water_recirculated



def BiomassFiltration (tech_period, harvesting_efficiency, concentration):
    
    biomass_balance_dict_sc1 ={}
    biomass_balance_dict = {}
    
    if tech_period == '1':
        concentration_sc1 = 1.07
        ## DATA COLLECTED
        broth_sc1, broth_DW_sc1, water_recirculated_sc1 = BrothFiltered (tech_period, 
                                                                         harvesting_efficiency, 
                                                                         concentration_sc1)
        slurry_sc1 = 257.71 # amount of slurry [kg]
        DM_slurry_sc1 = 14.75 # dry matter content of the slurry[% DM]
        slurry_DW_sc1 = slurry_sc1 * DM_slurry_sc1 /100
        biomass_balance_dict_sc1['broth'] = {'wet_mass':broth_sc1, 
                                             'concentration':concentration_sc1, 
                                             'dry_mass':broth_DW_sc1}
        biomass_balance_dict_sc1['slurry'] = {'wet_mass':slurry_sc1, 
                                              'DM_content':DM_slurry_sc1, 
                                              'dry_mass':slurry_DW_sc1}
        biomass_balance_dict_sc1['water recirculated']:water_recirculated_sc1
        ## DATA MODELLED
        broth, broth_DW, water_recirculated = BrothFiltered (tech_period, 
                                                             harvesting_efficiency, 
                                                             concentration)
        slurry_DW = broth_DW * slurry_DW_sc1 / broth_DW_sc1
        biomass_balance_dict['broth'] = broth_DW
        biomass_balance_dict['slurry'] = slurry_DW
        biomass_balance_dict['water_recirculated'] = water_recirculated
        biomass_balance_dict['biomass_recirculated'] = broth_DW - slurry_DW          
        
    if tech_period == '2': 
        concentration_sc1 = 0.64 # concentration of Spirulina in broth [g/L]
        ## DATA COLLECTED
        broth_sc1, broth_DW_sc1, water_recirculated_sc1 = BrothFiltered (tech_period, 
                                                                         harvesting_efficiency, 
                                                                         concentration_sc1)
        slurry_sc1 = 198.99 # amount of slurry [kg]
        DM_slurry_sc1 = 10.39 # dry matter content of the slurry[% DM]
        slurry_DW_sc1 = slurry_sc1 * DM_slurry_sc1 /100
        biomass_balance_dict_sc1['broth'] = {'wet_mass':broth_sc1, 
                                             'concentration':concentration_sc1, 
                                             'dry_mass':broth_DW_sc1}
        biomass_balance_dict_sc1['slurry'] = {'wet_mass':slurry_sc1, 
                                              'DM_content':DM_slurry_sc1, 
                                              'dry_mass':slurry_DW_sc1}
        biomass_balance_dict_sc1['water_recirculated']:water_recirculated_sc1
        ## DATA MODELLED
        broth, broth_DW, water_recirculated = BrothFiltered (tech_period, 
                                                             harvesting_efficiency, 
                                                             concentration)
        slurry_DW = broth_DW * slurry_DW_sc1 / broth_DW_sc1
        biomass_balance_dict['broth'] = broth_DW
        biomass_balance_dict['slurry'] = slurry_DW
        biomass_balance_dict['water_recirculated'] = water_recirculated
        biomass_balance_dict['biomass_recirculated'] = broth_DW - slurry_DW        
            
    return biomass_balance_dict_sc1, biomass_balance_dict


def ElectricityFiltrationPump (tech_period):
    '''
    Calculate the electricity used to pump the broth from the ORPs to the VFS. 
    Based on the data collected on site in 2019 in the frame of the SpiralG project.
    
    :param running_time: Running time of the pump [h].
    :type running_time: float
    :return: electricity used by the pump [kWh].
    :rtype: float

    '''   
    if tech_period == '1':
        running_time = 3
        
    if tech_period == '2':
        running_time = 6
    ## DATA COLLECTED
    pump_num = 3    
    intensity = (1.06 + 0.99 + 1.08)/3 # average intensity for the 3 pumps over 3 days [A]
    power = intensity * (1.7320508*0.85*380) # instant power of the pumps [W]
    ## DATA MODELLED
    elec_pumps = (power/1000) * running_time * pump_num # electricity use [kWh]

    return elec_pumps


def ElectricityFiltrationMotorVFS (tech_period):
    '''
    Calculate the electricity used by the motor of the 3 VFS. Based on the data 
    collected on site in 2019 in the frame of the SpiralG project.
    
    :param running_time: Running time of the motor of the VFS [h].
    :type running_time: float
    :return: electricity used by the motor of the VFS [kWh].
    :rtype: float

    '''   
    if tech_period == '1':
        running_time = 3
    else: 
        running_time = 6
    ## DATA COLLECTED
    VFS_num = 3    
    intensity = (1.43 + 1.45 + 1.49)/3 # average intensity for the 3 VFS [A]
    power = intensity * (1.7320508*0.85*380) # instant power of the VFS [W]
    ## DATA MODELLED
    elec_motorVFS = (power/1000) * running_time * VFS_num # electricity use [kWh]
    
    return elec_motorVFS


def ElectricityFiltrationPumpVFS (tech_period):
    '''
    Calculate the electricity used by the pump of the VFS. Based on the data 
    collected on site in 2019 in the frame of the SpiralG project.
    
    :param running_time: Running time of the pump [h].
    :type running_time: float
    :return: electricity used by the pump of the VFS [kWh].
    :rtype: float

    '''   
    if tech_period == '1':
        running_time = 3
    else: 
        running_time = 6
    ## DATA COLLECTED
    VFS_num = 3    
    intensity = (4.39 + 4.25 + 4.29)/3 # average intensity for the 3 VFS [A]
    power = intensity * (1.7320508*0.85*380) # instant power of the VFS [W]
    ## DATA MODELLED
    elec_pumpVFS = (power/1000) * running_time * VFS_num # electricity use [kWh]
    
    return elec_pumpVFS


def WaterFiltration (tech_period, broth_DW, harvesting_efficiency, concentration):
    '''  
    The data were collected for 2022 only. The water used during filtration 
    corresponds to the water used for cleaning and goes to sewer system.
    '''
    ## DATA COLLECTED ## for period 2 only
    broth_sc1, broth_DW_sc1, water_recirculated_sc1 = BrothFiltered (tech_period, 
                                                                     harvesting_efficiency, 
                                                                     concentration)
    water_sc1 = 528.295  
    ## DATA MODELLED
    water = broth_DW * water_sc1 / broth_DW_sc1
    
    return water


def FiltrationDataDict (tech_period, harvesting_efficiency, concentration):
    
    data_dict = {}
    
    ## BIOMASS INPUT
    biomass_balance_dict_sc1, biomass_balance_dict = BiomassFiltration (tech_period, 
                                                                        harvesting_efficiency, 
                                                                        concentration)
    broth_DW = biomass_balance_dict['broth']
    data_dict['broth'] = {}
    data_dict['broth']['amount'] = biomass_balance_dict['broth']
    data_dict['broth']['unit'] = 'kg DW-eq'
    data_dict['broth']['type'] = 'fg_input'
    
    ## BIOMASS OUTPUT
    data_dict['slurry'] = {}
    data_dict['slurry']['amount'] = biomass_balance_dict['slurry']
    data_dict['slurry']['unit'] = 'kg DW-eq'
    data_dict['slurry']['type'] = 'ref_flow'
    data_dict['losses'] = {}
    data_dict['losses']['amount'] = biomass_balance_dict['biomass_recirculated']
    data_dict['losses']['unit'] = 'kg DW-eq'
    data_dict['losses']['type'] = 'recirculated'   

    ## ELECTRICITY 
    elec_pumps = ElectricityFiltrationPump (tech_period)
    elec_motorVFS = ElectricityFiltrationMotorVFS (tech_period)
    elec_pumpVFS = ElectricityFiltrationPumpVFS (tech_period)
    data_dict['electricity_IT'] = {}
    data_dict['electricity_IT']['amount'] = elec_pumps + elec_motorVFS + elec_pumpVFS
    data_dict['electricity_IT']['unit'] = 'kWh'
    data_dict['electricity_IT']['type'] = 'tech_input'
   
    ## GROUND WATER
    data_dict['ground_water'] = {}
    data_dict['ground_water']['amount'] = WaterFiltration (tech_period, broth_DW, 
                                                           harvesting_efficiency, 
                                                           concentration)
    data_dict['ground_water']['unit'] = 'L'
    data_dict['ground_water']['type'] = 'tech_input'

    return data_dict