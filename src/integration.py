"""Integration page: what sensor fusion means for this vehicle, the framework choice, and where CSTI connects."""

SRC = {
    "aurelion": ("dSPACE: AURELION sensor simulation", "https://www.dspace.com/en/pub/home/products/sw/experimentandvisualization/aurelion_sensor-realistic_sim.cfm"),
    "hil": ("dSPACE: HIL for autonomous driving", "https://www.dspace.com/en/inc/home/products/systems/ecutest/hil_for_autonomous_driving.cfm"),
    "rosblock": ("dSPACE: Interface Blockset for ROS", "https://www.dspace.com/en/pub/home/products/sw/impsw/dspace_interface_blockset_ros.cfm"),
    "integrate": ("dSPACE: Integrating a virtual driving simulator (webinar)", "https://www.dspace.com/en/pub/home/learning-center/recordings/learningconnections/virtual-driving-sim-integratio.cfm"),
    "rr_ros": ("MathWorks: Publish data from RoadRunner Scenario to a ROS 2 network", "https://www.mathworks.com/help/ros/ug/publish-data-from-roadrunner-scenario-to-ros2-network-and-visualize-data-using-ros-data-analyzer-app.html"),
    "rr_cam": ("MathWorks: Generate RoadRunner scene using labeled camera images and raw lidar data", "https://www.mathworks.com/help/driving/ug/generate-road-scene-with-lanes-from-labeled-recorded-data.html"),
    "rr_lidar": ("MathWorks: Generate RoadRunner scene with trees and buildings using recorded lidar data", "https://www.mathworks.com/help/driving/ug/generate-scene-with-trees-buildings-using-lidar-data.html"),
    "rr_scene": ("MathWorks: RoadRunner exportScene", "https://www.mathworks.com/help/driving/ref/roadrunner.exportscene.html"),
    "rr_scen": ("MathWorks: RoadRunner exportScenario", "https://www.mathworks.com/help/driving/ref/roadrunner.exportscenario.html"),
    "dspace_ros": ("dSPACE vendor article on RTMaps and ROS 2", "https://www.dspace.com/en/pub/home/news/engineers-insights/ros-projects-with-rtmaps.cfm"),
    "rtmaps": ("dSPACE RTMaps product page", "https://www.dspace.com/en/pub/home/products/sw/impsw/rtmaps.cfm"),
    "arxiv": ("Performance evaluation of a ROS2 based Automated Driving System (arXiv)", "https://arxiv.org/html/2411.11607v2"),
    "zerocopy": ("ROS 2 design article: Zero Copy via Loaned Messages", "https://design.ros2.org/articles/zero_copy.html"),
}


def cite(k, text=None):
    t, u = SRC[k]
    return f'<a href="{u}">{text or t}</a>'


