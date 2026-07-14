from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'turtlebot_localization'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),
        (
            'share/' + package_name,
            ['package.xml']
        ),

        # Install launch files
        (
            os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')
        ),

        # Install config files
        (
            os.path.join('share', package_name, 'config'),
            glob('config/*.yaml')
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='robotics',
    maintainer_email='robotics@todo.todo',
    description='Localization package for TurtleBot',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
