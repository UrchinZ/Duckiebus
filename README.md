#Duckiebus
#- repo originally from Algorithmic Robotics #

ALWAYS git pull first!

terminal command to push local workspace to the repository:
git add src/ README.md 
git commit -m "commit message

git will say the following is untracked. Ignore.
build/
devel/

then: git push

Common code for class. Currently many of the packages are from the duckietown/Software github repository or built off of said packages.

To view image_compressed, run rqt_image_view
to view image with markers, run
 rosparam set /pi/line_detector_node/verbose true
To view relationship between nodes: run rqt_graph

### Contents ###
* ar_tags/
    * src/**tag_detector_node.py** - publishes AR tag detections (IDs, relative positions)
* dagu_car/
    * launch/**dagu_car.launch** - starts the dagu_car nodes and remaps topics
    * script/**drive_straight_test.py** - run this to test the wheel calibration
    * src/**kinematics_node.py** - converts car velocities to wheel speeds
    * src/**wheels_driver_node.py** - sets wheel speeds based on received commands
* duckiebus/
    * config/**duckiestop.yaml** - duckie stop information
    * src/**bus.py** - drives car in a fiexed routine defined in duckiestop.yaml
* duckietown/
    * config/dagu_car/kinematics/**pi.yaml** - wheel calibration
    * config/ground_projection/**pi.yaml** - extrinsic camera calibration
    * config/pi_camera/**pi.yaml** - intrinsic camera calibration
    * launch/ - launch files that start nodes across multiple packages
* duckietown_msgs/
    * msg/ - message definitions used across duckietown
* ground_projection/
    * scripts/**test_projection_auto.py** - run this to test extrinsic camera calibration
* intersection_control/
    * config/**maneuvers.yaml** - open-loop turn descriptions
    * 
    * src/**stop_line_filter.py** - publishes stop-line readings
    * src/**supervisor_node.py** - manages intersections (and control mode switching)
* keyboard_control/
    * src/**keyboard_control_node.py** - publishes car velocities based on key presses
* lane_control/
    * src/**lane_controller_node.py** - publishes car velocities based on lane pose estimates
* lane_filter/
    * src/**lane_filter_node.py** - publishes lane pose estimates
* line_detector/
    * config/**params.yaml** - parameters used for color and edge detection
    * src/**line_detector_node.py** - publishes line sesgment information
* localization/
    * config/**landmarks.yaml** - AR tag IDs and locations
    * src/**localization_node.py** - estimates car pose based on AR tags and odometry (lab 10)
* pi_camera/
    * launch/**camera.launch** - starts the camera nodes and remaps topics
    * src/**cam_info_node.py** - publishes camera calibration info each time an image is received
    * src/**camera_node.py** - publishes compressed camera images
* uber/
    * config/**town.yaml** - Linked list with intersection as nodes. Record of directions and road segment length.
    * src/**graph.py** - graph class that proceses town information and provide dijkstra shortest path computation.
    * src/**uber.py** - drives car from start position to end goal.

### Environment ###
* Raspberry Pi 3, Ubuntu Mate 14.04, Python 2.7.12, OpenCV 2.4.9, ROS Kinetic

### Future work ###
* Link ar_tags node to duckiebus so duckiebus stops at tag location
* Design better scheme for turning
* Redesign lane_controller
* Design color calibration procedure to for proper line_detector params under various lighting.

Team 22: Connor McGowan, Judy Zhang
