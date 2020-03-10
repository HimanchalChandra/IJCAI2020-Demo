AI-AMA: Automated and Interactive Attendance Management Application
###################################################################


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


.. image:: https://github.com/ankursikarwar/IJCAI2020-Demo/blob/master/UI.png


REFERENCES
==========

.. [ZHANG2016] Zhang, K., Zhang, Z., Li, Z., and Qiao, Y. (2016). Joint face detection and alignment using multitask cascaded convolutional networks. IEEE Signal Processing Letters, 23(10):1499–1503.

.. [CAO2018] Q. Cao, L. Shen, W. Xie, O. M. Parkhi, A. Zisserman (2018). VGGFace2: A dataset for recognising face across pose and age. International Conference on Automatic Face and Gesture Recognition, 2018.

.. [SCHROFF2015] Florian Schroff, Dmitry Kalenichenko, James Philbin (2015). FaceNet: A Unified Embedding for Face Recognition and Clustering. IEEE Computer Society Conference on Computer Vision and Pattern Recognition, 2015.



LICENSE
=======

This project is licensed under the MIT License.
