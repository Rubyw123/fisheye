#!python3
"""
Python 3 wrapper for fisheye images converting to perspective images

LIBJEPG installed required.

@author: Yizheng Wang
"""

from ctypes import *
import os
import math

#Global variables
TGA = 0
JPG = 3
PNG = 4
XTILT = 0
YROLL = 1
ZPAN = 2

class BITMAP4(Structure):
    _fields_ = [("r",c_ubyte),
                ("g",c_ubyte),
                ("b",c_ubyte),
                ("a",c_ubyte),]


class XYZ(Structure):
    _fields_ = [("x",c_double),
                ("y",c_double),
                ("z",c_double)]

class RGB(Structure):
    _fields_ = [("r",c_int),
                ("g",c_int),
                ("b",c_int)]

class TRANSFORM(Structure):
    _fields_ = [("axis",c_int),
                ("value",c_double),
                ("cvalue",c_double),
                ("svalue",c_double),]

class PARAMS(Structure):
    _fields_ = [("fishfov",c_double),
                ("fishheight",c_int),
                ("fishwidth",c_int),
                ("fishcenterx",c_int),
                ("fishcentery",c_int),
                ("fishradius",c_int),
                ("fishradiusy",c_int),
                ("antialias",c_int),
                ("remap",c_int),
                ("perspwidth",c_int),
                ("perspheight",c_int),
                ("perspfov",c_double),
                ("imageformat",c_int),
                ("rcorrection",c_int),
                ("a1",c_double),
                ("a2",c_double),
                ("a3",c_double),
                ("a4",c_double),
                ("missingcolour",BITMAP4),
                ("debug",c_int)]

def create_params(pwidth,pheight,ffov,fradius,fcenterx,fcentery, fheight,fwidth):
    global JPG
    params = PARAMS()
    params.perspwidth = pwidth
    params.perspheight = pheight
    params.fishfov = ffov
    params.fishradius = fradius
    params.fishradiusy = fradius
    params.fishcenterx = fcenterx
    params.fishcentery = fcentery
    params.fishwidth = fwidth
    params.fishheight = fheight
    params.debug = 0
    params.perspfov = 100
    params.antialias = 2
    params.a1 =1
    params.a2 =0
    params.a3 =0
    params.a4 =0
    params.missingcolour.r = 128
    params.missingcolour.g = 128
    params.missingcolour.b = 128
    params.missingcolour.a = 0
    params.imageformat = JPG

    return params

def create_transform(x,y,z,n):
    return lib.create_transform(x,y,z,n)

def transforming(transform,n):
    return lib.transforming(transform,n)

def open_fish_image(params,cptr,fishimage):
    return lib.open_fish_image(params,cptr,fishimage)


def create_persp_image(perspimg,params):
    return lib.create_persp_image(perspimg,params)

def params_check(params):
    return lib.params_check(params)

def convert(params,perspimage,fishimage,transform,n):
    return lib.convert(params, perspimage, fishimage, transform,n)

def write_file(params,fname,basename,perspimage):
    return lib.write_file(params,fname,basename,perspimage)

def debug_info(params,transform,n):
    return lib.debug_info(params,transform,n)

def free_memory(perspimage,fishimage,transform):
    return lib.free_memory(perspimage,fishimage,transform)

lib = CDLL("./libfish.so")

lib.CameraRay.argtypes = [c_double,c_double,POINTER(XYZ),PARAMS]
lib.CameraRay.restype = XYZ

lib.VectorSum.argtypes = [c_double,XYZ,c_double,XYZ,c_double,XYZ,c_double,XYZ]
lib.VectorSum.restype = XYZ

lib.GiveUsage.argtypes = [c_char_p]

lib.Normalise.argtypes = [POINTER(XYZ)]

lib.MakeRemap.argtypes = [c_char_p]

lib.transforming.argtypes = [POINTER(TRANSFORM),c_int]
lib.transforming.restype = POINTER(TRANSFORM)

lib.open_fish_image.argtypes = [PARAMS,c_char_p,POINTER(BITMAP4)]
lib.open_fish_image.restype = POINTER(BITMAP4)

lib.create_persp_image.argtypes = [POINTER(BITMAP4),PARAMS]
lib.create_persp_image.restype = POINTER(BITMAP4)

lib.convert.argtypes = [PARAMS,POINTER(BITMAP4),POINTER(BITMAP4),POINTER(TRANSFORM),c_int]
lib.convert.restype = POINTER(BITMAP4)

lib.write_file.argtypes = [PARAMS,c_char_p,c_char_p,POINTER(BITMAP4)]

lib.debug_info.argtypes = [PARAMS, POINTER(TRANSFORM), c_int]

lib.params_check.argtypes = [PARAMS]
lib.params_check.restype = PARAMS

lib.create_transform.argtypes = [c_int,c_int,c_int,c_int]
lib.create_transform.restype = POINTER(TRANSFORM)

lib.free_memory.argtypes = [POINTER(BITMAP4),POINTER(BITMAP4),POINTER(TRANSFORM)]










