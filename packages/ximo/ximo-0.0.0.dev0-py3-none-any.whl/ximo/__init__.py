from .spat import SpatialMath
from .side import Side
from .axis import Axis
from .temp import TemporalMeth
from .freq import Freqency
from .affine import Affine

__version__ = '0.0.0.dev0'


class Image(SpatialMath):
    """x, y, z, time axis are Image orientation space 
    determined by matrix and affine"""
    def __init__(self):
        pass

    def set_mask(self, mask):
        pass

    def l(self):
        return Side(self, 'left')

    def r(self):
        return Side(self, 'right')

    def i(self):
        return Side(self, 'inferior')

    def s(self):
        return Side(self, 'superior')

    def a(self):
        return Side(self, 'anterior')

    def p(self):
        return Side(self, 'posterior')
    
    @property
    def affine(self):
        return Affine(self, self._rotate, self._origin)
    
    @property
    def x(self):
        return Axis(self, 'x')

    @property
    def y(self):
        return Axis(self, 'y')

    @property
    def z(self):
        return Axis(self, 'z')

    @property
    def time(self):
        # time what to do for the time?
        # FFT, filter operation?
        return TemporalMeth(self)

    @property
    def freq(self):
        return Freqency()