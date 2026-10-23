from svgkit import D


# ---------------------------------------------------------------- context
def context():
    d = D("ctx", 1000, 720, "Context diagram",
          "CSTI with its three users and the simulation tools; the autonomy stack chain with its fault detection node "
          "and safety interlock on the right; the vehicle platform below. CSTI injects at fusion and only listens to "
          "the stack's status; it never commands the vehicle.")
    d.actor(70, 170, ["Test engineer"])
    d.actor(70, 330, ["Autonomy developer"])
    d.actor(70, 490, ["Safety driver / operator"])
    d.node(290, 200, 260, 160, None, "CSTI\nCross-Stage Test\nInfrastructure", "system", "sys")
    d.node(290, 40, 260, 60, None, "Simulation tools", "external", "ext")
    d.rect(650, 20, 330, 410, "ext", 6)
    d.text(815, 40, "«external system»", "st")
    d.text(815, 56, "Autonomy stack under test", "id")
    chain = ["Perception + fusion", "Planning", "Feature state machines\n(ACC, LCC, AIN)", "Safety interlock manager",
             "Vehicle interface"]
    for k, n in enumerate(chain):
        y = 70 + k * 66
        d.node(665, y, 190, 48, None, n, None)
        if k:
            d.path([(760, y - 18), (760, y)])
    d.node(870, 196, 100, 60, None, "Fault\ndetection", None)
    d.path([(870, 226), (855, 226)])
    d.rect(240, 500, 740, 200, "ext", 6)
    d.text(252, 690, "«external» Vehicle platform", "st", "start")
    parts = [("Data logger", ""), ("Driver override", "brake, steering,\naccelerator"), ("E-stop +\nmode switch", "hardware"),
             ("Dashboard", "driver alerts"), ("Actuation\ngateway ECU", "can disable\nautomation"),
             ("Sensors", "camera, radar,\nLiDAR, GNSS,\nIMU, V2X")]
    for k, (n, e) in enumerate(parts):
        d.node(250 + k * 122, 535, 115, 85, None, n, None, "box", e or None)
    # users
    d.path([(115, 200), (290, 230)], arrow="both")
    d.path([(115, 355), (290, 280)], arrow="both")
    d.path([(115, 515), (290, 330)], arrow="both")
    # tools, stack, vehicle
    d.path([(420, 100), (420, 200)], arrow="both")
    d.path([(550, 230), (610, 230), (610, 94), (665, 94)])
    d.path([(665, 292), (550, 292)])
    d.path([(700, 382), (700, 470), (673, 470), (673, 535)])
    d.path([(820, 382), (820, 470), (795, 470), (795, 535)])
    d.path([(429, 620), (429, 660), (795, 660), (795, 620)], "ln thin")
    d.path([(551, 620), (551, 660)], "ln thin", arrow=None)
    d.path([(917, 535), (917, 480), (990, 480), (990, 94), (855, 94)], "ln dash")
    d.path([(420, 500), (420, 360)])
    return d


# ---------------------------------------------------------------- component
def component():
    d = D("cmp", 1200, 560, "Component diagram",
          "CSTI's goals as blocks. Main flow left to right: define and check the test, run it, simulate the world, "
          "make sensor data, deliver it to the autonomy stack. Underneath: recording and judging, and vehicle placement and time.")
    d.node(400, 10, 170, 50, None, "Simulation tools", "external", "ext")
    row = [(20, "Define and check\nthe test", "scenario authoring;\nschema + ODD checks", "box"),
           (210, "Run the test", "stage profile, start/stop,\ncampaigns", "box"),
           (400, "Simulate the world", "simulators, actors,\ntriggers", "box"),
           (590, "Make sensor data", "sensor models,\nfault injection", "box"),
           (780, "Deliver to the stack", "gateway on fusion's\ninput topics;\nfrozen contract", "frozen")]
    for x, n, e, c in row:
        d.node(x, 110, 170, 110, None, n, None, c, e)
    for x in (190, 380, 570, 760, 950):
        d.path([(x, 165), (x + 20, 165)])
    d.node(970, 110, 210, 220, None, "Autonomy stack", "external", "ext",
           "ingest + time sync\nobject fusion\nplanning\nstate machines + fault detection\nsafety interlock\nvehicle interface")
    d.path([(485, 60), (485, 110)], arrow="both")
    band = [(20, "Record and judge", "recording + replay;\nscoring vs ground truth", "box"),
            (210, "Place the vehicle\nand keep time", "ego state, clock", "box")]
    for x, n, e, c in band:
        d.node(x, 380, 170, 100, None, n, None, c, e)
    d.node(970, 380, 210, 100, None, "Vehicle platform", "external", "ext", "sensors, actuation gateway,\noverride, E-stop")
    d.path([(295, 380), (295, 300), (450, 300), (450, 220)])
    d.path([(1075, 330), (1075, 380)])
    d.path([(1075, 480), (1075, 525), (295, 525), (295, 480)])
    d.lines(105, 500, ["taps every flow above"], "st")
    return d


