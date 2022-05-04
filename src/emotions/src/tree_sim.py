#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import numpy as np
from emotions.msg import motor_spd
import math as m
import matplotlib.pyplot as plt
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
class sim_node:
    def __init__(self):
        print("Starting tree_sim")
        self.fig=plt.figure()
        plt.axis([-1000,1000,-1000,1000])
        
        self.spd = motor_spd()
        self.pose = Pose()

        self.x = 0
        self.y = 0
        self.alpha = 0

        self.l = 1

        self.rate = rospy.Rate(1500)

        self.motor_speed_listener = rospy.Subscriber("/prio/motor_spd", motor_spd, self.spd_cb)
        self.motor_speed_listener = rospy.Subscriber("turtle1/pose", Pose, self.pose_cb)

        self.turtle_pub = rospy.Publisher("turtle1/cmd_vel", Twist, queue_size=1)

    def run(self):
        while not rospy.is_shutdown():
            angular = self.spd.m1-self.spd.m2
            speed_vec = (self.spd.m1 + self.spd.m2)/2
            
            twist = Twist()
            twist.angular.z = angular/3
            twist.linear.x = speed_vec/3
            self.turtle_pub.publish(twist)

            self.rate.sleep()

            # self.x = 0.5 * self.x + (self.spd.m1+self.spd.m2)*m.cos(self.alpha)
            # self.y = 0.5 * self.y + (self.spd.m1+self.spd.m2)*m.sin(self.alpha)
            # self.alpha=(1/self.l) * self.alpha + self.spd.m1-self.spd.m2
            # # print(self.x, self.y)
            # print(self.alpha)
            # self.rate.sleep()
            # plt.scatter(self.x, self.y)
            # self.fig.show()
            # self.fig.canvas.draw()
            
            # plt.pause(1) #Note this correction
        
    
    def spd_cb(self, msg):
        self.spd = msg

    def pose_cb(self, msg):
        self.pose = msg



if __name__ == "__main__":
    rospy.init_node("sim_node")

    e = sim_node()
    e.run()