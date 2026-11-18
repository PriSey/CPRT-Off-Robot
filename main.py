import numpy as np
import shape_processor as sp
import cv2 as cv
import math as m
import matplotlib.pyplot as plt
import file_manipulation as fm
import colour_processing as cproc
import yolo_detection as yd

PIXELATION = 10
GESTURE_LENGTH = 20
MIN_AREA = 20
SIMILARITY_THRESHOLD = 0.20


x_axis = []
y_axis = []
graph = plt.plot(x_axis,y_axis)[0]


def main():
    c_range_upper, c_range_lower = fm.load_hsv()

    plt.ion()

    cap = cv.VideoCapture(1)

    if not cap.isOpened():
        print("Camera unaccessable")
        exit()

    hsv_container = {'hsv':None}

    graph2 = plt.plot(x_axis,y_axis)[0]

    cx, cy = sp.make_circle()
        
    plt.plot(cx,cy)

    plt.xlim(0,1000)
        

    smooth_circle = sp.smooth_shape(sp.segment_line(cx,cy))
    plt.plot(smooth_circle[:,0],smooth_circle[:,1])



    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Waiting for frame")

        res = yd.yolo_result(frame)
        points = yd.find_points(res,[9],0.400)
        if len(points) > 0:
            point, conf = points[0]
            cx, cy = point
            x_axis.append(cx)
            y_axis.append(cy)    
                    
        if cv.waitKey(1) == ord('q'):
            break
        
        update_graph()
        
        
        gestures = fm.load_gestures()
        line = list(zip(x_axis, y_axis))
        
        for gesture in gestures.keys():
          difference = sp.compare(line, gestures[gesture])
          if difference < SIMILARITY_THRESHOLD:
            print(f"You made the {gesture} gesture.")
        
        
        plt.pause(0.000000000000001)
        
    cap.release()
    cv.destroyAllWindows()

def update_graph():
    global graph
    global x_axis
    global y_axis
    if len(x_axis) > GESTURE_LENGTH:
        x_axis = x_axis[-GESTURE_LENGTH:]
        y_axis = y_axis[-GESTURE_LENGTH:]
    
    graph.remove()
    graph = plt.plot(x_axis,y_axis)[0]

if __name__ == "__main__":
    main()