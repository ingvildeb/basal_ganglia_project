# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 11:45:11 2023

@author: ingvieb
"""

import numpy as np
import pandas as pd
from glob import glob
import os.path
from os import path
import matplotlib.pyplot as plt



def split_array(arr):
    n = len(arr)
    q, r = divmod(n, 3)
    return [arr[:q] , arr[q:q+q+r], arr[q+q+r:]]


def set_region_colors(input_file, R_col = "R", G_col = "G", B_col = "B"):    
    regioncolors = pd.read_excel(input_file, usecols = [R_col, G_col, B_col])
    regioncolors = regioncolors / 255
        
    rgb_colors = []

    for index, row in regioncolors.iterrows():
        rgb = (row[R_col], row[G_col], row[B_col])
        rgb_colors.append(rgb)
    
    return rgb_colors


def unique_list(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]



region_file = r"Z:\NESYS_Lab\PostDoc_project_Bjerke\Manuscripts\WHSv4_Basal ganglia\04_Material\Pax_colors.xlsx"

paxregions = pd.read_excel(region_file)
pax_region_list = paxregions.Name.values.tolist()


for paxregion in pax_region_list:    
    
        report_dir = "Z:/NESYS_Lab/PostDoc_project_Bjerke/Manuscripts/WHSv4_Basal ganglia/04_Material/nutil_Paxv6Regions/output_dir_" + paxregion + "/Reports/RefAtlasRegions//"   
        reports = glob(report_dir + "*_s*.csv")
        
        load_list = []
        region_list = []
        pixel_list = []
        section_list = []
        
        
        for report in reports:
            data = pd.read_csv(report, sep=";")
            
            section = (report.split(sep="_s")[-1]).split(sep=".")[0]
        
            loads = data["Load"]
            regions = data["Region Name"]
            pixels = data["Object pixels"]
                
                
            for region, load, pixel in zip(regions, loads, pixels):                        
                
                if load > 0:
                    #print(key, value)
                    region_list.append(region)
                    load_list.append(load)
                    pixel_list.append(pixel)
                    section_list.append(section)
                
           
        df = pd.DataFrame()
        
        df["Section"] = section_list
        
        df["Region"] = region_list
        df["Load"] = load_list
        df["Pixel"] = pixel_list
        
        

        
        
        unique_sections = unique_list(section_list)
        proportion_pax_in_whs_list = []
        
        for section in unique_sections:
            selection = df.loc[df["Section"] == section]
            proportion = selection["Pixel"] / selection["Pixel"].sum()
            proportion_pax_in_whs_list.append(proportion) 
            
        
        proportion_pax_in_whs_df = pd.concat(proportion_pax_in_whs_list)
            
        df["Pax-in-WHS_Proportion"] = proportion_pax_in_whs_df
        
        
        df.to_excel(r"Z:\NESYS_Lab\PostDoc_project_Bjerke\Manuscripts\WHSv4_Basal ganglia\04_Material\quantitative_overlap_analysis\\" + paxregion + "_summary.xlsx")



    

WHS_colors = pd.read_excel("Z:/NESYS_Lab/PostDoc_project_Bjerke/Manuscripts/WHSv4_Basal ganglia/04_Material/WHS_colors.xlsx")




new_colors = set_region_colors("Z:/NESYS_Lab/PostDoc_project_Bjerke/Manuscripts/WHSv4_Basal ganglia/04_Material/WHS_colors.xlsx")
new_color_dict = dict(zip(WHS_colors.Region, new_colors))


WHS_regions = []

for paxregion in pax_region_list:

        
    summary = "Z:/NESYS_Lab/PostDoc_project_Bjerke/Manuscripts/WHSv4_Basal ganglia/04_Material/quantitative_overlap_analysis/Paxinos_v6/" + paxregion + "_summary.xlsx"
    summary = pd.read_excel(summary)
    unique_sections = unique_list(summary["Section"])
    rostral_sections, mid_sections, caudal_sections = split_array(unique_sections)
    
    segment_list = []
    for s in summary["Section"]:
        if s in rostral_sections:
            segment = "Rostral"
        if s in mid_sections:
            segment = "Middle"
        if s in caudal_sections:
            segment = "Caudal"
        segment_list.append(segment)
    
    summary["Segment"] = segment_list
    
    #summary_mean = summary.groupby(["Segment", "Region"]).mean()
    summary_mean = summary.groupby(["Region"]).mean()

    summary_mean = summary_mean.reset_index()
    
    props = summary_mean["Pax-in-WHS_Proportion"]
    regs = summary_mean["Region"]
    #to_plot = summary_mean[["Segment", "Region", "Pax-in-WHS_Proportion"]]
    to_plot = summary_mean[["Region", "Pax-in-WHS_Proportion"]]
    to_plot["PaxRegion"] = paxregion

    to_plot.to_excel(r"Z:\NESYS_Lab\PostDoc_project_Bjerke\Manuscripts\WHSv4_Basal ganglia\04_Material\quantitative_overlap_analysis\Paxinos_v6\\" + paxregion + "_summary_segments_combined.xlsx")
    
    WHS_regions.append(regs.tolist())

    segments = ["Rostral", "Middle", "Caudal"]
    
    fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(12, 5))

    
    for segment_i, ax in zip(segments, axs.flat):
        to_plot_b = to_plot[to_plot['Segment'] == segment_i]
        labels = to_plot_b['Region']
        texts, autotexts, wedges = ax.pie(to_plot_b['Pax-in-WHS_Proportion'], shadow=False, colors=[new_color_dict[key] for key in labels], startangle=90, textprops=dict(color="black"), autopct='')

        ax.set_title(segment_i, size=16, weight="bold", y=-0.05)

    
        ax.legend(texts, labels, loc=6, mode="expand", bbox_to_anchor=(0, -0.30, 1, 0))
        
    plt.tight_layout()
    fig.suptitle(paxregion)
    plt.savefig("Z:/NESYS_Lab/PostDoc_project_Bjerke/Manuscripts/WHSv4_Basal ganglia/04_Material/quantitative_overlap_analysis/Paxinos_v6/" + paxregion + '_pie.svg', bbox_inches='tight', pad_inches=0.05, dpi=600)
    plt.show()















WHS_regions = []

for paxregion in pax_region_list:
        
    report = r"Z:\NESYS_Lab\PostDoc_project_Bjerke\Manuscripts\WHSv4_Basal ganglia\04_Material\quantitative_overlap_analysis\Paxinos_v6\\" + paxregion + "_summary_segments_combined.xlsx"
    report = pd.read_excel(report)
    
    regions = report["Region"].tolist()
    
    WHS_regions.append(regions)




WHS_regions_flat = [i for sublist in WHS_regions for i in sublist]
unique_WHS_regions = unique_list(WHS_regions_flat)

table = pd.DataFrame(unique_WHS_regions)
table.columns = ["Region"]


for paxregion in pax_region_list:
    
    report = r"Z:\NESYS_Lab\PostDoc_project_Bjerke\Manuscripts\WHSv4_Basal ganglia\04_Material\quantitative_overlap_analysis\Paxinos_v6\\" + paxregion + "_summary_segments_combined.xlsx"
    report = pd.read_excel(report)
    
    regs_in_report = report["Region"].tolist()
    
    table[paxregion] = ""
    
    for reg in regs_in_report:
        selection = report.loc[report["Region"] == reg]
        value = selection["Pax-in-WHS_Proportion"]
        value = float(value)
        paxreg = selection["PaxRegion"]

                
        
        regindex = table.index[table["Region"] == reg]
        table.loc[regindex, paxreg] = value

    




















                

    
