### Description of the files in this folder:

ShapesFromCSVMetadataGenericCRS.py:
Takes ShapesMetadata.csv as input and creates a GeoJson file ShapesRawGenericCRS.geojson from it. Some parameters related to shape and buffer dimension must be set directly in the Python script. Play around with the dimension of shape and buffer till the general appearance (ratio height/width, ratio shape/buffer) resembles the plots in the field.

The position of the shapes is defined by "Row" and "Column" attributes in the CSV input. These attributes don't have units and the distances are set with the dimension of shape and buffer. However, they are scalar and a distances should be represented respectively. That is, the distance *e.g.* between "Row" 10 and 20 should be 10 and if there are buffer rows in the experiment, they should be considered as additional rows to avoid situation where the "Row" argument continuous from before a buffer row to after a buffer row.

The position of the shapes is not that important at that stage, however, the directional orientation is! When "Row" attribute is increasing from left to right in the experiment on the image, the "Row" should also increase from left to right on the shapes. The same holds true for the "Column" argument. Sometimes, the shapes are rotated by about 45° in the images which makes such an orientation difficult. This doesn't matter as long as the situation of the shapes does not completely contradict the situation in the image. To check this, the shapes can be visualization in QGIS where also the image can be loaded directly. Set the layer labels to "Row" or "Column" (right click on layer > Properties > Labels) to check. Alternatively, use the "Identify Features" tool. Categorize the appearance of the shapes with the layer symbology to simplify the alignment and orientation of the shapes.

Once the orthogonal shapes are created, they can be transformed to perspective view in *2_GeometricTransformOfGeoJsonGenericCRS*.