# ---------------------------------------------------------------- deployment
def deployment():
    d = D("dep", 1200, 720, "Deployment diagram",
          "Desktop workstation (MiL and PiL: Simulink, RoadRunner, AURELION), target computer with the ROS 2 stack including "
          "fault detection and the safety interlock (PiL, HIL, ViL), in-vehicle test computer (ViL), the sensor cart "
          "(HIL) and the HIL bench with the Simulink vehicle model; plus the vehicle platform.")
    d.node3d(20, 50, 260, 300, "Desktop workstation (MiL, PiL)")
    d.node(36, 98, 228, 46, None, "Simulink controllers", None, "ext", "no safety interlock")
    d.node(36, 152, 228, 46, None, "RoadRunner, AURELION", None, "ext", "scenarios; sensor data, faults")
    d.node(36, 206, 228, 36, None, "Define, run, judge, replay", None)
    d.node(36, 250, 228, 50, None, "Simulate world, sensor data,\nvehicle placement, time", None)
    d.node(36, 308, 228, 30, None, "Gateway", None, "frozen")

    d.node3d(330, 50, 280, 300, "Target computer: AUTERA AutoBox")
    d.node(346, 98, 248, 96, None, "fusion → planning → state machines\n→ safety interlock → vehicle interface",
           "ROS 2 container: autonomy stack", "ext", "fault detection node")
    d.node(346, 202, 248, 34, None, "Gateway (ROS 2 node)", None, "frozen")
    d.node(346, 244, 248, 60, None, "Ingest middleware", None, "ext", "time sync, camera preprocessing,\nLiDAR sync + downsample")
    d.lines(470, 326, ["safety interlock active in HIL and ViL"], "st")

    d.node3d(720, 50, 270, 300, "In-vehicle test computer (ViL)")
    d.node(736, 98, 238, 40, None, "Test orchestrator (ViL profile)", None)
    d.node(736, 146, 238, 50, None, "Headless player, actors, sensor\nmodels, faults, ego state, clock", None)
    d.node(736, 204, 238, 40, None, "Operator view: stack status, stop", None)
    d.node(736, 252, 238, 40, None, "Load and validate scenario", None)

    d.node3d(20, 420, 260, 120, "Sensor cart (HIL)")
    d.node(36, 466, 228, 50, None, "Real sensors", None, "box", "camera, radar, LiDAR, ultrasonic")

    d.node3d(20, 580, 260, 120, "HIL bench")
    d.node(36, 626, 228, 30, None, "Simulink vehicle model", None)
    d.node(36, 662, 228, 30, None, "Ethernet commands in", None)

    d.rect(330, 430, 850, 270, "ext", 0)
    d.text(342, 690, "«device» Vehicle platform (production vehicle, safety driver)", "st", "start")
    d.node(350, 462, 190, 76, None, "Sensors", None, "box", "camera, radar, LiDAR,\nGNSS, IMU, V2X\nmounting: provisional")
    d.node(560, 470, 190, 68, None, "Actuation gateway ECU", None, "box", "can disable automation\nlimits: provisional")
    d.node(770, 470, 180, 68, None, "Driver override", None, "box", "brake, steering, accelerator\nthresholds: provisional")
    d.node(970, 470, 190, 68, None, "E-stop + mode switch", None, "box", "hardware, driver-operated")
    d.node(560, 600, 190, 60, None, "Data logger (Intrepid)", None, "box", "recording + CAN logs")
    d.node(970, 600, 190, 60, None, "Dashboard", None, "box", "driver alerts")

    d.path([(280, 150), (330, 150)], arrow="both")
    d.label(305, 136, "PiL")
    d.path([(610, 150), (720, 150)], arrow="both", label="dedicated test/\nlogging network", at=(665, 128))
    d.label(665, 172, "no cellular")
    d.path([(280, 480), (305, 480), (305, 274), (330, 274)], label="real sensor data", at=(300, 400), anchor="end")
    d.path([(280, 640), (318, 640), (318, 170), (330, 170)], arrow="both", label="Ethernet commands (HIL)", at=(300, 562), anchor="end")
    d.path([(445, 462), (445, 350)], "ln dash", label="real sensor data", at=(445, 380))
    d.path([(590, 350), (590, 470)], arrow="both", label="commands (Ethernet)", at=(590, 385))
    d.path([(770, 504), (750, 504)])
    d.path([(1065, 538), (1065, 576), (700, 576), (700, 538)], "ln thin", label="hardware", at=(900, 580))
    d.path([(530, 462), (530, 405), (855, 405), (855, 350)], label="GNSS, IMU, wheel speed; time ref", at=(730, 409))
    d.node(1010, 180, 170, 60, None, "Cloud log storage", None, "ext", "pulled later for replay")
    d.path([(750, 615), (955, 615), (955, 400), (1095, 400), (1095, 240)], label="uploads", at=(1095, 330))
    return d


