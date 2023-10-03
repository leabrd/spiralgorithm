# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 16:14:35 2022

@author: leabr
"""

def PasteToSpangles (tech_period, paste_DW):
    ''' 
    Function to find the amount of spangles that would have been produced 
    according to the amount of paste. This is necessary in the case of the 
    wet line to calculate the amount of nutrients required. The amount of 
    nutrient required are calcualted according to the amount of wet spangles 
    obtained. In the case of the wet line, the production stops at the paste
    so need to make assumption based on the period 1 and 2 data.
    '''
    if tech_period == '1':
        ## DATA COLLECTED 
        paste_sc1 = 91.45 # amount of paste [kg]
        DM_paste_sc1 = 33.07 # dry matter content of the paste [%]
        paste_DW_sc1 = paste_sc1 * DM_paste_sc1 /100
        dry_spangles_sc1 = 27.53 # amount of paste [kg]
        DM_dry_spangles_sc1 = 96.8 # dry matter content of the paste [%]
        dry_spangles_DW_sc1 = dry_spangles_sc1 * DM_dry_spangles_sc1 /100
        ## DATA MODELLED 
        dry_spangles_DW = paste_DW * dry_spangles_DW_sc1 / paste_DW_sc1

    else:
        ## DATA COLLECTED
        paste_sc1 = 77.38 # amount of paste [kg]
        DM_paste_sc1 = 23.26 # dry matter content of the paste [%]
        paste_DW_sc1 = paste_sc1 * DM_paste_sc1 /100
        dry_spangles_sc1 = 15.59 # amount of paste [kg]
        DM_dry_spangles_sc1 = 94.99 # dry matter content of the paste [%]
        dry_spangles_DW_sc1 = dry_spangles_sc1 * DM_dry_spangles_sc1 /100
        ## DATA MODELLED 
        dry_spangles_DW = paste_DW * dry_spangles_DW_sc1 / paste_DW_sc1

    return dry_spangles_DW


def ProductivityToConcentration (spangle_productivity, surface_per_ORP):
    '''
    Determine the concentration of Spirulina in the broth [g/L] from the spangle 
    productivity [g/m2/day]. This account for all the process i.e. how much 
    of dry spangles can be produced from a certain spirulina biomass concentration
    in the ORPs.  This means that the higher the concentration in the pond, the 
    more ddry spangles we get. 
    '''
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy import stats
    
    # data = [[0.685, 4.4686374, 4.43068, 2.526824, 2.413856], # ORP1 13/07/22
    #         [0.865, 5.5119778, 4.779063, 4.61784654, 3.1015152], # ORP2 13/07/22
    #         [0.41, 1.2775852, 1.404608, 1.35152208, 1.1820168], # ORP4 13/07/22
    #         [0.555, 1.8059982, 1.822079, 1.71434386, 3.1116448], # ORP5 13/07/22
    #         [0.645, 2.340188, 2.973402, 2.8307754, 2.7667998] # ORP6 13/07/22
    #     ]
    # df = pd.DataFrame(data, columns=['Concentration (g/L)', 'Slurry (kg DW-eq)',
    #                                  'Paste (kg DW-eq)', 'Wet spangles (kg DW-eq)',
    #                                  'Dry spangles (kg DW-eq)'])
    
    # concentration and dry spangles obtained per ORP on the 13/07/2022
    data = [[0,0],
            [0.685, 2.413856],
            [0.865, 3.1015152],
            [0.41, 1.1820168],
            [0.555, 3.1116448],
            [0.645, 2.7667998]]
    
    df = pd.DataFrame(data, columns = ['concentration (g/L)', 'dry spangles (kg DW-eq/day)'])
    x = df['dry spangles (kg DW-eq/day)'] * 1000 / surface_per_ORP # productivity [g/m2/day]
    y = df['concentration (g/L)']
    
    slope, intercept, r, p, std_err = stats.linregress(x, y)
        
    def myfunc(x):
        return slope * x + intercept
    
    mymodel = list(map(myfunc, x))

    plt.scatter(x, y)
    plt.plot(x, mymodel)
    plt.show()
    
    ### ADD THE DATA FROM 2019 TO TRY TO IMPROVE THE FUNCTION
    concentration = slope * spangle_productivity + intercept
    
    return concentration


def ProductivityToConcentration (tech_period, spangle_daily_areal_productivity, number_ORPs, surface_per_ORP):
    
    if tech_period == '1':
        ## DATA COLLECTED
        dry_spangles_sc1 = 27.53 # amount of dry spangles [kg]
        DM_dry_spangles_sc1 = 96.8 # dry matter content of the paste [%]
        dry_spangles_DW_sc1 = dry_spangles_sc1 * DM_dry_spangles_sc1 / 100 # dry spangles daily productivity [kg DW-eq/day]
        spangle_daily_areal_productivity_sc1 = dry_spangles_DW_sc1 * 1000 / (surface_per_ORP * number_ORPs) # dry spangles daily areal productivity [g DW-eq/m2/day]
        concentration_sc1 = 1.07 # concentration of Spirulina in the broth at harvesting [g/L]
        ## DATA MODELLED
        concentration = spangle_daily_areal_productivity * concentration_sc1 / spangle_daily_areal_productivity_sc1
        
    if tech_period == '2':
        ## DATA COLLECTED
        dry_spangles_sc1 = 15.59 # amount of paste [kg]
        DM_dry_spangles_sc1 = 94.99 # dry matter content of the paste [%]
        dry_spangles_DW_sc1 = dry_spangles_sc1 * DM_dry_spangles_sc1 / 100 # dry spangles daily productivity [kg DW-eq/day]
        spangle_daily_areal_productivity_sc1 = dry_spangles_DW_sc1 * 1000 / (surface_per_ORP * number_ORPs) # dry spangles daily areal productivity [g DW-eq/m2/day]
        concentration_sc1 = 0.64 # concentration of Spirulina in the broth at harvesting [g/L]
        ## DATA MODELLED
        concentration = spangle_daily_areal_productivity * concentration_sc1 / spangle_daily_areal_productivity_sc1
    
    return concentration



def SpirulinaProductionDict (tech_period, spangle_daily_productivity, working_days,
                             harvesting_efficiency, line, distance_car, distance_ship, distance_truck,
                             number_ORPs, surface_per_ORP, VFS_number, volume_ORP, lifetime_file_dir):
    
    ''' Creates the dataset for Spirulina cultivation according to the parameters.
    Dry spangles productivity (g/m2/day) is not considered as an input.Instead,
    the concentration of Spirulina in the broth i.e. culture medium at harvesting
    is considered.'''
    
    from S1A0_building import BuildingDataDict
    from S1A0_operation import OperationDataDict
    from S1A1_cultivation import CultivationDataDict
    from S1A2_filtration import FiltrationDataDict
    from S1A3_dewatering import DewateringDataDict
    from S1A4_shaping import ShapingDataDict
    from S1A5_drying import DryingDataDict
    from S1A6_packaging_wet_line import PackagingWetLineDataDict    
    from S1A6_packaging import PackagingDryLineDataDict
    from S1A7_freezing import FreezingDataDict
    from S1A8_transport import TransportDataDict 
    
    production_data_dict = {}
   
    ## CONVERSION SPANGLES PRODUCTIVITY TO CONCENTRATION
    print('\nCreation of the dataset for Spirulina production in ORPs...')
    print('\nDry spangles daily productivity: %.2f g DW-eq/m2/day (accounts for the pre-processing stages)' %spangle_daily_productivity)
    yearly_production = spangle_daily_productivity * working_days * surface_per_ORP * number_ORPs / 1000 / 1000
    print('Considering this productivity, the annual production over %s working days would be: %.2f ton DW-eq/year' % (working_days, yearly_production))
    dry_matter_content = 94.99 # DM content of the dry spangles measured in 2022 [%]
    yearly_production_wet_mass = (1-dry_matter_content/100) * yearly_production + yearly_production
    print('or %.2f ton/year at a DM content of 94.99 percent as measured in 2022.' %yearly_production_wet_mass)
    concentration = ProductivityToConcentration (tech_period, spangle_daily_productivity, number_ORPs, surface_per_ORP)
    print('Concentration at harvesting: %.2f g/L' %concentration)

    ## COMMON PROCESSES/ACTIVITIES TO THE WET & DRY LINES
    S1A0_Building_data_dict = BuildingDataDict (tech_period, lifetime_file_dir, VFS_number)
    production_data_dict['S1A0Building'] = S1A0_Building_data_dict
    print('S1A0_Building_data_dict done')
    
    S1A0_Operation_data_dict = OperationDataDict (tech_period, line, volume_ORP, number_ORPs, working_days)
    production_data_dict['S1A0Operation'] = S1A0_Operation_data_dict
    print('S1A0_Operation_data_dict done')
        
    S1A2_Filtration_data_dict = FiltrationDataDict (tech_period, harvesting_efficiency, concentration)
    production_data_dict['S1A2Filtration'] = S1A2_Filtration_data_dict
    slurry_DW = S1A2_Filtration_data_dict['slurry']['amount']
    print('S1A2_Filtration_data_dict done')

    S1A3_Dewatering_data_dict = DewateringDataDict (tech_period, slurry_DW)
    production_data_dict['S1A3Dewatering'] = S1A3_Dewatering_data_dict
    paste_DW = S1A3_Dewatering_data_dict['paste']['amount'] 
    print('S1A3_Dewatering_data_dict done')

    
    ## PROCESSES THAT ARE DIFFERENT BETWEEN THE WET & DRY LINES    
    if line == 'dry':
        print('line is dry')
    
        S1A4_Shaping_data_dict = ShapingDataDict (tech_period, paste_DW)
        production_data_dict['S1A4Shaping'] = S1A4_Shaping_data_dict
        wet_spangles_DW = S1A4_Shaping_data_dict['wet_spangles']['amount']  
        print('S1A4_Shaping_data_dict done')
        
        S1A5_Drying_data_dict = DryingDataDict (tech_period, wet_spangles_DW)
        production_data_dict['S1A5Drying'] = S1A5_Drying_data_dict
        dry_spangles_DW = S1A5_Drying_data_dict['dry_spangles']['amount']
        print('S1A5_Drying_data_dict done')
        
        S1A6b_Packaging_data_dict = PackagingDryLineDataDict (tech_period, dry_spangles_DW)
        production_data_dict['S1A6Packaging'] = S1A6b_Packaging_data_dict
        dry_spangles_packaged_DW = S1A6b_Packaging_data_dict['dry_spangles_packaged']['amount']
        print('S1A6b_Packaging_data_dict done')

        S1A8_Transport_data_dict = TransportDataDict (distance_car, distance_ship, distance_truck, dry_spangles_DW, dry_spangles_packaged_DW, line)
        production_data_dict['S1A8Transport'] = S1A8_Transport_data_dict
        print('S1A8_Transport_data_dict done')
        
        broth_DW = S1A2_Filtration_data_dict['broth']['amount']
        S1A1_Cultivation_data_dict = CultivationDataDict (tech_period, harvesting_efficiency, concentration, dry_spangles_DW, broth_DW)
        production_data_dict['S1A1Cultivation'] = S1A1_Cultivation_data_dict
        print('S1A1_Cultivation_data_dict done')
        
        
    if line == 'wet':
        print('line is wet')
        
        S1A6a_Packaging_data_dict = PackagingWetLineDataDict (tech_period, paste_DW)
        production_data_dict['S1A6Packaging'] = S1A6a_Packaging_data_dict
        paste_packaged_DW = S1A6a_Packaging_data_dict['paste_packaged']['amount']
        print('S1A6a_Packaging_data_dict done')
        
        ### NEED TO ADD THE WEIGHT OF PACKAGING
        S1A7_Freezing_data_dict = FreezingDataDict (tech_period, paste_packaged_DW)
        production_data_dict['S1A7Freezing'] = S1A7_Freezing_data_dict
        paste_packaged_frozen_DW = S1A7_Freezing_data_dict['paste_packaged_frozen']['amount']
        print('S1A7_Freezing_data_dict done')
                
        S1A8_Transport_data_dict = TransportDataDict(distance_car, distance_ship, distance_truck, paste_DW, paste_packaged_frozen_DW, line)
        production_data_dict['S1A8Transport'] = S1A8_Transport_data_dict
        print('S1A8_Transport_data_dict done')
        
        dry_spangles_DW = PasteToSpangles (tech_period, paste_DW)
        broth_DW = S1A2_Filtration_data_dict['broth']['amount']
        S1A1_Cultivation_data_dict = CultivationDataDict (tech_period, harvesting_efficiency, concentration, dry_spangles_DW, broth_DW)
        production_data_dict['S1A1Cultivation'] = S1A1_Cultivation_data_dict
        print('S1A1_Cultivation_data_dict done')

    if line != 'wet' and line != 'dry': 
        raise TypeError('The line type should be "dry" or "wet".')
        
    ## ORDER THE DICTIONARY TO HAVE CULTIVATION FIRST
    ordered_production_data_dict = {}
    ordered_production_data_dict['S1A0Building'] = production_data_dict['S1A0Building']
    ordered_production_data_dict['S1A0Operation'] = production_data_dict['S1A0Operation']
    ordered_production_data_dict['S1A1Cultivation'] = production_data_dict['S1A1Cultivation']
    for act in production_data_dict.keys():
        if 'S1A1Cultivation' not in act:
            ordered_production_data_dict[act] = production_data_dict[act]

    production_data_dict = ordered_production_data_dict
    
    print('\nDetails of the biomass flows:')
    print('Amount of broth: %.2f kg DW-eq' %broth_DW)
    print('Amount of slurry: %.2f kg DW-eq' %slurry_DW)
    print('Amount of paste: %.2f kg DW-eq' %paste_DW)
    #print('Amount of wet spangles: %s kg DW-eq' % wet_spangles_DW) # no value for wet spangle in the wet line
    print('Amount of dry spangles: %.2f kg DW-eq' % dry_spangles_DW)
    #print('Amount of dry spangles transported (with packaging): %s kg DW-eq' %dry_spangles_packaged_DW)
    print('Done!\n')
    
    return production_data_dict