# Requirements page content. Cell values are HTML. Requirement rows: id, text, accept, ver, prio (must/should), src.

REQPAGE_LEDE = ('What CSTI must do, how well, and what it must never do. Each requirement has a unique name, '
 'an acceptance criterion and a verification method.')

REQPAGE_PURPOSE = ('<p>Automated-vehicle software is tested on a desktop, on the target computer and on the vehicle. '
 'Each stage usually keeps its own copy of every test, so tests are rebuilt several times and results cannot be compared. '
 'CSTI lets <strong>one scenario run unchanged in four stages</strong>:</p>\n'
 '<dl class="defs">\n'
 '<dt>MiL (Model-in-the-Loop)</dt><dd>Controls: Simulink controllers against RoadRunner Scenario, with objects taken straight from RoadRunner, unprocessed. Perception: sensor placement and specs checked in RoadRunner, with AURELION adding realistic sensor data and sensor faults on the desktop. No fusion on the vehicle stack and no safety interlock.</dd>\n'
 '<dt>PiL (Processor-in-the-Loop)</dt><dd>Controls: each Simulink controller is code-generated separately into a C++ ROS 2 node on the AUTERA AutoBox, fed RoadRunner ground truth over ROS 2. Perception: RTMaps and the C++ object fusion run on the AUTERA, fed AURELION simulated sensor data from the desktop.</dd>\n'
 '<dt>HIL (Hardware-in-the-Loop)</dt><dd>The sensor cart: real sensors on a cart feed RTMaps and the full stack on the AUTERA with its safety interlock active, while the Simulink vehicle model on the HIL bench receives the stack’s Ethernet commands.</dd>\n'
 '<dt>ViL (Vehicle-in-the-Loop)</dt><dd>The production vehicle on a closed course with real sensors, a safety driver and the full safety chain, with virtual actors injected around its real position.</dd>\n'
 '</dl>\n'
 '<p>The autonomy stack is <em>outside</em> CSTI. CSTI feeds its inputs, records its outputs and never commands '
 'actuators. A <strong>shadow</strong> profile runs the stack live without engaging automation.</p>')

REQPAGE_CUSTOMER = ('<p><strong>Customer:</strong> the Virginia Tech HEVT EcoCAR connected and automated vehicles sub-team.</p>')

REQPAGE_STAKEHOLDERS = [('U-01', 'Test engineer', 'Write a scenario once, run it in any stage, get verdicts.'),
 ('U-02', 'Autonomy developer', 'Get realistic inputs and replay any run on a desktop.'),
 ('U-03', 'Safety driver / test operator', 'See the stack status and the virtual actors, and stop injection at once.'),
 ('U-04', 'Competition organizers (secondary)', 'Review traceable, reproducible test evidence.')]

REQPAGE_CONVENTIONS = ('<ul>\n'
 '<li><strong>Names.</strong> Each requirement has a unique name used on every page. Groups: Functional, '
 'Non-functional, Safety and Constraints.</li>\n'
 '<li><strong>Priority.</strong> <span class="tag must">Must</span> required; <span class="tag should">Should</span> '
 'expected but not essential.</li>\n'
 '<li><strong>Verification.</strong> <strong>T</strong> test, <strong>A</strong> analysis, <strong>I</strong> '
 'inspection, <strong>D</strong> demonstration.</li>\n'
 '<li><strong>Numbers.</strong> Every threshold is a team proposal, linked to the <a href="#proposed">proposed '
 'values</a> table.</li>\n'
 '<li><strong>Provisional.</strong> Sensor mounting, actuation limits, override thresholds and where camera detection '
 'and LiDAR clustering run are not yet settled.</li>\n'
 '</ul>')

