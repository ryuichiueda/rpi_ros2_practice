import launch
import launch.actions
import launch.substitutions
import launch_ros.actions

def generate_launch_description():
    lightsensors = launch_ros.actions.Node(
        package='rpi_ros2_practice',
        executable='lightsensors',
        output='screen',
        )
    motors = launch_ros.actions.Node(
        package='rpi_ros2_practice',
        executable='motors',
        output='screen',
        )
    agent = launch_ros.actions.Node(
        package='rpi_ros2_practice',
        executable='agent',
        output='screen',
        )

    return launch.LaunchDescription([lightsensors, motors, agent])
