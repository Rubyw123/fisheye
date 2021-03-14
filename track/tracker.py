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
    bbox1_x1 = bbox1[0]
    bbox1_y1 = bbox1[1]
    bbox1_x2 = bbox1[0] + bbox1[2]
    bbox1_y2 = bbox1[1] + bbox1[3]

    bbox2_x1 = bbox2[0]
    bbox2_y1 = bbox2[1]
    bbox2_x2 = bbox2[0] + bbox2[2]
    bbox2_y2 = bbox2[1] + bbox2[3]

    overlap_x1 = max(bbox1_x1, bbox2_x1)
    overlap_y1 = max(bbox1_y1, bbox2_y1)
    overlap_x2 = min(bbox1_x2, bbox2_x2)
    overlap_y2 = min(bbox1_y2, bbox2_y2)

    overlap_width = overlap_x2 - overlap_x1
    overlap_height = overlap_y2 - overlap_y1

    if overlap_width < 0 or overlap_height < 0:
        return 0.0

    overlap_area = overlap_width * overlap_height

    bbox1_area = (bbox1_x2 - bbox1_x1) * (bbox1_y2 - bbox1_y1)
    bbox2_area = (bbox2_x2 - bbox2_x1) * (bbox2_y2 - bbox2_y1)
    smaller_area = bbox1_area if bbox1_area < bbox2_area else bbox2_area

    epsilon = 1e-5 # small value to prevent division by zero
    overlap = overlap_area / (smaller_area + epsilon)
    return overlap


def remove_car(cars, existing_cars):
    for _id, car in list(cars.items()):
        if _id not in existing_cars:
            car.detection_fail += 1
        if car.detection_fail >= 2:
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
                car.update(bbox,_group,_confidence,_tracker)
                break
        
        if not car_found:
            _car = Car(bbox,_group,_confidence,_tracker)
            car_id = generate_id()
            cars[car_id] = _car
    cars = remove_car(cars,existing_cars)
    return cars

def update_tracker(car,_id,frame):
    success, bbox = car.tracker.update(frame)
    if success:
        car.tracking_fail = 0
        car.update(bbox)
    else:
        car.tracking_fail += 1
    
    return(_id,car)


def remove_duplicates(cars):
    
    for car_id, car_a in list(cars.items()):
        for _, car_b in list(cars.items()):
            if car_a == car_b:
                break
            if check_overlap(car_a.bounding_box, car_b.bounding_box) >= 0.6 and car_id in cars:
                del  cars[car_id]
    return cars





            
