#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 15:03:13 2023

@author: leabraud
"""

def EnergyProduction (recipe, data_dict_init):
    '''
    Function that calculates the amount of electricity and heat produced by the 
    AD as well as the quantities that are reused in the AD plant and exportable.
    The exportable electricity and heat correspond to the amount of energy that 
    can be used in the SpiralG biorefinery.

    Parameters
    ----------
    recipe : dict
        Dictionary from loaded recipe (YAML file).
    data_dict : dict
        Dictionary with the initial data and to be completed.

    Returns
    -------
    data_dict : dict
        Dictionary of data, completed.

    '''
    
    # copy the initial dictionary to complete it
    data_dict = data_dict_init
    
    # calculate the energy available in the biogas
    CV_CH4 = recipe['input']['CHP']['CV_CH4']['amount'] # calorific value of methane [kWh/m3] 
    energy = CV_CH4 * data_dict['total']['CH4_prod']['amount'] # energy available [kWh/day]
    data_dict['total']['energy'] = {}
    data_dict['total']['energy']['amount'] = energy
    data_dict['total']['energy']['unit'] = 'kWh/day'
    
    elec_gen_eff = recipe['input']['CHP']['elec_gen_eff']['amount'] # electricity generation efficiency [%]
    heat_gen_eff = recipe['input']['CHP']['heat_gen_eff']['amount'] # heat generation efficiency [%]
    
    # calculate the amount of electricity and heat generated from the biogas
    daily_elec_CHP = energy * elec_gen_eff/100 # electricity availablable [kWh/day]
    daily_heat_CHP = energy * heat_gen_eff/100 # heat available [kWh/day]
    elec_CHP = daily_elec_CHP/24 # electricity availablable [kW]
    heat_CHP = daily_heat_CHP/24 # heat availablable [kW]
    
    # add the results to the dict
    data_dict['total']['electricity'] = {}
    data_dict['total']['electricity']['amount'] = daily_elec_CHP
    data_dict['total']['electricity']['unit'] = 'kWh/day'
    data_dict['total']['heat'] = {}
    data_dict['total']['heat']['amount'] = daily_heat_CHP
    data_dict['total']['heat']['unit'] = 'kWh/day'   
    
    # calculate the amount of exportable electricity
    elec_reused_AD = recipe['input']['CHP']['elec_reused_AD']['amount'] # electricity reused in the AD plant [kW]
    elec_reused_else = recipe['input']['CHP']['elec_reused_others']['amount'] # electricity reused elswhere in the plant [kW]
    elec_reused = elec_reused_AD + elec_reused_else # total electricity reused [kW]
    exportable_elec = elec_CHP - elec_reused # exportable electricity [kW]
    daily_exportable_elec = exportable_elec * 24
    
    # add the results to the dict
    data_dict['total']['exportable_electricity'] = {}
    data_dict['total']['exportable_electricity']['amount'] = daily_exportable_elec
    data_dict['total']['exportable_electricity']['unit'] = 'kWh/day'
    
    # calculate the amount of exportable heat
    T_amb = recipe['input']['conditions']['T_amb']['amount']
    T_feed = recipe['input']['conditions']['T_feed']['amount']
    T_dig = recipe['input']['conditions']['T_dig']['amount']
    
    # calculate the amount of heat used to warm up the feedstock
    HC_feed = recipe['input']['conditions']['HC_feed']['amount'] # heat capacity of the feedstock assumed the same as water [kJ/kg°C ]
    heat_reused_feed = (data_dict['total']['m_feed']['amount']/(24*3600))*(1000*HC_feed)*(T_dig-T_feed) # heat used to warm up the feedstock [kW]
    
    # calculate heat loss through digester wall: 300 mm thick concrete
    U_wall = recipe['input']['heat_transfer']['wall_concrete_300mm']['U']['amount']
    A_surf_wall = recipe['input']['heat_transfer']['wall_concrete_300mm']['A']['amount']
    delta_T_wall = recipe['input']['heat_transfer']['wall_concrete_300mm']['delta_T']['amount']
    Q_wall = U_wall * A_surf_wall * delta_T_wall / 1000

    # calculate heat loss through digester lid: 100 mm thick concrete
    U_lid = recipe['input']['heat_transfer']['lid_concrete_100mm']['U']['amount']
    A_surf_lid = recipe['input']['heat_transfer']['lid_concrete_100mm']['A']['amount']
    delta_T_lid = recipe['input']['heat_transfer']['lid_concrete_100mm']['delta_T']['amount']
    Q_lid = U_lid * A_surf_lid * delta_T_lid / 1000    
    
    # calculate the total heat losses through the wall + lid
    Q_tot = Q_wall + Q_lid

    # calculate the total of heat used in the AD (to warm up the feedstock, due to the losses, and reused in the plant)
    heat_reused_AD = recipe['input']['CHP']['heat_reused_AD']['amount'] # heat reused in the AD plant [kW]
    heat_reused = heat_reused_AD + Q_tot + heat_reused_feed
    exportable_heat = heat_CHP - heat_reused
    daily_exportable_heat = exportable_heat * 24
    
    # add the results to the dict
    data_dict['total']['exportable_heat'] = {}
    data_dict['total']['exportable_heat']['amount'] = daily_exportable_heat
    data_dict['total']['exportable_heat']['unit'] = 'kWh/day'
        
    
    return data_dict
