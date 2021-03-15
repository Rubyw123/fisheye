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

    
    def updating_frame(self,frame):
        self.frame = frame
        cars_list = list(self.cars.items())
        cars_list = Parallel(n_jobs=NUM_CORES, prefer='threads')(
            delayed(updating_from_tracker)(car,i,self.frame)for i,car in cars
        )
        self.cars = dict(cars_list)

        for car_id, car in cars_list:
            if car.tracking_fail >= 3:
                del self.cars[car_id]

        if self.count >= self.fps:
            self.updating_from_detection()
            self.count = 0
        self.count += 1

    def updating_from_detection(self):
        bboxes, groups, scores, areas,centers = self.detector.get_detection_output(self.frame)
        self.cars = add_cars(bboxes,groups,scores, areas, centers,self.cars,self.frame)
        self.cars = remove_duplicates(self.cars)

    def visualize(self):
        f = self.frame

        for _id, car in self.cars.items():
            (x1,y1,w,h) = [int(v) for v in car.bounding_box]
            cv2.rectangle(f,(x1,y1),(x1+w,y1+h),self.color,2)
            if car.group is not None:
                car_info = '{0} {1}, {2}'.format(car.group, str(_id), str(car.group_confidence)[:4])
            else:
                car_info = str(_id)
            cv2.putText(f,car_info,(x1,y1-5),cv2.FONT_HERSHEY_COMPLEX,1,self.color,2,cv2.LINE_AA)
        
        return f