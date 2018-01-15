# coding:utf-8

import os
import time

from tyframework._private_.util.ftlog import ftlog


class CffiLoader(object):
    def __call__(self, *argl, **argd):
        return self

    def __init__(self):
        self.__fw_lib__ = None
        self.__fw_ffi__ = None

    def loadlib(self, baseffi_cdef, libName, py__file__, cffi_folder):
        '''
        so文件在启动脚本中进行编译生成, 此处仅做装载处理
        '''
        t1 = time.time()
        libpath = os.path.dirname(py__file__) + '/' + cffi_folder + '/'
        sofile = os.path.abspath(libpath + libName)
        ftlog.info('load exits so ->', sofile)
        lib = baseffi_cdef.dlopen(sofile)
        t1 = time.time() - t1
        ftlog.info('load so use time :', t1)
        return lib

    #     def loadlib(self, baseffi_cdef, libName, py__file__, cffi_folder):
    #         t1 = time.time()
    #         libpath = os.path.dirname(py__file__) + '/' + cffi_folder + '/'
    #         sofile = os.path.abspath(libpath + libName)
    #         ftlog.info('load try ->', sofile)
    #         if os.path.isfile(sofile) :
    #             ftlog.info('load exits so ->', sofile)
    #             lib = baseffi_cdef.dlopen(sofile)
    #         else:
    #             ftlog.info('========= make lib so ===============')
    #             cmd = 'cd ' + libpath + '; sh ./makeso.sh'
    #             ftlog.info(cmd)
    #             status, output = commands.getstatusoutput(cmd)
    #             ftlog.info(status, output)
    #             ftlog.info('========= make lib so ===============')
    #             if os.path.isfile(sofile):
    #                 ftlog.info('lib so ->', sofile, 'size=', os.path.getsize(sofile))
    #             else:
    #                 ftlog.error('lib so ->', sofile, 'not found')
    #             lib = baseffi_cdef.dlopen(sofile)
    #             ftlog.info('load make so ->', sofile)
    #         t1 = time.time() - t1
    #         ftlog.info('load so use time :', t1)
    #         return lib

    def load_framework_cffi(self):
        if self.__fw_lib__:
            return self.__fw_lib__, self.__fw_ffi__

        from cffi import FFI
        ffi = FFI()
        ffi.cdef("""
typedef enum
{
    GEOHASH_NORTH = 0,
    GEOHASH_EAST,
    GEOHASH_WEST,
    GEOHASH_SOUTH,
    GEOHASH_SOUTH_WEST,
    GEOHASH_SOUTH_EAST,
    GEOHASH_NORT_WEST,
    GEOHASH_NORT_EAST
} GeoDirection;

typedef struct
{
        uint64_t bits;
        uint8_t step;
} GeoHashBits;

typedef struct
{
        double max;
        double min;
} GeoHashRange;

typedef struct
{
        GeoHashBits hash;
        GeoHashRange latitude;
        GeoHashRange longitude;
} GeoHashArea;

typedef struct
{
        GeoHashBits north;
        GeoHashBits east;
        GeoHashBits west;
        GeoHashBits south;
        GeoHashBits north_east;
        GeoHashBits south_east;
        GeoHashBits north_west;
        GeoHashBits south_west;
} GeoHashNeighbors;

int geohash_encode(double latitude, double longitude, uint8_t step, GeoHashBits* hash);
int geohash_decode(const GeoHashBits* hash, GeoHashArea* area);
int geohash_get_neighbors(const GeoHashBits* hash, GeoHashNeighbors* neighbors);

int tycode(int seed, char *data, int datalen, char *out);
int des_decrypt(unsigned char *src, unsigned srclen, unsigned char *key, unsigned char *out);
int des_encrypt(unsigned char *src, unsigned srclen, unsigned char *key, unsigned char *out);

        """)
        libC = self.loadlib(ffi, 'tyframework.so', __file__, '/framework_cffi/')

        self.__fw_lib__ = libC
        self.__fw_ffi__ = ffi
        return libC, ffi


CffiLoader = CffiLoader()
