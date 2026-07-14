#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped

from tf_transformations import quaternion_from_euler


class CmdVelOdometry(Node):

    def __init__(self):
        super().__init__('cmd_vel_odometry')

        self.declare_parameter('odom_frame', 'odom')
        self.declare_parameter('base_frame', 'base_link')
        self.declare_parameter('publish_tf', True)
        self.declare_parameter('update_rate', 50.0)

        self.odom_frame = self.get_parameter(
            'odom_frame').value

        self.base_frame = self.get_parameter(
            'base_frame').value

        self.publish_tf = self.get_parameter(
            'publish_tf').value

        rate = self.get_parameter(
            'update_rate').value

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.vx = 0.0
        self.vth = 0.0

        self.last_time = self.get_clock().now()

        self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10)

        self.odom_pub = self.create_publisher(
            Odometry,
            '/odom',
            10)

        self.tf_broadcaster = TransformBroadcaster(self)

        self.timer = self.create_timer(
            1.0 / rate,
            self.update)

        self.get_logger().info(
            'cmd_vel odometry started')

    def cmd_vel_callback(self, msg):
        self.vx = msg.linear.x
        self.vth = msg.angular.z

    def update(self):
        now = self.get_clock().now()

        dt = (
            now - self.last_time
        ).nanoseconds / 1e9

        self.last_time = now
	
        if dt<= 0.0 or dt>0.5:
            return

        delta_x = (
            self.vx *
            math.cos(self.theta) *
            dt
        )

        delta_y = (
            self.vx *
            math.sin(self.theta) *
            dt
        )

        delta_theta = self.vth * dt

        self.x += delta_x
        self.y += delta_y
        self.theta += delta_theta

        q = quaternion_from_euler(
            0.0,
            0.0,
            self.theta
        )

        odom = Odometry()

        odom.header.stamp = now.to_msg()
        odom.header.frame_id = self.odom_frame

        odom.child_frame_id = self.base_frame

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0

        odom.pose.pose.orientation.x = q[0]
        odom.pose.pose.orientation.y = q[1]
        odom.pose.pose.orientation.z = q[2]
        odom.pose.pose.orientation.w = q[3]

        odom.twist.twist.linear.x = self.vx
        odom.twist.twist.angular.z = self.vth

        self.odom_pub.publish(odom)

        if self.publish_tf:

            t = TransformStamped()

            t.header.stamp = now.to_msg()
            t.header.frame_id = self.odom_frame
            t.child_frame_id = self.base_frame

            t.transform.translation.x = self.x
            t.transform.translation.y = self.y
            t.transform.translation.z = 0.0

            t.transform.rotation.x = q[0]
            t.transform.rotation.y = q[1]
            t.transform.rotation.z = q[2]
            t.transform.rotation.w = q[3]

            self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)

    node = CmdVelOdometry()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

