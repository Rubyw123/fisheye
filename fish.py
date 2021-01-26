from ctypes import *
import os

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
ARAMS
class TRANSFORM(Structure):
    _fields_ = [("axis",c_int),
                ("value",c_double),
                ("cvalue",c_double),
                ("salue",c_double),]

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

def parser():
    parser = argparse.ArgumentParser(description = "Fisheye To Perspective Convert")
    parser.add_argument("-s", type = float,  default = 180.0)
    #parser.add_argument("-fishheight", type = int, default = )
    #parser.add_argument("-fishwidth", type = int, default = )
    parser.add_argument("-cx", type = int, default = 1000)
    parser.add_argument("-cy", type = int, default = 548)
    parser.add_argument("-r", type = int, default = 553)
    parser.add_argument("-ry", type = int, default = )
    parser.add_argument("-a", type = int, default = 2 )
    parser.add_argument("-remap", action = 'store_false')
    parser.add_argument("-w", type = int, default = 800)
    parser.add_argument("-h", type = int, default = 600)
    parser.add_argument("-t", type = int, default = 100 )
    #parser.add_argument("-imageformat", type = int, default = )
    #parser.add_argument("-rcorrection", action = 'store_false')
    #parser.add_argument("-a1", type = float, default = 0.0)
    #parser.add_argument("-a2", type = float, default = 0.0)
    #parser.add_argument("-a3", type = float, default = 0.0)
    #parser.add_argument("-a4", type = float, default = 0.0)
    #parser.add_argument("-missingcolour", type = int, default = )
    parser.add_argument("-d", action = 'store_false')
    parser.add_argument("-x", type = float, default = 0.0)
    parser.add_argument("-y", type = float, default = 0.0)
    parser.add_argument("-z", type = float, default = 0.0)







