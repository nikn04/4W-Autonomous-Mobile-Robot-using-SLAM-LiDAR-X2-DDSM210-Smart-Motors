#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial
import json
import math

class DDSMBaseNode(Node):
    def __init__(self):
        super().__init__('ddsm_base_node')
        
        # 1. Setup Subscriber
        self.subscription = self.create_subscription(
            Twist, 
            '/cmd_vel', 
            self.cmd_vel_callback, 
            10
        )
        self.get_logger().info("ROS 2 Subscriber initialized on /cmd_vel")
        
        # 2. Open Hardware Serial Connection (115200 baud for ESP32)
        try:
            self.ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=0.1)
            self.get_logger().info("Successfully connected to serial interface: /dev/ttyAMA0")
        except Exception as e:
            self.get_logger().error(f"Failed to open serial port: {e}")
            
        # 3. Robot Physical Parameters
        self.wheel_radius = 0.0350    # DDSM210 wheel radius (~3.5cm)
        self.wheel_separation = 0.195 # 19.5 cm track width
        
        # 4. Motor ID Mappings (IDs: Left = 1,4 | Right = 2,3)
        self.left_ids = [1, 4]
        self.right_ids = [2, 3]

    def send_json_cmd(self, motor_id, target_01rpm):
        """Formats and transmits the target speed to the DDSM Driver."""
        # T: 10010 speed tracking mode, act: 3 acceleration smoothing
        data = {"T": 10010, "id": motor_id, "cmd": int(target_01rpm), "act": 3}
        payload = json.dumps(data) + "\n"
        try:
            self.ser.write(payload.encode('utf-8'))
        except Exception as e:
            self.get_logger().warn(f"Serial transmission failed for motor {motor_id}: {e}")

    def cmd_vel_callback(self, msg):
        self.get_logger().info(f"Incoming Command -> Linear X: {msg.linear.x}, Angular Z: {msg.angular.z}")
        
        linear_x = msg.linear.x
        angular_z = msg.angular.z
        
        # Differential Drive Kinematics
        v_left = linear_x - (angular_z * self.wheel_separation / 2.0)
        v_right = linear_x + (angular_z * self.wheel_separation / 2.0)
        
        # Convert Linear Speed (m/s) to RPM
        left_rpm = (v_left / self.wheel_radius) * 60.0 / (2.0 * math.pi)
        right_rpm = (v_right / self.wheel_radius) * 60.0 / (2.0 * math.pi)
        
        # Scale to protocol firmware values (1 unit = 0.1 RPM)
        left_cmd = left_rpm * 10.0
        right_cmd = -right_rpm * 10.0  # Inverted due to physical axial mirroring
        
        # Protect bounds
        left_cmd = max(min(left_cmd, 32767), -32767)
        right_cmd = max(min(right_cmd, 32767), -32767)
        
        # Transmit to motor groups
        for i in self.left_ids:
            self.send_json_cmd(i, left_cmd)
        for j in self.right_ids:
            self.send_json_cmd(j, right_cmd)

def main(args=None):
    rclpy.init(args=args)
    node = DDSMBaseNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Emergency stop all motors on shutdown
        for motor in [1, 2, 3, 4]:
            node.send_json_cmd(motor, 0)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
