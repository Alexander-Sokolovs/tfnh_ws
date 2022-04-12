#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Int16

class emotion_1:
    def __init__(self):
        print("Starting emotion 1")
        self.m1 = 0
        self.m2 = 0
        self.rate = rospy.Rate(15)

        self.motor1_speed_pub = rospy.Publisher("/emotion_1/m1", Int16, queue_size=1)
        self.motor2_speed_pub = rospy.Publisher("/emotion_1/m2", Int16, queue_size=1)

    def run(self):
        
        while not rospy.is_shutdown():
            self.count(0, 1, 100)
            self.count(100, -1, 0)

    def count(self, start, step, stop):
        for i in range(start, stop, step):
                self.m1 = i
                self.m2= 100-i
                self.motor1_speed_pub.publish(self.m1)
                self.motor2_speed_pub.publish(self.m2)
                self.rate.sleep()
                if rospy.is_shutdown():
                    return

if __name__ == "__main__":
    rospy.init_node("emotion_1")

    e = emotion_1()
    e.run()