# ---------------------------------------------------------------- lifecycle
def lifecycle():
    d = D("stm", 1060, 600, "Run lifecycle state machine",
          "Idle, Configuring, Ready, Armed, Running, Stopping, Stopped, Completed, Evaluating. Arming waits for the stack "
          "to report no fault; a stack fault or override, an operator stop or a CSTI failure stops injection.")

    def st(x, y, w, h, name, cls="state"):
        d.rect(x, y, w, h, cls, 12)
        ls = name.split("\n")
        d.lines(x + w / 2, y + h / 2 + 4 - (len(ls) - 1) * 7, ls)
    d.p.append('<circle class="dot" cx="42" cy="72" r="7"/>')
    d.path([(49, 72), (70, 72)])
    st(70, 50, 110, 44, "Idle")
    st(290, 50, 150, 44, "Configuring\n(load + validate)")
    st(560, 50, 110, 44, "Ready")
    st(790, 50, 110, 44, "Armed")
    d.path([(180, 66), (290, 66)], label="start(profile, scenario)", at=(235, 59))
    d.path([(290, 86), (180, 86)], label="[invalid] / report", at=(235, 104))
    d.path([(440, 66), (560, 66)], label="[valid]", at=(500, 59))
    d.path([(670, 66), (790, 66)], label="arm [checks pass]", at=(730, 59))
    d.path([(790, 86), (670, 86)], label="disarm /\ncheck lost", at=(730, 104))
    d.rect(830, 125, 200, 105, "sub", 6)
    d.text(840, 143, "Arming checks (HIL, ViL)", "id", "start")
    d.lines(840, 162, ["stack reports no fault", "scenario validated", "operator confirms driver ready",
                       "MiL, PiL: arm is automatic"], "st", "start", 16)
    st(300, 160, 440, 120, "Running\n(injecting)")
    d.lines(520, 250, ["The stack's own fault detection and safety interlock", "act on their own; CSTI only stops injecting."], "st")
    d.path([(805, 94), (805, 200), (740, 200)], label="start", at=(805, 112))
    st(300, 380, 170, 54, "Stopping\n(injection off, logged)", "safe")
    st(600, 380, 150, 54, "Completed")
    st(300, 490, 170, 44, "Stopped")
    st(830, 440, 150, 50, "Evaluating")
    d.path([(340, 280), (340, 380)], "ln red")
    d.lines(330, 312, ["stack fault or override,", "operator stop,", "CSTI component failure"], "lbl", "end", 13)
    d.path([(675, 280), (675, 380)], label="scenario end", at=(683, 330), anchor="start")
    d.path([(385, 434), (385, 490)], label="recording closed", at=(393, 466), anchor="start")
    d.path([(750, 407), (890, 407), (890, 440)], label="evaluate", at=(820, 411))
    d.path([(385, 534), (385, 565), (940, 565), (940, 490)], label="verdict = stopped (never pass)", at=(650, 569))
    d.path([(980, 465), (1045, 465), (1045, 22), (125, 22), (125, 50)], label="next run in campaign / done", at=(560, 26))
    return d


