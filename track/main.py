import cv2
import argparse
from CarTrack import *

COLOR = (255,0,255)

def parser():
    parser = argparse.ArgumentParser(description="Tracking with Detectron2")
    parser.add_argument("-input",type = str,default="")
    parser.add_argument("-output",type = str,default="")
    parser.add_argument("-weights",default = "./model_final.pth")
    parser.add_argument("-show",action='store_true')
    parser.add_argument("-thresh",type=float,default=.50)
    parser.add_argument("-classes",default="./coco_classes.txt")
    parser.add_argument("-numc",type=int,default="2")
    return parser.parse_args()

def get_fps(video):
    fps = int(video.get(cv2.CAP_PROP_FPS))
    return fps

def set_saved_video(input_video, output_video, size):
    fourcc = cv2.VideoWriter_fourcc(*"MP42")
    fps = int(input_video.get(cv2.CAP_PROP_FPS))
    video = cv2.VideoWriter(output_video, fourcc, fps, size)
    return video


if __name__ == '__main__':
    args = parser()
    video = args.input
    cap = cv2.VideoCapture(video)
    fps = get_fps(cap)

    ret,frame = cap.read()
    f_height, f_width = frame.shape

    detector = Detector(args.classes,args.numc,args.weights,args.thresh)
    track = CarTrack(frame,COLOR,fps,detector)

    saved_video = set_saved_video(cap,args.ouput,(f_width,f_height))

    try:
        while cap.isOpened():
            if not ret:
                break

            track.updating_frame(frame)
            tracked_frame = track.visualize()

            if args.output is not None:
                saved_video.write(tracked_frame)
            
            if args.show:
                cv2.imshow('Tracking with Detectron2',tracked_frame)

            ret,frame = cap.read()
    finally:
        cap.release()
        saved_video.release()
        cv2.destroyAllWindows()
            



    
