from .._tier0 import plugin_function
from .._tier0 import Image
from .._tier0 import create_none

@plugin_function(output_creator=create_none, categories=['label processing', 'in assistant', 'bia-bob-suggestion'])
def exclude_large_labels(source: Image, destination: Image = None, minimum_size: float = 100) -> Image:
    """Removes labels from a label map which are above a given maximum size.

    Size of the labels is given as the number of pixel or voxels per label.

    Parameters
    ----------
    source : Image
    destination : Image, optional
    minimum_size : Number, optional

    Returns
    -------
    destination

    References
    ----------
    .. [1] https://clij.github.io/clij2-docs/reference_excludeLabelsOutsideSizeRange
    """
    from .._tier3 import exclude_labels_out_of_size_range
    return exclude_labels_out_of_size_range(source, destination,
                                            minimum_size=0,
                                            maximum_size=minimum_size)
