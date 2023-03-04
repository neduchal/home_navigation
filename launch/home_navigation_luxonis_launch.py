import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch import launch_description_sources
from launch.actions import IncludeLaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution, TextSubstitution 



def generate_launch_description():

    luxonis_launch_dir = os.path.join(
        get_package_share_directory('depthai_examples'), 'launch')

    luxonis_launch = IncludeLaunchDescription(
        launch_description_sources.PythonLaunchDescriptionSource(
            os.path.join(luxonis_launch_dir, 'stereo_inertial_node.launch.py')),
        launch_arguments={'enableRviz':'0'}.items()
    )

    tf2_node = Node(package = "tf2_ros", 
                       executable = "static_transform_publisher",
                       arguments = ["0", "0", "0", "0", "0", "0", "oak-d_frame", "camera_depth_frame"])

    scan_height_arg = DeclareLaunchArgument(
        'scan_height', default_value=TextSubstitution(text='100')
    )
    range_max_arg = DeclareLaunchArgument(
        'range_max', default_value=TextSubstitution(text='3')
    )    

    return LaunchDescription([
        luxonis_launch,
        scan_height_arg,
        range_max_arg,
        tf2_node,
        Node(
            package='depthimage_to_laserscan',
            namespace='home_navigation',
            executable='depthimage_to_laserscan_node',
            name='sim',
            remappings=[
                ('/home_navigation/depth', '/stereo/depth'),
                ('/home_navigation/depth_camera_info', '/stereo/camera_info'),
            ],
            parameters=[
                {'scan_height': 50},
                {'range_max': 5.0}
            ]
        )
    ])
