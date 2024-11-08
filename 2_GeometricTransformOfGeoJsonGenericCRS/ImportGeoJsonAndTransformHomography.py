# Name: Transform orthogonal shapes to perspective adjusted shapes by estimating a homography based on 4 corresponding
# points.
# Author: Simon Treier
# Date: 2024-11-08

from osgeo import ogr
import os
import pandas as pd
import numpy as np
import json

# Use json instead of geopandas because it lets you write without bothering about the CRS, which is useful when working
# on images.

# Input file path
path = r'/Users/simon/Desktop/Agroscope_PhD/Writing/Thesis/GitHubRepos/ShapeFromCSVHomographyTransform/1_CreateGeoJsonFromCSV/ShapesRawGenericCRS.geojson'

# Output file path
output_path = r'/Users/simon/Desktop/Agroscope_PhD/Writing/Thesis/GitHubRepos/ShapeFromCSVHomographyTransform/2_GeometricTransformOfGeoJsonGenericCRS/ShapesHomographyTransform.geojson'

# 4 corresponding points must be defined to estimate the homography.
# Input coordinates refer to coordinates of the orthogonal shapes.
# Output coordinates refer to coordinates of the image.
# Point "input_bottom_left" must correspond to "output_bottom_left" etc. The coordinates are in tuples where the first
# number corresponds to the X coordinate and the second number to Y.

# 4 input coordinates of the orthogonal shapes.
input_bottom_left = [-121.2,246.6]
input_bottom_right = [1945.9,245.3]
input_top_right = [1945.6,2601.6]
input_top_left = [-118.0,2600.2]

# 4 output coordinates of the image.
output_bottom_left = [933.6,-1525.0]
output_bottom_right = [3349.8,-1641.1]
output_top_right = [2128.6,-743.7]
output_top_left = [1081.1,-465.7]


# This part was taken from Lee Socretquuliqaa's GitHub repository: https://gist.github.com/Socret360/bcefb0f95cfc20800ea3409f40b8bb58
def get_homography_matrix(source, destination): # Function to calculate homography matrix
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


if __name__ == "__main__":
    source_points = np.array([
        input_bottom_left,
        input_bottom_right,
        input_top_right,
        input_top_left
    ])

    destination_points = np.array([
        output_bottom_left,
        output_bottom_right,
        output_top_right,
        output_top_left
    ])

    h = get_homography_matrix(source_points, destination_points)

# Estimate the homography h
h = get_homography_matrix(source_points, destination_points)

print(h)

# Open the GeoJson
with open(path) as f:
    data = json.load(f)

for feature in data['features']:
    #print(feature['geometry']['coordinates'])
    for point in feature['geometry']['coordinates'][0]:

        point_coords = [point[0], point[1], 1]
        point_coords_transformed = np.dot(h, point_coords)
        point_coords_transformed = point_coords_transformed / point_coords_transformed[2]
        point[0] = point_coords_transformed[0]
        point[1] = point_coords_transformed[1]



with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)