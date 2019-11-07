#!/usr/bin/env python

from picamera.array import PiRGBArray
from std_msgs.msg import String
from std_msgs.msg import UInt8MultiArray
from picamera import PiCamera
import rospy

import numpy as np

from time import sleep

RES = (250, 250)

camera = PiCamera()
camera.color_effects = (128, 128)
# rawCapture = PiRGBArray(camera, size=RES)
output = "/home/pi/o.png" 

def make_photo_callback(resolution, pub):
    def take_photo(msg):
        rospy.loginfo(msg)

        msg_data = msg.data

        as_str = str(msg_data)
        int_arr = [int(x.strip()) for x in as_str.split(',')]

        if int_arr[0] == 21:
            # camera.capture(output, format="jpg")
            camera.capture(output)

            f = open(output, "rb")
            rawCapture = np.fromfile(f, dtype=np.uint8)
            # flatten array first perhaps

            as_list = list(rawCapture)

            rospy.loginfo(len(as_list))
            pub.publish(UInt8MultiArray(data=as_list))
        
    return take_photo

def main_loop(publisher):
    while not rospy.is_shutdown():
        try:
            sleep(0.01)
        except KeyboardInterrupt:
            rospy.loginfo("Keyboard interrupt")
            return
        except OSError:
            sleep(1.0)
            continue

if __name__ == '__main__':
    rospy.init_node('pi_cam_left')

    rospy.loginfo("initialized...")

    publisher = rospy.Publisher("limg", UInt8MultiArray, queue_size=10)
    rospy.Subscriber("q", String, make_photo_callback(RES, publisher))

    main_loop(publisher)