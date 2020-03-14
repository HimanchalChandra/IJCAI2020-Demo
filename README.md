# AI-AMA: Automated and Interactive Attendance Management Application


Automated Attendance Management is essential in educational institutions for efficient
monitoring of students, especially in countries with a high student-teacher ratio. The current
methods include RFID and Biometric based methods for automated attendance recording.
However, these methods come with their security and hygiene issues respectively. The
current state of the art Face Recognition technology has been proven to be highly secure and
efficient. This project focuses on an automated and interactive attendance management
application for mobile devices. The application provides four top-level services: real-time
attendance monitoring, attendance management, student registration, and student deletion.
Initial processing on frames like face detection and alignment is done using the MTCNN
algorithm. To support near real-time usability on mobile devices, we implemented memory and
compute-optimized version of FaceNet’s face clustering and recognition algorithm. The
network’s inference is a 512-dimensional embedding which is used for recognition based on
euclidean distances from other face embeddings.
<br>
<br>

<img src="https://github.com/ankursikarwar/IJCAI2020-Demo/blob/master/UI.png" alt="Image4" width="500" height="400"/>     

<br>
<br>

## INSTALLATIONS

1.Logged into your Ubuntu server as a sudo non-root user, first update and upgrade your system to ensure that your shipped version of Python 3 is up-to-date. 

```
sudo apt update -y && sudo apt full-upgrade -y
```

2. Check which version of Python 3 is installed by typing: 

```
python3 -V
```
You’ll receive output similar to the following, depending on when you have updated your system.

```
Python 3.6.9
```

3. Virtual environments enable you to have an isolated space on your server for Python projects. We’ll use venv, part of the standard Python 3 library, which we can install by typing:

```
sudo apt install -y python3-venv
```
4. Create a project folder


```
mkdir attendance_interface
cd attendance_interface
```
5. Initialize virtual environment 

```
python3 -m venv my_env
```
6. Activate the virtual environment

```
source my_env/bin/activate
```

7. Clone the Repo

```
(my_env) git clone https://github.com/ankursikarwar/IJCAI2020-Demo.git
```
8. Navigate to the sub-folder

```
(my_env) cd IJCAI2020-Demo
```

9. Install the dependencies

```
(my_env) pip install -r requirements.txt
```

10. Starting the Application


```
(my_env) python demo.py
```



## LICENSE


This project is licensed under the MIT License.