def body(fig, table):
    b = []

    b.append('<h2 id="definition">1. What sensor fusion means here</h2>')
    b.append("<p><strong>Sensor fusion</strong> turns every sensor's reports into one tracked list of objects around the vehicle, each with position, velocity, size, class and confidence. This vehicle uses <strong>object-level fusion</strong>: each sensor's data is first reduced to a list of objects, then the lists are combined. RTMaps prepares the data; ROS 2 fuses the objects.</p>")
    b.append(fig("pipeline", "Figure 7. RTMaps time-synchronizes and preprocesses each sensor; ROS 2 fuses the object lists. In ViL, CSTI's virtual object lists arrive on the same fusion inputs."))
    b.append(table(["Step", "Where", "What it does"], [
        ["Time synchronization", "RTMaps", "Puts every measurement on one time base."],
        ["Camera preprocessing and detection", "RTMaps (detector location to confirm)", "Turns images into an object list."],
        ["LiDAR sync and downsampling", "RTMaps", "Reduces point clouds before clustering into objects (clustering location to confirm)."],
        ["Transform to vehicle frame", "ROS 2", "Puts every detection in the vehicle's coordinates."],
        ["Association", "ROS 2", "Matches detections to each other and to existing tracks."],
        ["Tracking filter", "ROS 2", "Updates each object's position and velocity estimate."],
        ["Track management", "ROS 2", "Creates, confirms, deletes and prioritizes tracks for planning."],
    ]))

    b.append('<h2 id="sensors">2. Sensors and what fusion receives</h2>')
    b.append(table(["Sensor", "Native output", "Fusion receives", "What CSTI injects"], [
        ["Radars", "Object lists over CAN", "Object list", "Object lists in every stage"],
        ["Camera", "Raw images", "Object list", "Raw images on the bench; object lists on the vehicle"],
        ["LiDAR", "Point cloud", "Object list", "Raw point clouds on the bench; object lists on the vehicle"],
        ["V2X unit", "Messages from road users and infrastructure", "Object list", "Messages in every stage"],
    ]))

    b.append('<h2 id="datapath">3. Where CSTI connects</h2>')
    b.append(fig("datapath", "Figure 8. Two ways CSTI's virtual data could reach fusion in ViL: through a merge node in the real-data path (rejected), or as a second publisher on fusion's existing input topic (chosen)."))
    b.append("<p><strong>In the data path</strong> (rejected): real sensor data passes through a CSTI node that merges in virtual objects. If CSTI fails, real detections are lost too.</p>")
    b.append("<p><strong>Same topic, separate publisher</strong> (chosen): the real path is untouched. The CSTI gateway publishes virtual object lists on fusion's existing input topics, marked with a virtual source id and copied to <code>/virtual/</code> for logs. If CSTI fails, only the virtual objects stop, and fusion runs unchanged in every stage (D-07, FR-10, SR-01).</p>")
    b.append("<div class='note'><p><strong>What this asks of the stack:</strong> fusion must accept real and virtual object lists on the same topic. CSTI's virtual object lists go through RTMaps like any other input, unless CSTI already timestamps them on RTMaps' time base; only then may they enter at fusion's inputs. Either way, the RTMaps pipeline itself is validated twice: first in perception PiL with AURELION's simulated sensor data, then in HIL with the sensor cart's real data.</p></div>")

    b.append('<h2 id="simchain">4. Simulation chain</h2>')
    b.append("<p>The team's simulation loop joins RoadRunner, a MathWorks vehicle dynamics model in Simulink, and AURELION on the desktop (VEOS). It serves perception MiL and PiL; HIL uses the sensor cart's real sensors instead.</p>")
    b.append(table(["Step", "Tool", "What happens"], [
        ["Build scene and scenario", "RoadRunner", "Exports the road as glTF for AURELION and OpenDRIVE, and the scenario as OpenSCENARIO (" + cite("rr_scene", "scene export") + ", " + cite("rr_scen", "scenario export") + ")."],
        ["Drive the vehicle", "Simulink", "The controllers and vehicle dynamics model compute the ego pose each step."],
        ["Run the co-simulation", "AURELION Setup block", "Sends ego and fellow-vehicle poses to AURELION and keeps both sides in step at the update rate (20 ms in the team's setup)."],
        ["Render sensors", "AURELION", "Camera, radar, LiDAR and ultrasonic data; radar can also output detections or object lists (" + cite("aurelion", "AURELION") + ")."],
        ["Return sensor data", "V-ESI blocks or RTMaps", "V-ESI blocks bring data into Simulink for controls tests; RTMaps brings it to the ROS 2 stack on the AUTERA for perception PiL."],
    ]))
    b.append("<p><strong>MiL, controls:</strong> the Simulink controllers run against RoadRunner Scenario, taking its objects straight as ground truth, unprocessed. Scenes can be rebuilt from the team's drive data (" + cite("rr_cam", "camera example") + ", " + cite("rr_lidar", "LiDAR example") + "), and RoadRunner Scenario can generate scenarios from recordings, generate variations and automate test runs.</p>")
    b.append("<p><strong>MiL, perception:</strong> sensor placement and specs are checked in RoadRunner. AURELION co-simulates the same scenario on the desktop to produce realistic sensor data and to add sensor faults. This is still MiL.</p>")
    b.append("<p><strong>PiL, controls:</strong> each Simulink controller is code-generated separately into a C++ ROS 2 node on the AUTERA, fed RoadRunner ground truth such as ego odometry and actor positions over ROS 2 (" + cite("rr_ros", "MathWorks example") + ").</p>")
    b.append("<p><strong>PiL, perception:</strong> RTMaps and the C++ object fusion run on the AUTERA, fed AURELION's simulated sensor data from the desktop through RTMaps (" + cite("integrate", "dSPACE integration examples") + "). How AURELION's output reaches the AUTERA is to confirm.</p>")
    b.append("<p><strong>HIL, the sensor cart:</strong> real sensors on a cart feed RTMaps and the full stack on the AUTERA, with the safety interlock active. The stack commands steering, braking and acceleration over automotive Ethernet, as on the car, and the Simulink vehicle model on the HIL bench receives those commands, so the real vehicle interface is tested too. CSTI adds virtual objects through its gateway.</p>")
    b.append("<div class='note'><p><strong>To check:</strong> the V-ESI update rate sets the simulated sensor rate; it should match each real sensor's rate so perception PiL sees the same timing as the car.</p></div>")
    b.append('<h2 id="sources">Sources</h2><ul>' + "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in SRC.values() if t.startswith(("dSPACE:", "MathWorks:"))) + "</ul>")
    return "\n".join(b)
