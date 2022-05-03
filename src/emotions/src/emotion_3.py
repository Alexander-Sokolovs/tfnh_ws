#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import count
import rospy
from emotions.msg import motor_spd
import random

class emotion_3_node:
    def __init__(self):
        print("Starting emotion 3")
        self.m1 = 0
        self.m2 = 0
        self.counter = 0
        self.rate = rospy.Rate(1)

        self.motor_speed_pub = rospy.Publisher("/emotion_3/motor_spd", motor_spd, queue_size=1)

    def run(self):
        while not rospy.is_shutdown():
            speed = motor_spd()
            speed.m1 = self.m1
            speed.m2 = self.m2
            self.motor_speed_pub.publish(speed)
            self.rate.sleep()
            self.counter += 1
            if self.counter > self.period:
                self.counter = 0
                self.period = random.randint(1,10)
                self.m1 = 100
                self.m2 = 100
            else:
                self.m1 = 0
                self.m2 = 0

            

if __name__ == "__main__":
    rospy.init_node("emotion_3")

    e = emotion_3_node()
    e.run()