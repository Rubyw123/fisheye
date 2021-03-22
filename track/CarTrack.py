import cv2
import multiprocessing
import csv
from tracker import *
from joblib import Parallel,delayed

NUM_CORES = multiprocessing.cpu_count()

class CarTrack():

    def __init__(self,init_frame,frame_count,color,fps,detector):
        self.frame = init_frame
        self.frame_count = frame_count
        self.cars = {}
        self.color = color
        self.fps = fps
        self.count = 0
        self.detector = detector
        self.logger = []
        
        # Set up a list for output data
        header = ['Frame_id','Car_id','Car_p1','Car_p2','Car_p3','Car_p4','Car_center']
        logger.append(header)

        '''
        with open('./data.csv','w')as file:
            csv_writer = csv.writer(file)
            self.csv_writer.writerow(['Frame_id','Car_id','Car_p1','Car_p2','Car_p3','Car_p4','Car_center'])
        '''
        self.updating_from_detection()

    
    def updating_frame(self,frame,frame_count):
        self.frame = frame
        self.frame_count = frame_count
        cars_list = list(self.cars.items())
        cars_list = Parallel(n_jobs=NUM_CORES, prefer='threads')(
            delayed(updating_from_tracker)(car,i,self.frame,self.frame_count,self.csv_writer)for i,car in cars_list
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
        bboxes, groups, scores,centers = self.detector.get_detection_output(self.frame)
        self.cars = add_cars(bboxes,groups,scores, centers,self.cars,self.frame, self.frame_count,self.logger)
        self.cars = remove_duplicates(self.cars)

    def visualize(self):
        f = self.frame

        for _id, car in self.cars.items():
            (x1,y1,x2,y2) = [int(v) for v in car.bbox]
            cv2.rectangle(f,(x1,y1),(x2,y2),self.color,2)
            if car.group is not None:
                car_info = '{0} {1}, {2}'.format(car.group, str(_id), str(car.score)[:4])
            else:
                car_info = str(_id)
            cv2.putText(f,car_info,(x1,y1-5),cv2.FONT_HERSHEY_COMPLEX,1,self.color,2,cv2.LINE_AA)
        
        return f
    
    def write_csv_data(self,file_name):
        logger = self.logger

        with open(file_name,'w') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(logger)