#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry


class OdomCovarianceNode(Node):

    def __init__(self):
        super().__init__("odom_covariance")

        self.subscription = self.create_subscription(
            Odometry,
            "/odom",
            self.odom_callback,
            10
        )

        self.publisher = self.create_publisher(
            Odometry,
            "/odom_rf2o",
            10
        )

        self.get_logger().info("Odom covariance node started.")

    def odom_callback(self, msg: Odometry):

        # -------------------------
        # Pose covariance
        # -------------------------
        pose_cov = [0.0] * 36

        # x
        pose_cov[0] = 0.05

        # y
        pose_cov[7] = 0.05

        # z (unused)
        pose_cov[14] = 1e6

        # roll (unused)
        pose_cov[21] = 1e6

        # pitch (unused)
        pose_cov[28] = 1e6

        # yaw
        pose_cov[35] = 0.02

        msg.pose.covariance = pose_cov

        # -------------------------
        # Twist covariance
        # -------------------------
        twist_cov = [0.0] * 36

        # vx
        twist_cov[0] = 0.02

        # vy (robot can't move sideways)
        twist_cov[7] = 1e6

        # vz
        twist_cov[14] = 1e6

        # roll rate
        twist_cov[21] = 1e6

        # pitch rate
        twist_cov[28] = 1e6

        # yaw rate
        twist_cov[35] = 0.01

        msg.twist.covariance = twist_cov

        self.publisher.publish(msg)


def main(args=None):

    rclpy.init(args=args)

    node = OdomCovarianceNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
