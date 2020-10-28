
## how to build a face-tracking with Raspberry and OpenCV

This is my very first project on Raspberry. My motivations come from the article of [Leigh Johnson](undefined) :
>  [https://towardsdatascience.com/real-time-object-tracking-with-tensorflow-raspberry-pi-and-pan-tilt-hat-2aeaef47e134](https://towardsdatascience.com/real-time-object-tracking-with-tensorflow-raspberry-pi-and-pan-tilt-hat-2aeaef47e134)

It seems simple to start a project on Raspberry, so let’s start.

*My github repos for this project : [https://github.com/nguyenrobot/palt-tilt-cam](https://github.com/nguyenrobot/palt-tilt-cam)*

This project is realized in collaboration with **Clément COSTE, **one of my colleagues.
<img src="mono_face_GIF2.gif" alt="" style="width: 700px;"/>

## Part 1 — Build List

* Raspberry Pi 4 Model B — 4GB

* Pan-Tilt HAT for Raspberry Pi

* Pi Camera v2 8MP

* Micro-SD Card

* Mini-HDMI Cable

* Cable for Raspberry Pi Camera — Dimension : 457mm x 16mm (18" x 0.6")

* USB-C Charger

* USB-C External battery (optional by strongly recommended)

I spent roughly 100€ to get all necessary thing in France where we pay so much of TVA tax.

The choice of Pan-Tilt HAT is quite important. Because you have to find a way to control your Pan-Tilt HAT. I use the Pan-Tilt HAT from [Waveshare](https://www.waveshare.com/pan-tilt-hat.htm) which I have to spend sometimes to understand how to manually control the servo-motor via HAT by keyboard.

An external battery with USB-C output is highly useful for other projects on Raspberry in which your Raspberry must be mobile.

## Part 2 — Install software for Raspberry

* Install Raspberry Operating System : you can choose any system that Python could run well. Here is the official page for Raspberry OS : [https://www.raspberrypi.org/downloads](https://www.raspberrypi.org/downloads/). **Raspberry Pi OS **is recommended

* Enable Pi Camera for your Raspberry

* Enable SSH on your Raspberry

* Install Python, version 3 is recommended

* Install OpenCV, version 4.2 is recommended

* *if some modules are missing for Python, don’t be worry and search for their installations on Raspberry or Python community*

## Part 3— Control your pan-tilt camera by keyboard

This part is relatively difficult to me. I spent most of my time in the project just to be able to control my pan-tilt camera by keyboard.

Why this is so difficult for me ? Because, there are two ways to control your servo-motor :

* directly plug your servo-motor to Raspberry then control them directly by Raspberry, in this cases we will use GPIO interface

* plug your servo-motor to HAT platforme then HAT is pluged on Raspberry. So from Raspberry, we control the HAT platform then the HAT platform in turn control our servo-motors. In this case, I used given driver by waveshare PCA9685 : [https://github.com/nguyenrobot/palt-tilt-cam/blob/master/Pan-Tilt_HAT_user_manual_en.pdf](https://github.com/nguyenrobot/palt-tilt-cam/blob/master/Pan-Tilt_HAT_user_manual_en.pdf)

## Part 3*— Calibrate your pan-tilt servo-motors *at 0-position*

This part is not compulsory but highly recommended.
>  you can execute my code [https://github.com/nguyenrobot/palt-tilt-cam/blob/master/key_pantiltcontrol.py](https://github.com/nguyenrobot/palt-tilt-cam/blob/master/key_pantiltcontrol.py) to navigate your servos with a keyboard.

![servo shaft’s screw](https://cdn-images-1.medium.com/max/8064/1*xEy3-fl7H6INJpZwNZEKRw.jpeg)

It’s important that you should not tight the servo shaft’s screw in the beginning, you just need to slightly fix it in the way that is can freely rotate. With the control from your keyboard, you can try to rotate your servo at the 0-position and then you can move your camera to your prefered start-position. In the end, you can now tight the servo shaft’s screw.

*(the tilt-servo screw is under the base, so we need to install tilt-servo on the base, then calbrate, then disassemble, then tight the tilt-servo screw before reinstalling it)*

## Part 4 — Coding for face tracking

>I used pre-installed **CascadeClassifier **coming with OpenCV be default to get easy in the beginning. I focus my work on how to control the pan and tilt angles.
>  **CascadeClassifier **has a pre-trained for frontal face-recognition found in OpenCV directory + /data/haarcascade_frontalface_default.xml

The **CascadeClassifier **give us directly a set of information (x, y, w, h) for each detected face in a frame. (x,y) is the position of top-left corner of detected face, (w, h) is the height and with of detected face, from these informations we can calculate a detected face’s center.

**>Face’s center**

When we get (x,y), it’s to control our pan and tilt servo to move the camera to a position that face’center should be near to the frame’s center

**>Pseudo-PD controller**

Why pseudo-PD ? Because our servos don’t have position sensors so we don’t know pan-angle and tilt-angle of our robotised camera. Hence, we can not strictly use feedback control. I used a pseudo-PD controller which simply used delta_PAN to increment/decrement our camera pan-angle(resp. til-angle) :
>  delta_PAN = k_PAN * delta_x + kd_PAN * delta_x_dot

Roughly, it’s a kind of feed-forward controller.

If you find a better way to control when we don’t have information about servo’s position, please let me know by sending me an email.

**>Funny message**

I try to add some randomized message modules to get the algorithm funny :

* bonjour : randomized welcome messages when the camera first detected a face

* cachecache : randomized ‘stay away from me’ message when we stay too long before the camera

* missing : randomized messages when nothing detected

It’s really funny for a demo with my colleagues. But, the fact to add theses funny messages get my algorithm lagged sometimes. So, you can eliminate these modules to get your camera more speedy.

**>Multi-face detection**

**CascadeClassifier **can find multi faces in a frame, but I limited the PD controller to just the case that one face 1 face is detected. It’s your turn to improve this. An idea is to calculate a centroid of detected faces.
<img src="multi_face_GIF2.gif" alt="" style="width: 700px;"/>

>  The code : you can found all codes in my github repos  
>  **cam_pantiltcontrol.py** is the main script  
[**nguyenrobot/palt-tilt-cam**
*Use OpenCV for Face Detection then Pilote a Pi Camera with 2 servos in order to keep the tracked-face always in the…*github.com]  
(https://github.com/nguyenrobot/palt-tilt-cam)

## Part 5— 3D-printing of Raspberry casing

We found that in the end it’s cool to make 3D printing for our Raspberry casing. So we get started with a basic 3D-printer from Ender.

![3D-printed casing for Raspberry](https://cdn-images-1.medium.com/max/2480/1*1WVyH73Bi_Zmomw9YFkiOw.png)
