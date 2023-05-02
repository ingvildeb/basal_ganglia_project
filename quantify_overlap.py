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


## SETUP: PATHS AND ATLAS NAME

other_atlas = "Swanson_v3"
other_atlas_regions_file = "Z:/NESYS_Lab/PostDoc_project_Bjerke/Manuscripts/WHSv4_Basal ganglia/04_Material/Swa_colors.xlsx"
nutil_out_dir = "Z:/NESYS_Lab/PostDoc_project_Bjerke/Manuscripts/WHSv4_Basal ganglia/04_Material/nutil_Swav3Regions/"

analysis_dir = "Z:/NESYS_Lab/PostDoc_project_Bjerke/Manuscripts/WHSv4_Basal ganglia/04_Material/quantitative_overlap_analysis/"
WHS_regions_file = "Z:/NESYS_Lab/PostDoc_project_Bjerke/Manuscripts/WHSv4_Basal ganglia/04_Material/WHS_colors.xlsx"




## SETUP: COLORS AND REGION NAMES

other_atlas_regions = pd.read_excel(other_atlas_regions_file)
other_atlas_region_names = list(other_atlas_regions["Name"])
other_atlas_regions_abbreviations  = list(other_atlas_regions["Abbreviation"])


WHS_regions = pd.read_excel(WHS_regions_file)
WHS_region_names  = list(WHS_regions["Region"])
WHS_abbreviations = list(WHS_regions["Abbreviation"])

WHS_colors = grf.set_region_colors(WHS_regions_file, file_type = "excel")
WHS_colors_dict = dict(zip(WHS_region_names, WHS_colors))
WHS_abbrevs_dict = dict(zip(WHS_region_names, WHS_abbreviations))




## CREATE SUMMARY REPORTS OF SECTIONWISE PROPORTIONS OF ATLAS REGIONS IN WHS REGIONS

for name in other_atlas_region_names:    
    
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
            # this answers the question: "how much of area x in atlas y is located in area x in atlas z", or "how much of the nucleus accumbens shell of paxinos is located in the nucleus accumbens shell of waxholm?"
            # it does not answer the question of how much of area x in atlas z is occupied by area x in atlas y.
            proportion = selection["Object pixels"] / selection["Object pixels"].sum()
            
            # append proportion dfs to list
            proportion_other_atlas_reg_in_whs_list.append(proportion) 
            
        # create a dataframe of all the proportion dfs in the list, generated in the loop above
        proportion_other_atlas_reg_in_whs_df = pd.concat(proportion_other_atlas_reg_in_whs_list)
            
        # add proportions to the final dataframe
        df[name + "-in-WHS_Proportion"] = proportion_other_atlas_reg_in_whs_df
        
      
        # write dataframe to excel with the region name
        df.to_excel(analysis_dir + other_atlas + "/" + name + "_summary.xlsx")
        

    

## SETUP FOR PLOTS AND TABLES

# create a dictionary of summaries needed for plots and tables

dict_of_summaries = {}

for name in other_atlas_region_names:
    

    # find and read the summary file    
    summary_path = analysis_dir + other_atlas + "/" + name + "_summary.xlsx"
    summary = pd.read_excel(summary_path)
     
    # create a list of all the uniqe section numbers in the summary and divide them into three arrays, defined as rostral, middle and caudal sections
    unique_sections = unique_list(summary["Section"])
    rostral_sections, mid_sections, caudal_sections = split_array(unique_sections)
    
    
    # create a list of corresponding segment name for all the sections in the summary file
    
    segment_list = []
    
    for section in summary["Section"]:
        if section in rostral_sections:
            segment = "Rostral"
        if section in mid_sections:
            segment = "Middle"
        if section in caudal_sections:
            segment = "Caudal"
        segment_list.append(segment)
    
    # add the list of segment name to the summary dataframe. each row is now assigned to a segment.
    summary["Segment"] = segment_list
    summary = summary[["Segment", "Section", "Region", "Load", "Object pixels", "Region pixels", name + "-in-WHS_Proportion"]]
    
    dict_of_summaries[name] = summary
    
# make a list of all the WHS regions that are included in any summary

included_WHS_regions = []

