from fish import *
from ctypes import *
import argparse

def parser():
    parser = argparse.ArgumentParser(description = "Fisheye To Perspective Convert")
    parser.add_argument("-s", type = float,  default = 180.0)
    parser.add_argument("-cx", type = int, default = 640)
    parser.add_argument("-cy", type = int, default = 480)
    parser.add_argument("-r", type = int, default = 640)
    parser.add_argument("-ry", type = int, default = 640)
    parser.add_argument("-a", type = int, default = 2 )
    parser.add_argument("-remap", action = 'store_false')
    parser.add_argument("-w", type = int, default = 1000)
    parser.add_argument("-h2", type = int, default = 1000)
    parser.add_argument("-t", type = int, default = 105)
    parser.add_argument("-d", action = 'store_true')
    parser.add_argument("-x", type = int, default = 10)
    parser.add_argument("-y", type = int, default = -40)
    parser.add_argument("-z", type = int, default = 3)
    parser.add_argument("-input",type = str,default = "./data/Virginia_Mills/09162020_055956_to_09162020_065956/0.jpg")
    return parser.parse_args()

if __name__ == '__main__':
    args = parser()
    fname = str.encode(args.input)

    fishimage = BITMAP4()
    perspimage = BITMAP4()

    params = create_params(args.w,args.h2,args.s,args.r,args.cx,args.cy,args.t,960,1280)
    
    transform = create_transform(args.x,args.y,args.z,3)
    transform = transforming(transform,3)
    fishimage = open_fish_image(params,fname,byref(fishimage))
    perspimage = create_persp_image(byref(perspimage),params)
    params = params_check(params)
    if not args.d:
        debug_info(params,transform,3)
    perspimage = convert(params,perspimage,fishimage,transform,3)

    write_file(params,fname,b"1.jpg",perspimage)
    free_memory(perspimage,fishimage,transform)
