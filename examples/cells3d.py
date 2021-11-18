import pathlib
import os
import sys
import numpy as np
import napari


here = pathlib.Path(os.path.dirname(__file__))

# check for the data
if not os.path.exists(here / 'labs.npz'):
    print('Test data missing. Download from:')
    print('https://github.com/damiandn/scripts')
    print('and place it next to this script.')
    sys.exit()

# load the data
labs_orig = np.load(here / 'labs.npz')['arr_0']
nuc_orig = np.load(here / 'nuc_im.npz')['arr_0']
mem_orig = np.load(here / 'mem_im.npz')['arr_0']

# trim the data
nonzero = np.transpose(np.nonzero(labs_orig))
top_left = np.min(nonzero, axis=0)
bottom_right = np.max(nonzero, axis=0) + 1
indices = tuple(slice(m, M) for m, M in zip(top_left, bottom_right))
labs, nuc, mem = [arr[indices] for arr in (labs_orig, nuc_orig, mem_orig)]

# display the data
viewer = napari.Viewer(ndisplay=3)
viewer.add_image(nuc, colormap='magenta', blending='additive')
viewer.add_image(mem, colormap='green', blending='additive')
viewer.add_labels(labs)

# add the dock widget
viewer.window.add_plugin_dock_widget('explode-view', 'explode_view')

napari.run()
