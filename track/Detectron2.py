'''
A detectron2 detector performing Faster R-CNN detection on images.

'''
import torch
import numpy
from detectron2.utils.logger import setup_logger
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.structures import Boxes


class Detectron2():

    def __init__(self,path,num_classes,weights_path,thresh):
        self.name = 0
        self.path = path
        self.num_classes = num_classes
        self.weights_path = weights_path
        self.thresh = thresh
        self.classes = {}

        with open(self.path, 'r') as _file:
            self.classes = dict(enumerate([line.strip() for line in _file.readlines()]))

        # Config and weight of detectron2 model
        cfg = get_cfg()
        cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_X_101_32x8d_FPN_3x.yaml"))
        cfg.DATALOADER.NUM_WORKERS = 4
        cfg.MODEL.WEIGHTS = self.weights_path
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = self.num_classes
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = self.thresh
        if torch.cuda.is_available():
            cfg.MODEL.DEVICE = 'cuda'
        else:
            cfg.MODEL.DEVICE = 'cpu'

        self.predictor = DefaultPredictor(cfg)

    def get_name(self):
        return self.name

    def get_detection_output(self,image):
        outputs = self.predictor(image)

        groups = []
        scores = []
        bboxes = []
        centers = []

        for i, group in enumerate(outputs["instances"].pred_classes):
            array = []

            # Get group classes
            if int(group) == 0:
                groups.append('car')
            else:
                groups.append('car')

            #Get scores of groups
            score = float(outputs['instances'].scores[i])
            scores.append(score)

            #Get bboxs(x1,y1,x2,y2) in an array
            bbox =  outputs['instances'].pred_boxes[i]
            
            for j in bbox:
                for k in j:
                    array.append(float(k))
            
            #bbox_list = self.convert_box_to_array(_box)
            bboxes.append(array)
            
            #Get center of boxes as tuple
            c = bbox.get_centers()
            center = c.cpu().numpy().tolist()
           
            centers.append((center[0][0],center[0][1]))

        return bboxes, groups, scores,centers

