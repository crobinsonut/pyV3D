from numpy import array, float32

class Sender(object):
    def send(self, obj, first=False):
        raise NotImplementedError('send')


class WV_Sender(Sender):
    def __init__(self, wv, **kwargs):
        self.wv = wv
        self.initialize(**kwargs)

    def initialize(self, **kwargs):
        eye    = array([0.0, 0.0, 7.0], dtype=float32)
        center = array([0.0, 0.0, 0.0], dtype=float32)
        up     = array([0.0, 1.0, 0.0], dtype=float32)
        fov   = 30.0
        zNear = 1.0
        zFar  = 100.0

        bias = 0
        self.wv.createContext(bias, fov, zNear, zFar, eye, center, up)

    def send(self, obj, first=False):
        if not first:
            self.wv.clear()  # clear out old GPrim data

        if isinstance(obj, basestring): # assume it's a filename
            self.geom_from_file(obj)
        else:
            self.geom_from_obj(obj)
        self.wv.send(first)

    def on_close(self):
        self.wv = None

    def geom_from_file(self, fname):
        raise NotImplementedError("geom_from_file")
    
    def geom_from_obj(self, obj):
        raise NotImplementedError("geom_from_obj")

