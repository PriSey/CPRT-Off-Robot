import cv2 as cv
from ultralytics import YOLO

yolo = YOLO("yolo26n-pose.engine")

def yolo_result(frame):
    results = yolo.track(frame, verbose=False)
    
    anotated = results[0].plot()
    
    cv.imshow("detection",anotated)
    
    return results[0]

def find_right_wrist(result, points, confidence_threshold):
    points_result =[]
    kp = result.keypoints
    sizes = {}
    for box_number in range(len(result.boxes)):
      
      coords = result.boxes[box_number].xyxy.tolist()[0]
      size = (coords[2] - coords[0]) *  (coords[3] - coords[1])
      sizes[size] = box_number
      
    if len(sizes.keys()) > 0:
      if len(kp.xy)>0:
          print(sizes[max(sizes.keys())])
          kp_xys =kp.xy[sizes[max(sizes.keys())]]
          kp_confs = kp.conf[sizes[max(sizes.keys())]]
          for i in points:
              if kp_confs[i] > confidence_threshold:
                  points_result.append((kp_xys[i].cpu(), kp_confs[i].cpu()))
            
    
    return points_result    