
# Take a video input of x frames (pass a file into the video capture),
# path to a file thats passed into YOLO, YOLO will track gesture,
# we want to check how many frames (pass a video of x frames), pass it into open CV reader (thats first)
#It will repeatedly give points, add points to a list, then graph points (visual aid)
#That list should be written as a json as a gesture (all 5 gestures go into 1 json file)
import cv2 as cv
import file_manipulation.py as fm
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
    


    #Video is the video we're putting in, should it ask for it first or will we have one?
    cap = cv.VideoCapture(video)


    if not cap.isOpened():
        exit()
        
    total_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
        
    tracked_points = []
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        
        #YOLO will track gesture of RIGHT hand
        
        res = yd.yolo_result(frame)
        points = yd.find_right_wrist(res, [10], 0.400)
        
        if len(points) > 0:
            point, conf = points[0]
            
            px, py = point
            x_axis.append(px)
            y_axis.append(py)
            
            tracked_points.append([x_axis, y_axis])
            
    cap.release()
    cv.destroyAllWindows()
    plt.ioff()
    plt.close()   
    return tracked_points
    #I dont know how to get it to the json file
         

if __name__ == "__main__":
    video_file ="path_to_gesture_video.mp4"
    coll_data = process_gesture_vid(video_file)