REQPAGE_CONSTRAINTS = [('CON-01',
  "The stack runs on the target computer in one container: an ingest middleware syncs and preprocesses sensor data, "
  "and ROS 2 does object fusion and the rest. CSTI connects through ROS 2 topics at fusion's inputs."),
 ('CON-02', 'The stack is not modified for CSTI, apart from launch-time topic remapping.'),
 ('CON-03', 'Hardware is described generically; no vehicle-specific or confidential data appears on this public site.'),
 ('CON-04', "ViL runs only on a closed course with a safety driver. The vehicle's override, E-stop, mode switch and "
  'actuation gateway stay in place, and CSTI never commands them.'),
 ('CON-05', 'The vehicle publishes its position, heading, velocity and uncertainty on a ROS 2 topic.'),
 ('CON-06', "CSTI must work with more than one simulator and cannot depend on one vendor's format.")]

REQPAGE_FUNCTIONAL = ('',
 [('5.1 Scenario definition',
   [{'id': 'FR-01',
     'text': 'The system shall define each test as one scenario holding the road network, actors, triggers and pass/fail criteria.',
     'accept': 'A reference scenario with all four parts runs without outside inputs other than stage configuration.',
     'ver': 'I, T', 'prio': 'must', 'src': 'U-01'},
    {'id': 'FR-02',
     'text': 'The system shall run the same scenario file, unmodified, in every stage.',
     'accept': 'Each reference scenario, with the same checksum, completes in every stage.',
     'ver': 'T', 'prio': 'must', 'src': 'U-01, U-04'},
    {'id': 'FR-03',
     'text': 'The system shall store scenarios in ASAM OpenDRIVE and OpenSCENARIO.',
     'accept': 'No reference scenario needs a vendor-specific field.',
     'ver': 'I', 'prio': 'must', 'src': 'CON-06'},
    {'id': 'FR-04',
     'text': 'The system shall reject an invalid scenario before a run, naming every rule it breaks, including operating-domain limits.',
     'accept': 'Each seeded invalid scenario is rejected before arming with the correct cause.',
     'ver': 'T', 'prio': 'must', 'src': 'U-01, U-03'}]),
  ('5.2 Stages and simulation backends',
   [{'id': 'FR-05',
     'text': 'The system shall support a desktop simulator (MiL), a RoadRunner-to-ROS 2 publisher (controls PiL), a physics-based sensor simulator (perception MiL and PiL) and a headless object-level player (ViL).',
     'accept': 'The reference scenarios run on each backend.',
     'ver': 'D', 'prio': 'must', 'src': 'U-01'},
    {'id': 'FR-06',
     'text': 'The system shall select stage and backend by configuration only.',
     'accept': 'Switching stage or backend changes no code, scenario or stack.',
     'ver': 'I, T', 'prio': 'must', 'src': 'U-01'}]),
  ('5.3 Actors and sensors',
   [{'id': 'FR-07',
     'text': 'The system shall own actor behavior (vehicles, motorcycles, pedestrians) independently of the backend.',
     'accept': 'Two backends with the same seed agree within <a class="pv" href="#PV-13">PV-13</a>.',
     'ver': 'T', 'prio': 'must', 'src': 'U-01, U-02'},
    {'id': 'FR-08',
     'text': 'The system shall fire triggers on time, actor state and ego state.',
     'accept': 'Each trigger fires on the correct tick in MiL and within one tick in ViL.',
     'ver': 'T', 'prio': 'must', 'src': 'U-01'},
    {'id': 'FR-09',
     'text': 'The system shall generate sensor data as object lists (optional noise) or raw data (images, point clouds, radar detections, ultrasonic range).',
     'accept': 'Each level is selectable per sensor; raw simulated data is used only in MiL and PiL.',
     'ver': 'T', 'prio': 'must', 'src': 'U-02'},
    {'id': 'FR-10',
     'text': "The system shall deliver injected data on the stack's existing input topics, identical in format to real "
             'sensors in every stage, and keep a separate copy for logging.',
     'accept': 'The stack runs unmodified in every stage, and recorded injected data matches real-sensor format.',
     'ver': 'I, T', 'prio': 'must', 'src': 'U-02, CON-02'}]),
  ('5.4 Ego vehicle',
   [{'id': 'FR-11',
     'text': "In MiL, PiL and HIL, the system shall compute the ego state from a plant model driven by the stack's commands.",
     'accept': 'Stack commands change the ego trajectory on the next tick.',
     'ver': 'T', 'prio': 'must', 'src': 'U-01'},
    {'id': 'FR-12',
     'text': "In ViL, the system shall place every virtual actor relative to the vehicle's measured position.",
     'accept': 'On a surveyed path, logged actor positions match the scenario within <a class="pv" href="#PV-05">PV-05</a>.',
     'ver': 'T, A', 'prio': 'must', 'src': 'U-01, U-03'}]),
  ('5.5 Fault injection',
   [{'id': 'FR-13',
     'text': 'The system shall inject scheduled sensor faults: dropouts, latency, frozen output, noise, bias, ghost targets and frame drops.',
     'accept': 'Each fault appears in the recording at the scheduled time.',
     'ver': 'T', 'prio': 'must', 'src': 'U-01, U-02'},
    {'id': 'FR-14',
     'text': "In MiL, PiL and HIL, the system shall inject network, heartbeat, GNSS-outage and actuator faults to test the stack's fault response.",
     'accept': "Each fault is visible in the recording, together with the stack's response.",
     'ver': 'T', 'prio': 'should', 'src': 'U-01'}]),
  ('5.6 Orchestration and campaigns',
   [{'id': 'FR-15',
     'text': 'The system shall start a run, including validation and readiness checks, with one action.',
     'accept': 'One command starts a MiL run and reports ready or the failed checks.',
     'ver': 'D', 'prio': 'must', 'src': 'U-01'},
    {'id': 'FR-16',
     'text': 'The system shall run parameter-sweep campaigns unattended in MiL, PiL and HIL.',
     'accept': 'A two-parameter sweep completes unattended; a crashed run is logged and the campaign continues.',
     'ver': 'T', 'prio': 'must', 'src': 'U-01'},
    {'id': 'FR-17',
     'text': "The system shall give each run a pass/fail verdict linked to its recording, including whether the stack responded correctly to any injected fault.",
     'accept': 'Every completed run has a verdict, its deciding criterion and a working recording link.',
     'ver': 'I, T', 'prio': 'must', 'src': 'U-01, U-04'},
    {'id': 'FR-23',
     'text': 'The system shall offer a shadow profile in HIL and ViL: the stack runs live, automation stays off and would-have commands are logged.',
     'accept': 'The actuation gateway receives only neutral commands, and the recording holds the would-have commands.',
     'ver': 'T, I', 'prio': 'should', 'src': 'U-01, U-02'}]),
  ('5.7 Recording and replay',
   [{'id': 'FR-18',
     'text': 'The system shall record, with timestamps, all inputs, stack outputs and status, ego state, vehicle bus, '
             'operator actions and run configuration.',
     'accept': 'Every category is present and timestamped in a completed recording.',
     'ver': 'I, T', 'prio': 'must', 'src': 'U-02, U-04'},
    {'id': 'FR-19',
     'text': 'The system shall replay any recording, including ViL runs, in MiL with original timing.',
     'accept': 'A ViL recording replays in MiL and the stack receives the same message sequence.',
     'ver': 'T', 'prio': 'must', 'src': 'U-02'},
    {'id': 'FR-20',
     'text': 'The system shall store recordings in open formats (MCAP bags, standard CAN logs).',
     'accept': 'Recordings open in standard tools without CSTI.',
     'ver': 'I, D', 'prio': 'should', 'src': 'U-02, U-04'}]),
  ('5.8 Monitoring',
   [{'id': 'FR-21',
     'text': "During HIL and ViL, the system shall show the operator the run state, the stack's status (feature states, "
             'faults, touring mode) and the virtual actors, with a stop control.',
     'accept': 'All items are on one screen and update at least once a second.',
     'ver': 'D', 'prio': 'must', 'src': 'U-03'},
    {'id': 'FR-22',
     'text': 'The system shall show campaign progress and verdicts as they arrive.',
     'accept': 'A running campaign shows completed runs and their verdicts.',
     'ver': 'D', 'prio': 'should', 'src': 'U-01'}])])

