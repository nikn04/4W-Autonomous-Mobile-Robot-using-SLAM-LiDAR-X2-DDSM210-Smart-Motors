from setuptools import find_packages, setup

package_name = 'ddsm_nav_driver'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='robotics',
    maintainer_email='robotics@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
	  'ddsm_base = ddsm_nav_driver.ddsm_base:main',
	  'teleop_node = ddsm_nav_driver.ddsm_teleop:main',
          'odom = ddsm_nav_driver.ddsm_odom:main',
	  'joy_node = ddsm_nav_driver.ddsm_joy:main',
	  'odom_covariance = ddsm_nav_driver.odom_covariance:main',
        ],
    },
)