def pipeline():
    d = D("fus", 1060, 560, "Sensor fusion pipeline",
          "Radar, camera and LiDAR data enter an ingest middleware that time-synchronizes every stream, preprocesses camera "
          "images and synchronizes and downsamples LiDAR point clouds. Time-aligned object lists then go to the C++ object "
          "fusion core in ROS 2. CSTI publishes virtual object lists on the same fusion input topics, mirrored on /virtual/.")
    d.node(20, 75, 130, 60, None, "Radars", "sensor", "box", "object level, CAN")
    d.node(20, 185, 130, 60, None, "Camera", "sensor", "box", "raw images")
    d.node(20, 315, 130, 60, None, "LiDAR", "sensor", "box", "point cloud")
    d.rect(180, 20, 320, 400, "ext", 8)
    d.text(340, 42, "«ingest middleware»", "st")
    d.text(340, 58, "Time sync + preprocessing", "id")
    d.node(200, 75, 280, 60, None, "Timestamp and synchronize", None, "box", "object lists pass through")
    d.node(200, 170, 280, 90, None, "Preprocess + detect", None, "box", "camera preprocessing; detector on an\nembedded GPU module or here (to confirm)")
    d.node(200, 300, 280, 90, None, "Synchronize + downsample", None, "box", "LiDAR point cloud; clustering\ninto objects (location to confirm)")
    d.rect(560, 20, 300, 400, "sys", 8)
    d.text(710, 42, "«C++ core in ROS 2»", "st")
    d.text(710, 58, "Object fusion", "id")
    for k, s_ in enumerate(["Transform to vehicle frame", "Association", "Tracking filter", "Track management"]):
        y = 80 + k * 80
        d.node(580, y, 260, 48, None, s_, None)
        if k:
            d.path([(710, y - 32), (710, y)])
    d.node(890, 310, 150, 64, None, "Fused object list\nto planning", None)
    d.path([(840, 344), (890, 342)])
    d.path([(150, 105), (200, 105)])
    d.path([(150, 215), (200, 215)])
    d.path([(150, 345), (200, 345)])
    d.path([(480, 105), (530, 105)], arrow=None)
    d.path([(480, 215), (530, 215)], arrow=None)
    d.path([(480, 345), (530, 345)], arrow=None)
    d.path([(530, 104), (530, 478)], "ln thin", arrow=None)
    d.path([(530, 104), (580, 104)])
    d.label(545, 440, "time-aligned object lists", anchor="start")
    d.node(250, 452, 190, 56, None, "CSTI gateway (ViL)", None, "frozen")
    d.path([(440, 478), (530, 478)], "ln dash", arrow=None)
    d.label(545, 470, "virtual object lists on the same topics, stamped on the", anchor="start")
    d.label(545, 484, "same time base; mirrored on /virtual/ for logs", anchor="start")
    return d


def datapath():
    d = D("dpa", 1000, 300, "In the data path versus publishing on the same topic",
          "Left: CSTI merges real and virtual data, so real data passes through CSTI. Right: the real publisher is untouched; "
          "CSTI publishes virtual object lists on the same fusion input topic (remapped) and mirrors them on /virtual/.")
    for x, t in ((10, "CSTI in the data path (rejected)"), (510, "Same topic, separate publisher (chosen)")):
        d.rect(x, 10, 480, 280, "lane", 6)
        d.text(x + 12, 30, t, "lanet", "start")
    d.node(30, 90, 120, 50, None, "Real sensor", None)
    d.node(200, 90, 140, 50, None, "CSTI merge node", None, "safe")
    d.node(390, 90, 90, 50, None, "Fusion", None)
    d.node(200, 180, 140, 40, None, "virtual objects", None, "sub")
    d.path([(150, 115), (200, 115)])
    d.path([(340, 115), (390, 115)])
    d.path([(270, 180), (270, 140)])
    d.lines(250, 268, ["If CSTI stalls or crashes, real data stops too."], "st")
    d.node(525, 90, 110, 50, None, "Real sensor", None)
    d.node(670, 90, 150, 50, None, "fusion input topic", None, "sub")
    d.node(870, 90, 100, 50, None, "Fusion", None)
    d.node(670, 185, 150, 46, None, "CSTI gateway", None, "frozen")
    d.node(855, 185, 120, 46, None, "/virtual/ mirror", None, "sub", "logs only")
    d.path([(635, 115), (670, 115)])
    d.path([(820, 115), (870, 115)])
    d.path([(745, 185), (745, 140)], "ln dash", label="remapped, source id = virtual", at=(745, 166))
    d.path([(820, 208), (855, 208)], "ln dash")
    d.lines(750, 260, ["Real publisher untouched. If CSTI fails, only virtual objects stop."], "st")
    return d


