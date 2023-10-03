#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 14:54:58 2023

@author: leabraud
"""


def BiogasProductionPotential (recipe, data_dict_init):
    '''
    Function that calculates the biogas production potential of the mix of cattle
    slurry and grass silage.

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
 
    import yaml
    import io
    import pandas as pd
    
    # initialise the counters
    m_feed_tot = 0
    TS_tot = 0
    VS_tot = 0
    BG_tot = 0
    CH4_tot = 0
    V_feed_tot = 0
    N_tot = 0
    P2O5_tot = 0
    K2O_tot = 0
    
    # copy the initial dictionary to complete it
    data_dict = data_dict_init

    # for each feedstock in the list, do the calculculations and sums the results
    for i in recipe['input']['feedstocks'].keys():
    
        TS = (recipe['input']['feedstocks'][i]['TS%']['amount']/100) * recipe['input']['feedstocks'][i]['m_feed']['amount'] # total solids [t/day]
        VS = (recipe['input']['feedstocks'][i]['VS%']['amount']/100) * TS # volatile solids [t/day]
        BG_VS = recipe['input']['feedstocks'][i]['Y_pBG_VS']['amount'] * VS # biogas potential [m3/day]
        BG_FF = recipe['input']['feedstocks'][i]['Y_pBG_FF']['amount'] * recipe['input']['feedstocks'][i]['m_feed']['amount'] # biogas potential [m3/day]
        
        # if the values are different, choose the maximum between the two
        if BG_VS != BG_FF:
            BG = max(BG_VS,BG_FF)
            
        CH4 = (recipe['input']['feedstocks'][i]['CH4%']['amount']/100) * BG # CH4 potential [m3/day]
        V_feed = recipe['input']['feedstocks'][i]['m_feed']['amount'] / recipe['input']['feedstocks'][i]['d']['amount'] # volume flow of feedstock [m3/day]
        N = recipe['input']['feedstocks'][i]['N%']['amount']/100 * TS * 1000 # amount N [kg/day]
        P2O5 = recipe['input']['feedstocks'][i]['P2O5%']['amount']/100 * TS * 1000 # amount P205 [kg/day]
        K2O = recipe['input']['feedstocks'][i]['K2O%']['amount']/100 * TS * 1000 # amount K2O [kg/day]
        
        # add the calculated values to the dictionary
        data_dict[i]['TS'] = {}
        data_dict[i]['TS']['amount'] = TS
        data_dict[i]['TS']['unit'] = 't/day'
        data_dict[i]['VS'] = {}
        data_dict[i]['VS']['amount'] = VS
        data_dict[i]['VS']['unit'] = 't/day'
        data_dict[i]['BG'] = {}
        data_dict[i]['BG']['amount'] = BG
        data_dict[i]['BG']['unit'] = 'm3/day'
        data_dict[i]['CH4'] = {}
        data_dict[i]['CH4']['amount'] = CH4
        data_dict[i]['CH4']['unit'] = 'm3/day'
        data_dict[i]['V_feed'] = {}
        data_dict[i]['V_feed']['amount'] = round(V_feed,2)
        data_dict[i]['V_feed']['unit'] = 'm3/day'
        data_dict[i]['N'] = {}
        data_dict[i]['N']['amount'] = round(N,2)
        data_dict[i]['N']['unit'] = 'kg/day'
        data_dict[i]['P2O5'] = {}
        data_dict[i]['P2O5']['amount'] = round(P2O5,2)
        data_dict[i]['P2O5']['unit'] = 'kg/day'
        data_dict[i]['K2O'] = {}
        data_dict[i]['K2O']['amount'] = round(K2O,2)
        data_dict[i]['K2O']['unit'] = 'kg/day'
        
        # add the values of each feedstock to the counters
        m_feed_tot += recipe['input']['feedstocks'][i]['m_feed']['amount']
        TS_tot += TS
        VS_tot += VS
        BG_tot += BG
        CH4_tot += CH4
        V_feed_tot += V_feed
        N_tot += N
        P2O5_tot += P2O5
        K2O_tot += K2O
    
    # add the total values to the dictionary
    data_dict['total'] = {}    
    data_dict['total']['m_feed'] = {}
    data_dict['total']['m_feed']['amount'] = round(m_feed_tot,2)
    data_dict['total']['m_feed']['unit'] = 't/day'
    data_dict['total']['TS'] = {}
    data_dict['total']['TS']['amount'] = round(TS_tot,2)
    data_dict['total']['TS']['unit'] = 't/day'
    data_dict['total']['VS'] = {}
    data_dict['total']['VS']['amount'] = round(VS_tot,2)
    data_dict['total']['VS']['unit'] = 't/day'
    data_dict['total']['BG'] = {}
    data_dict['total']['BG']['amount'] = round(BG_tot,2)
    data_dict['total']['BG']['unit'] = 'm3/day'
    data_dict['total']['CH4'] = {}
    data_dict['total']['CH4']['amount'] = round(CH4_tot,2)
    data_dict['total']['CH4']['unit'] = 'm3/day'
    data_dict['total']['V_feed'] = {}
    data_dict['total']['V_feed']['amount'] = round(V_feed_tot,2)
    data_dict['total']['V_feed']['unit'] = 'm3/day'
    data_dict['total']['N'] = {}
    data_dict['total']['N']['amount'] = round(N_tot,2)
    data_dict['total']['N']['unit'] = 'kg/day'
    data_dict['total']['P2O5'] = {}
    data_dict['total']['P2O5']['amount'] = round(P2O5_tot,2)
    data_dict['total']['P2O5']['unit'] = 'kg/day'
    data_dict['total']['K2O'] = {}
    data_dict['total']['K2O']['amount'] = round(K2O_tot,2)
    data_dict['total']['K2O']['unit'] = 'kg/day'
    
    return data_dict