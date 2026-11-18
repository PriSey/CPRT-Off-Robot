import numpy as np
from scipy.ndimage import gaussian_filter1d
from scipy.spatial.distance import cdist 
import math as m
RESOLUTION = 100

def segment_line(line, resolution=RESOLUTION):
  if len(line) < 2:
    return
  pts_a = np.asarray(line, float)
  seg_dists = np.linalg.norm(np.diff(pts_a, axis=0), axis=1)
  seg_dists_from_origin = np.concatenate([[0],np.cumsum(seg_dists)])
  re_segmentation_points = np.linspace(0, seg_dists_from_origin[-1], resolution)
  return np.column_stack([np.interp(re_segmentation_points, seg_dists_from_origin, pts_a[:, i]) for i in range(pts_a.shape[1])])

def smooth_shape(segments, frac=0.01, closed=False,m=RESOLUTION):
  if segments is None:
      return
  mode = 'wrap' if closed else 'nearest'
  return gaussian_filter1d(segments, sigma=frac * m, axis=0, mode=mode)
    
def normalize_dist_matrix(line):
  if line is None:
    return
  dist_matrix = cdist(line, line)
  dist_matrix = dist_matrix - dist_matrix.mean()
  return dist_matrix / np.linalg.norm(dist_matrix)

def check_similarity(distA, distB):
  if (distA is None) or (distB is None):
    return
  return min(np.linalg.norm(distA - distB), np.linalg.norm(distA - distB[::-1, ::-1]))

def compare(lineA, lineB):
  return check_similarity(normalize_dist_matrix(smooth_shape(segment_line(lineA))),normalize_dist_matrix(smooth_shape(segment_line(lineB))))

#FOR TESTING
def make_circle(n=100, radius=100, center=(100, 100)):
  x = [(center[0] + radius * m.sin(a * (m.pi/100))) for a in range(0, 200)]
  y = [(center[0] + radius * m.cos(a * (m.pi/100))) for a in range(0, 200)]
  return (x,y)

