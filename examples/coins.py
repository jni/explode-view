"""
Display a labels layer above of an image layer using the add_labels and
add_image APIs
"""

from skimage import data
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label
from skimage.morphology import closing, square, remove_small_objects
import napari
from explode_view._widget import explode_view

image = data.coins()[50:-50, 50:-50]

# apply threshold
thresh = threshold_otsu(image)
bw = closing(image > thresh, square(4))

# remove artifacts connected to image border
cleared = remove_small_objects(clear_border(bw), 20)

# label image regions
label_image = label(cleared)

# initialise viewer with coins image
viewer = napari.view_image(image, name='coins', rgb=False)

# add the labels
label_layer = viewer.add_labels(label_image, name='segmentation')

viewer.window.add_plugin_dock_widget('explode-view', 'explode_view')

napari.run()