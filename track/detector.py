'''
Perform detection using models created with FAIR's Detectron2 framework.
https://github.com/facebookresearch/detectron2
'''

# pylint: disable=import-error,no-name-in-module,invalid-name,broad-except

import torch
from detectron2.utils.logger import setup_logger
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo


class Detector():

    def __init__(self,path,num_classes,weights_path,thresh):
        self.path = path
        self.num_classes = num_classes
        self.weights_path = weights_path
        self.thresh = thresh
        self.classes = {}

        with open(self.path, 'r') as classes_file:
            self.classes = dict(enumerate([line.strip() for line in classes_file.readlines()]))


        # Config and weight of detectron2 model
        cfg = get_cfg()
        cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
        cfg.DATALOADER.NUM_WORKERS = 2
        cfg.MODEL.WEIGHTS = self.weights_path
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = self.num_classes
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = self.thresh

        if torch.cuda.is_available():
            cfg.MODEL.DEVICE = 'cuda'
        else:
            cfg.MODEL.DEVICE = 'cpu'

        self.predictor = DefaultPredictor(cfg)


    def convert_box_to_array(self,box):
        '''
        Detectron2 returns results as a Boxes class
        (https://detectron2.readthedocs.io/modules/structures.html#detectron2.structures.Boxes).
        These have a lot of useful extra methods (computing area etc) however can't be easily
        serialized, so it's a pain to transfer these predictions over the internet (e.g., if
        this is being used in the cloud, and wanting to send predictions back) so this method
        converts it into a standard array format. Detectron2 also returns results in (x1, y1, x2, y2)
        format, so this method converts it into (x1, y1, w, h).
        '''
        res = []
        for val in box:
            for ind_val in val:
                res.append(float(ind_val))

        '''
        # Convert x2, y2 into w, h
        res[2] = res[2] - res[0]
        res[3] = res[3] - res[1]
        '''
        return res

    def get_bounding_boxes(self,image):
        '''
        Return a list of bounding boxes of objects detected,
        their classes and the confidences of the detections made.
        '''
        try:
            outputs = self.predictor(image)
        except Exception as error:
            print('Error detectrion!')

        _classes = []
        _confidences = []
        _bounding_boxes = []

        for i, pred in enumerate(outputs["instances"].pred_classes):
            class_id = int(pred)
            _class = self.classes[class_id]
            _classes.append(_class)
            confidence = float(outputs['instances'].scores[i])
            _confidences.append(confidence)
            _box =  outputs['instances'].pred_boxes[i]
            box_array = self.convert_box_to_array(_box)
            _bounding_boxes.append(box_array)

        return _bounding_boxes, _classes, _confidences