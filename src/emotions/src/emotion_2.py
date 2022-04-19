#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Int16
from emotions.msg import motor_spd

class emotion_2_node:
    def __init__(self):
        print("Starting emotion 2")
        self.m1 = 0
        self.m2 = 0
        self.rate = rospy.Rate(15)

        self.motor_speed_pub = rospy.Publisher("/emotion_2/motor_spd", motor_spd, queue_size=1)

    def run(self):
        self.m1 = 100
        self.m2 = 100
        while not rospy.is_shutdown():
            speed = motor_spd()
            speed.m1 = self.m1
            speed.m2 = self.m2
            self.motor_speed_pub.publish(speed)
            self.rate.sleep()

if __name__ == "__main__":
    rospy.init_node("emotion_2")

    e = emotion_2_node()
    e.run()