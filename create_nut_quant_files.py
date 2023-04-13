# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import create_nut_file_functions as nff
import pandas as pd
import os


metadata = r"Z:\NESYS_Lab\PostDoc_project_Bjerke\Manuscripts\WHSv4_Basal ganglia\04_Material\Pax_colors.xlsx"
metadata_df = pd.read_excel(metadata)

region_names = list(metadata_df["Name"])          
R = list(metadata_df["R"])     
G = list(metadata_df["G"]) 
B = list(metadata_df["B"]) 

for name in region_names:
    os.mkdir("Z:/NESYS_Lab/PostDoc_project_Bjerke/Manuscripts/WHSv4_Basal ganglia/04_Material/nutil_Paxv6Regions/output_dir_" + name)



for name, r, g, b in zip(region_names, R, G, B):
    
    
        
    r = str(r)
    g = str(g)
    b = str(b)
    
        
    nff.write_nut_quant_file(filename = name + "_quantifier", storepath = "Z:/NESYS_Lab/PostDoc_project_Bjerke/Manuscripts/WHSv4_Basal ganglia/04_Material/nutil_Paxv6Regions/nut_files//", 
                             quantifier_input_dir = "Z:/NESYS_Lab/PostDoc_project_Bjerke/Manuscripts/WHSv4_Basal ganglia/04_Material/nutil_Paxv6Regions/input_dir", 
                             quantifier_atlas_dir = "Z:/NESYS_Lab/PostDoc_project_Bjerke/Manuscripts/WHSv4_Basal ganglia/04_Material/nutil_Paxv6Regions/atlas_dir/atlas_maps",
                             xml_anchor_file = "Z:/NESYS_Lab/PostDoc_project_Bjerke/Manuscripts/WHSv4_Basal ganglia/04_Material/nutil_Paxv6Regions/atlas_dir/RBSC_PW_v6__cor_anchoring_nonlin-new.json",
                             quantifier_output_dir = "Z:/NESYS_Lab/PostDoc_project_Bjerke/Manuscripts/WHSv4_Basal ganglia/04_Material/nutil_Paxv6Regions/output_dir_" + name,
                             extraction_color = r + "," + g + "," + b, label_file = "WHS Atlas Rat v4",
                             object_splitting = "Yes")
        