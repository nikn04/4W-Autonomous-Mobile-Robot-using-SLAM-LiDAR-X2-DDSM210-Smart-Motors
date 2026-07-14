# 4W Autonomous Mobile Robot using SLAM, YDLIDAR X2 and DDSM210 Smart Motors

## Overview

This project implements a four-wheel differential drive autonomous mobile robot using ROS 2 Jazzy.

The robot is built around a Raspberry Pi and ESP32. The ESP32 communicates with four DDSM210 smart motors over UART while the Raspberry Pi performs localization, SLAM, and navigation using ROS 2.

The robot is capable of:

- Differential drive control
- Joystick and `/cmd_vel` teleoperation
- Wheel odometry
- IMU integration
- Online SLAM
- Autonomous navigation

---

## Hardware

- Raspberry Pi
- ESP32
- 4 × DDSM210 Smart Motors
- YDLIDAR X2
- MPU6500 IMU
- 4-wheel differential drive chassis

---

## Software Stack

- Ubuntu
- ROS 2 Jazzy
- SLAM Toolbox
- robot_localization
- RViz2

---

## Repository Structure

```
src/
├── ddsm_nav_driver/
├── imu_driver/
├── turtlebot_localization/
```

---

## External Packages

The following ROS 2 packages are **not included** in this repository.

Clone them into your workspace:

```bash
cd ~/turtlebot_ws/src

git clone https://github.com/MAPIRlab/rf2o_laser_odometry.git

git clone https://github.com/YDLIDAR/ydlidar_ros2_driver.git
```

---

## Build

```bash
cd ~/turtlebot_ws

colcon build

source install/setup.bash
```

---

## Running

Start the motor driver

```bash
ros2 run ddsm_nav_driver ddsm_base
```

Start IMU

```bash
ros2 run imu_driver imu_node
```

Start LiDAR

```bash
ros2 launch ydlidar_ros2_driver ydlidar_launch.py
```

Start localization

```bash
ros2 launch turtlebot_localization ekf.launch.py
```

---

## Mapping

Launch SLAM Toolbox

```bash
ros2 launch slam_toolbox online_async_launch.py
```

---

## Features

- UART communication with DDSM210 motors
- ROS2 Differential Drive
- Wheel Odometry
- IMU Driver
- EKF Sensor Fusion
- SLAM Toolbox Integration
- LiDAR Mapping

---

## Future Work

- Nav2 Integration
- Autonomous waypoint navigation
- Camera-based obstacle detection
- Docking station
- Battery monitoring

---

## License

MIT License
