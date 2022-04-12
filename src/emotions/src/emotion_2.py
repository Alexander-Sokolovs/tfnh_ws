#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Int16

class emotion_2:
    def __init__(self):
        print("Starting emotion 2")
        self.m1 = 0
        self.m2 = 0
        self.rate = rospy.Rate(15)

        self.motor1_speed_pub = rospy.Publisher("/emotion_2/m1", Int16, queue_size=1)
        self.motor2_speed_pub = rospy.Publisher("/emotion_2/m2", Int16, queue_size=1)

    def run(self):
        self.m1 = 100
        self.m2 = 100
        while not rospy.is_shutdown():
            self.motor1_speed_pub.publish(self.m1)
            self.motor2_speed_pub.publish(self.m2)
            self.rate.sleep()

if __name__ == "__main__":
    rospy.init_node("emotion_2")

    e = emotion_2()
    e.run()