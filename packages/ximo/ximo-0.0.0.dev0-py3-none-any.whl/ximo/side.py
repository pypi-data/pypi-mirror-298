class Side:
    """ Left, Right, Superior, Injerior, Anterior, Posterior"""
    def __init__(self, body, side):
        self.body = body
        self.side = side

    def __neg__(self):
        print('flipped image object (as well as affine matrix)')
        pass

    def __add__(self, distance):
        print('# add something next to')
        pass

    def __sub__(self, distance):
        print('# substract based on ')
        pass

    def __mul__(self, scale_factor):
        print('# scale image from center')
        pass

    def __truediv__(self, scale_factor):
        print('# scale image from center')

    def __repr__(self):
        return f"{self.body.__class__.__name__}(axis={self.axis})"

    def __matmul__(self, radian):
        print('rotate axis')

    def __rmatmul__(self, radian):
        print('rotate axis')