import os
import sys
import numpy as np
import napari

if not os.path.exists('labs.npz'):
    print('Test data missing. Download from:')
    print('https://github.com/damiandn/scripts')
    sys.exit()

labs = np.load('labs.npz')['arr_0']
nuc = np.load('nuc_im.npz')['arr_0']
mem = np.load('mem_im.npz')['arr_0']
viewer = napari.Viewer()
viewer.add_image(nuc, colormap='magenta', blending='additive')
viewer.add_image(mem, colormap='green', blending='additive')
viewer.add_labels(labs)

viewer.window.add_plugin_dock_widget('explode-view', 'explode_view')

napari.run()
