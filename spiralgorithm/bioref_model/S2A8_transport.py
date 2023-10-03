#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 12:48:40 2023

@author: leabraud
"""

def TransportDataDict (distance_truck, CPA_DW, CPA_packaged_DW):
    ''' 
    The transport function does not depend on the tech period, the transportation
    distances are the same in 2021 and 2022. 
    CPA_DW corresponds to the CPA unprocessed from S2.A2.Centrifugation.
    CPA_packaged_DW corresponds to the CPA unprocessed, packaged from S2.A7b.Packaging
    (i.e. weight of biomass + packaging).
    '''
    transport_data_dict = {}
    
    # conversion of dry mass into wet mass
    DM_CPA_2021 = 6.43 # dry matter content measured in S3.A1.Extraction [%DW]
    DM_CPA_2022 = 6.26 # dry matter content measured in S3.A1.Extraction [%DW]
    DM_CPA_average = (DM_CPA_2021 + DM_CPA_2022)/2
    CPA = CPA_DW / (DM_CPA_average/100) # amount of CPA expressed in wet mass
    weight_packaging = CPA_packaged_DW - CPA_DW # weight of the plastic packaging
    CPA_packaged = CPA + weight_packaging # weight of the wet CPA + packaging
    
    # transport distances
    transport_truck = distance_truck * CPA_packaged / 1000 # transport [ton*km]
    
    # transport dictionary
    transport_data_dict['transport_truck'] = {}
    transport_data_dict['transport_truck']['amount'] = transport_truck
    transport_data_dict['transport_truck']['unit'] = 'ton*km'
    transport_data_dict['transport_truck']['type'] = 'tech_input'
        
    return transport_data_dict