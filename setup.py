from setuptools import setup

package_name = 'rpi_ros2_practice'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Ryuichi Ueda',
    maintainer_email='ryuichiueda@gmail.com',
    description='TODO: Package description',
    license='BSD-3Clause',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'lightsensors = rpi_ros2_practice.lightsensors:main',
            'motors = rpi_ros2_practice.motors:main',
        ],
    },
)
