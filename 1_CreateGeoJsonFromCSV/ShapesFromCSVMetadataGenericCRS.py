# Name: Create a GeoJson with generic coordinate reference system (CRS) from a CSV file with positional arguments and
# metadata.
# Author: Simon Treier
# Date: 2024-11-08

from osgeo import ogr
import os
import pandas as pd
import numpy as np

# Input file path
df = pd.read_csv(r'/Users/simon/Desktop/Agroscope_PhD/Writing/Thesis/GitHubRepos/ShapeFromCSVHomographyTransform/1_CreateGeoJsonFromCSV/ShapesMetadata.csv', sep=";", encoding='latin1')
df = df.reset_index()  # make sure indexes pair with number of rows

# Output file path
outGeoJSONfn = r'/Users/simon/Desktop/Agroscope_PhD/Writing/Thesis/GitHubRepos/ShapeFromCSVHomographyTransform/1_CreateGeoJsonFromCSV/ShapesRawGenericCRS.geojson'

# Define the extent of the shape rectangles
width_rectan = 16
height_rectan = 145.6

# Definition of the space between rectangles in the units of the generic CRS
buffer_width = 40
buffer_height = 100

# Base shape for the 4-sided shapes is calculated
base_shape = np.array([
    [0, 0],
    [width_rectan, 0],
    [width_rectan, height_rectan],
    [0, height_rectan],
    [0, 0]])

# Create the output shapefile
GeoJSONDriver = ogr.GetDriverByName("GeoJSON")
if os.path.exists(outGeoJSONfn):
    GeoJSONDriver.DeleteDataSource(outGeoJSONfn)
outDataSource = GeoJSONDriver.CreateDataSource(outGeoJSONfn)
outLayer = outDataSource.CreateLayer(outGeoJSONfn, geom_type=ogr.wkbPoint)

# Define fields to be filled with the metadata attributes of the CSV file
idField = ogr.FieldDefn('Plot_seq', ogr.OFTString)
genField = ogr.FieldDefn('Genotype', ogr.OFTString)
columnField = ogr.FieldDefn('Column', ogr.OFTInteger)
treatmentField = ogr.FieldDefn('Treatment', ogr.OFTString)
rowField = ogr.FieldDefn('Row', ogr.OFTInteger)
repField = ogr.FieldDefn('Rep', ogr.OFTInteger)
categoryField = ogr.FieldDefn('Category', ogr.OFTString)
trialField = ogr.FieldDefn('Trial', ogr.OFTString)
yearField = ogr.FieldDefn('Year', ogr.OFTString)

# Add the metadata fields to the output layer
outLayer.CreateField(idField)
outLayer.CreateField(genField)
outLayer.CreateField(rowField)
outLayer.CreateField(columnField)
outLayer.CreateField(treatmentField)
outLayer.CreateField(repField)
outLayer.CreateField(categoryField)
outLayer.CreateField(trialField)
outLayer.CreateField(yearField)

# In a loop, for each entry in the CSV file, coordinates are calculated as based on the "Row" and "Column" arguments of
# the CSV file and rectangle and buffer dimensions defined above.
for index, row in df.iterrows():
    print(row['Plot_seq'], row['Genotype'], row['Row'], row['Column'], row['Treatment'], row['Rep'], row['Category'],
          row['Trial'], row['Year'])

    # Calculate coordinates of the ne shape
    x_internal = [((width_rectan + buffer_width) * (34-int(row['Row'])-1)) + cord[0] for cord in base_shape]
    y_internal = [((height_rectan + buffer_height) * (int(row['Column']))) + cord[1] for cord in base_shape]

    # Create a ring geometry from coordinates
    square = ogr.Geometry(ogr.wkbLinearRing)
    square.AddPoint(float(x_internal[0]), float(y_internal[0]))
    square.AddPoint(float(x_internal[1]), float(y_internal[1]))
    square.AddPoint(float(x_internal[2]), float(y_internal[2]))
    square.AddPoint(float(x_internal[3]), float(y_internal[3]))
    square.AddPoint(float(x_internal[4]), float(y_internal[4]))

    # Create polygon from ring geometry
    polygon = ogr.Geometry(ogr.wkbPolygon)
    polygon.AddGeometry(square)
    print(polygon.ExportToWkt())

    # Populate metadata fields with values from the CSV
    featureDefn = outLayer.GetLayerDefn()
    outFeature = ogr.Feature(featureDefn)
    outFeature.SetGeometry(polygon)
    outFeature.SetField('Plot_seq', row['Plot_seq'])
    outFeature.SetField('Genotype', row['Genotype'])
    outFeature.SetField('Row', row['Row'])
    outFeature.SetField('Column', row['Column'])
    outFeature.SetField('Treatment', row['Treatment'])
    outFeature.SetField('Rep', row['Rep'])
    outFeature.SetField('Category', row['Category'])
    outFeature.SetField('Trial', row['Trial'])
    outFeature.SetField('Year', row['Year'])

    outLayer.CreateFeature(outFeature)

    # dereference the features
    outFeature = None

# Save and close DataSources
outDataSource = None

