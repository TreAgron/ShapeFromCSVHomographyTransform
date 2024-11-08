### Description of the files in this folder:

ImportGeoJsonAndTransformHomography.py:
The GeoJson shape file *ShapesRawGenericCRS.geojson* generated in the previous step is transformed to perspective view with a Python script by estimating a homography between orthogonal shapes and the perspectivistic image. To estimate the homography, four correspondig points between shapes and image must be defined as further described in the Python script directly. The transformation is prone to error, espcially for regions distant from the four corresponding points recommend to select four distinct points in the four edges of the region of the shapes that are actually going to be analyzed.
The transform creates a perspective adjusted raw file like the file *ShapesHomographyTransform.geojson* and as can be seen on the main page of this repository. The shapes are adjusted in size and geometry at this step, but need some further manual cleaning and adjustment as can be seen when comparing *ShapesHomographyTransform.geojson* with the image *ExampleImage.dng*. An adjusted shape file like *ExampleImage-AdjustedShapes.geojson* can then be used for further processing.


