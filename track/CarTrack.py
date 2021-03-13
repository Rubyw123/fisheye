import cv2
import multiprocessing
from tracker import *
from joblib import Parallel,delayed

NUM_CORES = multiprocessing.cpu_count()

class CarTrack():

    def __init__(self,init_frame,color,fps,detector):
        self.frame = init_frame
        self.cars = {}
        self.color = color
        self.fps = fps
        self.count = 0
        self.detector = detector

        #inital frame
        _bounding_box, _classes, _confidence = self.detector.get_bounding_boxes(self.frame)
        self.cars = add_car(_bounding_box,_classes,_confidence,self.cars,self.frame)
    
    def updating_frame(self,frame):
        self.frame = frame
        cars = list(self.cars.items())
        cars = Parallel(n_jobs=NUM_CORES, prefer='threads')(
            delayed(update_tracker)(car, _id,self.frame)for _id,car in cars
        )
        self.cars = dict(cars)

        if self.count >= self.fps:
            _bounding_box, _classes, _confidence = self.detector.get_bounding_boxes(self.frame)
            self.cars = add_car(_bounding_box,_classes,_confidence,self.cars,self.frame)
            self.count = 0
        self.count += 1


    def get_cars():
        return self.cars
    
    def visualize(self):
        f = self.frame

        for _id, car in self.cars.items():
            (x1,y1,x2,y2) = [int(v) for v in car.bounding_box]
            cv2.rectangle(f,(x1,y1),(x2,y2),self.color,1)
            car_info = _id if car.group is None else '{0} {1}, {2}'.format(car.group, _id, str(car.group_confidence[:4]))
            cv2.putText(frame,car_info,(x1,y1-5),cv2.FONT_HERSHEY_COMPLEX,1,self.color,1,cv2.LINE_AA)
        
        return frame