for name in other_atlas_region_names:
        
    summary = dict_of_summaries[name]  
    regions = summary["Region"].tolist()
    
    included_WHS_regions.append(regions)
    
included_WHS_regions_flat = [i for sublist in included_WHS_regions for i in sublist]
included_unique_WHS_regions = unique_list(included_WHS_regions_flat)

included_abbreviations = []
for name in included_unique_WHS_regions:
    included_abbreviation = WHS_abbrevs_dict.get(name)
    included_abbreviations.append(included_abbreviation)
    


### PLOTS AND TABLES   


# create summaries of segment-wise proportions, to be used in pie charts
for name in other_atlas_region_names:
    
    summary = dict_of_summaries[name]
    
    # calculate the sum of each column, grouped by segment and WHS region (this sums the object pixels for all section in a segment / region)
    summary_sum = summary.groupby(["Segment", "Region"]).sum()  
    summary_sum = summary_sum.reset_index()
    summary_sum = summary_sum.drop(["Section"], axis=1)
    
    # calculate proportions per segment
    
    segments = ["Rostral", "Middle", "Caudal"]
    
    list_of_proportions = []
    list_of_names = []
    list_of_segments = []
    
    for segment in segments:
        
        selection = summary_sum[summary_sum["Segment"] == segment]
        total_object_pixels = selection["Object pixels"].sum()
        proportions = (selection["Object pixels"] / total_object_pixels)
        region = selection["Region"]
        segment_n = selection["Segment"]
        proportions = proportions.tolist()
        list_of_proportions.append(proportions)
        list_of_names.append(region)
        list_of_segments.append(segment_n)
        

    list_of_proportions = [i for sublist in list_of_proportions for i in sublist]
    list_of_names = [i for sublist in list_of_names for i in sublist]
    list_of_segments = [i for sublist in list_of_segments for i in sublist]
    
    segmentwise_proportions = pd.DataFrame()
    segmentwise_proportions["Segment"] = list_of_segments
    segmentwise_proportions["Region"] = list_of_names
    segmentwise_proportions["Proportion"] = list_of_proportions
   
    segmentwise_proportions.to_excel(analysis_dir + other_atlas + "/" + name + "_summary_per_segment.xlsx")    


# plot pie charts of region overlap per segment (rostral, middle, caudal)
    
    fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(12, 5))
    
    for segment, ax in zip(segments, axs.flat):
        
        to_plot_b = segmentwise_proportions[segmentwise_proportions['Segment'] == segment]
        labels = to_plot_b['Region']
        texts, autotexts, wedges = ax.pie(to_plot_b["Proportion"], shadow=False, colors=[WHS_colors_dict[key] for key in labels], startangle=90, textprops=dict(color="black"), autopct='')

        ax.set_title(segment, size=16, weight="bold", y=-0.05)    
        ax.legend(texts, labels, loc=6, mode="expand", bbox_to_anchor=(0, -0.30, 1, 0))
        
    plt.tight_layout()
    fig.suptitle(name)
    plt.savefig(analysis_dir + other_atlas + "/" + name + '_pie.svg', bbox_inches='tight', pad_inches=0.05, dpi=600)
    plt.show()
    

    


# create tables of overlap per atlas region in waxholm  (all sections and segments analyzed as one)   
    
table = pd.DataFrame()
table["Region"] = included_unique_WHS_regions 
table["Abbreviation"] = included_abbreviations

for name in other_atlas_region_names:
    summary = dict_of_summaries[name]
    
    WHS_regions_in_summary = list(summary["Region"])
    WHS_regions_in_summary = unique_list(WHS_regions_in_summary)
    total_object_pixels = summary["Object pixels"].sum()
    table[name] = ""
       
    for region in WHS_regions_in_summary:
        selection = summary.loc[summary["Region"] == region]
        proportion = selection["Object pixels"].sum() / total_object_pixels
        proportion = float(proportion)
        regindex = table.index[table["Region"] == region]
        table.loc[regindex, name] = proportion
        
table.columns = ["WHS region", "WHS abbreviation", *other_atlas_regions_abbreviations]   
table.to_excel(analysis_dir + other_atlas + "/" + other_atlas + "_summary_all_regions.xlsx")
    




















                

    
