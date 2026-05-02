# robot_bringup

Module 4 provides supervised map generation only. It launches robot TF,
the M10 LiDAR driver if requested, and `slam_toolbox` mapping mode.
It does not start Nav2, command robot motion, or perform obstacle avoidance.

Move the robot slowly under manual or existing platform control while mapping.

Default scan topic is `/scan`, matching `lslidar_m10_net.yaml`.

```bash
ros2 launch robot_bringup mapping.launch.py scan_topic:=/scan
```

Use `/x10/scan` only if `ros2 topic list` confirms that the live M10
LaserScan topic is namespaced:

```bash
ros2 launch robot_bringup mapping.launch.py scan_topic:=/x10/scan
```

After mapping, save the map:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/facility_map
```

Then copy the saved files into this package:

```bash
cp ~/facility_map.yaml src/robot_bringup/maps/
cp ~/facility_map.pgm src/robot_bringup/maps/
```
