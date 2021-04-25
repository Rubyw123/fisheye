'''
Tracking functions for CarTrack
'''

import cv2
import time
from car import Car
from azTools import *
id = 0
IOU_THRESH = 0.6


def csrt_create(bbox,frame):
    #convert (x1,y1,x2,y2) to (x,y,w,h)
    new_bbox = bbox.copy()
    new_bbox[2] = new_bbox[2(new_bbox))
    return tracker

def remove_inactive_cars(cars, active_cars):
    for i, car in list(cars.items()):
        if i not in active_cars:
            car.detection_fail += 1
        if car.detection_fail >= 2:
            del cars[i]
    return cars

def check_car_tracked(bbox,cars,center):
    for i, car in list(cars.items()):
        ios = get_ios(bbox,car.bbox)
        if ios > 0.6:
            error = distance_btw_points(center,car.center)
            return (i ,error)
    return (-1,0.0)

def center_loc_error(bbox,cars,center):
    error = 0.0
    for i, car in list(cars.items()):
        iou = get_iou(bbox,car.bbox)
        if iou > 0.5:
            error = distance_btw_points(center,car.center)
    
    return error
    


def write_logger_data(logger,frame_count,car_id,bbox,center,error,d_time,t_time):
    points = get_bbox_points(bbox)
    data_info = [frame_count,car_id,points[0],points[1],points[2],points[3],center,error,d_time,t_time]
    logger.append(data_info)



def add_cars(bboxes,groups,scores,time,centers,cars,frame,frame_count,logger):

    active_cars = []
    if bboxes is not None and groups is not None and scores is not None:
        for i, bbox in enumerate(bboxes):
            group = groups[i] 
            score = scores[i]
            center = centers[i] 
            tracker = csrt_create(bbox,frame)

            car_id,error = check_car_tracked(bbox,cars,center)
            #error = center_loc_error(bbox,cars,center)
            if car_id > 0 and error > 0:
                cars[car_id].update(bbox,center,None,None,tracker)
                active_cars.append(car_id)


                # add car info to logger
                if i == 0:
                    write_logger_data(logger,frame_count,car_id,bbox,center,error,time,0.0)
                else:
                    write_logger_data(logger,frame_count,car_id,bbox,center,error,0.0,0.0)

            else:
                #tracker = csrt_create(bbox,frame)
                car_id = generate_id()
                new_car = Car(bbox,group,score,center,tracker)
                cars[car_id] = new_car

                # add car info to logger
                if i == 0:
                    write_logger_data(logger,frame_count,car_id,bbox,center,error,time,0.0)
                else:
                    write_logger_data(logger,frame_count,car_id,bbox,center,error,0.0,0.0)

        cars = remove_inactive_cars(cars,active_cars)
    return cars

def updating_from_tracker(car,i,frame,frame_count,logger):
    prev_time = time.time()
    ret, bbox = car.tracker.update(frame)
    spent_time = time.time()-prev_time
    if ret:
        car.tracking_fail = 0

        #convert (x,y,w,h) to (x1,y1,x2,y2)
        (x,y,w,h) = bbox
        new_bbox = (x,y,x+w,y+h)
        new_center = get_center(new_bbox)
        car.update(new_bbox,new_center)

        # add car info to logger
        write_logger_data(logger,frame_count,i,new_bbox,new_center,0.0,0.0,spent_time)
    else:
        car.tracking_fail += 1
    
    return(i,car)


def remove_duplicates(cars):
    
    for i, car in list(cars.items()):
        car_id, error = check_car_tracked(car.bbox,cars,car.center)
        if car_id > 0 and car_id != i:
            del cars[car_id]
    return cars





            
