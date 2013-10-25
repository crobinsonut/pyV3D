# file: pyV3D.pyx
#
# References:
#
# Tutorial for passing a numpy array into a function:
#     http://wiki.cython.org/tutorials/NumpyPointerToC
#
# Help for passing a python function into a C library
#     http://stackoverflow.com/questions/8800838/how-to-pass-a-function-pointer-to-an-external-program-in-cython?rq=1
#
# Passing string (char*) into Cython
#     http://docs.cython.org/src/tutorial/strings.html
#
# Passing string (char*) back into Python
#     http://docs.cython.org/src/tutorial/strings.html
#
# Passing Python objects in and out of the C code
#     http://www.cython.org/release/Cython-0.12/Cython/Includes/python.pxd

from libc.stdio cimport printf, fprintf, fopen, fclose, FILE
from libc.stdlib cimport free
from cpython cimport PyBytes_AsString

import numpy as np
cimport numpy as np
np.import_array()

import struct

from wv cimport wvContext

cdef int callback(void *wsi, unsigned char *buf, int ibuf, void *f)
   
cdef float* _get_focus(bbox, float focus[4])

cdef class WV_Wrapper:

    cdef wvContext* context
