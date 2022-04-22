#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from emotions.msg import motor_spd
import serial

class serial_out_node:
    def __init__(self):
        print("Starting serial_out")

        self.arduino = serial.Serial('/dev/ACM0', baudrate=1000000)

        self.rate = rospy.Rate(15)

        while not self.arduino.isOpen():
            print("[Serial out] Connecting to arduino...")
            rospy.sleep(1)    

        print("{} connected!".format(self.arduino.port))

        self.prio_listener = rospy.Subscriber("/prio/motor_spd", motor_spd, self.serial_out_cb)

    def serial_out_cb(self, msg):
        message = str(msg.m1) +','+str(msg.m2)

        self.arduino.write(str.encode(message))

if __name__ == "__main__":
    rospy.init_node("serial_out")

    s_out = serial_out_node()
    rospy.spin()
    s_out.arduino.close()
