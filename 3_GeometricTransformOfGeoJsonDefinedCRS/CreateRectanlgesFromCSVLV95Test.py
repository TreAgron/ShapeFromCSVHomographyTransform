# Run in /Users/simon/PycharmProjects/envs/GeoGDALPy39

from osgeo import ogr
import osgeo.osr as osr
import os
import pandas as pd
import numpy as np

# df = pd.read_csv('/Users/simon/PycharmProjects/Scripts/GeoPandas/Innov_22.csv')
df = pd.read_csv(r'/Users/simon/Desktop/Agroscope_PhD/Writing/Thesis/GitHubRepos/ShapeFromCSVHomographyTransform/1_CreateGeoJsonFromCSV/ShapesMetadata.csv', sep=";", encoding='latin1')
df = df.reset_index()  # make sure indexes pair with number of rows


# File name
outGeoJSONfn = r'/Users/simon/Desktop/Agroscope_PhD/Writing/Thesis/GitHubRepos/ShapeFromCSVHomographyTransform/3_GeometricTransformOfGeoJsonDefinedCRS/Innov_21_LV95.geojson'



srs = osr.SpatialReference()
srs.ImportFromEPSG(2056)


# Input Data
width_rectan = 0.7
hight_rectan = 4.4
spacing_width = 0.9
spacing_hight = 3.5

# Coordinates of the routh position of the field
lon_offset = 2507555
lat_offset = 1139303


border_spacing = 0

x_intersept = border_spacing
y_intersept = border_spacing


base_shape = np.array([
    [0, 0],
    [width_rectan, 0],
    [width_rectan, hight_rectan],
    [0, hight_rectan],
    [0, 0]])

def get_homography_matrix(source, destination):
    """ Calculates the entries of the Homography matrix between two sets of matching points.
    Args
    ----
        - `source`: Source points where each point is int (x, y) format.
        - `destination`: Destination points where each point is int (x, y) format.
    Returns
    ----
        - A numpy array of shape (3, 3) representing the Homography matrix.
    Raises
    ----
        - `source` and `destination` is lew than four points.
        - `source` and `destination` is of different size.
    """
    assert len(source) >= 4, "must provide more than 4 source points"
    assert len(destination) >= 4, "must provide more than 4 destination points"
    assert len(source) == len(destination), "source and destination must be of equal length"
    A = []
    b = []
    for i in range(len(source)):
        s_x, s_y = source[i]
        d_x, d_y = destination[i]
        A.append([s_x, s_y, 1, 0, 0, 0, (-d_x)*(s_x), (-d_x)*(s_y)])
        A.append([0, 0, 0, s_x, s_y, 1, (-d_y)*(s_x), (-d_y)*(s_y)])
        b += [d_x, d_y]
    A = np.array(A)
    h = np.linalg.lstsq(A, b,rcond=None)[0]
    h = np.concatenate((h, [1]), axis=-1)
    return np.reshape(h, (3, 3))


# create fields
idField = ogr.FieldDefn('Plot_seq', ogr.OFTString)
varField = ogr.FieldDefn('Var', ogr.OFTString)
rowField = ogr.FieldDefn('row', ogr.OFTInteger)
rangeField = ogr.FieldDefn('range', ogr.OFTInteger)
treatmentField = ogr.FieldDefn('Treatment', ogr.OFTString)
rowinfieldField = ogr.FieldDefn('Row_in_Field', ogr.OFTInteger)
repField = ogr.FieldDefn('Rep', ogr.OFTInteger)
categoryField = ogr.FieldDefn('Category', ogr.OFTString)
trialField = ogr.FieldDefn('Trial', ogr.OFTString)
yearField = ogr.FieldDefn('Year', ogr.OFTString)
EUField = ogr.FieldDefn('Experimental_Unit', ogr.OFTString)


# Create the output shapefile
GeoJSONDriver = ogr.GetDriverByName("GeoJSON")
if os.path.exists(outGeoJSONfn):
    GeoJSONDriver.DeleteDataSource(outGeoJSONfn)
outDataSource = GeoJSONDriver.CreateDataSource(outGeoJSONfn)
outLayer = outDataSource.CreateLayer(outGeoJSONfn, geom_type=ogr.wkbPoint)

outLayer.CreateField(idField)
outLayer.CreateField(varField)
outLayer.CreateField(rowField)
outLayer.CreateField(rangeField)
outLayer.CreateField(treatmentField)
outLayer.CreateField(rowinfieldField)
outLayer.CreateField(repField)
outLayer.CreateField(categoryField)
outLayer.CreateField(trialField)
outLayer.CreateField(yearField)
outLayer.CreateField(EUField)


idField = ogr.FieldDefn('Plot_seq', ogr.OFTString)
varField = ogr.FieldDefn('Var', ogr.OFTString)
rowField = ogr.FieldDefn('row', ogr.OFTInteger)
rangeField = ogr.FieldDefn('range', ogr.OFTInteger)
treatmentField = ogr.FieldDefn('Treatment', ogr.OFTString)
rowinfieldField = ogr.FieldDefn('Row_in_Field', ogr.OFTInteger)
repField = ogr.FieldDefn('Rep', ogr.OFTInteger)
categoryField = ogr.FieldDefn('Category', ogr.OFTString)
trialField = ogr.FieldDefn('Trial', ogr.OFTString)
yearField = ogr.FieldDefn('Year', ogr.OFTString)
EUField = ogr.FieldDefn('Experimental_Unit', ogr.OFTString)




for index, row in df.iterrows():
    print(row['Plot_seq'], row['Var'], row['Row'], row['Range'], row['Treatment'], row['Row_in_Field'], row['Rep'], row['Category'],
          row['Trial'], row['Year'], row['Experimental_Unit'])


    x_internal = [x_intersept + ((width_rectan + spacing_width) * (int(row['Row_in_Field'])-1)) + cord[0] + lon_offset for cord in base_shape]
    y_internal = [y_intersept + ((hight_rectan + spacing_hight) * (12-int(row['Range']))) + cord[1] + lat_offset for cord in base_shape]
    print(x_internal)

    # Create ring
    square = ogr.Geometry(ogr.wkbLinearRing)
    square.AddPoint(float(x_internal[0]), float(y_internal[0]))
    square.AddPoint(float(x_internal[1]), float(y_internal[1]))
    square.AddPoint(float(x_internal[2]), float(y_internal[2]))
    square.AddPoint(float(x_internal[3]), float(y_internal[3]))
    square.AddPoint(float(x_internal[4]), float(y_internal[4]))

    # Create polygon
    polygon = ogr.Geometry(ogr.wkbPolygon)
    polygon.AddGeometry(square)
    print(polygon.ExportToWkt())


    # Create the feature and set values
    featureDefn = outLayer.GetLayerDefn()
    outFeature = ogr.Feature(featureDefn)
    outFeature.SetGeometry(polygon)
    outFeature.SetField('Plot_seq', row['Plot_seq'])
    outFeature.SetField('Var', row['Var'])
    outFeature.SetField('row', row['Row'])
    outFeature.SetField('range', row['Range'])
    outFeature.SetField('Treatment', row['Treatment'])
    outFeature.SetField('Row_in_Field', row['Row_in_Field'])
    outFeature.SetField('Rep', row['Rep'])
    outFeature.SetField('Category', row['Category'])
    outFeature.SetField('Trial', row['Trial'])
    outFeature.SetField('Year', row['Year'])
    outFeature.SetField('Experimental_Unit', row['Experimental_Unit'])



    outLayer.CreateFeature(outFeature)


    # dereference the feature
    outFeature = None

# Save and close DataSources
outDataSource = None

