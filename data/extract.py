import sys
import os
import subprocess
import cv2
#from csv_generation import  ntu_csv_generation


def video_jpg_process(dir_path, dst_dir_path, label_name):
    if os.path.exists(dir_path):
        label = label_name
        #if video_name[17:20] not in {'001','008','009','024','025','031','059','060'}:
         # return
    else:
        print("No file found")

    dst_class_path = os.path.join(dst_dir_path, label)
    if not os.path.exists(dst_class_path):
        os.mkdir(dst_class_path)
    video_dir_path = os.path.join(dir_path, label)
    for video_file in os.listdir(video_dir_path):
        video_name = video_file[:-4]
        dst_frame_path = os.path.join(dst_class_path, video_name)
        if not os.path.exists(dst_frame_path):
            os.mkdir(dst_frame_path)
        else:
            return
            #subprocess.call('rm -r \"{}\" '.format(dst_frame_path), shell=True)
            #print('remove {}'.format(dst_frame_path)
            #os.mkdir(dst_frame_path)
        video_file_path = os.path.join(video_dir_path, video_file)
        video = cv2.VideoCapture(video_file_path)
        count = 1
        if video.isOpened():
            sucess, frame = video.read()
        else:
            sucess = False
        while sucess:
            dim = (80, 80)
            frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
            str_count = "%04d" % count
            cv2.imwrite(os.path.join(dst_frame_path, str_count+'.jpg'), frame)
            count += 1
            sucess, frame = video.read()
            cv2.waitKey(1)
        video.release()

  #  with open(os.path.join(dst_frame_path, 'n_frames'), 'w') as count_file:
   #     count_file.write(str(count-1))
    return


if __name__=="__main__":
    dir_path = sys.argv[1]
    dst_dir_path = sys.argv[2]

    if not os.path.exists(dst_dir_path):
        os.mkdir(dst_dir_path)

    for label_name in os.listdir(dir_path):
        video_jpg_process(dir_path, dst_dir_path, label_name)



