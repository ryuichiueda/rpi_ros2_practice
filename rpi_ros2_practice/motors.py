# SPDX-FileCopyrightText: 2023 Ryuichi Ueda 　　　　　
# SPDX-License-Identifier: BSD-3-Clause
import rclpy, math
from rclpy.node import Node
from std_msgs.msg import Int16MultiArray

class Motors(Node):
    def __init__(self):
        super().__init__("motors")
        self.sub_freqs = self.create_subscription(Int16MultiArray, 'motor_raw', self.callback_motor_raw, 10)


    def callback_motor_raw(self, msg):
        #self.node.get_logger().info("send {}".format(msg))
        lfile = '/dev/rtmotor_raw_l0'
        rfile = '/dev/rtmotor_raw_r0'
        
        try:
            lf = open(lfile,'w')
            rf = open(rfile,'w')
            #self.node.get_logger().info("send {}".format(msg.data[0]))
            lf.write("%s\n" % msg.data[0])
            rf.write("%s\n" % msg.data[1])
            lf.flush()
            rf.flush()
        except:
            self.get_logger().info("cannot write to rtmotor_raw_*")
    
        lf.close()
        rf.close()


def main():
    rclpy.init()
    motors = Motors()
    rclpy.spin(motors)
