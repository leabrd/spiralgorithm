#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 15:02:17 2023

@author: leabraud
"""

def DigesterProperties (recipe, data_dict_init):
    '''
    Function that calculates the digesters properties (e.g. fill level, organic
    load rate).

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
    
    import numpy as np
    
    # copy the initial dictionary to complete it
    data_dict = data_dict_init
        
    # calculation of the active digester volume assuming no solid retention device
    V_active_dig = data_dict['total']['V_feed']['amount'] * recipe['input']['conditions']['RT']['amount'] # active digester volume [m3]
    
    # calculation of the digester tank volume assuming cylinder
    V_dig_tank = recipe['input']['conditions']['tank_height']['amount'] * np.pi * recipe['input']['conditions']['tank_diameter']['amount']** 2 / 4 # digester tank volume [m3]
    
    # calculation of the fill level of the tank
    fill_level = (V_active_dig / V_dig_tank) * 100 # fill level [%]
    
    # calculation of the organic load rate 
    OLD =  data_dict['total']['VS']['amount']*1000 / V_active_dig # organic load rate [kg VS / m3 day]

    # add the new calculated values to the dictionary
    data_dict['total']['V_active_dig'] = {}
    data_dict['total']['V_active_dig']['amount'] = V_active_dig
    data_dict['total']['V_active_dig']['unit'] = 'm3'
    data_dict['total']['V_dig_tank'] = {}
    data_dict['total']['V_dig_tank']['amount'] = V_dig_tank  
    data_dict['total']['V_dig_tank']['unit'] = 'm3'  
    data_dict['total']['fill_level'] = {}
    data_dict['total']['fill_level']['amount'] = fill_level    
    data_dict['total']['fill_level']['unit'] = '%'    
    data_dict['total']['OLD'] = {}    
    data_dict['total']['OLD']['amount'] = OLD
    data_dict['total']['OLD']['unit'] = 'kg VS/m3 day'
    
    return data_dict