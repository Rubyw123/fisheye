class Car:
    
    def __init__(self, _bounding_box, _group, _confidence, _tracker):
        self.bounding_box = _bounding_box
        self.group = _group
        self.group_confidence = _confidence
        self.tracker = _tracker
        self.tracking_fail = 0
        self.detection_fail = 0

    def update(self, _bounding_box, _group=None, _confidence=None, _tracker=None):
        self.bounding_box = _bounding_box
        self.group = _group if _group is not None else self.group
        self.group_confidence = _confidence if _confidence is not None else self.group_confidence
        if _tracker:
            self.tracker = _tracker