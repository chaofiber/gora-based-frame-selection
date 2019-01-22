import sys
import os
import cv2
from scipy import misc
import numpy as np
from numpy import linalg
import matplotlib.pyplot as plt
from shutil import copy

SELECTED_FRAME = 16

def rgb2grey(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

def mapping(frame_dir, label_path):

    frame_dir_path = os.path.join(label_path, frame_dir)
    number = len(os.listdir(frame_dir_path))
    img = np.empty((number, 6400, 1))
    step = 1 / (number - 1)
    count = 0
    for jpg_file in os.listdir(frame_dir_path):
        jpg_path = os.path.join(frame_dir_path, jpg_file)
        img[count] = np.reshape(rgb2grey(misc.imread(jpg_path)), (6400,1))
        count += 1
    deviation_x = np.empty((number, 1))
    for i in range(number):
        if i == number -1:
            deviation_x[i] = deviation_x[i-1]
        else:
            deviation_x[i] = linalg.norm(img[i] - img[i+1])
    min_dev = min(deviation_x)
    deviation_x -= min_dev
    c = np.trapz(deviation_x[:, 0], np.linspace(0, 1, number))
    inverse_f = np.zeros((number, 1))

    for i in range(number):
        inverse_f[i, 0] = np.trapz(deviation_x[0:i, 0], np.linspace(0, i*step, i)) / c
    dis = 1 / SELECTED_FRAME
    target = np.zeros((number, 1))
    target[0, 0] = 1
    target[number-1, 0] = number

    k = 1
    target = np.zeros((SELECTED_FRAME+1, 1))
    even = np.zeros((SELECTED_FRAME+1, 1))
    even[0, 0] = 1
    target[0, 0] = 1
    line_f = np.zeros((number, 1))
    line_f[:, 0] = np.linspace(0, 1, number)
    for i in range(number):
        if inverse_f[i, 0] >= k / SELECTED_FRAME:
            target[k, 0] = i
            k += 1
    k = 1
    for i in range(number):
        if line_f[i, 0] >= k / SELECTED_FRAME:
            even[k, 0] = i
            k += 1

    if target[SELECTED_FRAME, 0]==0:
        target[SELECTED_FRAME, 0] = number

    #lines = plt.plot(inverse_f[:, 0], np.linspace(1, number, number))
    #plt.setp(lines, color='r', ls='steps')
    #plt.show()
    return target[:, 0], even[:, 0]


if __name__=="__main__":
    video_dir = sys.argv[1]
    even_dir = sys.argv[2]
    map_dir = sys.argv[3]

    if not os.path.exists(even_dir):
        os.mkdir(even_dir)
    if not os.path.exists(map_dir):
        os.mkdir(map_dir)

    for label_class in os.listdir(video_dir):
        label_path = os.path.join(video_dir, label_class)
        even_label_path = os.path.join(even_dir, label_class)
        map_label_path = os.path.join(map_dir, label_class)
        if not os.path.exists(even_label_path):
            os.mkdir(even_label_path)
        if not os.path.exists(map_label_path):
            os.mkdir(map_label_path)

        for frame_dir in os.listdir(label_path):
            ini_frame_dir = os.path.join(label_path, frame_dir)
            even_frame_dir = os.path.join(even_label_path, frame_dir)
            map_frame_dir = os.path.join(map_label_path, frame_dir)
            if not os.path.exists(even_frame_dir):
                os.mkdir(even_frame_dir)
            if not os.path.exists(map_frame_dir):
                os.mkdir(map_frame_dir)
            target, even = mapping(frame_dir, label_path)

            i = j = 0
            map_number = "%04d" % int(target[i])
            even_number = "%04d" % int(even[j])
            for frame_name in os.listdir(ini_frame_dir):
                frame_number = frame_name[:-4]

                if frame_number == map_number:
                    frame_path = os.path.join(ini_frame_dir, frame_name)
                    copy(frame_path, map_frame_dir)
                    i += 1
                    if i <= SELECTED_FRAME:
                        map_number = "%04d" % int(target[i])
                if frame_number == even_number:
                    frame_path = os.path.join(ini_frame_dir, frame_name)
                    copy(frame_path, even_frame_dir)
                    j += 1
                    if j <= SELECTED_FRAME:
                        even_number = "%04d" % int(even[j])



