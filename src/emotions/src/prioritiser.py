#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Int16
import numpy as np

class prioritiser:
    def __init__(self):
        print("Starting prioritiser")
        self.rate = rospy.Rate(15)

        self.e1 = np.zeros([2, 1])
        self.e2 = np.zeros([2, 1])

        self.motor1_speed_pub = rospy.Publisher("/prio/m1", Int16, queue_size=1)
        self.motor2_speed_pub = rospy.Publisher("/prio/m2", Int16, queue_size=1)

        self.emotion_1_listener = rospy.Subscriber("/emotion_1/m1", Int16,self.e1_m1_callback)
        self.emotion_1_listener = rospy.Subscriber("/emotion_1/m2", Int16,self.e1_m2_callback)        
        
        self.emotion_2_listener = rospy.Subscriber("/emotion_2/m1", Int16,self.e2_m1_callback)
        self.emotion_2_listener = rospy.Subscriber("/emotion_2/m2", Int16,self.e2_m1_callback)

    def run(self):
        while not rospy.is_shutdown():
            prio_tmp = self.priority_function_1(self.e1, self.e2)
            self.drive_motors(prio_tmp[0], prio_tmp[1])
            self.rate.sleep()

    def priority_function_1(self, e1, e2):
        result = (e1+e2)/2
        return int(result[0]), int(result[1])


## Emotion 1 ##
    def e1_m1_callback(self, msg):
        self.e1[0] = msg.data

    def e1_m2_callback(self, msg):
        self.e1[1] = msg.data

## Emotion 2 ##
    def e2_m1_callback(self, msg):
        self.e2[0] = msg.data

    def e2_m2_callback(self, msg):
        self.e2[1] = msg.data

## Interface to motors
    def drive_motors(self, m1, m2):
        # print(str(m1) + " : " + str(m2))
        self.motor1_speed_pub.publish(m1)
        self.motor2_speed_pub.publish(m2)
        return

if __name__ == "__main__":
    rospy.init_node("prioritiser")

    p = prioritiser()
    p.run()