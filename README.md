# Gora-based-frame-selection
This project is used for implementation of Action Recognition using GORA-based frame selection preprocessing method
## Getting Started
Before running the code successfully, you should have some packgaes reinstalled and data downloaded.

### Installing
Assume you have Python, temsorflow and keras 2 or later preinstalled, and you have some common packages such as numpy, pandas installed.
```
pip install opencv-python
pip install Pillow
```
I may forget some packages and you can install them as instructed in running the code.
### Getting the data
```
mkdir data
cd data
mkdir sequences
mkdir checkpoints
```
First, download the dataset from UCF and then unzip the videos.
```
wget http://crcv.ucf.edu/data/UCF101/UCF101.rar
unrar e UCF101.rar
```
Assume the videos are under the folder UCF101, extract out the frames.
```
python extract.py UCF101 UCF101_frame
```
Now the frames have the storage structure UCF101_frame/label_name/video_name/frames

Generate the training_testing list.
```
python find_name UCF101_frame
```
## Temporal Reparameterization
Choose frames for learning use based on GORA method.
```
python temporal_mapping.py UCF101_frame even map
```
## Extract features of each video.
You can limit the number of labels by manully set the label number in extract_feature.py file. You have also to set the frame folder manully in the file and extract out the feature for each frame folder respectively.
```
cd 
python extract_features.py
```
## Training models
You can choose which models to train by making changes directly in the train.py file.
```
python train.py
```
## Test 

```
python validate_rnn.py
```
## Authors
* **Chao NI**

## Acknowledgement
Part of this code is forked from https://github.com/harvitronix/five-video-classification-methods

## License
This project is licensed under the MIT License.

