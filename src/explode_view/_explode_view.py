import numpy as np
from skimage import measure


def get_exploded_view_func(labels, image, channel_axis=None):
    """Return a function that takes only a scale and returns the exploded view.

    Parameters
    ----------
    labels : array of int
        The input labels.
    image : array
        The image data
    channel_axis : int, optional
        Which channel in `image` to treat as an axis.

    Returns
    -------
    func : Callable
        Function that takes in a scale factor and returns a modified labels and
        image views.
    """
    if channel_axis is not None:
        # we place the channel axis at the end as expected by regionprops
        image = np.rollaxis(image, channel_axis, image.ndim)
    rp = measure.regionprops(labels, image)

    def explode(scale_factor):
        output_shape = [
                np.ceil(ax_size * scale_factor).astype(int)
                for ax_size in labels.shape
                ]
        image_output_shape = output_shape[:]
        if channel_axis is not None:
            image_output_shape.insert(channel_axis, image.shape[channel_axis])
        labels_out = np.zeros(output_shape, dtype=labels.dtype)
        image_out = np.zeros(image_output_shape, dtype=image.dtype)
        for p in rp:
            starts, sizes = list(
                    zip(*[(sl.start, sl.stop - sl.start) for sl in p.slice])
                    )
            new_starts = [round(start * scale_factor) for start in starts]
            positions = tuple([
                    slice(start, start + size)
                    for start, size in zip(new_starts, sizes)
                    ])
            labels_out[positions][p.image] = p.label
            image_out[positions][p.image] = image[p.slice][p.image]
        return labels_out, image_out

    return explode
