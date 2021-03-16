import cv2
from car import Car
from azTools import *
id = 0
IOU_THRESH = 0.6


def _csrt_create(bbox,frame):
    #convert (x1,y1,x2,y2) to (x,y,w,h)
    new_bbox = bbox.copy()
    new_bbox[2] = new_bbox[2]-new_bbox[0]
    new_bbox[3] = new_bbox[3]-new_bbox[1]
    tracker = cv2.TrackerCSRT_create()
    tracker.init(frame,tuple(new_bbox))
    return tracker

def remove_inactive_cars(cars, active_cars):
    for i, car in list(cars.items()):
        if i not in active_cars:
            car.detection_fail += 1
        if car.detection_fail >= 2:
            del cars[i]
    return cars

def check_car_tracked(box,cars):
    for i, car in list(cars.items()):
        iou = get_iou(box,car.bbox)
        if iou > IOU_THRESH:
            return i 
    return None


def add_cars(bboxes,groups,scores,areas,centers,cars,frame):

    active_cars = []
    if bboxes is not None and groups is not None and scores is not None:
        for i, bbox in enumerate(bboxes):
            group = groups[i] 
            score = scores[i]
            area = areas[i]
            center = centers[i] 

            car_id = check_car_tracked(bbox,cars)
            if car_id is not None:
                cars[car_id].update(bbox,area,center)
                active_cars.append(car_id)
            else:
                tracker = _csrt_create(bbox,frame)

                car_id = generate_id()
                new_car = Car(bbox,group,score,area,center,tracker)
                cars[car_id] = new_car
        cars = remove_inactive_cars(cars,active_cars)
    return cars

def updating_from_tracker(car,i,frame):
    ret, bbox = car.tracker.update(frame)
    if ret:
        car.tracking_fail = 0
        #convert (x,y,w,h) to (x1,y1,x2,y2)
        (x,y,w,h) = bbox
        new_bbox = (x,y,x+w,y+h)
        new_area = get_box_area(new_bbox)
        new_center = get_center(new_bbox)
        car.update(new_bbox,new_area,new_center)
    else:
        car.tracking_fail += 1
    
    return(i,car)


def remove_duplicates(cars):
    
    for i, car in list(cars.items()):
        car_id = check_car_tracked(car.bbox,cars)
        if car_id is not None and car_id != i:
            del cars[car_id]
    return cars





            
