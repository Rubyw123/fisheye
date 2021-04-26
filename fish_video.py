from fish import *
from ctypes import *
import argparse
import cv2
import numpy

def parser():
    parser = argparse.ArgumentParser(description = "Fisheye To Perspective Convert")
    parser.add_argument("-s", type = float,  default = 190.0)
    parser.add_argument("-cx", type = int, default = 640)
    parser.add_argument("-cy", type = int, default = 480)
    parser.add_argument("-r", type = int, default = 640)
    parser.add_argument("-ry", type = int, default = 640)
    parser.add_argument("-a", type = int, default = 2 )
    parser.add_argument("-remap", action = 'store_false')
    parser.add_argument("-w", type = int, default = 1000)
    parser.add_argument("-h2", type = int, default = 1000)
    parser.add_argument("-t", type = int, default = 100 )
    parser.add_argument("-d", action = 'store_true')
    parser.add_argument("-x", type = int, default = 10)
    parser.add_argument("-y", type = int, default = -40)
    parser.add_argument("-z", type = int, default = 3)
    parser.add_argument("-input",type = str,default = "./6.avi")
    parser.add_argument("-output",type = str,default= "./6_persp.avi")
    return parser.parse_args()

def str2int(video_path):
    try:
        return int(video_path)
    except ValueError:
        return video_path

def set_saved_video(input_video, output_video, size):
    fourcc = cv2.VideoWriter_fourcc(*"MP42")
    fps = int(input_video.get(cv2.CAP_PROP_FPS))
    video = cv2.VideoWriter(output_video, fourcc, fps, size)
    return video

def video_capture(args):
    stop = False
    while cap.isOpened():
        ret,frame = cap.read()
        if not ret:
            break
        #frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        cv2.imwrite('./tmp.jpg',frame)
        tmp_img = cv2.imread('./tmp.jpg')
        while(not stop):

            img_shape = tmp_img.shape
            height = img_shape[0]
            width = img_shape[1]
            stop = True
        #print("Height of img:{}\n".format(height))
        #print("Width of img:{}\n".format(width))

        fish2persp(args,height,width)
        persp_img = cv2.imread('./tmp_persp.jpg')
        res = cv2.resize(persp_img,(persp_img.shape[1],persp_img.shape[0]),interpolation= cv2.INTER_AREA)

        video.write(res)
    cap.release()
    video.release()
    cv2.destroyAllWindows()

def fish2persp(args,h,w):
    fname = str.encode('./tmp.jpg')
    params = create_params(args.w,args.h2,args.s,args.r,args.cx,args.cy,h,w)


    fishimage = BITMAP4()
    perspimage = BITMAP4()
    
    transform = create_transform(args.x,args.y,args.z,3)
    transform = transforming(transform,3)
    fishimage = open_fish_image(params,fname,byref(fishimage))
    perspimage = create_persp_image(byref(perspimage),params)
    params = params_check(params)
    if not args.d:
        debug_info(params,transform,3)
    perspimage = convert(params,perspimage,fishimage,transform,3)

    write_file(params,fname,b"tmp",perspimage)
    free_memory(perspimage,fishimage,transform)

    


if __name__ == '__main__':
    args = parser()
    input_path = str2int(args.input)
    cap = cv2.VideoCapture(input_path)
    video = set_saved_video(cap,args.output,(args.w,args.h2))
    video_capture(args)