#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import numpy as np

from emotions.msg import motor_spd
from std_msgs.msg import Int16


class prioritiser_node:
    def __init__(self):
        print("Starting prioritiser")
        self.rate = rospy.Rate(15)

        self.num_us_sensors = 1

        self.us_distances = np.zeros([1, self.num_us_sensors])[0]

        self.e1 = motor_spd()
        self.e2 = motor_spd()

        self.motor_speed_pub = rospy.Publisher("/prio/motor_spd", motor_spd, queue_size=1)

        self.emotion_1_listener = rospy.Subscriber("/emotion_1/motor_spd", motor_spd, self.e1_callback)
        self.emotion_2_listener = rospy.Subscriber("/emotion_2/motor_spd", motor_spd, self.e2_callback)
        self.emotion_3_listener = rospy.Subscriber("/emotion_3/motor_spd", motor_spd, self.e3_callback)

        self.us_listener = rospy.Subscriber("/us/distances_0", Int16, self.us_callback, (0)) # continue here

    def run(self):
        while not rospy.is_shutdown():
            prio_tmp = self.priority_function_1(self.e1, self.e2, self.e3)
            self.drive_motors(prio_tmp)
            self.rate.sleep()

    def priority_function_1(self, e1, e2, e3):
        speed = motor_spd()
        result = np.array([(e1.m1+e2.m1)/2, (e1.m2+e2.m2)/2])

        speed.m1 = int(result[0])
        speed.m2 = int(result[1])

        return speed

## Sensor callbacks
    def us_callback(self, msg, arg):
        self.us_distances[arg] = msg.data

## Emotion 1 ##
    def e1_callback(self, msg):
        self.e1 = msg

## Emotion 2 ##
    def e2_callback(self, msg):
        self.e2 = msg

## Emotion 3 ##
    def e3_callback(self, msg):
        self.e3 = msg

## Interface to motors
    def drive_motors(self, speed):
        # print(str(m1) + " : " + str(m2))
        self.motor_speed_pub.publish(speed)
        return

if __name__ == "__main__":
    rospy.init_node("prioritiser")

    p = prioritiser_node()
    p.run()