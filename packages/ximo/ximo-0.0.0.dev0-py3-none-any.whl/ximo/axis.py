class Axis:
    """ the effect of operation changes the data directly """
    def __init__(self, body, axis):
        self.body = body
        self.axis = axis

    def __lshift__(self, distance):
        pass

    def __rshift__(self, distance):
        # maybe this for transpose?
        pass
    
    def __neg__(self):
        print('flipped image object (as well as affine matrix)')
        pass

    def __add__(self, scale_factor):
        print('# transpose scale to + side')
        pass

    def __sub__(self, scale_factor):
        print('# transpose scale to - side')
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

    def __or__(self, something):
        print('slice!!')

    def __and__(self, something):
        print('do something')