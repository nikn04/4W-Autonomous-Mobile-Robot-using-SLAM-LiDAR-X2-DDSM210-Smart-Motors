import rclpy

from rclpy.node import Node

from sensor_msgs.msg import Imu

from imu_driver.mpu6500 import MPU6500
from imu_driver.calibration import GyroCalibration


class IMUNode(Node):

    def __init__(self):

        super().__init__("imu_node")

        self.declare_parameter("frame_id", "imu_link")
        self.declare_parameter("publish_rate", 100.0)

        self.frame_id = (
            self.get_parameter("frame_id")
            .get_parameter_value()
            .string_value
        )

        self.publish_rate = (
            self.get_parameter("publish_rate")
            .get_parameter_value()
            .double_value
        )

        self.publisher = self.create_publisher(
            Imu,
            "/imu/data",
            10,
        )

        self.imu = MPU6500()

        self.calibration = GyroCalibration(self.imu)

        self.timer = self.create_timer(
            1.0 / self.publish_rate,
            self.timer_callback,
        )

        self.get_logger().info("IMU node started.")

    def timer_callback(self):

        ax, ay, az = self.imu.read_accel()
        gx, gy, gz = self.imu.read_gyro()

        gx, gy, gz = self.calibration.correct(
            gx,
            gy,
            gz,
        )

        #
        # IMPORTANT
        #
        # Your MPU6500 currently reports
        # gravity as NEGATIVE Z.
        #
        # Flip only Z so that ROS uses
        # +Z upward.
        #

        az = -az

        msg = Imu()

        msg.header.stamp = (
            self.get_clock()
            .now()
            .to_msg()
        )

        msg.header.frame_id = self.frame_id

        #
        # Orientation unavailable
        #

        msg.orientation_covariance[0] = -1.0

        #
        # Angular velocity
        #

        msg.angular_velocity.x = gx
        msg.angular_velocity.y = gy
        msg.angular_velocity.z = gz

        #
        # Linear acceleration
        #

        msg.linear_acceleration.x = ax
        msg.linear_acceleration.y = ay
        msg.linear_acceleration.z = az

        #
        # Covariances
        #

        msg.angular_velocity_covariance = [

            0.0004, 0.0, 0.0,
            0.0, 0.0004, 0.0,
            0.0, 0.0, 0.0004

        ]

        msg.linear_acceleration_covariance = [

            0.04, 0.0, 0.0,
            0.0, 0.04, 0.0,
            0.0, 0.0, 0.04

        ]

        self.publisher.publish(msg)


def main():

    rclpy.init()

    node = IMUNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()
