import smbus2
import time
import math

# MPU6500 Registers
WHO_AM_I       = 0x75
PWR_MGMT_1     = 0x6B
SMPLRT_DIV     = 0x19
CONFIG         = 0x1A
GYRO_CONFIG    = 0x1B
ACCEL_CONFIG   = 0x1C
ACCEL_CONFIG2  = 0x1D

ACCEL_XOUT_H   = 0x3B
TEMP_OUT_H     = 0x41
GYRO_XOUT_H    = 0x43


class MPU6500:

    def __init__(self, bus=1, address=0x68):

        self.bus = smbus2.SMBus(bus)
        self.address = address

        self.accel_scale = 16384.0      # ±2g
        self.gyro_scale = 131.0         # ±250 deg/s

        self.initialize()


    def write(self, reg, value):
        self.bus.write_byte_data(self.address, reg, value)


    def read_word(self, reg):

        high = self.bus.read_byte_data(self.address, reg)
        low  = self.bus.read_byte_data(self.address, reg + 1)

        value = (high << 8) | low

        if value >= 0x8000:
            value = -((65535 - value) + 1)

        return value


    def initialize(self):

        who = self.bus.read_byte_data(self.address, WHO_AM_I)

        print(f"WHO_AM_I = 0x{who:02X}")

        # wake sensor
        self.write(PWR_MGMT_1, 0x00)
        time.sleep(0.1)

        # sample rate
        self.write(SMPLRT_DIV, 9)

        # DLPF 41Hz
        self.write(CONFIG, 3)

        # gyro ±250 dps
        self.write(GYRO_CONFIG, 0x00)

        # accel ±2g
        self.write(ACCEL_CONFIG, 0x00)

        # accel DLPF
        self.write(ACCEL_CONFIG2, 0x03)

        time.sleep(0.1)


    def read_accel(self):

        ax = self.read_word(ACCEL_XOUT_H)
        ay = self.read_word(ACCEL_XOUT_H + 2)
        az = self.read_word(ACCEL_XOUT_H + 4)

        g = 9.80665

        return (
            ax/self.accel_scale * g,
            ay/self.accel_scale * g,
            az/self.accel_scale * g
        )


    def read_gyro(self):

        gx = self.read_word(GYRO_XOUT_H)
        gy = self.read_word(GYRO_XOUT_H + 2)
        gz = self.read_word(GYRO_XOUT_H + 4)

        return (
            math.radians(gx/self.gyro_scale),
            math.radians(gy/self.gyro_scale),
            math.radians(gz/self.gyro_scale)
        )


    def read_temperature(self):

        temp = self.read_word(TEMP_OUT_H)

        return temp/333.87 + 21.0


    def read_all(self):

        ax, ay, az = self.read_accel()

        gx, gy, gz = self.read_gyro()

        temp = self.read_temperature()

        return {

            "accel": (ax, ay, az),

            "gyro": (gx, gy, gz),

            "temperature": temp

        }
