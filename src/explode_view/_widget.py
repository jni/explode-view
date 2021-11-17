from magicgui import magic_factory, widgets
import napari
from napari_plugin_engine import napari_hook_implementation
import numpy as np
from typing import List

from ._explode_view import get_exploded_view_func


@magic_factory(
        auto_call=True,
        factor={
                'widget_type': widgets.FloatSlider,  # yapf: disable
                'min': 1,
                'max': 4,
                'step': 0.1
                },
        )
def explode_view(
        viewer: napari.viewer.Viewer,
        factor: float,
        ) -> List[napari.types.LayerDataTuple]:
    labels_layer = [
            layer for layer in viewer.layers
            if isinstance(layer, napari.layers.Labels)
            ][0]
    image_layers = [
            layer for layer in viewer.layers
            if isinstance(layer, napari.layers.Image)
            ]
    if not hasattr(explode_view, '_explode_funcs'):
        explode_view._explode_funcs = [
                get_exploded_view_func(labels_layer.data, image_layer.data)
                for image_layer in image_layers
                ]
    funcs = explode_view._explode_funcs
    new_labels, new_image_0 = funcs[0](factor)
    shape = np.asarray(labels_layer.data.shape)
    scale = np.asarray(labels_layer.scale)
    translate = np.asarray(labels_layer.translate
                           ) + scale * shape * (1-factor) / 2
    meta = {'scale': scale, 'translate': translate}
    new_images = [new_image_0] + [func(factor)[1] for func in funcs[1:]]
    new_layers = []
    for image, image_layer in zip(new_images, image_layers):
        new_layers.append((
                image, {**meta, 'name': image_layer.name + ' exploded', 'blending': image_layer.blending, 'colormap': image_layer.colormap},
                'image'
                ))
    new_layers.append((
            new_labels, {**meta, 'name': labels_layer.name + ' exploded', 'visible': False},
            'labels'
            ))
    return new_layers


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return explode_view