ALL = {"context": context, "component": component, "deployment": deployment, "lifecycle": lifecycle,
       "pipeline": pipeline, "datapath": datapath}


# ---------------------------------------------------------------- stage-by-stage deployment
def _n(d, x, y, w, h, title, extra=None, cls="box"):
    d.node(x, y, w, h, None, title, None, cls, extra)


def stages():
    d = D("stg", 1000, 330, "Stages by track",
          "Controls and perception each run MiL and PiL separately, then run together on the full stack in HIL on the "
          "sensor cart and in ViL on the car.")
    for i, s in enumerate(["MiL", "PiL", "HIL", "ViL"]):
        d.text(240 + i * 210, 30, s, "id")
    d.text(70, 108, "Controls", "id")
    d.text(70, 228, "Perception", "id")
    _n(d, 140, 50, 200, 110, "Simulink controllers", "vs RoadRunner Scenario;\nobjects straight from\nRoadRunner, unprocessed")
    _n(d, 350, 50, 200, 110, "C++ controller nodes", "code-generated from Simulink,\non the AUTERA; RoadRunner\nground truth over ROS 2")
    _n(d, 140, 175, 200, 110, "Sensor placement", "checked in RoadRunner;\nAURELION adds realistic\ndata and sensor faults")
    _n(d, 350, 175, 200, 110, "RTMaps + fusion", "on the AUTERA, fed\nAURELION sensor data\nfrom the desktop")
    _n(d, 560, 50, 200, 235, "Sensor cart", "real sensors → RTMaps →\nfull stack on the AUTERA;\nSimulink vehicle model on\nthe bench over Ethernet;\ninterlock active", "sys")
    _n(d, 770, 50, 200, 235, "Full stack on the car", "real sensors plus CSTI's\nvirtual object lists;\nsafety driver;\ninterlock active", "sys")
    for x in (340, 550, 760):
        d.path([(x, 105), (x + 10, 105)])
        d.path([(x, 230), (x + 10, 230)])
    d.lines(500, 315, ["The tracks join in HIL on the sensor cart."], "st")
    return d


def mil_controls():
    d = D("milc", 1000, 300, "Controls MiL", "On one desktop, RoadRunner Scenario gives its objects straight to the Simulink "
          "controllers as unprocessed ground truth; the controllers command the Simulink vehicle model, whose pose goes back to RoadRunner.")
    d.node3d(20, 50, 960, 230, "Desktop workstation")
    _n(d, 50, 100, 230, 90, "RoadRunner Scenario", "actors; objects as\nground truth")
    _n(d, 385, 100, 230, 90, "Simulink controllers", "ACC, LCC, AIN")
    _n(d, 720, 100, 230, 90, "Simulink vehicle model", "vehicle dynamics")
    d.path([(280, 145), (385, 145)])
    d.path([(615, 145), (720, 145)])
    d.path([(835, 190), (835, 225), (165, 225), (165, 190)])
    d.label(667, 136, "commands")
    d.label(332, 136, "objects")
    d.label(500, 229, "ego pose")
    d.lines(500, 262, ["Objects come straight from RoadRunner, unprocessed. No fusion and no safety interlock."], "st")
    return d


