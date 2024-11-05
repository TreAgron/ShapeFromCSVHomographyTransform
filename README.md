# Shape creation and geometric transformation using homography

This repository is a tutorial to create 4-sided polygons as shapes as plot masks for agricultural trials. It contain two steps:

1. A GeoJson file is created in Python based on a CSV file that contains meta data
1. The GeoJson is transformed based on the homography calculated from four corresponding points



It contains a description of the process, example code and all example data required. It's suggested to work through this example and make it run on your computer before you try it on your own data.

This repository is related to the publication "PhenoCams", published in [The Plant Phenome Journal](https://acsess.onlinelibrary.wiley.com/journal/25782703?utm_source=google&utm_medium=paidsearch&utm_campaign=R3MR425&utm_content=LifeSciences&gad_source=1&gclid=Cj0KCQiAoae5BhCNARIsADVLzZcx_z2oN_tmu4lxL6P_ClUyUV0RayKF0oClDRJePuZDpdBW5dsR6c8aAkmBEALw_wcB) ([Add DOI here](Add DOI here)).

The research was conducted at and financed by [Agroscope](https://www.agroscope.admin.ch) in the group of [Cultivation Techniques and Varieties in Arable Farming](https://www.agroscope.admin.ch/agroscope/en/home/about-us/organization/competence-divisions-strategic-research-divisions/plant-production/cultivation-techniques-varieties-arable-farming.html).

## Generating shape files to 

This protocol present a pipeline to use multi-view back projection for analyzing thermal images that were taken with a drone. Compared to analyzing thermal images on orthomosaics directly, this approach allows to include effects of measurement time and viewing geometry in the analysis as well as to improve spatial correction of the measurements. Same as for the orthomosaic analysis, images have to be aligned but the analysis is done on single images instead of orthomosaics by means back projection. Aligning the images is only done to orient the single images in space for analysis (georeferencing).
The approach can be used to analyse thermal images that were taken during a drone mapping campaign of an agricultural plot experiments.

## Tutorial

The numbered folders contain code and/or instruction on the respective step, the folders without numbering contain example data. Work through the code in the order indicated. Inside the folders, the different processing steps and files are described. 

In short:
1. Plot shape files are created in Python and and georeferenced in Qgis
1. Images are aligned in Agisoft Metashape
1. Shapes are projected on single images
1. From radiometric .jpg files, .tiff files are derived that represent temperature as [C°] * 1000 
1. Plot-wise temperature is extracted (plot-wise mean and all percentiles for all image-plot combinations)
1. Plot centroids are extracted for subsequent calculations of viewing geometries
1. Viewing geometries are calculated and timestamps extracted for each plot on each images, the final percentile for further data analysis is chosen at this step
1. Single output files are merged to a complete file for subsequent analysis, e.g. in R

Alle  data for this example is provided, also the results of single steps that provide the input of a subsequent step are provided.

![Example of Agisoft](Images/AgisoftExample.PNG)
*Example of aligned thermal images in an Agisoft project.*

![Examle of a geojson shape file ](Images/GeoJson.png)
*Example of a geojson shape file. Different colours indicate different experimental treatments. Centroids are in red. Background is a georeferenced DEM.*


### Code for spatial correction in R-Package SpATS

A basic code for temporal/spatial correction in SpATS to provide a starting point:

Load the SpATS package:
```R
library(SpATS)
```
Example of spats model for temporal/spatial correction:
```R
SpATS_fit_SpATS_aggreg <- SpATS(response = "Trait_of_Interest",
				random = ~ Xf + Yf + Plot_label + FlightDuratExposF +
				genotype:block_factor_names.treatment +
				block_factor_names.treatment:block_factor_names.replication,
				fixed = ~ block_factor_names.treatment,
				spatial = ~PSANOVA(X, Y, nseg = c(nX, nY), nest.div = c(1,1)),
				genotype = "genotype", genotype.as.random = TRUE, data = df_for_correction,
				weights = df_for_correction$weights,
				control = list(maxit = 100, tolerance = 1e-03, monitoring = 0))
```
