#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import serial
from std_msgs import String

class serial_in_node:
    def __init__(self):
        print("Starting serial_out")

        self.arduino = serial.Serial('/dev/ACM0', baudrate=1000000)

        self.rate = rospy.Rate(15)

        while not self.arduino.isOpen():
            print("[Serial in] Connecting to arduino...")
            rospy.sleep(1)    

        print("{} connected!".format(self.arduino.port))

        self.serial_pub = rospy.Publisher("/arduino_serial", String, queue_size=1)

    def run(self):
        while not rospy.is_shutdown():
            while self.arduino.inWaiting()==0: pass
            if self.arduino.inWaiting()>0: 
                answer=self.arduino.readline()
                self.serial_pub.publish(answer)
                self.arduino.flushInput() #remove data after reading

if __name__ == "__main__":
    rospy.init_node("serial_in")

    s_in = serial_in_node()
    rospy.spin()
    s_in.arduino.close()
