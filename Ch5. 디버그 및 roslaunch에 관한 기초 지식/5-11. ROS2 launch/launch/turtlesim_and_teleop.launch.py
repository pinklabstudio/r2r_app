from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package='turtlesim', executable='turtlesim_node',
                namespace='turtlesim', output='screen'
            ),

            Node(
                package='my_first_package', executable='my_publisher',
                namespace='pub_cmd_vel', output='screen'
            )
        ]
    )