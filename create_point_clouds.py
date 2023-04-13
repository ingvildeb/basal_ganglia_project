# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 17:48:12 2023

@author: ingvieb
"""

#POINT CLOUD THAT REPRESENTS THE AVERAGE OF ALL ADULT MICE

#STEP 1: Create probability map

#STEP 2: Load numbers of cells per region

#Place cells in each region based on probabilities

from tqdm import tqdm
import nibabel as nib
import nrrd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd




#we are going to place cells in atlas regions based on both the precomupted counts and probabilities
#here we open the probability volume and atlas delineations we will need for this
prob_path = r"C:\Users\ingvieb\Downloads/heat_volume_interpolated_smoothed_half_res_16bit_int(1).nii.gz"
atlas_path = r"C:\Users\ingvieb\Downloads/annotation_25.nrrd"
prob_volume = np.array(nib.load(prob_path).dataobj)
atlas_volume, atlas_header =  nrrd.read(atlas_path)

#the probability volume is in a different orientation than the atlas so we swap the axes to make it match
prob_volume = np.transpose(prob_volume, (1, 2, 0))

#we need to know the number of cells per custom region so we open the precomputed excel file
path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\Derived_data//descriptive_statistics_D1R.xlsx"
cell_numbers_file = pd.ExcelFile(path)
cell_numbers = pd.read_excel(cell_numbers_file, 'Totals_by_age')


#we need to be able to look at the custom regions in atlas space, this file has the atlas ids in each custom region
regionID_path = r"Y:\Dopamine_receptors\Analysis\resources/ID_to_custom.xlsx"
regionIDs = pd.read_excel(regionID_path)
idx = 0
meshViewList = []
#iterate through unique custom regions
for region in tqdm(regionIDs['custom region'].unique()):
    #here we create a mask for the pandas dataframe that will give us the rows of the dataframe for this custom region
    maskDF= regionIDs['custom region'] == region
    customRegionIDs = regionIDs[maskDF]['region ID'].values
    #this gives a mask where the atlas volume regions are in the custom region
    custom_region_atlas_mask = np.isin(atlas_volume, customRegionIDs)
    # we will use this mask to get the probability map for only these voxels 
    custom_region_prob_volume = prob_volume[custom_region_atlas_mask]
    custom_region_all_coordinates = np.argwhere(custom_region_atlas_mask)
    #now we get the precomputed cell numbers for this region
    region_column_number = np.where(cell_numbers.columns == region)[0][0]
    #since excel gives the column names a funny formatting we need to add 1 to the column that is equal to the region as this will be the mean
    region_mean_column_number = region_column_number + 1
    #we use this as the column index and 6 as the row index to get the count for P70
    target_cell_number = cell_numbers.iloc[6,region_mean_column_number]
    #if theres no cell number then skip the loops
    if np.sum(custom_region_prob_volume) == 0:
        continue
    if np.isnan(target_cell_number):
        continue
    index = list(range(len(custom_region_all_coordinates)))
    custom_region_prob_volume = custom_region_prob_volume[~np.isnan(custom_region_prob_volume)]
    custom_region_prob_volume = custom_region_prob_volume / np.sum(custom_region_prob_volume)

    index = np.array(index)
    index = index[~np.isnan(custom_region_prob_volume)]
    chosen_index = np.random.choice(index, int(target_cell_number), p=custom_region_prob_volume)
    chosen_coordinates = custom_region_all_coordinates[chosen_index]
    chosen_coordinates_flatten = chosen_coordinates.flatten()
    chosen_coordinates_flatten_random = chosen_coordinates_flatten + np.random.uniform(0.0, 0.5, len(chosen_coordinates_flatten))
    
    # print("-------------------------------------")
    # print("non_zero_voxels: ", np.sum(custom_region_prob_volume!=0))
    # print("target_number_cells" , target_cell_number)
    region_cells = {"idx": idx ,
                    "count":target_cell_number,
                    "r":38,
                    "g":143,
                    "b":69,
                    "name":region,
                    "triplets" : chosen_coordinates_flatten_random.tolist()
                    }
    meshViewList.append(region_cells)
    idx += 1


import json
with open('average-cloud-d1.json', 'w') as f:
    json.dump(meshViewList, f)



   # {
   #      "idx": 0,
   #      "count": 1891,
   #      "r": 38,
   #      "g": 143,
   #      "b": 69,
   #      "name": "Frontal pole, cerebral cortex",
   #      "triplets": [