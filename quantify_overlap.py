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
import nutil_scripts.graphing_functions as grf


def split_array(arr):
    n = len(arr)
    q, r = divmod(n, 3)
    return [arr[:q] , arr[q:q+q+r], arr[q+q+r:]]


def unique_list(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]


other_atlas = "Paxinos_v6"
other_atlas_regions_file = "Z:/NESYS_Lab/PostDoc_project_Bjerke/Manuscripts/WHSv4_Basal ganglia/04_Material/Pax_colors.xlsx"

nutil_out_dir = "Z:/NESYS_Lab/PostDoc_project_Bjerke/Manuscripts/WHSv4_Basal ganglia/04_Material/nutil_Paxv6Regions/"
analysis_dir = "Z:/NESYS_Lab/PostDoc_project_Bjerke/Manuscripts/WHSv4_Basal ganglia/04_Material/quantitative_overlap_analysis/"



other_atlas_regions = pd.read_excel(other_atlas_regions_file)
other_atlas_regions_list = list(other_atlas_regions["Name"])


WHS_regions_file = "Z:/NESYS_Lab/PostDoc_project_Bjerke/Manuscripts/WHSv4_Basal ganglia/04_Material/WHS_colors.xlsx"
WHS_regions = pd.read_excel(WHS_regions_file, usecols = ["Region"])
WHS_regions  = list(WHS_regions["Region"])

WHS_colors = grf.set_region_colors(WHS_regions_file, file_type = "excel")
WHS_colors_dict = dict(zip(WHS_regions, WHS_colors))

## CREATE SUMMARY REPORTS OF SECTIONWISE PROPORTIONS OF ATLAS REGIONS IN WHS REGIONS

for name in other_atlas_regions_list:    
    
        # find all sectionwise reports
    
        report_dir = nutil_out_dir + "output_dir_" + name + "/Reports/RefAtlasRegions//"   
        reports = glob(report_dir + "*_s*.csv")
        
        # create empty list, to be populated with the section number of the report
        
        section_list = []
        
        # create empty lists, to be populated with load, region name, object pixel and region pixels from reports
        
        load_list = []
        region_list = []
        obj_pixel_list = []
        region_pixel_list = []
        
        
        # loop through sectionwise reports
        
        for report in reports:
            
            #read the report and the section number
            
            data = pd.read_csv(report, sep=";")            
            section = (report.split(sep="_s")[-1]).split(sep=".")[0]            
            
            # get the loads, regions, object pixels and region pixels from the sectionwise report
            
            loads = data["Load"]
            regions = data["Region Name"]
            obj_pixels = data["Object pixels"]
            region_pixels = data["Region pixels"]
                            
                
            for region, load, obj_pixel, region_pixel in zip(regions, loads, obj_pixels, region_pixels):                        
                
                # create lists of load, region name, object pixel, section number and region pixels, only if the load is > 0
                # the section number is appended for the same length as the zipped lists
                
                if load > 0:

                    region_list.append(region)
                    load_list.append(load)
                    obj_pixel_list.append(obj_pixel)
                    section_list.append(section)
                    region_pixel_list.append(region_pixel)
                
        # create a dataframe with the selected loads, region names, object pixels and region pixels   
        df = pd.DataFrame()
        
        df["Section"] = section_list        
        df["Region"] = region_list
        df["Load"] = load_list
        df["Object pixels"] = obj_pixel_list
        df["Region pixels"] = region_pixel_list
        


        # get a list of the unique section numbers for the data        
        unique_sections = unique_list(section_list)
        
        
        # calculate proportion of the other atlas region that is in each WHS region, weighed by its total size in each section
        proportion_other_atlas_reg_in_whs_list = []
        
        # loop through unique section list
        
        for section in unique_sections:
            
            # select all the rows for the section
            selection = df.loc[df["Section"] == section]
            
            # divide each of the selected object pixel values by the sum of all the object pixels in the section (i.e. size of the area in region x / total size of the area)
            proportion = selection["Object pixels"] / selection["Object pixels"].sum()
            
            # append proportion dfs to list
            proportion_other_atlas_reg_in_whs_list.append(proportion) 
            
        # create a dataframe of all the proportion dfs in the list, generated in the loop above
        proportion_other_atlas_reg_in_whs_df = pd.concat(proportion_other_atlas_reg_in_whs_list)
            
        # add proportions to the final dataframe
        df[name + "-in-WHS_Proportion"] = proportion_other_atlas_reg_in_whs_df
        
      
        # write dataframe to excel with the region name
        df.to_excel(analysis_dir + other_atlas + "/" + name + "_summary.xlsx")
        



    




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

    




















                

    
