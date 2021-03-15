class Car:
    
    def __init__(self, bbox, group, score, area, center, tracker):
        self.bbox = bbox
        self.group = group
        self.score = score
        self.area = area
        self.center = center
        self.tracker = tracker
        self.tracking_fail = 0
        self.detection_fail = 0

    def update(self, bbox, area, center, group=None, score=None, tracker=None):
        self.bbox = bbox
        self.area = area
        self.center = center
        if group is not None:
            self.group = group
        if score is not None:
            self.score = score
        if tracker is not None:
            self.tracker = tracker
