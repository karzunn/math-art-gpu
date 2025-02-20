from enum import Enum
import numpy as np


class Bounds:

    def __init__(self, x_min: float, x_max: float, y_min: float, y_max: float):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max


class BitDepth(Enum):
    EIGHT = 8
    SIXTEEN = 16
    THIRTY_TWO = 32


class ImageConfig:

    def __init__(self, width: int, height: int, bit_depth: BitDepth):
        self.width = width
        self.height = height
        self.bit_depth = bit_depth

    @property
    def max_val(self) -> int:
        return 2 ** self.bit_depth.value - 1
    
    @property
    def numpy_dtype(self):
        numpy_dtype_mapping = {
            BitDepth.EIGHT: np.uint8,
            BitDepth.SIXTEEN: np.uint16,
            BitDepth.THIRTY_TWO: np.uint32
        }
        return numpy_dtype_mapping[self.bit_depth]
    
    @property
    def pil_mode(self) -> str:
        pil_mode_mapping = {
            BitDepth.EIGHT: 'L',
            BitDepth.SIXTEEN: 'I;16',
            BitDepth.THIRTY_TWO: 'I'
        }
        return pil_mode_mapping[self.bit_depth]
