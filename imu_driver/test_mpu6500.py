from imu_driver.mpu6500 import MPU6500
import time

imu = MPU6500()

print("Reading MPU6500...\n")

while True:

    data = imu.read_all()

    ax, ay, az = data["accel"]
    gx, gy, gz = data["gyro"]

    print(
        f"ACC "
        f"{ax:6.2f} "
        f"{ay:6.2f} "
        f"{az:6.2f} | "
        f"GYR "
        f"{gx:6.3f} "
        f"{gy:6.3f} "
        f"{gz:6.3f}"
    )

    time.sleep(0.1)
