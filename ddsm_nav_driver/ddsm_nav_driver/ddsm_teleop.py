#!/usr/bin/env python3

import serial
import rclpy

from rclpy.node import Node
from geometry_msgs.msg import Twist


class CmdVelSerial(Node):

    def __init__(self):
        super().__init__('cmd_vel_serial')

        self.ser = serial.Serial(
            '/dev/ttyACM0',
            115200,
            timeout=0.1)

        self.sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_cb,
            10)

    def cmd_vel_cb(self, msg):
        line = f"{msg.linear.x},{msg.angular.z}\n"
        self.ser.write(line.encode())


def main():
    rclpy.init()

    node = CmdVelSerial()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