REQPAGE_NONFUNCTIONAL = ('',
 [('6.1 Extensibility and vendor neutrality',
   [{'id': 'NFR-01',
     'text': 'Adding a simulator shall require only a new adapter.',
     'accept': 'The change touches only the adapter and configuration; reference scenarios then run.',
     'ver': 'I, D', 'prio': 'must', 'src': 'U-01, CON-06'},
    {'id': 'NFR-02',
     'text': 'Adding a sensor type shall only add to the stack interface, never change it.',
     'accept': 'No existing interface definition is modified or removed.',
     'ver': 'I', 'prio': 'must', 'src': 'U-02'},
    {'id': 'NFR-03',
     'text': 'Only adapters shall depend on simulator vendor code.',
     'accept': 'Dependency review finds vendor code only in adapters.',
     'ver': 'I', 'prio': 'must', 'src': 'CON-06'},
    {'id': 'NFR-04',
     'text': 'Runtime components shall run on the desktop and the target computer without code changes.',
     'accept': 'The same build runs on both.',
     'ver': 'I, D', 'prio': 'should', 'src': 'U-01'}]),
  ('6.2 Timing and accuracy',
   [{'id': 'NFR-05',
     'text': 'In ViL, injection latency from pose sample to published data shall not exceed <a class="pv" href="#PV-01">PV-01</a>.',
     'accept': 'The 99th-percentile latency in a reference run is within PV-01.',
     'ver': 'T', 'prio': 'must', 'src': 'U-02, U-03'},
    {'id': 'NFR-06',
     'text': 'Clock offset between any node and the stage clock shall not exceed <a class="pv" href="#PV-02">PV-02</a>.',
     'accept': 'Logged offsets stay within PV-02 for the whole run.',
     'ver': 'T', 'prio': 'must', 'src': 'U-02'},
    {'id': 'NFR-07',
     'text': 'In ViL, virtual-actor placement error at 50 m shall not exceed <a class="pv" href="#PV-05">PV-05</a>, given '
             'localization within <a class="pv" href="#PV-03">PV-03</a> and <a class="pv" href="#PV-04">PV-04</a>.',
     'accept': 'An error budget shows the bound holds, confirmed by the surveyed-path test.',
     'ver': 'A, T', 'prio': 'must', 'src': 'U-03'},
    {'id': 'NFR-08',
     'text': 'Repeated MiL runs with the same scenario, seed and configuration shall produce identical inputs.',
     'accept': 'Two runs produce identical injected data and timestamps.',
     'ver': 'T', 'prio': 'must', 'src': 'U-02, U-04'},
    {'id': 'NFR-09',
     'text': 'In ViL, the system shall keep full publication rates with up to <a class="pv" href="#PV-06">PV-06</a> actors.',
     'accept': 'A PV-06 scenario misses no publication periods and stays within PV-01.',
     'ver': 'T', 'prio': 'must', 'src': 'U-01'}]),
  ('6.3 Recording integrity',
   [{'id': 'NFR-10',
     'text': 'Recordings shall drop no messages, and any drop shall mark the run invalid.',
     'accept': 'A reference run shows no gaps; a forced drop marks the run invalid.',
     'ver': 'T', 'prio': 'must', 'src': 'U-02, U-04'},
    {'id': 'NFR-11',
     'text': 'Replay shall keep message order and timing within <a class="pv" href="#PV-02">PV-02</a>.',
     'accept': 'Replay count, order and intervals match the recording.',
     'ver': 'T', 'prio': 'must', 'src': 'U-02'}]),
  ('6.4 Usability',
   [{'id': 'NFR-12',
     'text': 'The operator stop control shall always be visible during ViL and work with one action.',
     'accept': 'Every ViL screen shows the stop control, and one action stops injection.',
     'ver': 'I, T', 'prio': 'must', 'src': 'U-03'},
    {'id': 'NFR-13',
     'text': 'Fault and feature states shall not rely on color alone.',
     'accept': 'Every state shown has a text label.',
     'ver': 'I', 'prio': 'must', 'src': 'U-03'},
    {'id': 'NFR-14',
     'text': 'A new team member shall modify and run a template scenario in MiL within <a class="pv" href="#PV-07">PV-07</a>.',
     'accept': 'Three new members each finish within PV-07 in a timed trial.',
     'ver': 'D', 'prio': 'should', 'src': 'U-01'}])])

