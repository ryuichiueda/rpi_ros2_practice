# SPDX-FileCopyrightText: 2023 Ryuichi Ueda 　　　　　
# SPDX-License-Identifier: BSD-3-Clause
import rclpy, math
from rclpy.node import Node
from std_msgs.msg import Int16MultiArray

class Agent(Node):
    def __init__(self):
        super().__init__("agent")
        self.ranges = [0, 0, 0, 0]
        self.motors = [0, 0]

        self.sub_lightsensors = self.create_subscription(Int16MultiArray, 'lightsensors', self.callback_lightsensors, 10)
        self.pub_motors = self.create_publisher(Int16MultiArray, "motor_raw", 10)
        self.timer = self.create_timer(0.1, self.callback_motors)


    def callback_lightsensors(self, msg):
        self.ranges = [int(e) for e in msg.data] 


    def callback_motors(self):
        #前向きのセンサーの値を足す
        front_range = self.ranges[0] + self.ranges[3]
        self.get_logger().info("front_range: {}".format(front_range))
        #最終的にfront_rangeをどんな値にしたいかをtargetに設定
        target = 1500
        #目標との差を求める
        delta = target - front_range
        #ゲイン
        k = 0.3
        #差にゲインをかけて入力周波数を決める
        p_freq = delta * k
        cur_freq = self.motors[0]
        #急に周波数を増加すると脱調するので制限
        diff_limit = 20
        if math.fabs(p_freq) > math.fabs(cur_freq) + diff_limit:
            if p_freq < 0:  p_freq -= diff_limit
            else:           p_freq += diff_limit
        
        msg = Int16MultiArray()
        self.motors = [p_freq, p_freq]
        msg.data = [int(p_freq), int(p_freq)]
        self.pub_motors.publish(msg)


def main():
    rclpy.init()
    agent = Agent()
    rclpy.spin(agent)
