import cv2 as cv
import numpy as np
import file_manipulation as fm



def filter_image(frame):
    frame = cv.GaussianBlur(frame, (3,3), 0)
    return frame


def generate_hsvframe(frame):
    hsvframe = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    return hsvframe

def generate_mask(hsvframe,upper,lower):
    
    #mask range
    mask_lower = np.array(lower, np.uint8)
    mask_upper = np.array(upper, np.uint8)
    mask = cv.inRange(hsvframe, mask_lower, mask_upper)
    
    kernel = np.ones((3,3), np.uint8)
    
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)   # removes small specks
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)  # fills small holes
    
    return mask
#HELLO WORLD

def generate_contours(frame, mask):
        res = cv.bitwise_and(frame, frame, mask=mask)
        contours, heirarchy = cv.findContours(mask,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        return contours

def find_largest_contour(contours):
    if contours:
        c = max(contours, key=cv.contourArea)
        return c
    else:
        return None

def generate_contour_centroid(c,min_area):
    area = cv.contourArea(c)
    if (area > min_area):
        M = cv.moments(c)
        cx, cy = M['m10']/M['m00'], M['m01']/M['m00']
        return(cx,cy)
    else:
        return (None,None)

def generate_bounding_rect(c,frame):
    x,y,w,h = cv.boundingRect(c)            
    frame_proc = cv.rectangle((frame), (x,y), (x+w, y+h), (189,0,255), 2)
    cv.putText(frame_proc, "Color identified", (x, y), 
                cv.FONT_HERSHEY_SIMPLEX, 1.0, 
                (189,0,255))
    return frame_proc

def frame_proc(frame, upper, lower, min_area):
    hsvframe = generate_hsvframe(frame)
    
    mask = generate_mask(hsvframe, upper, lower)
    
    contours = generate_contours(frame,mask)
    
    c = find_largest_contour(contours)
    
    if c is not None:
        f = generate_bounding_rect(c, frame)
        cx,cy = generate_contour_centroid(c,min_area)
        
        return (f, hsvframe, cx, cy)

    else:
        return (frame,hsvframe,None,None)

def get_hsv(event, x, y, flags, param:dict):
    global c_range_upper
    global c_range_lower
    hsvframe = param['hsv']
    
    if event == cv.EVENT_LBUTTONDOWN:
        radius = 4
        patch = hsvframe[max(y-radius,0):y+radius+1, max(x-radius,0):x+radius+1].reshape(-1,3).astype(int)
        med = np.median(patch, axis=0)
        std = patch.std(axis=0)
        
        h_mod = max(8,2*std[0])
        sv_mod = max(30,2*std[1])
        
        print(hsvframe[y, x])
        
        hsv_h = med[0]
        hsv_s = med[1]
        hsv_v = med[2]
        
        generate_lower = {
            'h':hsv_h-h_mod,
            's':hsv_s-sv_mod,
            'v':hsv_v-sv_mod
        }
        
        generate_upper = {
            'h':hsv_h+h_mod,
            's':hsv_s+sv_mod,
            'v':hsv_v+sv_mod
        }
        
        maxes   = {'h': 179,    's': 255,    'v': 255}
        
        lower = {k: np.clip(v,0,maxes[k]) for k,v in generate_lower.items() }
        upper = {k: np.clip(v,0,maxes[k]) for k,v in generate_upper.items() }

            
        fm.write_hsv(upper, lower)
        
        return(upper,lower)