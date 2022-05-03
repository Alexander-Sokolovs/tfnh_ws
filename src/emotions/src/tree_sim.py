#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from emotions.msg import motor_spd
import math as m

class sim_node:
    def __init__(self):
        print("Starting emotion 1")
        
        self.spd = motor_spd()
        self.x = 0
        self.y = 0
        self.alpha = 0

        self.l = 1

        self.rate = rospy.Rate(15)

        self.motor_speed_pub = rospy.Subscriber("/prio/motor_spd", motor_spd, self.spd_cb)

    def run(self):
        self.x = 0.5 * self.x + (self.spd.m1+self.spd.m2)*m.cos(self.alpha)
        self.y = 0.5 * self.y + (self.spd.m1+self.spd.m2)*m.sin(self.alpha)
        self.alpha=1/self.l * self.alpha + self.spd.m1-self.spd.m2
        print(self.x, self.y)
    
    def spd_cb(self, msg):
        self.spd = msg



if __name__ == "__main__":
    rospy.init_node("sim_node")

    e = sim_node()
    e.run()