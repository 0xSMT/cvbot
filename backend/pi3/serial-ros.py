#!/usr/bin/env python

import rospy
from rosserial_python import SerialClient
from serial import SerialException

from time import sleep

import json

def main_loop():
    while not rospy.is_shutdown():
        try:
            serial_client.run()
        except KeyboardInterrupt:
            rospy.loginfo("Keyboard interrupt")
            return
        except SerialException:
            sleep(1.0)
            continue
        except OSError:
            sleep(1.0)
            continue

if __name__ == '__main__':
    rospy.init_node("serial_node")

    baud = None
    port = None

    if not port:
        port = rospy.get_param('~port','/dev/ttyUSB0')

    if not baud:
        baud = int(rospy.get_param('~baud','9600')) #57600

    serial_client = SerialClient(port, baud)

    main_loop()
