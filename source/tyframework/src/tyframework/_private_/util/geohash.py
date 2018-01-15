#!/usr/bin/env python
# -*- coding=utf-8 -*-

'''
GeoHash封装
算法参照:https://github.com/yinqiwen/ardb/blob/master/doc/spatial-index.md
zhouxin,2014.4.15
'''
import math


class GeoHash(object):
    DEFAULT_STEP = 26
    QUERY_STEP = 17

    def __call__(self, *argl, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        pass

    def _init_singleton_(self):
        self.C, self.ffi = self.__ctx__.CffiLoader.load_framework_cffi()

    # 给定经纬度，返回geohash-int，step为精度26步最精确，误差0.6m
    def encode(self, lat, lon, step=DEFAULT_STEP):
        geobits = self.ffi.new("GeoHashBits *")
        ret = self.C.geohash_encode(lat, lon, step, geobits)
        if ret < 0:
            return None
        return geobits.bits

    def decode(self, geobit, step=DEFAULT_STEP):
        geobits = self.ffi.new("GeoHashBits *")
        geobits.bits = geobit
        geobits.step = step
        geoarea = self.ffi.new("GeoHashArea *")
        ret = self.C.geohash_decode(geobits, geoarea)
        if ret < 0:
            return None
        return [geoarea.latitude.min, geoarea.latitude.max,
                geoarea.longitude.min, geoarea.longitude.max]

    # 给定geohash-int，返回相邻8块的geohash-int
    def get_neighbors(self, geobit, step=DEFAULT_STEP):
        geobits = self.ffi.new("GeoHashBits *")
        geobits.bits = geobit
        geobits.step = step
        geoneig = self.ffi.new("GeoHashNeighbors *")
        ret = self.C.geohash_get_neighbors(geobits, geoneig)
        if ret < 0:
            return None
        return [geoneig.west.bits, geoneig.east.bits,
                geoneig.south.bits, geoneig.north.bits,
                geoneig.north_west.bits, geoneig.north_east.bits,
                geoneig.south_east.bits, geoneig.south_west.bits]

    def _deg2rad(self, d):
        return d * math.pi / 180.0

    def get_distance(self, geoint1, geoint2, step=DEFAULT_STEP):
        """
        计算两者之间的距离 单位：米
        """
        EARTH_RADIUS_METER = 6378137.0;
        geo1 = self.decode(geoint1, step)
        geo2 = self.decode(geoint2, step)
        location1 = (geo1[2], geo1[0])
        location2 = (geo2[2], geo2[0])
        # print(location1, location2)
        flon = self._deg2rad(location1[0])
        flat = self._deg2rad(location1[1])
        tlon = self._deg2rad(location2[0])
        tlat = self._deg2rad(location2[1])
        con = math.sin(flat) * math.sin(tlat)
        con += math.cos(flat) * math.cos(tlat) * math.cos(flon - tlon)
        return int(math.acos(con) * EARTH_RADIUS_METER)


GeoHash = GeoHash()
