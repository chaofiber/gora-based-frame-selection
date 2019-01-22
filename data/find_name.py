import cv2
from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize
import os
import sys
import random
import csv
def generate_list(frame_dir):
    count = -1
    data_file = []
    for label_dir in os.listdir(frame_dir):
        count += 1
        label_dir_path = os.path.join(frame_dir, label_dir)
        name_list = []
        #data_file = []
        length = len((next(os.walk(label_dir_path))[1])) #number of videos for certain label
        for video_dir in os.listdir(label_dir_path):
            video_dir_path = os.path.join(label_dir_path, video_dir)
            sequence = len((next(os.walk(video_dir_path))[2]))
            if sequence<16:
                continue
            name_list.append(label_dir+'/'+video_dir+'.avi')
            #data_file.append([label_dir, video_dir, 17])
	    #name_list.append(video_dir_path)
        random.shuffle(name_list)

        with open('trainlist.txt','a') as f:
            for item in name_list[0:int(length*0.7)]:
                f.write("%s\n" % str(item))
        with open('testlist.txt','a') as f:
            for item in name_list[int(length*0.7):length]:
                f.write("%s\n" % str(item))
        for item in name_list[0:int(length*0.7)]:
            parts = item.split(os.path.sep)
            filename = parts[1]
            filename_no_ext = filename.split('.')[0]
            classname = parts[0]
            data_file.append(['train',classname,filename_no_ext,17])
        for item in name_list[int(length*0.7):length]:
            parts = item.split(os.path.sep)
            filename = parts[1]
            filename_no_ext = filename.split('.')[0]
            classname = parts[0]
            data_file.append(['test',classname,filename_no_ext,17])
    with open('data_file_ucf.csv','w') as fout:
        writer = csv.writer(fout)          
        writer.writerows(data_file)
if __name__=="__main__":
    frame_dir = sys.argv[1]
    generate_list(frame_dir)
