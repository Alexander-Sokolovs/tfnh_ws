#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Int16
from emotions.msg import motor_spd

class emotion_1_node:
    def __init__(self):
        print("Starting emotion 1")
        self.m1 = 0
        self.m2 = 0
        self.rate = rospy.Rate(15)

        self.motor_speed_pub = rospy.Publisher("/emotion_1/motor_spd", motor_spd, queue_size=1)

    def run(self):
        
        while not rospy.is_shutdown():
            self.count(0, 1, 100)
            self.count(100, -1, 0)

    def count(self, start, step, stop):
        for i in range(start, stop, step):
            self.m1 = i
            self.m2= 100-i

            speed = motor_spd()
            speed.m1 = self.m1
            speed.m2 = self.m2
            self.motor_speed_pub.publish(speed)
            self.rate.sleep()
            if rospy.is_shutdown():
                return

if __name__ == "__main__":
    rospy.init_node("emotion_1")

    e = emotion_1_node()
    e.run()