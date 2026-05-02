from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    scan_topic = LaunchConfiguration("scan_topic")
    use_sim_time = LaunchConfiguration("use_sim_time")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "scan_topic",
                default_value="/scan",
                description="LaserScan topic for future localization. Override only if ros2 topic list confirms a different live M10 topic.",
            ),
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="false",
                description="Use simulation clock.",
            ),
            LogInfo(
                msg=(
                    "robot_bringup localization.launch.py is a Module 5 placeholder. "
                    "It loads a baseline slam_toolbox localization config, but localization is not validated in Module 4."
                )
            ),
            Node(
                package="slam_toolbox",
                executable="localization_slam_toolbox_node",
                name="slam_toolbox",
                output="screen",
                parameters=[
                    PathJoinSubstitution(
                        [
                            FindPackageShare("robot_bringup"),
                            "config",
                            "slam_toolbox_localization.yaml",
                        ]
                    ),
                    {
                        "base_frame": "BASE_LINK",
                        "scan_topic": scan_topic,
                        "use_sim_time": use_sim_time,
                    },
                ],
            ),
        ]
    )
