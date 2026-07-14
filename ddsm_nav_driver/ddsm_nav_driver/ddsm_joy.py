#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist


class JoyToCmdVel(Node):

    def __init__(self):
        super().__init__('joy_to_cmd_vel')

        self.MAX_LINEAR  = 0.6   
        self.MAX_ANGULAR = 1.8   

        self.AXIS_LINEAR  = 2    
        self.AXIS_ANGULAR = 1    

        
        self.DEADZONE = 0.05

        self.create_subscription(
            Joy,
            '/joy',
            self.joy_cb,
            10
        )

        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.get_logger().info("Joystick → cmd_vel node started")

    def joy_cb(self, msg: Joy):
        lin = msg.axes[self.AXIS_LINEAR]
        ang = msg.axes[self.AXIS_ANGULAR]

        lin = 0.0 if abs(lin) < self.DEADZONE else lin
        ang = 0.0 if abs(ang) < self.DEADZONE else ang

        cmd = Twist()
        cmd.linear.x  = lin * self.MAX_LINEAR
        cmd.angular.z = ang * self.MAX_ANGULAR

        self.cmd_pub.publish(cmd)


def main():
    rclpy.init()
    node = JoyToCmdVel()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()