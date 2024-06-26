


__all__ = ['get_orientation',
           'reorient_image2',
           'get_possible_orientations',
           'get_center_of_mass']

import numpy as np
from tempfile import mktemp

import ants
from ants.decorators import image_method
from ants.internal import get_lib_fn



_possible_orientations = ['RIP','LIP',  'RSP',  'LSP',  'RIA',  'LIA',
'RSA',  'LSA',  'IRP',  'ILP',  'SRP',  'SLP',  'IRA',  'ILA',  'SRA',
'SLA',  'RPI',  'LPI',  'RAI',  'LAI',  'RPS',  'LPS',  'RAS',  'LAS',
'PRI',  'PLI',  'ARI',  'ALI',  'PRS',  'PLS',  'ARS',  'ALS',  'IPR',
'SPR',  'IAR',  'SAR',  'IPL',  'SPL',  'IAL',  'SAL',  'PIR',  'PSR',
'AIR',  'ASR',  'PIL',  'PSL',  'AIL',  'ASL']


def get_possible_orientations():
    return _possible_orientations

@image_method
def get_orientation(image):
    direction = image.direction

    orientation = []
    for i in range(3):
        row = direction[:,i]
        idx = np.where(np.abs(row)==np.max(np.abs(row)))[0][0]

        if idx == 0:
            if row[idx] < 0:
                orientation.append('L')
            else:
                orientation.append('R')
        elif idx == 1:
            if row[idx] < 0:
                orientation.append('P')
            else:
                orientation.append('A')
        elif idx == 2:
            if row[idx] < 0:
                orientation.append('S')
            else:
                orientation.append('I')
    return ''.join(orientation)

@image_method
def reorient_image2(image, orientation='RAS'):
     """
     Reorient an image.
     Example
     -------
     >>> import ants
     >>> mni = ants.image_read(ants.get_data('mni'))
     >>> mni2 = mni.reorient_image2()
     """
     if image.has_components:
         return ants.merge_channels([img.reorient_image2(orientation) for img in ants.split_channels(image)],
                                    channels_first=image.channels_first)
     
     if image.dimension != 3:
         raise ValueError('image must have 3 dimensions')

     inpixeltype = image.pixeltype
     ndim = image.dimension
     if image.pixeltype != 'float':
         image = image.clone('float')

     libfn = get_lib_fn('reorientImage2')
     itkimage = libfn(image.pointer, orientation)

     new_img = ants.from_pointer(itkimage)
     if inpixeltype != 'float':
         new_img = new_img.clone(inpixeltype)
     return new_img
     
@image_method
def get_center_of_mass(image):
    """
    Compute an image center of mass in physical space which is defined
    as the mean of the intensity weighted voxel coordinate system.

    ANTsR function: `getCenterOfMass`

    Arguments
    ---------
    image : ANTsImage
        image from which center of mass will be computed

    Returns
    -------
    scalar

    Example
    -------
    >>> fi = ants.image_read( ants.get_ants_data("r16"))
    >>> com1 = ants.get_center_of_mass( fi )
    >>> fi = ants.image_read( ants.get_ants_data("r64"))
    >>> com2 = ants.get_center_of_mass( fi )
    """
    if image.pixeltype != 'float':
        image = image.clone('float')

    libfn = get_lib_fn('centerOfMass')
    com = libfn(image.pointer)

    return tuple(com)
