#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Int16
from emotions.msg import motor_spd
import time
import random
class emotion_1_node:
    def __init__(self):
        print("Starting emotion 1")
        self.m1 = 0
        self.m2 = 0
        self.rate = rospy.Rate(15)

        self.motor_speed_pub = rospy.Publisher("/emotion_1/motor_spd", motor_spd, queue_size=1)

    def run(self):
        
        while not rospy.is_shutdown():
            r = (random.randint(0,100))/1000
            self.count(50, 1, 100, r)
            self.count(100, -1, 50, r)
            print("r: ",r)
    def count(self, start, step, stop, r):
        for i in range(start, stop, step):
            self.m1 = i
            self.m2= 100-i

            speed = motor_spd()
            speed.m1 = self.m1
            speed.m2 = self.m2
            self.motor_speed_pub.publish(speed)
            time.sleep(r)
            if rospy.is_shutdown():
                return

if __name__ == "__main__":
    rospy.init_node("emotion_1")

    e = emotion_1_node()
    e.run()