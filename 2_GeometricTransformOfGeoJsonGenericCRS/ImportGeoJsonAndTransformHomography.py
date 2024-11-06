# Run in /Users/simon/PycharmProjects/envs/GeoGDALPy39

from osgeo import ogr
import os
import pandas as pd
import numpy as np
import json

# Use json instead of geopandes (which canot be installed at the moment om mac m1) because it lets you write without
# bothering about the CRS (which is useful when working on images).


path = r'/Users/simon/Desktop/Agroscope_PhD/Writing/Thesis/GitHubRepos/ShapeFromCSVHomographyTransform/1_CreateGeoJsonFromCSV/ShapesRawGenericCRS.geojson'

output_path = r'/Users/simon/Desktop/Agroscope_PhD/Writing/Thesis/GitHubRepos/ShapeFromCSVHomographyTransform/2_GeometricTransformOfGeoJsonGenericCRS/ShapesHomographyTransform.geojson'

# Order of coordinates is X and Y

input_bottom_left = [-111.2,256.6]
input_bottom_right = [1955.9,255.3]
input_top_right = [1955.6,2611.6]
input_top_left = [-108.0,2610.2]

output_bottom_left = [933.6,-1525.0]
output_bottom_right = [3349.8,-1641.1]
output_top_right = [2128.6,-743.7]
output_top_left = [1081.1,-465.7]



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


h = get_homography_matrix(source_points, destination_points)

print(h)

with open(path) as f:
    data = json.load(f)

x_coords = []
y_coords = []
for feature in data['features']:
    #print(feature['geometry']['coordinates'])
    for point in feature['geometry']['coordinates'][0]:
        x_coords.append(point[0])
        y_coords.append(point[1])
        point_coords = [point[0], point[1], 1]
        point_coords_transformed = np.dot(h, point_coords)
        point_coords_transformed = point_coords_transformed / point_coords_transformed[2]
        point[0] = point_coords_transformed[0]
        point[1] = point_coords_transformed[1]



with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)