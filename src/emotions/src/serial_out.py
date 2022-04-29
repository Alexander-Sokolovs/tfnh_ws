#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from emotions.msg import motor_spd
import serial

class serial_out_node:
    def __init__(self):
        print("Starting serial_out")

        self.message = ""

        self.arduino = serial.Serial('/dev/ttyACM0', baudrate=1000000)

        self.rate = rospy.Rate(15)

        while not self.arduino.isOpen():
            print("[Serial out] Connecting to arduino...")
            rospy.sleep(1)    

        print("{} connected!".format(self.arduino.port))

        self.prio_listener = rospy.Subscriber("/prio/motor_spd", motor_spd, self.serial_out_cb)

        self.run()

    def run(self):
        while not rospy.is_shutdown():
            self.arduino.write(str.encode(self.message))
            self.rate.sleep()

    def serial_out_cb(self, msg):
        self.message = str(msg.m1) +','+str(msg.m2) + '\n'

        

if __name__ == "__main__":
    rospy.init_node("serial_out")

    s_out = serial_out_node()
    rospy.spin()
    s_out.arduino.close()
