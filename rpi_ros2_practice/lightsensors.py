# SPDX-FileCopyrightText: 2023 Ryuichi Ueda 　　　　　
# SPDX-License-Identifier: BSD-3-Clause
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int16MultiArray

class LightSensors():
    def __init__(self, node_ref):
        self.node = node_ref
        self.node.declare_parameter("freq", 10)
        self.pub = self.node.create_publisher(Int16MultiArray, "lightsensors", 10)
        self.freq = self.node.get_parameter("freq").value
        self.timer = self.node.create_timer(1/self.freq, self.cb)

    def cb(self):
        if self.freq != self.node.get_parameter("freq").value:
            self.freq = self.node.get_parameter("freq").value
            self.timer.destroy()
            self.timer = self.node.create_timer(1/self.freq, self.cb)

        devfile = '/dev/rtlightsensor0'
        try:
            with open(devfile, 'r') as f:
                data = f.readline().split()
                msg = Int16MultiArray()
                msg.data = [ int(e) for e in data ] 
                self.pub.publish(msg)
        except:
            self.node.get_logger().info("cannot publish")

def main():
    rclpy.init()
    node = Node("lightsensors")
    talker = LightSensors(node)
    rclpy.spin(node)


if __name__ == '__main__':
    main()
