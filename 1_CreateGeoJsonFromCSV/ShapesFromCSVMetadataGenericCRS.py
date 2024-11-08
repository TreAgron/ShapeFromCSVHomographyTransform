# Run in /Users/simon/PycharmProjects/envs/GeoGDALPy39
from osgeo import ogr
import os
import pandas as pd
import numpy as np

df = pd.read_csv(r'/Users/simon/Desktop/Agroscope_PhD/Writing/Thesis/GitHubRepos/ShapeFromCSVHomographyTransform/1_CreateGeoJsonFromCSV/ShapesMetadata.csv', sep=";", encoding='latin1')
df = df.reset_index()  # make sure indexes pair with number of rows


# File name
outGeoJSONfn = r'/Users/simon/Desktop/Agroscope_PhD/Writing/Thesis/GitHubRepos/ShapeFromCSVHomographyTransform/1_CreateGeoJsonFromCSV/ShapesRawGenericCRS.geojson'

# Input Data
width_rectan = 16
hight_rectan = 20
spacing_width = 40
spacing_hight = 100

border_spacing = 10

x_intersept = border_spacing
y_intersept = border_spacing


extent_bottom_left = [0, -3456]
extent_bottom_right = [4608, -3456]
extent_top_right = [4608, 0]
extent_top_left = [0, 0]


width_rectan = (extent_top_right[0] - extent_bottom_left[0]) / (np.max(df['Row'])) - 2*spacing_width
hight_rectan = (extent_top_right[1] - extent_bottom_left[1]) / (np.max(df['Column'])) - 2*spacing_hight

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
genField = ogr.FieldDefn('Genotype', ogr.OFTString)
columnField = ogr.FieldDefn('Column', ogr.OFTInteger)
treatmentField = ogr.FieldDefn('Treatment', ogr.OFTString)
rowField = ogr.FieldDefn('Row', ogr.OFTInteger)
repField = ogr.FieldDefn('Rep', ogr.OFTInteger)
categoryField = ogr.FieldDefn('Category', ogr.OFTString)
trialField = ogr.FieldDefn('Trial', ogr.OFTString)
yearField = ogr.FieldDefn('Year', ogr.OFTString)


# Create the output shapefile
GeoJSONDriver = ogr.GetDriverByName("GeoJSON")
if os.path.exists(outGeoJSONfn):
    GeoJSONDriver.DeleteDataSource(outGeoJSONfn)
outDataSource = GeoJSONDriver.CreateDataSource(outGeoJSONfn)
outLayer = outDataSource.CreateLayer(outGeoJSONfn, geom_type=ogr.wkbPoint)

outLayer.CreateField(idField)
outLayer.CreateField(genField)
outLayer.CreateField(rowField)
outLayer.CreateField(columnField)
outLayer.CreateField(treatmentField)
outLayer.CreateField(repField)
outLayer.CreateField(categoryField)
outLayer.CreateField(trialField)
outLayer.CreateField(yearField)


idField = ogr.FieldDefn('Plot_seq', ogr.OFTString)
genField = ogr.FieldDefn('Genotype', ogr.OFTString)
rowField = ogr.FieldDefn('Row', ogr.OFTInteger)
columnField = ogr.FieldDefn('Column', ogr.OFTInteger)
treatmentField = ogr.FieldDefn('Treatment', ogr.OFTString)
repField = ogr.FieldDefn('Rep', ogr.OFTInteger)
categoryField = ogr.FieldDefn('Category', ogr.OFTString)
trialField = ogr.FieldDefn('Trial', ogr.OFTString)
yearField = ogr.FieldDefn('Year', ogr.OFTString)


for index, row in df.iterrows():
    print(row['Plot_seq'], row['Genotype'], row['Row'], row['Column'], row['Treatment'], row['Rep'], row['Category'],
          row['Trial'], row['Year'])

    x_internal = [x_intersept + ((width_rectan + spacing_width) * (34-int(row['Row'])-1)) + cord[0] for cord in base_shape]
    y_internal = [y_intersept + ((hight_rectan + spacing_hight) * (int(row['Column']))) + cord[1] for cord in base_shape]
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
    outFeature.SetField('Genotype', row['Genotype'])
    outFeature.SetField('row', row['Row'])
    outFeature.SetField('Column', row['Column'])
    outFeature.SetField('Treatment', row['Treatment'])
    outFeature.SetField('Rep', row['Rep'])
    outFeature.SetField('Category', row['Category'])
    outFeature.SetField('Trial', row['Trial'])
    outFeature.SetField('Year', row['Year'])


    outLayer.CreateFeature(outFeature)


    # dereference the feature
    outFeature = None

# Save and close DataSources
outDataSource = None

