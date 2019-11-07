#!/usr/bin/env python

import rospy

from std_msgs.msg import UInt8MultiArray
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Float64
from std_msgs.msg import String

import time
from time import sleep

import json    
import robot_state

rs = robot_state.RobotState()

def make_recv_fn(topic, rmap, json_data):
    cont_name = None

    # print(str(json_data))

    for name in json_data["names"]:
        for key in json_data["topics"][name]:
            if json_data["topics"][name][key] == topic:
                # print("`" + topic + "` is for `" + name + "`")
                cont_name = name
                break

    def recv_fn(sent_string):
        # print("recv for: [" + cont_name + "] on topic -> (" + topic + ")")
        as_str = sent_string.data

        # echo_publisher.publish(String(data=as_str))

        if json_data["topics"][cont_name]["button"] == topic:
            int_arr = [int(x.strip()) for x in as_str.split(',')]

            rmap[cont_name][int_arr[0]](rs)


        elif json_data["topics"][cont_name]["left_joystick"] == topic:
            float_arr = [float(x.strip()) for x in as_str.split(',')]

            rmap[cont_name][json_data["map"]["left_joystick_move"]](rs, float_arr[0], float_arr[1])


        elif json_data["topics"][cont_name]["right_joystick"] == topic:
            str_arr = [x.strip() for x in as_str.split(',')]
            float_arr = [float(x) for x in str_arr]

            rmap[cont_name][json_data["map"]["right_joystick_move"]](rs, float_arr[0], float_arr[1])


        elif json_data["topics"][cont_name]["right_trigger"] == topic:
            float_arr = [float(x.strip()) for x in as_str.split(',')]

            rmap[cont_name][json_data["map"]["right_trigger_change"]](rs, float_arr[0])


        elif json_data["topics"][cont_name]["left_trigger"] == topic:
            float_arr = [float(x.strip()) for x in as_str.split(',')]

            rmap[cont_name][json_data["map"]["left_trigger_change"]](rs, float_arr[0])
    
    return recv_fn

def main_loop(avr_publisher):
    last_time = time.time()
    INTERVAL = 0.25

    while not rospy.is_shutdown():
        try:
            if rs.stale:
                rospy.loginfo("Robot Updated State: %s" % list(rs.as_arr()))
                avr_publisher.publish(Float32MultiArray(data=rs.as_arr()))
                rs.stale = False
            else:
                if time.time() - last_time >= INTERVAL:
                    avr_publisher.publish(Float32MultiArray(data=rs.as_arr()))
                    last_time = time.time()
        except KeyboardInterrupt:
            rospy.loginfo("Keyboard interrupt")
            return
        except OSError:
            sleep(1.0)
            continue
        
        sleep(0.01) # might help?

if __name__ == '__main__':
    rospy.init_node("control_node")

    config_file_path = "/home/tulsarmc/catkin_ws/src/cv_bot2/scripts/config.json"
    json_data = json.load(open(config_file_path))

    cont_map = robot_state.make_controller_map(json_data["controller"]["map"], json_data["controller"]["names"])
    mqtt_topics = json_data["mqtt"]["topics"]
    for topic in mqtt_topics:
        rospy.Subscriber(topic, String, make_recv_fn(topic, cont_map, json_data["controller"]))

    avr_topic = json_data["ros"]["arduino"]
    avr_publisher = rospy.Publisher(avr_topic, Float32MultiArray, queue_size=100)

    main_loop(avr_publisher)