"""
Some useful funtions used for bboxes calculations.

"""
import math
id = 0

def generate_id():
    global id
    id +=1
    return id

def get_bbox_info(bbox):
    '''
    Return width and height of a bbox. 
    Plus one for screen coordinates.
    '''
    return (bbox[2]-bbox[0]+1),(bbox[3]-bbox[1]+1)

def get_box_area(bbox):
    w,h = get_bbox_info(bbox)
    return w*h


def get_iou(bbox1, bbox2):
    '''
    Calculate the intersection over union of two boxes
    '''
    #coordinates of intersection rec
    irec = []
    irec.append(max(bbox1[0], bbox2[0]))
    irec.append(max(bbox1[1], bbox2[1]))
    irec.append(min(bbox1[2], bbox2[2]))
    irec.append(min(bbox1[3], bbox2[3]))

    irec_w, irec_h = get_bbox_info(irec)

    if irec_w < 0 or irec_h < 0:
        return 0.0

    irec_area = get_box_area(irec)
    bbox1_area = get_box_area(bbox1)
    bbox2_area = get_box_area(bbox2)

    iou = irec_area / float(bbox1_area+bbox2_area-irec_area)

    return iou

def get_ios(bbox1, bbox2):
    '''
    If two bboxes overlapped, intersection area 
    over smaller bbox area
    '''
    #coordinates of intersection rec
    irec = []
    irec.append(max(bbox1[0], bbox2[0]))
    irec.append(max(bbox1[1], bbox2[1]))
    irec.append(min(bbox1[2], bbox2[2]))
    irec.append(min(bbox1[3], bbox2[3]))

    irec_w, irec_h = get_bbox_info(irec)

    if irec_w < 0 or irec_h < 0:
        return 0.0

    irec_area = get_box_area(irec)
    bbox1_area = get_box_area(bbox1)
    bbox2_area = get_box_area(bbox2)

    s_area = min(bbox1_area,bbox2_area)
    overlapping = irec_area / float (s_area)

    return overlapping

def get_bbox_points(bbox):
    '''
    Return four points of a bbox as a list,
    in order of top_left, top_right, bottom_left, bottom_right.
    '''
    points = []
    points.append(tuple((bbox[0],bbox[1])))
    points.append(tuple((bbox[2],bbox[0])))
    points.append(tuple((bbox[0],bbox[3])))
    points.append(tuple((bbox[2],bbox[3])))
    return points

def get_center(bbox):
    x1,y1,x2,y2 = bbox
    return(float((x1+x2)/2),float((y1+y2)/2))

def distance_btw_points(p1,p2):
    '''
    Return distances between two points in pixels.
    '''
    p1_x, p1_y = p1
    p2_x, p2_y = p2

    distance = math.sqrt((p1_x-p2_x)**2+(p1_y-p2_y)**2)

    return distance