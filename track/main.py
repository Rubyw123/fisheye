import cv2
import argparse
import os
from CarTrack import *
from Detectron2 import *
from Yolo import *

COLOR = (255,0,255)

def parser():
    parser = argparse.ArgumentParser(description="Tracking with Detectron2")
    parser.add_argument("-input",type = str,default="./input/3_persp.avi",
                        help = "Input video path")
    parser.add_argument("-output",type = str,default="./output/3_persp_demo2.avi",
                        help = "Output video path. Not save if empty.")
    parser.add_argument("-weights",default = "./model_final1.pth",
                        help = "Detector model weights")
    parser.add_argument("-cfg",default = "./yolo/custom-yolov4-detector.cfg",
                        help = "Detector model config file")
    parser.add_argument("-data",default = "./yolo/custom.data",
                        help = "Path to data file")
    parser.add_argument("-show",action='store_true',
                        help = "Not show for headless systems")
    parser.add_argument("-thresh",type=float,default=.50,
                        help = "Remove detections below this score")
    parser.add_argument("-classes",default="./coco_classes.txt",
                        help = "Path to classes file")
    parser.add_argument("-numc",type=int,default="3",
                        help = "Number of classes")
    parser.add_argument("-detector", type = int, default=2,
                        help="Detecor type. 1 = yolo, 2 = Detectron2")
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
    frame_count = 0
    ret,frame = cap.read()
    f_height, f_width, _ = frame.shape

    if args.detector == 1:
        #yolo Detector
        detector = Yolo(args.data, args.weights,args.cfg,args.thresh)
    if args.detector == 2:
        #Detectron2 Detector
        detector = Detectron2(args.classes,args.numc,args.weights,args.thresh)


    track = CarTrack(frame,frame_count,COLOR,fps,detector)

    #Output video settings
    saved_video = set_saved_video(cap,args.output,(f_width,f_height))
    (path, filename) = os.path.split(args.output)
    (f,ext) = os.path.splitext(filename)

    try:
        while cap.isOpened():
            if not ret:
                break

            track.updating_frame(frame,frame_count)
            tracked_frame = track.visualize()

            if args.output is not None:
                saved_video.write(tracked_frame)
            
            if args.show:
                cv2.imshow('Tracking with Detectron2',tracked_frame)

            frame_count += 1

            ret,frame = cap.read()
    finally:
        cap.release()
        saved_video.release()
        cv2.destroyAllWindows()

        track.write_csv_data(f)
            



    
