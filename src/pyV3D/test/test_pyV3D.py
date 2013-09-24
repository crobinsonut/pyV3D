
import os
import unittest
import tempfile
import shutil

import pyV3D
from pyV3D import WV_Wrapper
from pyV3D.cube import FocusedCubeGeometry, CubeGeometry, CubeSender
from pyV3D.stl import STLSender

import numpy as np
class WV_test_Wrapper(WV_Wrapper):

    def __init__(self, fname):
        super(WV_test_Wrapper, self).__init__()
        self.binfile = open(fname, 'wb')

    def send(self, first=False):
        self.prepare_for_sends()

        if first:
            self.send_GPrim(self, 1, self.send_binary_data)  # send init packet
            self.send_GPrim(self, -1, self.send_binary_data)  # send initial suite of GPrims
        else:  
            self.send_GPrim(self, -1, self.send_binary_data)  # send initial suite of GPrims

        self.finish_sends()
        
    def send_binary_data(self, wsi, buf, ibuf):
        """This is called multiple times during the sending of a 
        set of graphics primitives.
        """
        self.binfile.write(buf)
        return 0


class PyV3DTestCase(unittest.TestCase):

    def setUp(self):
        self.tdir = tempfile.mkdtemp()
        self.path = os.path.dirname(os.path.abspath(__file__))
        
    def tearDown(self):
        try:
            shutil.rmtree(self.tdir)
        except:
            pass

    def _compare(self, s1, s2, name1, name2):
        if len(s1) != len(s2):
            self.fail("%s has different length than %s" % (name1, name2))
        
        for i in range(len(s1)):
            if s1[i] != s2[i]:
                self.fail("byte %d (at least) differs between files %s and %s. (%s != %s)" % 
                              (i, name1, name2, s1[i], s2[i]))

    def test_cube(self):
        cname = os.path.join(self.path, 'cube.bin')
        newname = os.path.join(self.tdir, 'cube.bin')

        sender = CubeSender(WV_test_Wrapper(newname))
        sender.send(CubeGeometry(), first=True)
        sender.wv.binfile.close()

        with open(cname) as f:
            content = f.read()
        with open(newname) as f:
            newcontent = f.read()
        self._compare(content, newcontent, cname, newname)
        
    def test_stl(self):
        cname = os.path.join(self.path, 'star.bin')
        newname = os.path.join(self.tdir, 'star.bin')

        sender = STLSender(WV_test_Wrapper(newname))
        sender.send(os.path.join(self.path, 'star.stl'), first=True)
        sender.wv.binfile.close()

        with open(cname) as f:
            content = f.read()
        with open(newname) as f:
            newcontent = f.read()
        self._compare(content, newcontent, cname, newname)

    def test_focusing_vertices(self):
        cname = os.path.join(self.tdir, 'cube.bin')
        sender = CubeSender(WV_test_Wrapper(cname))

        sender.send(FocusedCubeGeometry(), first=True)
        vertices = pyV3D.get_vertices(sender.wv)
        #gprims = sender.wv.context.gPrims
        #num_gprims = sender.context.nGPrim

        bounding_box = np.array([-.5, -.5, -.5, .5, .5, .5])
        for point in vertices:
            x = point[0]
            y = point[1]
            z = point[2]
        
            if( x > bounding_box[3] or x < bounding_box[0] ):
                self.fail("Point (%f, %f, %f) lies outside of bounding box [%f, %f, %f ,%f ,%f, %f]" %
                    (
                        x, y, z, 
                        bounding_box[0], bounding_box[1], bounding_box[2],
                        bounding_box[3], bounding_box[4], bounding_box[5]
                    )
                )

            if( y > bounding_box[4] or x < bounding_box[1] ):
                self.fail("Point (%f, %f, %f) lies outside of bounding box [%f, %f, %f ,%f ,%f, %f]" %
                    (
                        x, y, z, 
                        bounding_box[0], bounding_box[1], bounding_box[2],
                        bounding_box[3], bounding_box[4], bounding_box[5]
                    )
                )
                
            if( z > bounding_box[5] or x < bounding_box[2] ):
                self.fail("Point (%f, %f, %f) lies outside of bounding box [%f, %f, %f ,%f ,%f, %f]" %
                    (
                        x, y, z, 
                        bounding_box[0], bounding_box[1], bounding_box[2],
                        bounding_box[3], bounding_box[4], bounding_box[5]
                    )
                )
            
        sender.wv.binfile.close()

        
        
if __name__ == "__main__":
    unittest.main()
