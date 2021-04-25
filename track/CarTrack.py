import cv2
import multiprocessing
import csv
import time
from tracker import *
from joblib import Parallel,delayed

NUM_CORES = multiprocessing.cpu_count()

class CarTrack():

    def __init__(self,init_frame,frame_count,color,fps,detector):
        self.frame = init_frame
        self.track_frame = init_frame
        self.frame_count = frame_count
        self.cars = {}
        self.color = color
        self.fps = fps
        self.count = 0
        self.detector = detector
        '''
        if detector.get_name() == 1:

            # Resize frame for yolo format
            width = detector.get_w()
            height = detector.get_h()

            f_rgb = cv2.cvtColor(init_frame,cv2.COLOR_BGR2RGB)

            self.track_frame = cv2.resize(f_rgb,(width,height),interpolation = cv2.INTER_LINEAR)
        '''

        self.logger = []
        
        # Set up a list for output data
        header = ['Frame_id','Car_id','Car_p1','Car_p2','Car_p3','Car_p4','Car_center','Center_error','D_Time','T_Time']
        self.logger.append(header)
        self.updating_from_detection()

    
    def updating_frame(self,frame,frame_count):
        self.frame = frame
        track_frame = frame
        self.frame_count = frame_count

        '''
        if self.detector.get_name() == 1:

            # Resize frame for yolo format
            width = self.detector.get_w()
            height = self.detector.get_h()

            f_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

            track_frame = cv2.resize(f_rgb,(width,height),interpolation = cv2.INTER_LINEAR)
            print("Yolo!")

        '''
        #Start tracker after first frame
        if frame_count > 0:
            cars_list = list(self.cars.items())
            cars_list = Parallel(n_jobs=NUM_CORES, prefer='threads')(
                delayed(updating_from_tracker)(car,i,self.frame,self.frame_count,self.logger)for i,car in cars_list
            )
            self.cars = dict(cars_list)

            for car_id, car in cars_list:
                if car.tracking_fail >= 2:
                    del self.cars[car_id]

        if self.count >= self.fps:
            self.updating_from_detection()
            self.count = 0
        else:
            self.count += 1

    def updating_from_detection(self):
        prev_time = time.time()
        bboxes, groups, scores,centers = self.detector.get_detection_output(self.frame)
        spent_time = time.time()-prev_time
        self.cars = add_cars(bboxes,groups,scores, spent_time,centers,self.cars,self.frame, self.frame_count,self.logger)
        self.cars = remove_duplicates(self.cars)

        return spent_time

    def visualize(self):
        f = self.frame
        write_frame = f
        '''
        if self.detector.get_name() == 1:

            # Resize frame for yolo format
            width = self.detector.get_w()
            height = self.detector.get_h()

            f_rgb = cv2.cvtColor(f,cv2.COLOR_BGR2RGB)

            write_frame = cv2.resize(f_rgb,(width,height),interpolation = cv2.INTER_LINEAR)
        '''

        '''
        width = self.detector.get_w()
        height = self.detector.get_h()

        f_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        f = cv2.resize(f_rgb,(width,height),interpolation = cv2.INTER_LINEAR)
        '''
        for car_id, car in self.cars.items():
            (x1,y1,x2,y2) = [int(v) for v in car.bbox]
            cv2.rectangle(f,(x1,y1),(x2,y2),self.color,2)
            if car.group is not None:
                car_info = '{0} {1}'.format(car.group, str(car_id))
            else:
                car_info = str(car_id)
            cv2.putText(f,car_info,(x1,y1-5),cv2.FONT_HERSHEY_COMPLEX,1,self.color,2,cv2.LINE_AA)
        
        return f
    
    def write_csv_data(self,file_name):
        logger = self.logger
        file_name = file_name + '.csv'

        with open(file_name,'w') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(logger)