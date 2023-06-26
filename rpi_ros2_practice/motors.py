# SPDX-FileCopyrightText: 2023 Ryuichi Ueda 　　　　　
# SPDX-License-Identifier: BSD-3-Clause
import rclpy, math
from rclpy.node import Node
from rpi_ros2_practice_msgs.msg import MotorFreqs
from rpi_ros2_practice_msgs.srv import SwitchMotors

class Motors(Node):
    def __init__(self):
        super().__init__("motors")
        self.sub_freqs = self.create_subscription(MotorFreqs, 'motor_raw', self.callback_motor_raw, 10)
        self.srv_motor_power = self.create_service(SwitchMotors, 'switch_motors', self.callback_motor_sw)


    def callback_motor_sw(self, request, response):
        enfile = '/dev/rtmotoren0'
        try:
            with open(enfile,'w') as f:
                if request.command == "on":    f.write("1\n")
                elif request.command == "off": f.write("0\n")
                else: 
                    self.get_logger().info("invalid request")
                    response.result = "NG"
                    return response    

            response.result = "OK"
        except:
            self.get_logger().info("cannot write to " + enfile)
            response.result = "NG"

        return response    


    def callback_motor_raw(self, msg):
        lfile = '/dev/rtmotor_raw_l0'
        rfile = '/dev/rtmotor_raw_r0'
        
        try:
            lf = open(lfile,'w')
            rf = open(rfile,'w')
            lf.write("%s\n" % msg.left)
            rf.write("%s\n" % msg.right)
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