def mil_perception():
    d = D("milp", 1000, 330, "Perception MiL", "On one desktop, drive data rebuilds the test site in RoadRunner and sensor placement "
          "and specs are checked; AURELION co-simulates the scenario on VEOS to produce realistic sensor data and add sensor faults.")
    d.node3d(20, 50, 960, 260, "Desktop workstation (VEOS)")
    _n(d, 50, 95, 200, 80, "Drive data", "camera, LiDAR, GPS\nfrom the car", "ext")
    _n(d, 290, 95, 200, 80, "RoadRunner scene", "test site rebuilt\nfrom drive data")
    _n(d, 530, 95, 200, 80, "Sensors placed", "on the vehicle model")
    _n(d, 770, 95, 180, 80, "Placement and\nspec check", "fields of view, range")
    for x in (250, 490, 730):
        d.path([(x, 135), (x + 40, 135)])
    _n(d, 290, 205, 200, 70, "AURELION", "co-simulates the scenario")
    _n(d, 530, 205, 200, 70, "Realistic sensor data", "with injected sensor faults")
    d.path([(390, 175), (390, 205)])
    d.path([(490, 240), (530, 240)])
    d.lines(500, 296, ["Still MiL: no fusion on the car's stack and no safety interlock."], "st")
    return d


def pil_controls():
    d = D("pilc", 1000, 320, "Controls PiL", "The desktop runs RoadRunner Scenario and the Simulink vehicle model and publishes ground "
          "truth over ROS 2 to the code-generated C++ controller nodes on the AUTERA, which send commands back.")
    d.node3d(20, 50, 440, 250, "Desktop workstation")
    _n(d, 45, 95, 190, 80, "RoadRunner Scenario", "actors, ground truth")
    _n(d, 250, 95, 190, 80, "Simulink vehicle model", "vehicle dynamics")
    _n(d, 45, 200, 395, 60, "ROS 2 publisher", "ego odometry and actor positions")
    d.node3d(540, 50, 440, 250, "AUTERA AutoBox")
    _n(d, 565, 95, 390, 90, "C++ controller nodes", "one per controller (ACC, LCC, AIN),\ncode-generated from Simulink")
    d.lines(760, 275, ["No fusion: the controllers receive ground truth."], "st")
    d.path([(235, 135), (250, 135)], arrow="both")
    d.path([(140, 175), (140, 200)])
    d.path([(345, 175), (345, 200)])
    d.path([(440, 230), (660, 230), (660, 185)])
    d.path([(565, 160), (440, 160)])
    d.label(560, 250, "ground truth (ROS 2)")
    d.label(503, 154, "commands (ROS 2)")
    return d


def pil_perception():
    d = D("pilp", 1000, 330, "Perception PiL", "AURELION on the desktop co-simulates the RoadRunner scenario and sends simulated "
          "sensor data to the AUTERA, where RTMaps time-syncs and preprocesses it and the C++ object fusion runs in ROS 2.")
    d.node3d(20, 50, 400, 250, "Desktop workstation (VEOS)")
    _n(d, 45, 95, 350, 60, "RoadRunner Scenario", "scene and actors")
    _n(d, 45, 185, 350, 80, "AURELION", "realistic camera, radar, LiDAR,\nultrasonic data; sensor faults")
    d.path([(220, 155), (220, 185)])
    d.node3d(540, 50, 440, 250, "AUTERA AutoBox")
    _n(d, 565, 185, 390, 80, "RTMaps", "time sync, camera preprocessing,\nLiDAR sync + downsample", "ext")
    _n(d, 565, 95, 390, 60, "Object fusion (C++, ROS 2)", "tracked object list")
    d.path([(760, 185), (760, 155)])
    d.path([(395, 225), (565, 225)])
    d.label(480, 216, "sensor data")
    d.lines(500, 318, ["How AURELION's output reaches the AUTERA is to confirm."], "st")
    return d


