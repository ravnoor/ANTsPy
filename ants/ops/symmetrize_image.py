

__all__ = ['symmetrize_image']

from tempfile import mktemp

import ants
from ants.decorators import image_method

@image_method
def symmetrize_image(image):
    """
    Use registration and reflection to make an image symmetric

    ANTsR function: N/A

    Arguments
    ---------
    image : ANTsImage
        image to make symmetric

    Returns
    -------
    ANTsImage

    Example
    -------
    >>> import ants
    >>> image = ants.image_read( ants.get_ants_data('r16') , 'float')
    >>> simage = ants.symimage(image)
    """
    imager = ants.reflect_image(image, axis=0)
    imageavg = imager * 0.5 + image
    for i in range(5):
        w1 = ants.registration(imageavg, image, type_of_transform='SyN')
        w2 = ants.registration(imageavg, imager, type_of_transform='SyN')
        
        xavg = w1['warpedmovout']*0.5 + w2['warpedmovout']*0.5
        nada1 = ants.apply_transforms(image, image, w1['fwdtransforms'], compose=w1['fwdtransforms'][0])
        nada2 = ants.apply_transforms(image, image, w2['fwdtransforms'], compose=w2['fwdtransforms'][0])

        wavg = (ants.image_read(nada1) + ants.image_read(nada2)) * (-0.5)
        wavgfn = mktemp(suffix='.nii.gz')
        ants.image_write(wavg, wavgfn)
        xavg = ants.apply_transforms(image, imageavg, wavgfn)

    return xavg


