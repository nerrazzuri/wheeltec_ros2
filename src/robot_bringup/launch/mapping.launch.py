from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    scan_topic = LaunchConfiguration("scan_topic")
    use_sim_time = LaunchConfiguration("use_sim_time")
    start_lidar = LaunchConfiguration("start_lidar")

    description_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [
                    FindPackageShare("edu_description"),
                    "launch",
                    "description.launch.py",
                ]
            )
        ),
        launch_arguments={"use_sim_time": use_sim_time}.items(),
    )

    lidar_launch = TimerAction(
        period=1.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    PathJoinSubstitution(
                        [
                            FindPackageShare("lslidar_driver"),
                            "launch",
                            "lsm10_net_launch.py",
                        ]
                    )
                ),
                condition=IfCondition(start_lidar),
            )
        ],
    )

    slam_node = TimerAction(
        period=3.0,
        actions=[
            Node(
                package="slam_toolbox",
                executable="async_slam_toolbox_node",
                name="slam_toolbox",
                output="screen",
                parameters=[
                    PathJoinSubstitution(
                        [
                            FindPackageShare("robot_bringup"),
                            "config",
                            "slam_toolbox_mapping.yaml",
                        ]
                    ),
                    {
                        "base_frame": "BASE_LINK",
                        "scan_topic": scan_topic,
                        "use_sim_time": use_sim_time,
                    },
                ],
            )
        ],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "scan_topic",
                default_value="/scan",
                description="LaserScan topic for slam_toolbox. Override only if ros2 topic list confirms a different live M10 topic.",
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
            description_launch,
            lidar_launch,
            slam_node,
        ]
    )
