#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from emotions.msg import motor_spd
import math as m
import random

class emotion_4_node:
    def __init__(self):
        print("Starting emotion 4")
        self.m1 = 0
        self.m2 = 0
        self.rate = rospy.Rate(1500)

        self.motor_speed_pub = rospy.Publisher("/emotion_4/motor_spd", motor_spd, queue_size=1)

    def run(self):
        
        while not rospy.is_shutdown():
            r = (random.randint(0,20)-10)/10
            self.count(0, 1, int(200*m.pi), r)
            self.count(int(200*m.pi), -1, 0, r)

    def count(self, start, step, stop, r):
        for i in range(start, stop, step):
            self.m1 = int(m.sin(i/100)*100)
            self.m2= int(m.cos(i/100*r)*100*r)

            speed = motor_spd()
            speed.m1 = self.m1
            speed.m2 = self.m2
            self.motor_speed_pub.publish(speed)
            self.rate.sleep()
            if rospy.is_shutdown():
                return


if __name__ == "__main__":
    rospy.init_node("emotion_4")

    e = emotion_4_node()
    e.run()