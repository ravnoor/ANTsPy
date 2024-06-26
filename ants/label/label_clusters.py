
 

__all__ = ['label_clusters']

import ants
from ants.internal import get_lib_fn, process_arguments
from ants.decorators import image_method

@image_method
def label_clusters(image, min_cluster_size=50, min_thresh=1e-6, max_thresh=1, fully_connected=False):
    """
    This will give a unique ID to each connected 
    component 1 through N of size > min_cluster_size

    ANTsR function: `labelClusters`

    Arguments
    ---------
    image : ANTsImage 
        input image e.g. a statistical map
    
    min_cluster_size : integer  
        throw away clusters smaller than this value
    
    min_thresh : scalar
        threshold to a statistical map
    
    max_thresh : scalar
        threshold to a statistical map
    
    fully_connected : boolean
        boolean sets neighborhood connectivity pattern
    
    Returns
    -------
    ANTsImage

    Example
    -------
    >>> import ants
    >>> image = ants.image_read( ants.get_ants_data('r16') )
    >>> timageFully = ants.label_clusters( image, 10, 128, 150, True )
    >>> timageFace = ants.label_clusters( image, 10, 128, 150, False )
    """
    dim = image.dimension
    clust = ants.threshold_image(image, min_thresh, max_thresh)
    temp = int(fully_connected)
    args = [dim, clust, clust, min_cluster_size, temp]
    processed_args = process_arguments(args)
    libfn = get_lib_fn('LabelClustersUniquely')
    libfn(processed_args)
    return clust
