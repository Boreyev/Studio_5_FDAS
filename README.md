# Studio_5_FDAS
Repository for the development of FDAS (Face Detection Attendance System).

## Purpose
This system is designed to detect students faces to mark them down as present, late or absent for class.
The purpose of the system is to automate the attendance taking process for tutors. Which will allow the allocation of more time for learning, and a decreased workload for tutors. 

## Requirements
- Python
- IDE 
- USB 2.0 Webcam
### Libraries
- numpy
- face_recognition
- opencv-python
- cvui
- screeninfo
- cmake

## How to get app running:
###### 1. open vs code terminal
ctrl + shift + `
###### 2. create virtual env: 
``` 
python -m venv venv 
```
###### 3. activate virtual env: 
``` 
venv/Scripts/activate 
```
###### 4. install libraries:
``` 
pip install numpy 
```
``` 
pip install face_recognition 
```
``` 
pip install opencv-python
```
``` 
pip install cvui
```
``` 
pip install screeninfo
```

### Note:
you may need to run
``` 
pip install cmake 
```
in order to install face_recognition
