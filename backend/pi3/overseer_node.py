#!/usr/bin/env python

"""Responsible for launching the 'managerial node' of the ROS network
Samuel Taylor

The Overseer node is the first node any transmitted packet on the MQTT network will reach. It is the 
master node of the robot. It supports a minimal facility for forwarding packets appropriately and 
launching/killing other ROS nodes as needed.
"""
import rospy

from time import sleep

from std_msgs.msg import UInt8MultiArray
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Float64
from std_msgs.msg import String

import json    
import paho.mqtt.client as mqttc

import struct

import shlex, subprocess

control_process = None
serial_avr_process = None

started = False

def make_image_callback(mqtt_client, topic):
    def screenshot_callback(msg):
        rospy.loginfo("got image:\n")
        rospy.loginfo("publishing to topic: [" + topic + "]")
        
        mqtt_client.publish(topic, msg.data)
    
    return screenshot_callback

def make_forwarding_fn(publishersm, json_config):
    def conv_fn(sent_arr, topic):
        global control_process, started

        arr = [x.encode('UTF8') for x in sent_arr]
        as_str = ''.join(arr)

        # rospy.loginfo("[" + as_str + " vs " + str(json_config["controller"]["map"]["start"]) + "\n")
        # rospy.loginfo(as_str)
        # rospy.loginfo(str(json_config["controller"]["map"]["start_press"]))
        # rospy.loginfo(topic)
        # rospy.loginfo(json_config["controller"]["topics"]["drive"]["button"])

        rospy.loginfo(as_str == str(json_config["controller"]["map"]["start_press"]))
        rospy.loginfo(topic == json_config["controller"]["topics"]["drive"]["button"])

        if as_str == str(json_config["controller"]["map"]["start_press"]) and topic == json_config["controller"]["topics"]["drive"]["button"]:
            if not started:
                control_process = subprocess.Popen(shlex.split("rosrun cv_bot2 control_node.py")) # TODO
                serial_avr_process = subprocess.Popen(shlex.split("rosrun cv_bot2 serial-ros.py")) # TODO
                started = True
            else:
                control_process.kill()
                serial_avr_process.kill()
                started = False
        publishers[topic].publish(String(data=as_str))

    return conv_fn

# The callback for when a PUBLISH message is received from the server.
def make_on_message(map_fn, debug=True):
    def on_message(mqtt_client, userdata, msg):
        if debug:
            rospy.loginfo("MQTT payload: %s" % list(msg.payload))

        map_fn(list(msg.payload), msg.topic) 

    return on_message

def make_on_connect(topics, debug=True):
    def on_connect(mqtt_client, userdata, flags, rc):
        if debug: 
            rospy.loginfo("MQTT connected with result code " + str(rc))

        for topic in topics:
            mqtt_client.subscribe(topic)
    
    return on_connect

def main_loop():
    while not rospy.is_shutdown():
        try:
            mqtt_client.loop()
        except KeyboardInterrupt:
            rospy.loginfo("Keyboard interrupt")
            return
        except OSError:
            sleep(1.0)
            continue

if __name__ == '__main__':
    rospy.init_node("overseer_node")

    config_file_path = "/home/tulsarmc/catkin_ws/src/cv_bot2/scripts/config.json"

    json_data = json.load(open(config_file_path))

    server = json_data["mqtt"]["server"]
    mqtt_topics = json_data["mqtt"]["topics"]

    publishers = {}

    for topic in mqtt_topics:
        publishers[topic] = rospy.Publisher(topic, String, queue_size=10)

    map_fn = make_forwarding_fn(publishers, json_data)

    mqtt_client = mqttc.Client(transport="websockets")
    mqtt_client.on_connect = make_on_connect(mqtt_topics)
    mqtt_client.on_message = make_on_message(map_fn)

    mqtt_client.connect(server, port=9001)

    rospy.Subscriber(json_data["ros"]["img_from_lefteye_topic"], UInt8MultiArray, make_image_callback(mqtt_client, json_data["ros"]["left_img_from_master_topic"]))
    rospy.Subscriber(json_data["ros"]["img_from_righteye_topic"], UInt8MultiArray, make_image_callback(mqtt_client, json_data["ros"]["right_img_from_master_topic"]))

    main_loop()