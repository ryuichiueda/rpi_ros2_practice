# SPDX-FileCopyrightText: 2023 Ryuichi Ueda 　　　　　
# SPDX-License-Identifier: BSD-3-Clause
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int16MultiArray

class Agent(Node):
    def __init__(self):
        super().__init__("agent")
        self.ranges = [0, 0, 0, 0]
        self.sub_lightsensors = self.create_subscription(Int16MultiArray, 'lightsensors', self.callback_lightsensors, 10)
        self.pub_motors = self.create_publisher(Int16MultiArray, "motor_raw", 10)
        self.timer = self.create_timer(0.1, self.callback_motors)


    def callback_lightsensors(self, msg):
        self.ranges = [int(e) for e in msg.data] 
        #self.get_logger().info("receive {}".format(self.ranges))


    def callback_motors(self):
        msg = Int16MultiArray()
        msg.data = [100, 100]
        self.pub_motors.publish(msg)


def main():
    rclpy.init()
    agent = Agent()
    rclpy.spin(agent)
