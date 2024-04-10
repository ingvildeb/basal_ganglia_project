# Scripts for quantitative spatial analysis of basal ganglia annotations across atlases

This repository contains the code used for the quantitative comparison of basal ganglia annotations in Brain Maps and The Rat Brain in Stereotaxic Coordinates with regions in the Waxholm Space rat brain atlas. This analysis is part of the publication "Anatomy of the rat and mouse basal ganglia: Understanding terms and boundaries across brain atlases" by Kleven H, Schlegel U, Groenewegen HJ, Leergaard TB, Bjerke IE (in preparation).

The data related to the analysis is available on the EBRAINS Knowledge Graph (ref), including excel sheets that are used in the scripts. However, due to copyright restrictions, we can only share the full raw data (including atlas plate images) for Brain Maps. 


**The following scripts are included:**

- ***quantitative_overlap_create-nut-quant-files:*** Used to batch create nutil quantifier files. The functions used for this can be found in the nutil scripts repository.
- ***quantify_overlap:*** Used to post-process results from nutil quantified, and create the pie charts presented in the paper.
