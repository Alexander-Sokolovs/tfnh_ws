#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from emotions.msg import motor_spd
import serial

class serial_out_node:
    def __init__(self):
        print("Starting serial_out")

        self.ser = serial.Serial('/dev/ACM0', baudrate=9600)

        self.rate = rospy.Rate(15)

        self.prio_listener = rospy.Subscriber("/prio/motor_spd", motor_spd, self.serial_out_cb)

    def serial_out_cb(self, msg):
        #print("Insert code for serial sending")
        message = str(msg.m1) +','+str(msg.m2)

        self.ser.write(str.encode(message))

if __name__ == "__main__":
    rospy.init_node("serial_out")

    s_out = serial_out_node()
    rospy.spin()
    s_out.ser.close()
