# A Detection And Tracking System For Fisheye Videos From Traffic Intersections

## Overview
- The project aims to present a comprehensive system for detecting and tracking vehicles in fisheye videos obtained from traffic intersections.
- The system calibrates fisheye videos into perspective views, then feeds processed videos into pre-trained detection model and tracking algorithms to handle tasks such as vehicles counts or path data collection.
- The system's performance is evaluated using metrics including mean average precision, center location error and processing time.
  ![image](/


### Table of Contents
-[Project sections](#project-sections-)
-[Installation Requirements](#install-req-)
-[Useage](#useage-)
-[Weight Files](#weight-)
-[Publication information](#publication-)



## Project sections <a name="project-sections-"></a>



## Installation Requirments <a name="install-req-"></a>
1. LIBJEPG
2. Yolov4 [darknet](https://github.com/AlexeyAB/darknet)
3. Detectron2 [detectron2](https://github.com/facebookresearch/detectron2)


## Useage <a name="useage-"></a>
1. Run fish_img.py/fish_video.py to covnert a fisheye imagery/video
2. Download the weight files and put them inside the track folder
3. Modify the input video path to the convert video in the track folder
4. Run main.py

## Weight Files <a name="weight-"></a>
[yolo](https://drive.google.com/file/d/1Zv09wHEFFCeh0nuCtSFfq6QlM35DPxcY/view?usp=sharing)
[detectron2](https://drive.google.com/file/d/1nJBU6yKydEzAmOYYFUTAHYA5ytyKxXAL/view?usp=sharing)

## Publication Information
Citation information:
```
Y. Wang and H. ElAarag, "A Detection And Tracking System For Fisheye Videos From Traffic Intersections," SoutheastCon 2022, Mobile, AL, USA, 2022, pp. 427-433, doi: 10.1109/SoutheastCon48659.2022.9764081.Abstract: Traditional pinhole camera models use rectilinear lenses and yield a smaller field of view (FOV). In order to survey wide areas in traffic intersections, multiple Closed-Circuit TeleVision (CCTV) cameras are needed. A fisheye camera lens can provide a larger FOV than a traditional camera without blind spots, but the images are often distorted. It is a valuable tool in both vehicle detection and tracking systems. In this research we propose a system for detecting and tracking vehicles in fisheye videos obtained from a traffic intersection. We first calibrated the fisheye videos into perspective views, then we trained several detection models on the collected image datasets. After training, we applied tracking algorithms on the video combined with detection results. We tested the performance of our system using mean average precision, center location error and processing time. Our experiments have shown that the different combinations of detection and tracking algorithms have tradeoffs in accuracy and processing time.
URL: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9764081&isnumber=9763889
```

```BibTex
@INPROCEEDINGS{9764081,
  author={Wang, Yizheng and ElAarag, Hala},
  booktitle={SoutheastCon 2022}, 
  title={A Detection And Tracking System For Fisheye Videos From Traffic Intersections}, 
  year={2022},
  volume={},
  number={},
  pages={427-433},
  doi={10.1109/SoutheastCon48659.2022.9764081}}
```

## Notices
Test imagery and video are included. [video](https://drive.google.com/file/d/1UfA7xOOc2zDEMO_QJl0M7KCMptu2tEEg/view?usp=sharing)
If you want to test your own data, make sure to modify the filepath.
