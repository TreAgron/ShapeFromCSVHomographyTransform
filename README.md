# Shape creation and geometric transformation using homography

This repository is a tutorial to create 4-sided polygons as shapes as plot masks for agricultural trials. It contain two steps:

1. A GeoJson file is created in Python based on a CSV file that contains meta data
1. The GeoJson is transformed based on the homography calculated from four corresponding points

It contains a description of the process, example code and all example data required. It's suggested to work through this example and make it run on your computer before you try it on your own data.

This repository is related to the publication "PhenoCams", published in [The Plant Phenome Journal](https://acsess.onlinelibrary.wiley.com/journal/25782703?utm_source=google&utm_medium=paidsearch&utm_campaign=R3MR425&utm_content=LifeSciences&gad_source=1&gclid=Cj0KCQiAoae5BhCNARIsADVLzZcx_z2oN_tmu4lxL6P_ClUyUV0RayKF0oClDRJePuZDpdBW5dsR6c8aAkmBEALw_wcB) ([Add DOI here](Add DOI here)).

The research was conducted at and financed by [Agroscope](https://www.agroscope.admin.ch) in the group of [Cultivation Techniques and Varieties in Arable Farming](https://www.agroscope.admin.ch/agroscope/en/home/about-us/organization/competence-divisions-strategic-research-divisions/plant-production/cultivation-techniques-varieties-arable-farming.html).

## Generating shape files to mask plots in agricultural experiments

This protocol present a pipeline to use multi-view back projection for analyzing thermal images that were taken with a drone. Compared to analyzing thermal images on orthomosaics directly, this approach allows to include effects of measurement time and viewing geometry in the analysis as well as to improve spatial correction of the measurements. Same as for the orthomosaic analysis, images have to be aligned but the analysis is done on single images instead of orthomosaics by means back projection. Aligning the images is only done to orient the single images in space for analysis (georeferencing).
The approach can be used to analyse thermal images that were taken during a drone mapping campaign of an agricultural plot experiments.

![Example of shape files generated from CSV](Images/ShapesRawQgis.PNG)
*Example of shape files generated from CSV.*
