class Affine:
    """ the effect of operation only changes the affine orientation """
    def __init__(self, body, rotate, origin):
        self.body = body
        self.rotate = rotate
        self.origin = origin

    def __repr__(self):
        return f"{self.body.__class__.__name__}(affine)"