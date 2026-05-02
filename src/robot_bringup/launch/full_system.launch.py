from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    scan_topic = LaunchConfiguration("scan_topic")
    use_sim_time = LaunchConfiguration("use_sim_time")
    start_lidar = LaunchConfiguration("start_lidar")
    map_file = LaunchConfiguration("map_file")

    localization_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    FindPackageShare("robot_bringup"),
                    "launch",
                    "localization.launch.py",
                ]
            )
        ),
        launch_arguments={
            "scan_topic": scan_topic,
            "use_sim_time": use_sim_time,
            "start_lidar": start_lidar,
            "map_file": map_file,
        }.items(),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "scan_topic",
                default_value="/scan",
                description="LaserScan topic. Override only if ros2 topic list confirms a different live M10 topic.",
            ),
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="false",
                description="Use simulation clock.",
            ),
            DeclareLaunchArgument(
                "start_lidar",
                default_value="true",
                description="Start the M10 Ethernet LiDAR driver. Set false when the driver is already running.",
            ),
            DeclareLaunchArgument(
                "map_file",
                default_value="",
                description="Path to saved map file (without extension). Required for localization.",
            ),
            localization_launch,
        ]
    )
