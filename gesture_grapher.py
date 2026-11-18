import file_manipulation as fm
import matplotlib.pyplot as plt

def main():
  gestures = fm.load_gestures()
  for gesture in gestures.keys():
    x_axis, y_axis = zip(*gestures[gesture])
    x_axis = list(x_axis)
    y_axis = list(y_axis)
    graph = plt.plot(x_axis, y_axis)
     


if __name__ == "__main__":
  main()