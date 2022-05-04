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
        self.e3 = motor_spd()
        self.e4 = motor_spd()

        self.motor_speed_pub = rospy.Publisher("/prio/motor_spd", motor_spd, queue_size=1)

        self.emotion_1_listener = rospy.Subscriber("/emotion_1/motor_spd", motor_spd, self.e1_callback)
        self.emotion_2_listener = rospy.Subscriber("/emotion_2/motor_spd", motor_spd, self.e2_callback)
        self.emotion_3_listener = rospy.Subscriber("/emotion_3/motor_spd", motor_spd, self.e3_callback)
        self.emotion_4_listener = rospy.Subscriber("/emotion_4/motor_spd", motor_spd, self.e4_callback)

        self.us_listener = rospy.Subscriber("/us/distances_0", Int16, self.us_callback, (0)) # continue here

    def run(self):
        while not rospy.is_shutdown():
            prio_tmp = self.priority_function_5(self.e1, self.e2, self.e3, self.e4)
            self.drive_motors(prio_tmp)
            self.rate.sleep()

    def priority_function_1(self, e1, e2, e3, e4):
        speed = motor_spd()
        result = np.array([(e1.m1+e2.m1)/2, (e1.m2+e2.m2)/2])

        speed.m1 = int(result[0])
        speed.m2 = int(result[1])

        # speed.m1 = 5
        # speed.m2 = 2

        return speed

    def priority_function_2(self, e1, e2, e3, e4):
        speed = motor_spd()
        #e4.m1*(100-self.us_distances[0])*0.5+e1.m1*0.3+e2.m1*0.1+e3.m1*0.1
        result = np.array([e4.m1*(100-self.us_distances[0])*0.5+e1.m1*0.3+e2.m1*0.1+e3.m1*0.1, e4.m2*(100-self.us_distances[0])*0.5+e1.m2*0.3+e2.m2*0.1+e3.m2*0.1])
        speed.m1 = int(result[0])
        speed.m2 = int(result[1])

        return speed

    def priority_function_3(self, e1, e2, e3, e4):
        speed = motor_spd()
        result = np.array([e1.m1, e1.m2])

        speed.m1 = int(result[0])
        speed.m2 = int(result[1])

        # speed.m1 = 20
        # speed.m2 = 50

        return speed

    def priority_function_4(self, e1, e2, e3, e4):
        speed = motor_spd()
        m1 = min(abs(e1.m1), abs(e2.m1), abs(e3.m1), abs(e4.m1))
        m2 = min(abs(e1.m2), abs(e2.m2), abs(e3.m2), abs(e4.m2))
        #result = np.array([e1.m1, e1.m2])

        speed.m1 = int(m1)
        speed.m2 = int(m2)

        # speed.m1 = 20
        # speed.m2 = 50

        return speed

    def priority_function_5(self, e1, e2, e3, e4):
        speed = motor_spd()
        result = np.array([(e1.m1+e4.m1)/2, (e1.m2+e4.m2)/2])

        speed.m1 = int(result[0])
        speed.m2 = int(result[1])

        # speed.m1 = e4.m1
        # speed.m2 = e4.m2

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

## Emotion 4 ##
    def e4_callback(self, msg):
        self.e4 = msg

## Interface to motors
    def drive_motors(self, speed):
        # print(str(m1) + " : " + str(m2))
        self.motor_speed_pub.publish(speed)
        return

if __name__ == "__main__":
    rospy.init_node("prioritiser")

    p = prioritiser_node()
    p.run()