def hil():
    d = D("hil", 1000, 470, "HIL: the sensor cart", "Real sensors on a cart feed RTMaps and the full ROS 2 stack on the AUTERA "
          "with the interlock active; the stack sends Ethernet commands to the Simulink vehicle model on the HIL bench. "
          "CSTI adds virtual objects through its gateway.")
    d.node3d(20, 50, 300, 170, "HIL bench (SCALEXIO)")
    _n(d, 40, 95, 260, 90, "Simulink vehicle model", "steering, braking,\nacceleration in")
    d.node3d(20, 280, 300, 150, "Sensor cart")
    _n(d, 40, 325, 260, 80, "Real sensors", "camera, radar, LiDAR,\nultrasonic")
    d.node3d(400, 50, 340, 380, "AUTERA AutoBox")
    stack = [("Vehicle interface", 95), ("Safety interlock (active)", 140), ("Planning + state machines", 185),
             ("Object fusion (ROS 2)", 230)]
    for t, y in stack:
        _n(d, 420, y, 280, 36, t)
    for (_, y1), (_, y2) in zip(stack, stack[1:]):
        d.path([(560, y2), (560, y1 + 36)])
    _n(d, 420, 280, 280, 56, "RTMaps", "time sync, camera preprocessing,\nLiDAR sync + downsample", "ext")
    d.path([(560, 280), (560, 266)])
    _n(d, 420, 350, 280, 50, "CSTI gateway", "virtual objects, faults", "frozen")
    d.path([(700, 375), (722, 375), (722, 248), (700, 248)], "ln dash")
    d.node3d(810, 50, 170, 380, "Desktop (CSTI)")
    for i, t in enumerate(["Test orchestrator", "Fault injector", "Operator view", "Scoring"]):
        _n(d, 825, 95 + i * 60, 140, 44, t)
    d.path([(810, 366), (700, 366)])
    d.path([(420, 113), (300, 113)])
    d.label(360, 104, "Ethernet")
    d.path([(300, 365), (360, 365), (360, 310), (420, 310)])
    d.label(360, 300, "raw data")
    d.lines(500, 458, ["Perception and controls run together on the full stack with real sensor data."], "st")
    return d


def vil():
    d = D("vil", 1000, 470, "ViL", "On the car, real sensors go through RTMaps into the full stack on the AUTERA, which commands "
          "the actuation gateway over Ethernet. The in-vehicle test computer adds virtual object lists through the CSTI "
          "gateway, placed around the car's real pose. The Intrepid logger records the run and uploads it to the cloud.")
    d.rect(20, 20, 960, 430, "ext", 6)
    d.text(36, 440, "«device» Production vehicle with safety driver", "st", "start")
    _n(d, 40, 70, 170, 80, "Real sensors", "camera, radar, LiDAR,\nGNSS, IMU, V2X")
    d.node3d(260, 60, 340, 340, "AUTERA AutoBox")
    stack = [("RTMaps", 100), ("Object fusion (ROS 2)", 148), ("Planning + state machines", 192),
             ("Safety interlock (active)", 236), ("Vehicle interface", 280)]
    for t, y in stack:
        _n(d, 280, y, 290, 36, t, None, "ext" if t == "RTMaps" else "box")
    for (_, y1), (_, y2) in zip(stack, stack[1:]):
        d.path([(425, y1 + 36), (425, y2)])
    _n(d, 280, 334, 290, 40, "CSTI gateway", "virtual object lists", "frozen")
    d.path([(570, 354), (588, 354), (588, 166), (570, 166)], "ln dash")
    _n(d, 650, 70, 160, 50, "Intrepid logger", "uploads to the cloud", "ext")
    _n(d, 650, 250, 160, 60, "Actuation gateway ECU", "can disable automation")
    _n(d, 650, 340, 160, 50, "Driver override, E-stop", "hardware", "ext")
    d.node3d(840, 160, 125, 190, "Test computer")
    _n(d, 850, 205, 105, 50, "Headless player")
    _n(d, 850, 265, 105, 50, "Operator view")
    d.path([(210, 110), (280, 118)])
    d.path([(570, 298), (650, 285)])
    d.label(622, 272, "Ethernet")
    d.path([(730, 340), (730, 310)])
    d.path([(600, 95), (650, 95)])
    d.path([(900, 350), (900, 412), (608, 412), (608, 360), (570, 360)])
    d.path([(125, 150), (125, 428), (930, 428), (930, 350)])
    d.label(520, 432, "pose")
    return d


ALL.update({"stages": stages, "mil-controls": mil_controls, "mil-perception": mil_perception, "pil-perception": pil_perception,
            "pil-controls": pil_controls, "hil": hil, "vil": vil})
