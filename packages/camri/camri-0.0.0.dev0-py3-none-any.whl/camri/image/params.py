from dataclasses import dataclass
from typing import List, Tuple, Union, Optional


@dataclass
class SliceViewParameters:
    max_columns: int = 5
    frame_id: int = 0
    axis: Optional[int] = None
    indexes: Optional[Union[List[int], Tuple[int]]] = None
    
    def __init__(self, **kwargs):
        """
        
        """
        # max_columns = kwargs.get('max_columns') or 5
        # frame_id = kwargs.get('frame_id') or 0
        # axis = kwargs.get('axis')
        # indexes = kwargs.get('indexes')
        # indexes = indexes if isinstance(indexes, (tuple, list)) else [indexes]
        # axes_kw = kwargs.get('axes_kw')
        # imshow_kw = kwargs.get('imshow_kw')
        # subplots_kw = kwargs.get('subplots_kw') or {}
        
        # if axis is None:
        #     plane = kwargs.get('plane') or 'coronal'
        #     coords = kwargs.get('coords') or 0.0
        #     coords = coords if isinstance(coords, (list, tuple)) else [coords]
        #     num_slices = len(coords)
        # else:
        #     num_slices = len(indexes)
                
        # num_row = int(num_slices / max_columns) + (num_slices % max_columns)
        # num_column = num_slices if num_slices < max_columns else max_columns