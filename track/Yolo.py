'''
A Yolo detector performing Yolov4 detection on images
'''

from ctypes import *
import darknet
from azTools import *
import cv2

class Yolo():

    def __init__(self,data_path,weights_path,cfg_path,thresh):
        self.name = 1
        self.data_path = data_path
        self.weights_path = weights_path
        self.cfg_path = cfg_path
        self.thresh = thresh

        self.network,self.class_names,self.class_colors = darknet.load_network(cfg_path,data_path,weights_path,batch_size = 1)

        self.width = darknet.network_width(self.network)
        self.height = darknet.network_height(self.network)

        #print("network_w: "+ str(self.width))
        #print("network_h: "+str(self.height))

    
    def get_name(self):
        return self.name


    def get_w(self):
        return self.width

    def get_h(self):
        return self.height    


    def resize_image(self,image,width,height,d_image):
        image_rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        image_resized = cv2.resize(image_rgb,(width,height),interpolation = cv2.INTER_LINEAR)

        darknet.copy_image_from_bytes(d_image,image_resized.tobytes())

        return d_image

    def get_detection_output(self,image):
        groups = []
        scores = []
        bboxes = []
        centers = []

        #width = darknet.network_width(self.network)
        #height = darknet.network_height(self.network)
        d_image = darknet.make_image(self.width,self.height,3)

        darknet_image = self.resize_image(image,self.width,self.height,d_image)

        detections = darknet.detect_image(self.network,self.class_names,darknet_image,self.thresh)
        
        i_width = image.shape[1]
        i_height = image.shape[0]

        for group,score,bbox in detections:
            array = []
            x1,y1,x2,y2 = darknet.bbox2points(bbox)

            groups.append(group)

            scores.append(float(score))

            #Translate the coordinates of bbox into original frame size
            array.append(float(x1*(i_width/416)))
            array.append(float(y1*(i_width/416)))
            array.append(float(x2*(i_height/416)))
            array.append(float(y2*(i_height/416)))
            bboxes.append(array)

            centers.append((float((array[0]+array[2])/2),float((array[1]+array[3])/2)))
        
        darknet.free_image(darknet_image)


        return bboxes, groups,scores,centers









