# ESP32 Motor Controller

This Arduino sketch runs on an ESP32 and controls four DDSM210 Smart Motors over UART.

## Features

- Receives velocity commands from ROS 2 over USB Serial.
- Parses commands in the format:

```
linear_velocity,angular_velocity
```

Example:

```
0.5,0.2
```

- Converts linear and angular velocity into left and right wheel RPM.
- Sends velocity commands to all four DDSM210 smart motors.

## Hardware

- ESP32
- 4 × DDSM210 Smart Motors
- UART communication (GPIO18 RX, GPIO19 TX)

## Motor IDs

| Motor | ID |
|-------|----|
| Left Front | 1 |
| Right Rear | 2 |
| Right Front | 3 |
| Left Rear | 4 |
