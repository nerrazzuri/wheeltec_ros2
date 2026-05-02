# robot_bringup

## Module 4 — Mapping

Supervised map generation. Launches robot TF, the M10 LiDAR driver if requested,
and `slam_toolbox` async mapping mode. Does not start Nav2, command robot motion,
or perform obstacle avoidance.

Move the robot slowly under manual or existing platform control while mapping.

```bash
# Default (with LiDAR driver)
ros2 launch robot_bringup mapping.launch.py scan_topic:=/scan

# LiDAR driver already running
ros2 launch robot_bringup mapping.launch.py scan_topic:=/scan start_lidar:=false
```

Use `/x10/scan` only if `ros2 topic list` confirms that the live M10 LaserScan topic
is namespaced:

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

---

## Module 5 — Localization

Localization using `slam_toolbox` localization mode against a previously saved map.
Requires a saved map from Module 4, `/scan` from the M10 LiDAR, `/odom` from the
ROS2 bridge, and the TF `odom -> BASE_LINK` transform.

### Runtime dependencies

| Dependency | Source |
|---|---|
| `/scan` | M10 LiDAR via lslidar_driver |
| `/odom` | autonomous-platform-main ROS2 bridge |
| TF `odom -> BASE_LINK` | autonomous-platform-main ROS2 bridge |
| `maps/facility_map.yaml` + `facility_map.pgm` | Saved from Module 4 |

> **Full localization is not proven until all four dependencies above are live and
> a valid `map_file` is provided.**

### Dry launch (no hardware — verifies launch/config only)

```bash
ros2 launch robot_bringup localization.launch.py start_lidar:=false
```

slam_toolbox will start but wait for `/scan`, `/odom`, the TF chain, and map data.
This is the expected outcome for a dry launch with no running hardware.

### Normal launch (hardware present, map saved)

```bash
ros2 launch robot_bringup localization.launch.py \
  scan_topic:=/scan \
  map_file:=/path/to/facility_map
```

Or using the maps directory inside the installed package:

```bash
ros2 launch robot_bringup localization.launch.py \
  scan_topic:=/scan \
  map_file:=$(ros2 pkg prefix robot_bringup)/share/robot_bringup/maps/facility_map
```

### Optional scan topic override

Use `/x10/scan` **only** if `ros2 topic list` confirms that the live M10 LaserScan
topic is namespaced:

```bash
ros2 launch robot_bringup localization.launch.py scan_topic:=/x10/scan
```

### Full system wrapper

`full_system.launch.py` is a clean wrapper that passes all args through to
`localization.launch.py`. Use it when you want a single entry point:

```bash
ros2 launch robot_bringup full_system.launch.py \
  scan_topic:=/scan \
  start_lidar:=false \
  map_file:=/path/to/facility_map
```