REQPAGE_SAFETY = ('<div class="note safety">\n'
 '<p><strong>Safety principle.</strong> CSTI has no safety role. Safety belongs to the stack: a fault detection node '
 'watches critical systems, the ACC, LCC and AIN state machines watch for driver overrides, and the safety interlock '
 'sends default commands and alerts the driver on any fault. CSTI only adds objects that are not there, listens to the '
 "stack's status, and stops injecting when the stack or the operator says so.</p>\n"
 '</div>',
 [(None,
   [{'id': 'SR-01',
     'text': 'In ViL, the system shall add synthetic data without blocking, changing or delaying real sensor data.',
     'accept': 'Real-sensor recordings with and without CSTI match within PV-02.',
     'ver': 'I, T', 'prio': 'must', 'src': 'U-03'},
    {'id': 'SR-02',
     'text': 'In HIL and ViL, the system shall start injecting only when the stack reports no active fault, the scenario '
             'has passed validation and the operator confirms the safety driver is ready.',
     'accept': 'Failing each condition in turn blocks the start and names the cause.',
     'ver': 'T', 'prio': 'must', 'src': 'U-03, U-04'},
    {'id': 'SR-03',
     'text': 'The system shall stop injecting within <a class="pv" href="#PV-10">PV-10</a> when the stack reports a fault, '
             'a driver override or a disengaged feature.',
     'accept': 'Each reported event stops injection within PV-10 and is recorded.',
     'ver': 'T', 'prio': 'must', 'src': 'U-03'},
    {'id': 'SR-04',
     'text': 'The system shall stop injecting within <a class="pv" href="#PV-10">PV-10</a> on operator command.',
     'accept': 'One operator action stops injection within PV-10.',
     'ver': 'T', 'prio': 'must', 'src': 'U-03'},
    {'id': 'SR-05',
     'text': "The system shall never introduce an actor in the ego path closer than <a class=\"pv\" href=\"#PV-09\">PV-09</a>.",
     'accept': 'Such scenarios are rejected; such run-time triggers are suppressed and logged.',
     'ver': 'T, A', 'prio': 'must', 'src': 'U-03'},
    {'id': 'SR-06',
     'text': "A CSTI crash, stall or bad output shall not block, delay or change the stack's fault detection, state "
             'machines or safety interlock.',
     'accept': "Killing each CSTI component during HIL runs leaves the stack's fault response unchanged.",
     'ver': 'T, I', 'prio': 'must', 'src': 'U-03, U-04'},
    {'id': 'SR-08',
     'text': 'The system shall record every stack fault, state transition, driver override and interlock default during a run.',
     'accept': 'Each such event in a HIL run appears in the recording with its time.',
     'ver': 'T', 'prio': 'must', 'src': 'U-03, U-04'},
    {'id': 'SR-13',
     'text': 'In ViL, only synthetic sensor streams shall be fault-injected.',
     'accept': 'ViL scenarios with network, actuator or GNSS faults are rejected; those fault paths are not deployed on the vehicle.',
     'ver': 'I, T', 'prio': 'must', 'src': 'U-03'}])])

