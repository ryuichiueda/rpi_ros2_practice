# SPDX-FileCopyrightText: 2023 Ryuichi Ueda 　　　　　
# SPDX-License-Identifier: BSD-3-Clause
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int16MultiArray

class LightSensors(Node):
    def __init__(self):
        super().__init__("lightsensors")
        self.declare_parameter("freq", 10)
        self.pub = self.create_publisher(Int16MultiArray, "lightsensors", 10)
        self.freq = self.get_parameter("freq").value
        self.timer = self.create_timer(1/self.freq, self.cb)

    def cb(self):
        if self.freq != self.get_parameter("freq").value:
            self.freq = self.get_parameter("freq").value
            self.timer.destroy()
            self.timer = self.create_timer(1/self.freq, self.cb)

        devfile = '/dev/rtlightsensor0'
        try:
            with open(devfile, 'r') as f:
                data = f.readline().split()
                msg = Int16MultiArray()
                msg.data = [ int(e) for e in data ] 
                self.pub.publish(msg)
        except:
            self.get_logger().info("cannot publish")

def main():
    rclpy.init()
    lightsensors = LightSensors()
    rclpy.spin(lightsensors)
