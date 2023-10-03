# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 17:10:03 2022

@author: leabr
"""

def PCExtractionDict (tech_period, dry_spangles_DW, PC_content, PC_extraction_eff, distance_truck):
    
    ### S2: PHYCOCYANIN EXTRACTION
    from S2A1_maceration import MacerationDataDict
    from S2A2_centrifugation import CentrifugationDataDict
    from S2A3_filtration import FiltrationDataDict
    from S2A4_ultrafiltration1 import Ultrafiltration1DataDict
    from S2A5_ultrafiltration2 import Ultrafiltration2DataDict
    from S2A6_concentration import ConcentrationCPDDataDict
    from S2A7a_packaging import PackagingBlueExtractDataDict
    from S2A7b_packaging import PackagingCPDConcentrateDataDict
    from S2A7c_packaging import PackagingCPADataDict
    from S2A8_transport import TransportDataDict
    
    ### ADD THE TRANSPORT AND PACKAGING/STORING
    
    PC_extraction_data_dict = {}
    
    S2A1Maceration_data_dict =  MacerationDataDict (tech_period, dry_spangles_DW)
    PC_extraction_data_dict['S2A1Maceration'] = S2A1Maceration_data_dict
    mix_DW = S2A1Maceration_data_dict['mix']['amount']
    
    S2A2Centrifugation_data_dict = CentrifugationDataDict (tech_period, mix_DW, PC_content, PC_extraction_eff)
    PC_extraction_data_dict['S2A2Centrifugation'] = S2A2Centrifugation_data_dict
    supernatant_DW = S2A2Centrifugation_data_dict['supernatant']['amount']
    CPA_DW = S2A2Centrifugation_data_dict['CPA']['amount']
    
    S2A3Filtration_data_dict = FiltrationDataDict (tech_period, supernatant_DW)
    PC_extraction_data_dict['S2A3Filtration'] = S2A3Filtration_data_dict
    filtrate_DW = S2A3Filtration_data_dict['filtrate']['amount']
    
    S2A4Ultrafiltration1_data_dict = Ultrafiltration1DataDict (tech_period, filtrate_DW)
    PC_extraction_data_dict['S2A4Ultrafiltration1'] = S2A4Ultrafiltration1_data_dict
    blue_extract_UF1_DW = S2A4Ultrafiltration1_data_dict['blue_extract_UF1']['amount']
    CPD_DW_UF1 = S2A4Ultrafiltration1_data_dict['CPD']['amount']
    
    S2A5Ultrafiltration2_data_dict = Ultrafiltration2DataDict (blue_extract_UF1_DW)
    PC_extraction_data_dict['S2A5Ultrafiltration2'] = S2A5Ultrafiltration2_data_dict
    blue_extract_UF2_DW = S2A5Ultrafiltration2_data_dict['blue_extract_UF2']['amount']
    CPD_DW_UF2 = S2A5Ultrafiltration2_data_dict['CPD']['amount']
    total_CPD_DW = CPD_DW_UF1 + CPD_DW_UF2
    
    S2A6Concentration_data_dict = ConcentrationCPDDataDict (total_CPD_DW)
    PC_extraction_data_dict['S2A6Concentration'] = S2A6Concentration_data_dict
    CDP_concentrate_DW = S2A6Concentration_data_dict['CPD_concentrate']['amount']
    
    S2A7aPackaging_data_dict = PackagingBlueExtractDataDict(blue_extract_UF2_DW)
    PC_extraction_data_dict['S2A7aPackaging'] = S2A7aPackaging_data_dict
    blue_extract_packaged_DW = S2A7aPackaging_data_dict['blue_extract_packaged']['amount']
    
    S2A7bPackaging_data_dict = PackagingCPDConcentrateDataDict(CDP_concentrate_DW)
    PC_extraction_data_dict['S2A7bPackaging'] = S2A7bPackaging_data_dict
    CPD_concentrate_packaged_DW = S2A7bPackaging_data_dict['CPD_concentrate_packaged']['amount']
    
    S2A7cPackaging_data_dict = PackagingCPADataDict(CPA_DW)
    PC_extraction_data_dict['S2A7cPackaging'] = S2A7cPackaging_data_dict
    CPA_packaged_DW = S2A7cPackaging_data_dict['CPA_packaged']['amount']
    
    S2A8Transport_data_dict = TransportDataDict (distance_truck, CPA_DW, CPA_packaged_DW)
    PC_extraction_data_dict['S2A8Transport'] = S2A8Transport_data_dict
    
    return PC_extraction_data_dict


def CPATreatmentDataDict (tech_period, CPA_DW):
    
    from S3A1_extraction import ExtractionDataDict
    from S3A2_diafiltration import DiafiltrationDataDict
    from S3A3_ultrafiltration import UltafiltrationDataDict
    from S3A4_concentration import ConcentrationCPADataDict
    from S3A5_packaging import PackagingDataDict
    from S3A6_stabilisation import StabilisationDataDict    

    CPA_treatment_data_dict = {}
    
    S3A1Extraction_data_dict = ExtractionDataDict (tech_period, CPA_DW)
    CPA_treatment_data_dict['S3A1Extraction'] = S3A1Extraction_data_dict
    hydrolysate_DW = S3A1Extraction_data_dict['hydrolysate']['amount']
    
    S3A2Diafiltration_data_dict = DiafiltrationDataDict(tech_period, hydrolysate_DW)
    CPA_treatment_data_dict['S3A2Diafiltration'] = S3A2Diafiltration_data_dict    
    permeate_DF_DW = S3A2Diafiltration_data_dict['permeate_DF']['amount']
    retentate_DF_DW = S3A2Diafiltration_data_dict['retentate_DF']['amount']
    
    S3A3Ultrafiltration_data_dict = UltafiltrationDataDict(tech_period, permeate_DF_DW)
    CPA_treatment_data_dict['S3A3Ultrafiltration'] = S3A3Ultrafiltration_data_dict        
    retentate_UF_DW = S3A3Ultrafiltration_data_dict['retentate_UF']['amount']
    permeate_UF_DW = S3A3Ultrafiltration_data_dict['permeate_UF']['amount']
    
    S34AConcentration_data_dict = ConcentrationCPADataDict(retentate_UF_DW)
    CPA_treatment_data_dict['S3A4Concentration'] = S34AConcentration_data_dict            
    concentrate_DW = S34AConcentration_data_dict['concentrate']['amount'] 
    
    S345Packaging_data_dict = PackagingDataDict(concentrate_DW)
    CPA_treatment_data_dict['S3A5Packaging'] = S345Packaging_data_dict            
    concentrate_packaged_DW = S345Packaging_data_dict['concentrate_packaged']['amount'] 
    
    S3A6Stabilisation_data_dict = StabilisationDataDict(concentrate_packaged_DW)
    CPA_treatment_data_dict['S3A6STabilisation'] = S3A6Stabilisation_data_dict            
    concentrate_packaged_stabilised_DW = S3A6Stabilisation_data_dict['concentrate_packaged_stabilised']['amount'] 
    
    return CPA_treatment_data_dict
