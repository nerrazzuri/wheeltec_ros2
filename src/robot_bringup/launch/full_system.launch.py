from launch import LaunchDescription
from launch.actions import LogInfo


def generate_launch_description():
    return LaunchDescription(
        [
            LogInfo(
                msg=(
                    "robot_bringup full_system.launch.py is reserved for a later module. "
                    "Module 4 only provides supervised map generation; it does not start Nav2 or command robot motion."
                )
            )
        ]
    )
