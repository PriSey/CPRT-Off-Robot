
from ultralytics import YOLO
#THIS IS A SCRIPT, DO NOT RUN IT IN THE PROJECT
#Generates an engine to make the yolo stuff faster (on an NVIDIA GPU only)
model = YOLO("yolo26n-pose.pt")
model.export(format="engine", quantize=16, imgsz=640, verbose=False)