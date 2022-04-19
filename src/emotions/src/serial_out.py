#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from emotions.msg import motor_spd

class serial_out_node:
    def __init__(self):
        print("Starting serial_out")

        self.rate = rospy.Rate(15)

        self.prio_listener = rospy.Subscriber("/prio/motor_spd", motor_spd,self.serial_out_cb)

    def serial_out_cb(self):
        print("Insert code for serial sending")

if __name__ == "__main__":
    rospy.init_node("serial_out")

    s_out = serial_out_node()
    s_out.run()