REQPAGE_PV_INTRO = ('<p>All values are <span class="tag proposed">proposed</span> by the team, each with a basis and a way to confirm it.</p>')

REQPAGE_PV = [('PV-01', 'Injection latency (99th percentile)', '&le; 50 ms',
  'At the speed cap, 50 ms is 0.75 m of travel, inside the placement budget.', 'Measure in HIL.'),
 ('PV-02', 'Clock offset to any node', '&le; 1 ms', 'Negligible next to the latency limit.', 'Measure on the vehicle network.'),
 ('PV-03', 'Localization position error (95%)', '&le; 0.20 m', 'Leaves most of the placement budget for heading and latency.', 'Measure on the test site.'),
 ('PV-04', 'Localization heading error (95%)', '&le; 0.5&deg;', 'About 0.44 m sideways at 50 m.', 'Measure on the test site.'),
 ('PV-05', 'Virtual-actor placement error at 50 m (95%)', '&le; 1.0 m',
  'Keeps a virtual car in its lane; the combined errors above total about 0.89 m.', 'Surveyed-path test.'),
 ('PV-06', 'Simultaneous virtual actors in ViL', '20', 'Covers a busy multi-lane scene.', 'Check the scenario library.'),
 ('PV-07', 'New-user time to run a template scenario', '&le; 60 min', 'Onboarding target each semester.', 'Timed trial.'),
 ('PV-08', 'Maximum ViL speed', "15 m/s or the site limit, whichever is lower", 'Bounds placement error and exposure.', 'Safety review.'),
 ('PV-09', 'Minimum time gap for an actor in the ego path', '2 s', 'The two-second rule; avoids forced hard braking.', 'Safety review; tune in MiL.'),
 ('PV-10', 'Stop-injection reaction time', '&le; 100 ms', 'Two latency periods.', 'Bench and ViL dry runs.'),
 ('PV-13', 'Cross-backend actor agreement', '&le; 0.10 m', 'CSTI computes actor state, so only numerics differ.', 'Run on two backends.')]

