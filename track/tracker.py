import cv2
from car import Car
id = 0


def _csrt_create(bbox,frame):
    tracker = cv2.TrackerCSRT_create()
    tracker.init(frame,tuple(bbox))
    return tracker

def generate_id():
    global id
    id +=1
    return id

def get_bbox_info(bbox):
    return (bbox[2]-bbox[0]),(bbox[3]-bbox[1])

def check_overlap(bbox1, bbox2):
    bbox1_w, bbox1_h = get_bbox_info(bbox1)
    bbox2_w, bbox2_h = get_bbox_info(bbox2)

    overlap_x1 = max(bbox1[0], bbox2[0])
    overlap_y1 = max(bbox1[1], bbox2[1])
    overlap_x2 = min(bbox1[2], bbox2[2])
    overlap_y2 = min(bbox1[3], bbox2[3])

    overlap_w = overlap_x2 - overlap_x1 if overlap_x2 - overlap_x1 >= 0 else return 0.0
    overlap_h = overlap_y2 - overlap_y1 if f overlap_y2 - overlap_y1 >= 0 else return 0.0

    overlap_area = overlap_w * overlap_h

    bbox1_area = bbox1_w * bbox1_h
    bbox2_area = bbox2_w * bbox2_h
    min_area = min(bbox1_area,bbox2_area)
    overlap = overlap_area/min_area
    return overlap        


def remove_car(cars, existing_cars):
    for _id, car in cars.items():
        if _id not in existing_cars:
            del cars[_id]
    return cars


def add_car(bboxes,classes,confidences,cars,frame):

    existing_cars = []
    for i, bbox in enumerate(bboxes):
        _group = classes[i] if classes is not None else None
        _confidence = confidences[i] if confidences is not None else None
        _tracker = _csrt_create(bbox,frame)

        car_found = False
        for _id, car in cars.items():
            if check_overlap(bbox, car.bounding_box) >= 0.6:
                car_found = True
                if _id not in existing_cars:
                    existing_cars.append(_id)
                car.update(box,_group,_confidence,_tracker)
                break
        
        if not car_found:
            _car = Car(box,_group,_confidence,_tracker)
            car_id = generate_id()
            cars[car_id] = _car
    cars = remove_car(cars,existing_cars)
    return cars

def update_tracker(car,id,frame):
    success, bbox = car.tracker.update(frame)
    if success:
        car.update(bbox)
    
    return(id,car)

def remove_duplicates(cars):
'''
    for car_id, car_a in list(cars.items()):
        for _, car_b in list()
'''



            
