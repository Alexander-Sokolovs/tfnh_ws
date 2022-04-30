#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy

from gpiozero import DistanceSensor
from time import sleep
from std_msgs.msg import Int16


class ultrasound_node:
    def __init__(self):
        self.rate = rospy.Rate(5)
        
        self.sensors = []
        self.us_pubs = []
        self.echo_pins = [18]
        self.trig_pins = [17]
        for i in range(self.echo_pins):
            self.sensors.append(DistanceSensor(echo=self.echo_pins[i], trigger=self.trig_pins[i]))
            self.us_pubs.append(rospy.Publisher(str("/us/distances_"+i), Int16, queue_size=1))

    def run(self):
        while not rospy.is_shutdown():
            for i in range(self.echo_pins):
                self.us_pubs.publish(self.sensors.distance*100)
                sleep(0.1)
            self.rate.sleep()

if __name__ == "__main__":
    rospy.init_node("utrasound")

    us = ultrasound_node()
    us.run()