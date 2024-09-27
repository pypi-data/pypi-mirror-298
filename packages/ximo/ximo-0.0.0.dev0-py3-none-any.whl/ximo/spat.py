class SpatialMath:
    """ Image math mainly for spatial domain"""
    def __neg__(self):
        print('flipped image object (as well as affine matrix)')
        pass

    def __add__(self, distance):
        print('# transpose image to + side')
        pass

    def __sub__(self, distance):
        print('# transpose image to - side')
        pass

    def __mul__(self, scale_factor):
        print('# scale image from center')
        pass

    def __truediv__(self, scale_factor):
        print('# scale image from center')