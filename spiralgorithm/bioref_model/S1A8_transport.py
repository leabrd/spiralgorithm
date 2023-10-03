# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 15:42:16 2022

@author: leabr
"""

def TransportDataDict (distance_car, distance_ship, distance_truck, biomass_DW, biomass_packaged_DW, line):
    ''' 
    The transport function does not depend on the tech period, the transportation
    distances are the same in 2019 and 2022. 
    biomass_DW can either be the Spirulina paste or the dry spangles depending 
    on the line (wet or dry). The biomass_packaged_DW correponds to the biomass
    packaged (i.e. weight of biomass + packaging).
    '''
    transport_data_dict = {}
    
    ### conversion of dry mass into wet mass
    if line == 'dry':
        DM_spangles_2019 = 96.8
        DM_spangles_2022 = 94.99
        DM_spangles_average = (DM_spangles_2019 + DM_spangles_2022) / 2
        biomass = biomass_DW / (DM_spangles_average/100)
        weight_packaging = biomass_packaged_DW - biomass_DW
        biomass_packaged = biomass + weight_packaging
    if line == 'wet':
        DM_paste_2019 = 33.07
        DM_paste_2022 = 23.26
        DM_paste_average = (DM_paste_2019 + DM_paste_2022) / 2
        biomass = biomass_DW / (DM_paste_average/100)
        weight_packaging = biomass_packaged_DW - biomass_DW
        biomass_packaged = biomass + weight_packaging
    
    ### transport distances
    transport_car = distance_car * biomass_packaged / 1000 # transport [ton*km]
    transport_truck = distance_truck * biomass_packaged / 1000 # transport [ton*km]
    transport_ship = distance_ship * biomass_packaged / 1000 # transport [ton*km]

    ## TRANSPORT BY CAR
    transport_data_dict['transport_car'] = {}
    transport_data_dict['transport_car']['amount'] = transport_car
    transport_data_dict['transport_car']['unit'] = 'km'
    transport_data_dict['transport_car']['type'] = 'tech_input'
    
    if line == 'dry':
        ## TRANSPORT BY FERRY
        transport_data_dict['transport_ship'] = {}
        transport_data_dict['transport_ship']['amount'] = transport_ship
        transport_data_dict['transport_ship']['unit'] = 'ton*km'
        transport_data_dict['transport_ship']['type'] = 'tech_input'
        ## TRANSPORT BY TRUCK
        transport_data_dict['transport_truck'] = {}
        transport_data_dict['transport_truck']['amount'] = transport_truck
        transport_data_dict['transport_truck']['unit'] = 'ton*km'
        transport_data_dict['transport_truck']['type'] = 'tech_input'
        
    if line == 'wet':
        ## TRANSPORT BY FERRY - REFREGIRATED
        transport_data_dict['transport_ship_refrigerated'] = {}
        transport_data_dict['transport_ship_refrigerated']['amount'] = transport_ship
        transport_data_dict['transport_ship_refrigerated']['unit'] = 'ton*km'
        transport_data_dict['transport_ship_refrigerated']['type'] = 'tech_input'
        ## TRANSPORT BY TRUCK - REFREGIRATED
        transport_data_dict['transport_truck_refrigerated'] = {}
        transport_data_dict['transport_truck_refrigerated']['amount'] = transport_truck
        transport_data_dict['transport_truck_refrigerated']['unit'] = 'ton*km'
        transport_data_dict['transport_truck_refrigerated']['type'] = 'tech_input'
        
    return transport_data_dict