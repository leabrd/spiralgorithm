#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 15:04:35 2023

@author: leabraud
"""

def BiogasDigestateProduction (recipe, data_dict_init):
    '''
    Function that calculates the amount of biogas and digestate produced by 
    co-digestion of the cattle slurry and grass silage. 

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

    # definition of the parameters which depend on the temperature regime        
    if recipe['input']['conditions']['temperature_regime']['amount'] == 'mesophilic':
        k4 = 0.494
        k5 = 0.0704
        k6 = 23.81 # k6 = 0.00233 in the paper?
        k7 = 0.0023 # k7 = 0.323 in the paper?
        k8 = 0.323 # k8 = 23.8 in the paper?
    elif recipe['input']['conditions']['temperature_regime']['amount'] == 'thermophilic': 
        k4 = 22.8
        k5 = 0.107
        k6 = 21.0
        k7 = 0.113
        k8 = 58.6
    else: 
        print("The temperature regime has to be 'mesophilic' or 'thermophilic'.")
        
    T = recipe['input']['conditions']['T_dig']['amount']
        
    B = k4* np.exp(k5 * (T - k6)) - k7* np.exp(k8* (T - k6))
    
    DT = 4
    # k1 is used in the method 1
    k1 = 0.2
    # k2-3 are used in the method 2
    k2 = 13.7
    k3 = 18.9
    '''
    About 39% of the influent leaves the reactor within half the average retention 
    time, and 13% of the influent leaves after remaining for over twice the retention 
    time.
    '''
    k9 = 0.39
    k10 = 0.13
    k11 =  0.9 # 0.8 in the paper?
    
    imperfect_mixing_adjustement = recipe['input']['conditions']['imperfect_mixing_adjustment']['amount']
    
    RT = recipe['input']['conditions']['RT']['amount']

    
    for i in recipe['input']['feedstocks'].keys():
        
        VSD_A1 = ((B * k1 * (RT - DT)) / (1 + B * k1 * (RT - DT))) * 100 # [%]
        
        VSD_A2 = k2 * np.log(B * (RT - DT)) + k3 # [%]
        
        if imperfect_mixing_adjustement == True: 
            
            VSD_A1_05 = ((B * k1 * (0.5*RT - DT)) / (1 + B * k1 * (0.5*RT - DT))) * 100
            VSD_A1_2 = ((B * k1 * (2*RT - DT)) / (1 + B * k1 * (2*RT - DT))) * 100
            VSD_A1_tot = k9 * VSD_A1_05 + k10 * VSD_A1_2 + (1 - k9 - k10) * VSD_A1
            
            VSD_A2_05 = k2 * np.log(B * (0.5 * RT - DT)) + k3
            VSD_A2_2 = k2 * np.log(B * (2 * RT - DT)) + k3
            VSD_A2_tot = k9 * VSD_A2_05 + k10 * VSD_A2_2 + (1 - k9 - k10) * VSD_A2
            
        else:
        
            VSD_A1_tot = VSD_A1
            VSD_A2_tot = VSD_A2
    
        # weighted average of the two approaches
        VSD = k11 * VSD_A1_tot + (1 - k11) * VSD_A2_tot # [%]
        
        # calculation of the estimated biogas production
        BG_prod = VSD/100 * data_dict['total']['BG']['amount'] # [m3/day]
        
        # calculation of the estimated methane production
        CH4_prod = VSD/100 * data_dict['total']['CH4']['amount'] # [m3/day]
        
        # calculation of the estimated CH4 content
        C_CH4 = CH4_prod / BG_prod * 100 # [%]
        
        # calculation of the amount of digestate produced assuming that the feedstock has the density of water...
        m_dig = data_dict['total']['m_feed']['amount'] - (data_dict['total']['VS']['amount']*VSD/100) * (data_dict['total']['V_feed']['amount']/data_dict['total']['m_feed']['amount'])
        
        # add the calculated data to the dictionary
        data_dict['total']['VSD'] = {}
        data_dict['total']['VSD']['amount'] = VSD
        data_dict['total']['VSD']['unit'] = '%'
        data_dict['total']['BG_prod'] = {}
        data_dict['total']['BG_prod']['amount'] = BG_prod
        data_dict['total']['BG_prod']['unit'] = 'm3/day'
        data_dict['total']['CH4_prod'] = {}
        data_dict['total']['CH4_prod']['amount'] = CH4_prod
        data_dict['total']['CH4_prod']['unit'] = 'm3/day'    
        data_dict['total']['C_CH4'] = {}
        data_dict['total']['C_CH4']['amount'] = C_CH4
        data_dict['total']['C_CH4']['unit'] = '%'         
        data_dict['total']['m_dig'] = {}
        data_dict['total']['m_dig']['amount'] = m_dig
        data_dict['total']['m_dig']['unit'] = 'm3/day'
    
    return data_dict