REQPAGE_PV_NOTE = ''

REQPAGE_COVERAGE_INTRO = '<p>Each required topic and the requirements that cover it:</p>'

REQPAGE_COVERAGE = [('One scenario in every stage', 'FR-01, FR-02, FR-03, FR-06'),
 ('New simulator without stack changes', 'NFR-01, NFR-03, FR-05'),
 ('Injection on real position in ViL', 'FR-12, FR-10, SR-01'),
 ('Latency and sync limits', 'NFR-05, NFR-06'),
 ('Pose accuracy for placement', 'NFR-07, PV-03, PV-04, PV-05'),
 ('Replay determinism', 'NFR-08, NFR-11, FR-19'),
 ('Starting and stopping injection', 'SR-02, SR-03, SR-04'),
 ("CSTI never affects the stack's safety chain", 'SR-06, SR-01'),
 ("Stack fault response tested and recorded", 'FR-14, FR-17, SR-08'),
 ('No pop-in actors', 'SR-05'),
 ('Shadow runs', 'FR-23, FR-18'),
 ('Recording completeness', 'FR-18, FR-20, NFR-10, NFR-11'),
 ('Operator usability', 'FR-21, NFR-12, NFR-13, NFR-14'),
 ('Fault injection', 'FR-13, FR-14, SR-13')]

REQPAGE_OPEN_ISSUES = ['<strong>Stack behavior when injection stops.</strong> Resolved by <a href="rationale.html#D-10">D-10</a>: '
 'CSTI removes all virtual objects at once, and the stack\'s safety interlock sends default commands and alerts the driver.',
 '<strong>Where virtual and real data meet.</strong> Resolved by <a href="rationale.html#D-07">D-07</a>: on fusion\'s existing topics, with a logging copy.',
 '<strong>Raw data in ViL.</strong> Resolved by <a href="rationale.html#D-04">D-04</a>: object lists only.',
 '<strong>Unmeasured values.</strong> PV-01, PV-02 and PV-03 depend on hardware not yet measured.',
 '<strong>Provisional inputs.</strong> Sensor mounting, actuation limits, override thresholds, and camera detection and LiDAR clustering locations.']
