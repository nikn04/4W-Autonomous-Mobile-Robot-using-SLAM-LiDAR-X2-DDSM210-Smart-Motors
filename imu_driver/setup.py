from setuptools import find_packages, setup

package_name = 'imu_driver'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),
        (
            'share/' + package_name,
            ['package.xml'],
        ),
    ],
    install_requires=[
        'setuptools',
        'numpy',
        'smbus2',
    ],
    zip_safe=True,
    maintainer='robotics',
    maintainer_email='robotics@example.com',
    description='ROS2 MPU6500 IMU Driver',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'imu_node = imu_driver.imu_node:main',
        ],
    },
)
