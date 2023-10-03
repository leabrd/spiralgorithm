# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 09:18:40 2022

@author: leabr
"""

def NylonVFS (tech_period = '2', lifetime = 2, VFS_number = 3):
    
    import numpy as np
    
    if tech_period == '1':
        amount_nylon_per_day = 0
        
    if tech_period == '2': 
        weight_nylon_piece = 2.379 #  weight of a piece of net [g]
        surface_nylon_piece = 0.039 # surface of the piece of nylon [m2]
        diameter_VFS = 1.5 # diameter of a VFS [m]
        surface_VFS = np.pi * (diameter_VFS / 2)**2
        nylon_one_VFS = (surface_VFS * weight_nylon_piece / surface_nylon_piece)/1000
        nylon = VFS_number * nylon_one_VFS
        amount_nylon_per_year = nylon / lifetime
        amount_nylon_per_day = amount_nylon_per_year / 365
        
    return amount_nylon_per_day


def EPSBricks (lifetime = 10):

    volume_small_bricks = 120 # volume of the EPS brick 40x38.5x120 cm (6 ORPs) [m3]
    volume_large_bricks = 62.4 # volume of the EPS brick 40x62x200 cm (6 ORPs) [m3]
    density_EPS = 21.5 # density of EPS [kg/m3] => from literature
    EPS_bricks = (volume_small_bricks + volume_large_bricks) * density_EPS
    amount_EPS_bricks_per_year = EPS_bricks / lifetime
    amount_EPS_bricks_per_day = amount_EPS_bricks_per_year / 365
        
    return amount_EPS_bricks_per_day


def PVC_layer (lifetime = 10):
    
    surface_covered = 5540 # surface covered by the PVC layer [m2]
    weight = 0.63 # weight of the PVC layer [kg/m2]
    PVC_layer = surface_covered * weight # [kg]   
    amount_PVC_layer_per_year = PVC_layer / lifetime
    amount_PVC_layer_per_day = amount_PVC_layer_per_year / 365
    
    return amount_PVC_layer_per_day


def GalvanisedSteel (lifetime = 20):

    element_dict = {'el4': {'weight': 3.8, 'length': 37.9}, # weight [kg/m], length [m]
                    'el5': {'weight': 2.7, 'length': 26.03},
                    'el6': {'weight': 5.2, 'length': 2.94},
                    'el7': {'weight': 3.7, 'length': 2.94},
                    'el8': {'weight': 3.3, 'length': 2.75},
                    'el9': {'weight': 3.3, 'length': 28.88},
                    'el10': {'weight': 2.6, 'length': 30},
                    'el11': {'weight': 2.1, 'length': 23.44},
                    'el12': {'weight': 4.5, 'length': 6},
                    'el13': {'weight': 0.2, 'length': 15},
                    'el14': {'weight': 2.23, 'length': 36},
                    'el15': {'weight': 0.92, 'length': 108},
                    'el16': {'weight': 4.32, 'length': 15.75},
                    'el17': {'weight': 4.32, 'length': 33.45},
                    'el18': {'weight': 4.32, 'length': 5.8},
                    'el19': {'weight': 1.94, 'length': 4}
                    }
    
    amount_dict = {} 
    
    for el in element_dict.keys():
        amount_dict[el] = element_dict[el]['weight'] * element_dict[el]['length']
        
    amount_steel = sum(amount_dict.values())
    amount_steel_per_year = amount_steel / lifetime # total divided per the lifetime 
    amount_steel_per_day = amount_steel_per_year / 365

    return amount_steel_per_day


def InsulatedPanels (lifetime = 20):

    weight_100mm_panel = 9.76 # weight of a 100 mm (U=0,22W/m2K) panel [kg/m2]
    weight_60mm_panel = 8.2 # weight of a 60 mm (U=0,37W/m2K) panel [kg/m2]
    weight_30mm_panel = 7.06 # weight of a 30 mm (U=0,71W/m2K) panel [kg/m2]
    weight_roof_panel = 7.06 # weight of a roof panel [kg/m2]
    
    surface_100mm_panel = 69.45 # surface covered by 100 mm (U=0,22W/m2K) panels [m2]
    surface_60mm_panel = 88.26 # surface covered by 60 mm (U=0,37W/m2K) panels [m2]
    surface_30mm_panel = 90 # surface covered  by  30 mm (U=0,71W/m2K) panels [m2]
    surface_roof_panel = 115.5 # surface covered by roof panels [m2]
 
    amount_100mm_panel = weight_100mm_panel * surface_100mm_panel
    amount_60mm_panel = weight_60mm_panel * surface_60mm_panel
    amount_30mm_panel = weight_30mm_panel * surface_30mm_panel
    amount_roof_panel = weight_roof_panel * surface_roof_panel

    insulated_panels =  amount_100mm_panel + amount_60mm_panel + amount_30mm_panel + amount_roof_panel
    
    amount_panels_per_year = insulated_panels / lifetime # amount of insulated panels per year
    
    amount_panels_per_day = amount_panels_per_year / 365
    
    return amount_panels_per_day 


def PumiceBrick (lifetime = 20):
    
    number_bricks = 214 # number of pumice bricks [unit]
    weight_per_brick = 27.5 # weight of a 50x30x20 cm pumice brick [kg/unit]
    
    pumice_bricks = number_bricks * weight_per_brick
    amount_bricks_per_year = pumice_bricks / lifetime
    amount_bricks_per_day = amount_bricks_per_year / 365
    
    return amount_bricks_per_day


def ConcreteBrick (lifetime = 20):
    
    number_bricks = 251 # number of concrete bricks [unit]
    weight_per_brick = 24.8 # weight of a 50x20x20 cm concrete brick [kg]
   
    concrete_brick = number_bricks * weight_per_brick
    amount_bricks_per_year = concrete_brick / lifetime
    amount_bricks_per_day = amount_bricks_per_year / 365
    
    return amount_bricks_per_day


def FloorTiles (lifetime = 20):
    
    number_tiles = 3000 # number of tiles used [unit]
    weight_per_tile = 1.02 # weight of a floor tile 20x20cm [kg/unit]

    floor_tiles = number_tiles * weight_per_tile
    amount_tiles_per_year = floor_tiles / lifetime
    amount_tiles_per_day = amount_tiles_per_year / 365

    return amount_tiles_per_day


def Concrete (lifetime = 20):
    
    volume_el1 = 0.79 # volume of element 1 [m3]
    volume_el2 = 1.56 # volume of element 2 [m3]
    volume_el3 = 12 # volume of element 3 [m3]
    
    concrete_el1 = 350 * volume_el1 # amount of concrete [kg]
    concrete_el2 = 350 * volume_el2
    croncrete_el3 = 150 * volume_el3
    
    concrete = concrete_el1 + concrete_el2 + croncrete_el3
    amount_concrete_per_year = concrete / lifetime
    amount_concrete_per_day = amount_concrete_per_year / 365
    
    return amount_concrete_per_day


def Sand (lifetime = 20):
    
    volume_el1 = 0.79 # volume of element 1 [m3]
    volume_el2 = 1.56 # volume of element 2 [m3]
    volume_el3 = 12 # volume of element 3 [m3]
    
    sand_el1 = 1800 * volume_el1
    sand_el2 = 1800 * volume_el2
    sand_el3 = 1800 * volume_el3
    
    sand = sand_el1 + sand_el2 + sand_el3
    amount_sand_per_year = sand / lifetime
    amount_sand_per_day = amount_sand_per_year / 365
    
    return amount_sand_per_day 


def PEPipes (lifetime = 10):
    
    ## RAINWATER COLLECTION SYSTEM
    PE_rainwater = 506.5 #  amount of PE pipes used in the rainwater collection system [kg]
    
    ## ORP PUMPING SYTSEM
    diameter = 63 # diameter of the pipes [mm]
    length_line1 = 111 # length of the line [m]
    length_line2 = 60 
    length_line3 = 123
    lenght_pipes_facility = 50
    total_length = length_line1 + length_line2 + length_line3 + lenght_pipes_facility
    weight_PE_pipe = 0.715 # weight of a PE pipe [kg/m]
    
    PE_pipes = weight_PE_pipe * total_length + PE_rainwater
    amount_PE_pipes_per_year = PE_pipes / lifetime
    amount_PE_pipes_per_day = amount_PE_pipes_per_year / 365
    
    return amount_PE_pipes_per_day


def PVCPipes (lifetime = 10):
    
    ## ORP PUMPING SYSTEM
    length = 75 # total length of the PVC pipes [m]
    weight = 1.125 # weight of the PVC pipes [kg/m]
    PVC_pipes_ORP = length * weight

    ## HEATING SYSTEM
    diameter = 140 # diameter of the PVC pipes [mm]
    length = 600 # length of the PVC pipes [m]
    weight = 5.95 # weight of the PVC pipes [kg/m]
    PVC_pipes_heating = length * weight
    
    PVC_pipes = PVC_pipes_ORP + PVC_pipes_heating
    PVC_pipes_per_year = PVC_pipes / lifetime
    PVC_pipes_per_day = PVC_pipes_per_year / 365

    return PVC_pipes_per_day


def PPRPipes (lifetime = 10):
    
    diameter = 63 # diameter of the PPR pipes [mm]
    length = 320 # total length of the PPR pipes [m]
    weight = 1.065 # weight of the PVC pipes [kg/m]
    PPR_pipes = length * weight 
    amount_PPR_pipes_per_year = PPR_pipes / lifetime
    amount_PPR_pipes_per_day = amount_PPR_pipes_per_year / 365
    
    return amount_PPR_pipes_per_day


def PEXcPipes (lifetime = 10):
    
    diameter = 140 # diameter of the PE-Xc pipes [mm]
    length = 18000 # total length of the PE-Xc pipes [m]
    weight = 0.115 # weight of the 
    PEXc_pipes = length * weight
    amount_PEXc_pipes_per_year = PEXc_pipes / lifetime
    amount_PEXc_pipes_per_day = amount_PEXc_pipes_per_year / 365
    
    return amount_PEXc_pipes_per_day

def Polycarbonate (lifetime = 10):
    
    surface_covered = 300 # surface covered by PC [m2]
    PC_front_back_corner = 500 # amount of PC used for the front/back/corners [kg]
    PC_below_mosquitos_net = 120 # amount of PC used below the mosquitos net [kg]
    PC = PC_front_back_corner + PC_below_mosquitos_net
    amount_PC_per_year = PC / lifetime
    amount_PC_per_day = amount_PC_per_year / 365

    return amount_PC_per_day

def SolarShadingNet (lifetime = 10):
    
    surface_covered = 4416 # surface covered by solar shading nets [m2]
    weight = 0.095 # weight of the solar shading net [kg/m2]
    HDPE_net = surface_covered * weight
    amount_HDPE_per_year = HDPE_net / lifetime 
    amount_HDPE_per_day = amount_HDPE_per_year / 365

    return amount_HDPE_per_day

def PolyethyleneMembrane (lifetime = 10):
    
    PE_film_roof = 2694 # amount of PE_film used for the roof [kg]
    PE_film_side1 = 110 # amount of PE_film used for the side1 [kg]
    PE_film_side2 = 39.5 # amount of PE_film used for the side2 [kg]
    PE_film = PE_film_roof + PE_film_side1 + PE_film_side2
    
    amount_PE_film_per_year = PE_film / lifetime
    amount_PE_film_per_day = amount_PE_film_per_year / 365
    
    return amount_PE_film_per_day


#### TO CHANGE
def MosquitosNet ():
    
    mosquitos_net = 13.5 # amount of mosquitos net used [kg]
    
    return mosquitos_net


def BuildingDataDict (tech_period, lifetime_file_dir, VFS_number):
    
    data_dict = {}
    
    import pandas as pd
            
    df = pd.read_excel(lifetime_file_dir) # convert the Excel file into a dataframe
    lifetime_dict = df.set_index('product').to_dict(orient = 'index') # convert the dataframe into a temporary dictionary
   
    ## NYLON
    data_dict['nylon'] = {}
    lifetime_nylon = lifetime_dict['nylon']['lifetime']
    data_dict['nylon']['amount'] =  NylonVFS (tech_period, lifetime_nylon, VFS_number)
    data_dict['nylon']['unit'] = 'kg'
    data_dict['nylon']['type'] = 'tech_input'
    
    ## EPS BRICKS
    data_dict['polystyrene'] = {}
    lifetime_EPS_bricks = lifetime_dict['EPS_bricks']['lifetime']
    data_dict['polystyrene']['amount'] = EPSBricks (lifetime_EPS_bricks)
    data_dict['polystyrene']['unit'] = 'kg'
    data_dict['polystyrene']['type'] = 'tech_input' 
    
    ## PVC LAYER
    data_dict['polyvinylchloride_layer'] = {}
    lifetime_PVC_layer = lifetime_dict['PVC_layer']['lifetime']
    data_dict['polyvinylchloride_layer']['amount'] = PVC_layer (lifetime_PVC_layer)
    data_dict['polyvinylchloride_layer']['unit'] = 'kg'
    data_dict['polyvinylchloride_layer']['type'] = 'tech_input' 
 
    ## STEEL (GALVANISED)
    data_dict['steel'] = {}
    lifetime_steel = lifetime_dict['steel']['lifetime']
    data_dict['steel']['amount'] = GalvanisedSteel (lifetime_steel)
    data_dict['steel']['unit'] = 'kg'
    data_dict['steel']['type'] = 'tech_input' 
    
    ## INSULATED PANELS
    data_dict['polyurethane'] = {}
    lifetime_insulated_panels = lifetime_dict['insulated_panels']['lifetime']
    data_dict['polyurethane']['amount'] = InsulatedPanels (lifetime_insulated_panels)
    data_dict['polyurethane']['unit'] = 'kg'
    data_dict['polyurethane']['type'] = 'tech_input'

    ## PUMICE BRICKS 
    data_dict['pumice'] = {}
    lifetime_pumice_bricks = lifetime_dict['pumice_bricks']['lifetime']  
    data_dict['pumice']['amount'] = PumiceBrick (lifetime_pumice_bricks)
    data_dict['pumice']['unit'] = 'kg'
    data_dict['pumice']['type'] = 'tech_input'  
    
    ## CONCRETE BRICKS + CONCRETE
    data_dict['concrete'] = {}
    lifetime_concrete_bricks = lifetime_dict['concrete_bricks']['lifetime']  
    concrete_brick = ConcreteBrick (lifetime_concrete_bricks)
    lifetime_concrete = lifetime_dict['concrete']['lifetime']   
    concrete = Concrete (lifetime_concrete)
    data_dict['concrete']['amount'] = concrete_brick + concrete
    data_dict['concrete']['unit'] = 'kg'
    data_dict['concrete']['type'] = 'tech_input'      
    
    ## FLOOR TILES
    data_dict['ceramic_tile'] = {}
    lifetime_floor_tiles = lifetime_dict['floor_tiles']['lifetime']   
    data_dict['ceramic_tile']['amount'] = FloorTiles (lifetime_floor_tiles)
    data_dict['ceramic_tile']['unit'] = 'kg'
    data_dict['ceramic_tile']['type'] = 'tech_input'  
    
    ## SAND 
    data_dict['sand'] = {}
    lifetime_sand = lifetime_dict['sand']['lifetime']      
    data_dict['sand']['amount'] = Sand (lifetime_sand)
    data_dict['sand']['unit'] = 'kg'
    data_dict['sand']['type'] = 'tech_input'  
    
    ## POLYETHYLENE PIPES
    data_dict['polyethylene_pipe'] = {}
    lifetime_PE_pipes = lifetime_dict['PE_pipes']['lifetime']          
    data_dict['polyethylene_pipe']['amount'] = PEPipes (lifetime_PE_pipes)
    data_dict['polyethylene_pipe']['unit'] = 'kg'
    data_dict['polyethylene_pipe']['type'] = 'tech_input'      
    
    ## PVC PIPES
    data_dict['polyvinylchloride_pipe'] = {}
    lifetime_PVC_pipes = lifetime_dict['PVC_pipes']['lifetime']              
    data_dict['polyvinylchloride_pipe']['amount'] = PVCPipes (lifetime_PVC_pipes)
    data_dict['polyvinylchloride_pipe']['unit'] = 'kg'
    data_dict['polyvinylchloride_pipe']['type'] = 'tech_input' 

    ## PPR PIPES
    data_dict['polypropylene'] = {}
    lifetime_PPR_pipes = lifetime_dict['PPR_pipes']['lifetime']                  
    data_dict['polypropylene']['amount'] = PPRPipes (lifetime_PPR_pipes)
    data_dict['polypropylene']['unit'] = 'kg'
    data_dict['polypropylene']['type'] = 'tech_input' 
    
    ## PE-Xc PIPES
    data_dict['polyethylene_HDPE_pipe'] = {}
    lifetime_PEXc_pipes = lifetime_dict['PEXc_pipes']['lifetime']                      
    data_dict['polyethylene_HDPE_pipe']['amount'] = PEXcPipes (lifetime_PEXc_pipes) 
    data_dict['polyethylene_HDPE_pipe']['unit'] = 'kg'
    data_dict['polyethylene_HDPE_pipe']['type'] = 'tech_input' 
    
    ## POLYCARBONATE
    data_dict['polycarbonate'] = {}
    lifetime_PC = lifetime_dict['polycarbonate']['lifetime']                         
    data_dict['polycarbonate']['amount'] =  Polycarbonate (lifetime_PC)
    data_dict['polycarbonate']['unit'] = 'kg'
    data_dict['polycarbonate']['type'] = 'tech_input' 
    
    ## HDPE FILM
    data_dict['polyethylene_HDPE_shading'] = {}
    lifetime_HDPE_film = lifetime_dict['HDPE_film']['lifetime']                            
    data_dict['polyethylene_HDPE_shading']['amount'] =  SolarShadingNet (lifetime_HDPE_film)
    data_dict['polyethylene_HDPE_shading']['unit'] = 'kg'
    data_dict['polyethylene_HDPE_shading']['type'] = 'tech_input'    
    
    ## POLYETHYLENE FILM
    data_dict['polyethylene'] = {}
    lifetime_PE_film = lifetime_dict['PE_film']['lifetime']                            
    data_dict['polyethylene']['amount'] =  PolyethyleneMembrane (lifetime_PE_film)
    data_dict['polyethylene']['unit'] = 'kg'
    data_dict['polyethylene']['type'] = 'tech_input'     
    
   
    return data_dict










