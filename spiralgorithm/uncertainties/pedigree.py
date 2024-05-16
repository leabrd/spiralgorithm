#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 11:35:19 2023

@author: leabraud
"""

def CalculateLoc (mean):
    '''
    Loc (or mu) is the logarithm of the deterministic value (geometric mean or
    mean) entered by the LCA practitioner. 
    '''
    import numpy as np
    return np.log(abs(mean))


def BasicUncertainty ():
    ''' 
    For now, the basic uncertainty was fixed to 0.0006, the value used for most 
    exchanges in the foreground activities. The basic uncertainty is also known
    as variance of logtransformed data.
    TO DO: include all options of basic uncertainty.
    '''    
    basic_uncertainty = 0.0006    
    return basic_uncertainty


def AdditionalUncertainty (pm_text):
    ''' 
    Calculates the total additional uncertainty based on the pedigree matrix 
    score entered by the LCA practitioner. The uncertainty factors are based
    on the report "data quality guideline for the ecoinvent database
    version 3" and correspond to sigma^2 (and not GSD^2). The pedigree matrix
    scores are entered as a text (e.g., '(2,1,1,1,5)').
    '''
    uf_matrix = [
        (0., 0.0006, 0.002, 0.008, 0.04), # reliability
        (0., 0.0001, 0.0006, 0.002, 0.008), # completeness
        (0., 0.0002, 0.002, 0.008, 0.04), # temporal correlation
        (0., 2.5e-5, 0.0001, 0.0006, 0.002), # geographical correlation
        (0., 0.0006, 0.008, 0.04, 0.12) # further technological correlation
        ]
        
    # transform the pedigree matrix scores (string) into a list of numbers
    pm_list = []
    for i in pm_text:
        if i in ['1','2','3','4','5']:
            pm_list.append(int(i))
            
    # print the list of pedigree score + corresponding uncertainty factors 
    uf_list = []
    for i in range(len(pm_list)):
        pm_score = pm_list[i]
        #print('\npedigree matrix score: %s' %pm_score)
        uf = uf_matrix[i][pm_score-1]
        #print('uncertainty factor: %s' %uf)
        uf_list.append(uf)
    #print('\nuncertaity factors: %s' %uf_list)

    additional_uncertainty = sum(uf_list)
    #print('additional uncertainty: %s' %additional_uncertainty)

    return additional_uncertainty


def TotalUncertainty (basic_uncertainty, additional_uncertainty):
    ''' 
    Sum of the basic and additional uncertainty. Also known as variance of data 
    with pedigree.
    '''    
    return basic_uncertainty + additional_uncertainty


def CalculateScale (total_uncertainty):
    ''' 
    Scale (or sigma) is the standard deviation.
    '''
    import numpy as np
    return np.sqrt(total_uncertainty)


def CalculateGSD (scale):
    '''
    GSD (or sigma*) is the geometric standard deviation.
    '''
    import numpy as np
    return np.exp(scale)

