
# Take a video input of x frames (pass a file into the video capture),
# path to a file thats passed into YOLO, YOLO will track gesture,
# we want to check how many frames (pass a video of x frames), pass it into open CV reader (thats first)
#It will repeatedly give points, add points to a list, then graph points (visual aid)
#That list should be written as a json as a gesture (all 5 gestures go into 1 json file)
import cv2 as cv
import file_manipulation as fm
import matplotlib.pyplot as plt
import shape_processor as sp
import yolo_detection as yd

def process_gesture_vid(video_path: str):
    x_axis = []
    y_axis = []
    
    #Interactive plotting
    plt.ion()
    
    fig, ax = plt.subplots()
    (graph,) = ax.plot(x_axis, y_axis)
    #Setting limit for the axes:
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 1000)

    #A little confused here, need to generate a circle for comparison?
    # Is that the plan still?
    #use shape_processor function make_circle
    
    #Seysha: No you do not. This will replace the circle initially
    
    cap = cv.VideoCapture(video_path)


    if not cap.isOpened():
        exit()
        
        
    tracked_points = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break        
        #YOLO will track gesture of RIGHT hand

        
        cv.imshow("base",frame)
        if cv.waitKey(1) & 0xFF == ord("q"):  # press q to quit early
          break
        res = yd.yolo_result(frame)
        
        points = yd.find_points(res, [10], 0.400)        
        if len(points) > 0:
            point, conf = points[0]
            
            px, py = point
            px = float(px)
            py = float(py)
            x_axis.append(px)
            y_axis.append(py)
            
            tracked_points.append((px, py))
            
        plt.pause(0.000000000000001)

            
    cap.release()
    cv.destroyAllWindows()
    return tracked_points
  
    #I dont know how to get it to the json file
    #Seysha: Yep. Done
         

if __name__ == "__main__":
    video_file = input("Please entire file name: ")
    name = input("Please enter gesture name: ")
    line = process_gesture_vid(video_file)
    fm.add_gesture(name, line)
    plt.ioff()
    plt.close()   