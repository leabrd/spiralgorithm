# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 12:36:41 2022

@author: leabr
"""

def graph_colours (list_to_plot):
    
    '''
    Choose colour palette accoridng to the length of list to plot.
    https://colorbrewer2.org/#type=diverging&scheme=PuOr&n=8
    '''
    colour_name = 'div_red2yellow2blue'
    
    colour_list = []
    
    dict_colours =                {'div_purple2green':{
                                    '3': ['#af8dc3','#f7f7f7','#7fbf7b'],
                                    '4': ['#7b3294','#c2a5cf','#a6dba0','#008837'],
                                    '5': ['#7b3294','#c2a5cf','#f7f7f7','#a6dba0','#008837'],
                                    '6': ['#762a83','#af8dc3','#e7d4e8','#d9f0d3','#7fbf7b','#1b7837'],
                                    '7': ['#762a83','#af8dc3','#e7d4e8','#f7f7f7','#d9f0d3','#7fbf7b','#1b7837'],
                                    '8': ['#762a83','#9970ab','#c2a5cf','#e7d4e8','#d9f0d3','#a6dba0','#5aae61','#1b7837']
                                   },
                                  'div_orange2purple':{
                                        '3': ['#f1a340','#f7f7f7','#998ec3'],
                                        '4': ['#e66101','#fdb863','#b2abd2','#5e3c99'],
                                        '5': ['#e66101','#fdb863','#f7f7f7','#b2abd2','#5e3c99'],
                                        '6': ['#b35806','#f1a340','#fee0b6','#d8daeb','#998ec3','#542788'],
                                        '7': ['#b35806','#f1a340','#fee0b6','#f7f7f7','#d8daeb','#998ec3','#542788'],
                                        '8': ['#b35806','#e08214','#fdb863','#fee0b6','#d8daeb','#b2abd2','#8073ac','#542788']
                                       },
                                  'div_brown2green':{
                                        '3': ['#d8b365','#f5f5f5','#5ab4ac'],
                                        '4': ['#a6611a','#dfc27d','#80cdc1','#018571'],
                                        '5': ['#a6611a','#dfc27d','#f5f5f5','#80cdc1','#018571'],
                                        '6': ['#8c510a','#d8b365','#f6e8c3','#c7eae5','#5ab4ac','#01665e'],
                                        '7': ['#8c510a','#d8b365','#f6e8c3','#f5f5f5','#c7eae5','#5ab4ac','#01665e'],
                                        '8': ['#8c510a','#bf812d','#dfc27d','#f6e8c3','#c7eae5','#80cdc1','#35978f','#01665e']
                                       },        
                                  'qualitative':{
                                        '3': ['#66c2a5','#fc8d62','#8da0cb'],
                                        '4': ['#66c2a5','#fc8d62','#8da0cb','#e78ac3'],
                                        '5': ['#66c2a5','#fc8d62','#8da0cb','#e78ac3','#a6d854'],
                                        '6': ['#66c2a5','#fc8d62','#8da0cb','#e78ac3','#a6d854','#ffd92f'],
                                        '7': ['#66c2a5','#fc8d62','#8da0cb','#e78ac3','#a6d854','#ffd92f','#e5c494'],
                                        '8': ['#66c2a5','#fc8d62','#8da0cb','#e78ac3','#a6d854','#ffd92f','#e5c494','#b3b3b3'],
                                        '9': ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6']
                                       },
                                  'div_red2white2blue':{
                                        '3': ['#ef8a62','#f7f7f7','#67a9cf'],
                                        '4': ['#ca0020','#f4a582','#92c5de','#0571b0'],
                                        '5': ['#ca0020','#f4a582','#f7f7f7','#92c5de','#0571b0'],
                                        '6': ['#b2182b','#ef8a62','#fddbc7','#d1e5f0','#67a9cf','#2166ac'],
                                        '7': ['#b2182b','#ef8a62','#fddbc7','#f7f7f7','#d1e5f0','#67a9cf','#2166ac'],
                                        '8': ['#b2182b','#d6604d','#f4a582','#fddbc7','#d1e5f0','#92c5de','#4393c3','#2166ac'],
                                        '9': ['#b2182b','#d6604d','#f4a582','#fddbc7','#f7f7f7','#d1e5f0','#92c5de','#4393c3','#2166ac']
                                       },
                                  'div_red2yellow2blue':{
                                        '3': ['#fc8d59','#ffffbf','#91bfdb'],
                                        '4': ['#d7191c','#fdae61','#abd9e9','#2c7bb6'],
                                        '5': ['#d7191c','#fdae61','#ffffbf','#abd9e9','#2c7bb6'],
                                        '6': ['#d73027','#fc8d59','#fee090','#e0f3f8','#91bfdb','#4575b4'],
                                        '7': ['#d73027','#fc8d59','#fee090','#ffffbf','#e0f3f8','#91bfdb','#4575b4'],
                                        '8': ['#d73027','#f46d43','#fdae61','#fee090','#e0f3f8','#abd9e9','#74add1','#4575b4'],
                                        '9': ['#d73027','#f46d43','#fdae61','#fee090','#ffffbf','#e0f3f8','#abd9e9','#74add1','#4575b4'],
                                        '12':['#d73027','#f46d43','#fdae61','#fee090','#ffffbf','#e0f3f8','#abd9e9','#74add1','#4575b4','#e0ecf4','#9ebcda']
                                       },
                                  'seq_blue_purple':{
                                        '3': ['#e0ecf4','#9ebcda','#8856a7'],
                                        '4': ['#edf8fb','#b3cde3','#8c96c6','#88419d'],
                                        '5': ['#edf8fb','#b3cde3','#8c96c6','#8856a7','#810f7c'],
                                        '6': ['#edf8fb','#bfd3e6','#9ebcda','#8c96c6','#8856a7','#810f7c'],
                                        '7': ['#edf8fb','#bfd3e6','#9ebcda','#8c96c6','#8c6bb1','#88419d','#6e016b'],
                                        '8': ['#f7fcfd','#e0ecf4','#bfd3e6','#9ebcda','#8c96c6','#8c6bb1','#88419d','#6e016b'],
                                        '9': ['#f7fcfd','#e0ecf4','#bfd3e6','#9ebcda','#8c96c6','#8c6bb1','#88419d','#810f7c','#4d004b']
                                       },
                                  'seq_green2blue':{
                                        '3': ['#e0f3db','#a8ddb5','#43a2ca'],
                                        '4': ['#f0f9e8','#bae4bc','#7bccc4','#2b8cbe'],
                                        '5': ['#f0f9e8','#bae4bc','#7bccc4','#43a2ca','#0868ac'],
                                        '6': ['#f0f9e8','#ccebc5','#a8ddb5','#7bccc4','#43a2ca','#0868ac'],
                                        '7': ['#f0f9e8','#ccebc5','#a8ddb5','#7bccc4','#4eb3d3','#2b8cbe','#08589e'],
                                        '8': ['#f7fcf0','#e0f3db','#ccebc5','#a8ddb5','#7bccc4','#4eb3d3','#2b8cbe','#08589e'],
                                        '9': ['#f7fcf0','#e0f3db','#ccebc5','#a8ddb5','#7bccc4','#4eb3d3','#2b8cbe','#0868ac','#084081']
                                       }
                                  
                                  }
    length = len(list_to_plot)

    if length <3:
        
        colour_list = dict_colours[colour_name][str(3)]
        
    else: 
        
        colour_list = dict_colours[colour_name][str(length)]
        
        
    from matplotlib.pyplot import cm
    import numpy as np
    
    #variable n below should be number of curves to plot
    
    #version 1:
    
    colour_list = cm.viridis(np.linspace(0, 1, length))
        
    return colour_list