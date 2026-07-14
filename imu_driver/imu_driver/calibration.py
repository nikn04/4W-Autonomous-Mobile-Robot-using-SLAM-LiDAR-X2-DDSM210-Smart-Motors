import time
import numpy as np


class GyroCalibration:
    def __init__(self, imu, samples=500):

        print("===================================")
        print("Calibrating IMU...")
        print("Keep the robot completely still.")
        print("===================================")

        gx = []
        gy = []
        gz = []

        for _ in range(samples):
            x, y, z = imu.read_gyro()

            gx.append(x)
            gy.append(y)
            gz.append(z)

            time.sleep(0.002)

        self.bias_x = np.mean(gx)
        self.bias_y = np.mean(gy)
        self.bias_z = np.mean(gz)

        print("Gyro calibration complete.")
        print(f"Bias X = {self.bias_x:.6f}")
        print(f"Bias Y = {self.bias_y:.6f}")
        print(f"Bias Z = {self.bias_z:.6f}")

    def correct(self, gx, gy, gz):

        return (
            gx - self.bias_x,
            gy - self.bias_y,
            gz - self.bias_z,
        )
