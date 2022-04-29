#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import serial
from std_msgs.msg import String

class serial_in_node:
    def __init__(self):
        print("Starting serial_in")

        self.arduino = serial.Serial('/dev/ttyACM0', baudrate=1000000)
        rospy.sleep(1)
        self.rate = rospy.Rate(15)

        while not self.arduino.isOpen():
            print("[Serial in] Connecting to arduino...")
            rospy.sleep(1)    

        print("{} connected!".format(self.arduino.port))

        self.serial_pub = rospy.Publisher("/arduino_serial", String, queue_size=1)
        self.run()

    def run(self):
        print("started")
        try:
            while not rospy.is_shutdown():
                while self.arduino.inWaiting()==0: pass
                if  self.arduino.inWaiting()>0: 
                    answer=self.arduino.readline()
                    self.serial_pub.publish(str(answer))
                    self.arduino.flushInput() #remove data after reading
        except KeyboardInterrupt:
            print("KeyboardInterrupt has been caught.")

if __name__ == "__main__":
    rospy.init_node("serial_in")

    s_in = serial_in_node()
    rospy.spin()
    s_in.arduino.close()
