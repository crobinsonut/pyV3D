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

cdef extern from "wv.h":

    int BUFLEN

    ctypedef struct wvStripe:
        int            nsVerts
        int            nsIndices
        int            nlIndices
        int            npIndices
        int            *gIndices
        float          *vertices
        float          *normals
        unsigned char  *colors
        unsigned short *sIndice2
        unsigned short *lIndice2
        unsigned short *pIndice2

    ctypedef struct wvGPrim:
        int            gtype
        int            updateFlg
        int            nStripe
        int            attrs
        int            nVerts
        int            nIndex
        int            nlIndex
        int            npIndex
        int            nameLen
        float          pSize
        float          pColor[3]
        float          lWidth
        float          lColor[3]
        float          fColor[3]
        float          bColor[3]
        float          normal[3]
        char           *name
        float          *vertices
        float          *normals
        unsigned char  *colors
        int            *indices
        int            *lIndices
        int            *pIndices
        wvStripe       *stripes
        
    ctypedef struct wvContext:
        int     ioAccess
        int     dataAccess
        int     bias
        float   fov
        float   zNear
        float   zFar
        float   eye[3]
        float   center[3]
        float   up[3]
        int     nGPrim
        int     mGPrim
        int     cleanAll
        wvGPrim *gPrims
        
    ctypedef struct wvData:
        int    dataType
        int    dataLen
        void  *dataPtr
        float  data[3]
  
    wvContext* wv_createContext(int bias, float fov,
                                float zNear, float zFar, float *eye,
                                float *center, float *up)

    int wv_setData(int type, int len, void *data, 
                   int VBOtype, wvData *dstruct)
                   
    int wv_addGPrim(wvContext *cntxt, char *name, int gtype, int attrs, 
                    int nItems, wvData *items)
                    
    void wv_printGPrim(wvContext *cntxt, int index)

    int wv_indexGPrim(wvContext *cntxt, char *name)

    ctypedef int (*cy_callback) (void *wsi, unsigned char *buf,
                                 int ibuf, void *f) 

    int wv_sendGPrim(void *wsi, wvContext *cntxt, unsigned char *buf, int flag,
                      cy_callback callback1, void* callback2)

    void wv_removeGPrim(wvContext *cntxt, int index)
    
    void wv_removeAll(wvContext *cntxt)
    
    void wv_prepareForSends(wvContext *cntxt)
    
    void wv_finishSends(wvContext *cntxt)
    
    void wv_destroyContext(wvContext **context)

    int wv_addArrowHeads(wvContext *cntxt, int index, float size, 
                         int nHeads, int *heads)

    void wv_adjustVerts(wvData *dstruct, float *focus)
    
