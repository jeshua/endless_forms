/**
 * Hexagonal Modular Puppet System - JSCAD Implementation
 *
 * This file can be loaded into https://openjscad.xyz/ for proper CAD output
 * and exports to STL, DXF, and other formats.
 *
 * Three floating robotic puppets that clip together to form a perfect hexagon
 * using 120-degree rotational symmetry (C3 symmetry).
 */

const jscad = require('@jscad/modeling');
const { cube, cuboid, cylinder, sphere, polygon } = jscad.primitives;
const { extrudeLinear, extrudeRotate } = jscad.extrusions;
const { union, subtract, intersect } = jscad.booleans;
const { translate, rotateX, rotateY, rotateZ, scale, mirrorX } = jscad.transforms;
const { hull, hullChain } = jscad.hulls;
const { colorize } = jscad.colors;
const { degToRad } = jscad.utils;

// ============================================================================
// PARAMETERS - Adjust these to customize your puppets
// ============================================================================

const getParameterDefinitions = () => {
    return [
        { name: 'hexRadius', type: 'float', initial: 50, min: 30, max: 100, step: 1, caption: 'Hexagon Radius (mm)' },
        { name: 'puppetHeight', type: 'float', initial: 25, min: 10, max: 50, step: 1, caption: 'Puppet Height (mm)' },
        { name: 'tolerance', type: 'float', initial: 0.2, min: 0.1, max: 0.5, step: 0.05, caption: 'Fit Tolerance (mm)' },
        { name: 'wallThickness', type: 'float', initial: 2.5, min: 1.5, max: 4, step: 0.5, caption: 'Wall Thickness (mm)' },
        { name: 'magnetDiameter', type: 'float', initial: 5, min: 3, max: 8, step: 1, caption: 'Magnet Diameter (mm)' },
        { name: 'magnetHeight', type: 'float', initial: 2, min: 1, max: 4, step: 0.5, caption: 'Magnet Height (mm)' },
        { name: 'showPuppet1', type: 'checkbox', checked: true, caption: 'Show Puppet 1 (Scout)' },
        { name: 'showPuppet2', type: 'checkbox', checked: true, caption: 'Show Puppet 2 (Lifter)' },
        { name: 'showPuppet3', type: 'checkbox', checked: true, caption: 'Show Puppet 3 (Swarm)' },
        { name: 'explodedView', type: 'checkbox', checked: false, caption: 'Exploded View' },
        { name: 'exportMode', type: 'choice', caption: 'Export Mode', values: ['assembled', 'individual', 'print-layout'], captions: ['Assembled', 'Individual Files', 'Print Layout'], initial: 'assembled' }
    ];
};

// ============================================================================
// MAIN ENTRY POINT
// ============================================================================

const main = (params) => {
    const {
        hexRadius,
        puppetHeight,
        tolerance,
        wallThickness,
        magnetDiameter,
        magnetHeight,
        showPuppet1,
        showPuppet2,
        showPuppet3,
        explodedView,
        exportMode
    } = params;

    const puppets = [];
    const explodeDistance = explodedView ? hexRadius * 0.8 : 0;

    // Create each puppet
    if (showPuppet1) {
        let puppet1 = createPuppet1(hexRadius, puppetHeight, tolerance, wallThickness, magnetDiameter, magnetHeight);
        puppet1 = colorize([0.91, 0.27, 0.38, 1], puppet1); // #e94560
        if (explodedView) {
            puppet1 = translate([explodeDistance * Math.cos(Math.PI / 6), explodeDistance * Math.sin(Math.PI / 6), 0], puppet1);
        }
        puppets.push(puppet1);
    }

    if (showPuppet2) {
        let puppet2 = createPuppet2(hexRadius, puppetHeight, tolerance, wallThickness, magnetDiameter, magnetHeight);
        puppet2 = rotateZ(degToRad(120), puppet2);
        puppet2 = colorize([0.06, 0.30, 0.46, 1], puppet2); // #0f4c75
        if (explodedView) {
            puppet2 = translate([explodeDistance * Math.cos(degToRad(120 + 30)), explodeDistance * Math.sin(degToRad(120 + 30)), 0], puppet2);
        }
        puppets.push(puppet2);
    }

    if (showPuppet3) {
        let puppet3 = createPuppet3(hexRadius, puppetHeight, tolerance, wallThickness, magnetDiameter, magnetHeight);
        puppet3 = rotateZ(degToRad(240), puppet3);
        puppet3 = colorize([0, 0.72, 0.58, 1], puppet3); // #00b894
        if (explodedView) {
            puppet3 = translate([explodeDistance * Math.cos(degToRad(240 + 30)), explodeDistance * Math.sin(degToRad(240 + 30)), 0], puppet3);
        }
        puppets.push(puppet3);
    }

    // Handle export modes
    if (exportMode === 'print-layout') {
        // Arrange puppets side by side for printing
        const spacing = hexRadius * 2.5;
        return puppets.map((p, i) => translate([i * spacing - spacing, 0, 0], p));
    }

    return puppets;
};

// ============================================================================
// RHOMBUS BASE SHAPE (1/3 of hexagon)
// ============================================================================

const createRhombusBase = (hexRadius, height, bevelSize = 2) => {
    // A regular hexagon divided into 3 rhombi by connecting center to alternating vertices
    // Each rhombus has vertices at: center, two adjacent hexagon vertices

    const angle1 = 0;
    const angle2 = degToRad(60);

    // Rhombus vertices (starting from center)
    const points = [
        [0, 0],
        [hexRadius * Math.cos(angle1), hexRadius * Math.sin(angle1)],
        [hexRadius * Math.cos(angle1) + hexRadius * Math.cos(angle2), hexRadius * Math.sin(angle1) + hexRadius * Math.sin(angle2)],
        [hexRadius * Math.cos(angle2), hexRadius * Math.sin(angle2)]
    ];

    // Create polygon and extrude
    const rhombus2D = polygon({ points: points });
    const rhombusBase = extrudeLinear({ height: height * 0.4 }, rhombus2D);

    // Add slight bevel at top using hull with smaller shape
    const beveledTop = translate([0, 0, height * 0.35],
        hull(
            extrudeLinear({ height: 0.1 }, rhombus2D),
            translate([bevelSize, bevelSize, height * 0.08],
                scale([0.92, 0.92, 1],
                    extrudeLinear({ height: 0.1 }, rhombus2D)
                )
            )
        )
    );

    return union(rhombusBase, beveledTop);
};

// ============================================================================
// CLIP MECHANISM - Central interlocking system
// ============================================================================

const createClipMechanism = (hexRadius, height, tolerance) => {
    const clipRadius = 5;
    const clipHeight = height * 0.35;

    // Main cylindrical post (hexagonal for stronger connection)
    const mainPost = cylinder({ radius: clipRadius, height: clipHeight, segments: 6 });

    // Interlocking tooth (male connector)
    const tooth = translate([clipRadius + 1.5, 0, 0],
        cuboid({ size: [3, 2, clipHeight * 0.8] })
    );

    // Receiving slot (female connector) - slightly larger for tolerance
    const slotSize = 3 + tolerance * 2;
    const slot = translate([-clipRadius - 1.5, 4, 0],
        cuboid({ size: [slotSize, 2 + tolerance * 2, clipHeight * 0.8] })
    );

    // Combine post with tooth, but cut out slot
    const clipPositive = union(mainPost, tooth);
    const clipMechanism = subtract(clipPositive, slot);

    // Position at center connection point
    return translate([2, 2, clipHeight / 2], clipMechanism);
};

// ============================================================================
// MAGNET SLOTS - For magnetic coupling
// ============================================================================

const createMagnetSlots = (hexRadius, height, magnetDiameter, magnetHeight, tolerance) => {
    const magnetRadius = (magnetDiameter / 2) + (tolerance / 2);
    const slotDepth = magnetHeight + tolerance;

    // Two magnet positions near the center for secure connection
    const slot1 = translate([8, 3, slotDepth / 2],
        cylinder({ radius: magnetRadius, height: slotDepth, segments: 32 })
    );

    const slot2 = translate([3, 8, slotDepth / 2],
        cylinder({ radius: magnetRadius, height: slotDepth, segments: 32 })
    );

    return union(slot1, slot2);
};

// ============================================================================
// PUPPET 1: "THE SCOUT" - Cyclopean sensor with hover thrusters
// ============================================================================

const createPuppet1 = (hexRadius, height, tolerance, wallThickness, magnetDiameter, magnetHeight) => {
    // Base rhombus
    let puppet = createRhombusBase(hexRadius, height);

    // Calculate centroid of rhombus for feature placement
    const cx = hexRadius * 0.5 * (1 + Math.cos(degToRad(60)));
    const cy = hexRadius * 0.5 * Math.sin(degToRad(60));

    // Main sensor dome
    const domeRadius = 10;
    const dome = translate([cx - 5, cy, height * 0.4 + domeRadius * 0.5],
        sphere({ radius: domeRadius, segments: 32 })
    );

    // Cut dome in half (hemisphere)
    const domeCutter = translate([cx - 5, cy, height * 0.4 - domeRadius],
        cuboid({ size: [domeRadius * 3, domeRadius * 3, domeRadius * 2] })
    );
    const hemisphere = subtract(dome, domeCutter);

    // Sensor lens ring
    const lensOuter = cylinder({ radius: domeRadius * 0.7, height: 4, segments: 32 });
    const lensInner = cylinder({ radius: domeRadius * 0.5, height: 5, segments: 32 });
    const lens = translate([cx - 5, cy, height * 0.4 + domeRadius * 0.7],
        rotateX(degToRad(90),
            subtract(lensOuter, lensInner)
        )
    );

    // Hover thrusters (3 positioned around base)
    const thrusters = [];
    for (let t = 0; t < 3; t++) {
        const angle = (t / 3) * degToRad(120) + degToRad(30);
        const dist = hexRadius * 0.35;

        const thrusterOuter = cylinder({ radius: 5, height: 6, segments: 16 });
        const thrusterInner = cylinder({ radius: 3.5, height: 7, segments: 16 });
        const thruster = subtract(thrusterOuter, thrusterInner);

        thrusters.push(
            translate([
                cx + Math.cos(angle) * dist * 0.8,
                cy + Math.sin(angle) * dist * 0.5,
                3
            ], thruster)
        );
    }

    // Antenna
    const antennaPost = translate([cx + 10, cy - 5, height * 0.5],
        cylinder({ radius: 0.8, height: height * 0.5, segments: 8 })
    );
    const antennaTip = translate([cx + 10, cy - 5, height * 0.9],
        sphere({ radius: 2.5, segments: 16 })
    );

    // Combine all features
    puppet = union(puppet, hemisphere, lens, ...thrusters, antennaPost, antennaTip);

    // Add clip mechanism
    const clip = createClipMechanism(hexRadius, height, tolerance);
    puppet = union(puppet, clip);

    // Cut magnet slots
    const magnetSlots = createMagnetSlots(hexRadius, height, magnetDiameter, magnetHeight, tolerance);
    puppet = subtract(puppet, magnetSlots);

    return puppet;
};

// ============================================================================
// PUPPET 2: "THE LIFTER" - Industrial robot with articulated arms
// ============================================================================

const createPuppet2 = (hexRadius, height, tolerance, wallThickness, magnetDiameter, magnetHeight) => {
    // Base rhombus
    let puppet = createRhombusBase(hexRadius, height);

    const cx = hexRadius * 0.5 * (1 + Math.cos(degToRad(60)));
    const cy = hexRadius * 0.5 * Math.sin(degToRad(60));

    // Central body housing
    const bodyMain = translate([cx, cy, height * 0.5],
        cuboid({ size: [14, 12, height * 0.5] })
    );

    // Rounded top
    const bodyTop = translate([cx, cy, height * 0.7],
        hull(
            cuboid({ size: [14, 12, 2] }),
            translate([0, 0, 4], cuboid({ size: [10, 8, 2] }))
        )
    );

    // Articulated arms (both sides)
    const arms = [];
    const armLength = 18;

    for (let side = -1; side <= 1; side += 2) {
        // Shoulder joint
        const shoulder = translate([cx + side * 10, cy, height * 0.65],
            sphere({ radius: 4, segments: 16 })
        );

        // Upper arm
        const upperArm = translate([cx + side * 14, cy, height * 0.7],
            rotateY(degToRad(side * 20),
                hull(
                    sphere({ radius: 3, segments: 12 }),
                    translate([side * 8, 0, 6], sphere({ radius: 2.5, segments: 12 }))
                )
            )
        );

        // Elbow joint
        const elbow = translate([cx + side * 18, cy, height * 0.85],
            sphere({ radius: 3, segments: 16 })
        );

        // Lower arm / forearm
        const forearm = translate([cx + side * 20, cy, height * 0.95],
            rotateY(degToRad(side * 35),
                hull(
                    sphere({ radius: 2.5, segments: 12 }),
                    translate([side * 6, 0, 4], sphere({ radius: 2, segments: 12 }))
                )
            )
        );

        // Gripper fingers
        const finger1 = translate([cx + side * 24, cy - 2.5, height * 1.1],
            rotateY(degToRad(side * 45),
                cuboid({ size: [2, 1.5, 6] })
            )
        );
        const finger2 = translate([cx + side * 24, cy + 2.5, height * 1.1],
            rotateY(degToRad(side * 45),
                cuboid({ size: [2, 1.5, 6] })
            )
        );

        arms.push(shoulder, upperArm, elbow, forearm, finger1, finger2);
    }

    // Utility pack on top
    const utilityPack = translate([cx, cy, height * 0.85],
        cuboid({ size: [10, 8, 5] })
    );

    // Combine features
    puppet = union(puppet, bodyMain, bodyTop, ...arms, utilityPack);

    // Add clip mechanism
    const clip = createClipMechanism(hexRadius, height, tolerance);
    puppet = union(puppet, clip);

    // Cut magnet slots
    const magnetSlots = createMagnetSlots(hexRadius, height, magnetDiameter, magnetHeight, tolerance);
    puppet = subtract(puppet, magnetSlots);

    return puppet;
};

// ============================================================================
// PUPPET 3: "THE SWARM MIND" - Multi-sensor array with data tendrils
// ============================================================================

const createPuppet3 = (hexRadius, height, tolerance, wallThickness, magnetDiameter, magnetHeight) => {
    // Base rhombus
    let puppet = createRhombusBase(hexRadius, height);

    const cx = hexRadius * 0.5 * (1 + Math.cos(degToRad(60)));
    const cy = hexRadius * 0.5 * Math.sin(degToRad(60));

    // Main head structure (dodecahedron-like)
    // Approximate with hulled spheres
    const headCore = translate([cx, cy, height * 0.6],
        sphere({ radius: 8, segments: 6 }) // Low segments for faceted look
    );

    // Outer shell
    const headShell = translate([cx, cy, height * 0.6],
        subtract(
            sphere({ radius: 11, segments: 8 }),
            sphere({ radius: 9, segments: 8 })
        )
    );

    // Sensor array - multiple small sensor pods
    const sensors = [];
    const sensorCount = 8;

    for (let s = 0; s < sensorCount; s++) {
        const phi = Math.acos(-1 + (2 * s + 1) / sensorCount);
        const theta = Math.sqrt(sensorCount * Math.PI) * phi;

        const sensorRadius = 13;
        const sx = cx + sensorRadius * Math.cos(theta) * Math.sin(phi);
        const sy = cy + sensorRadius * Math.sin(theta) * Math.sin(phi) * 0.8;
        const sz = height * 0.6 + sensorRadius * Math.cos(phi) * 0.5;

        // Only add sensors above the base
        if (sz > height * 0.3) {
            const sensorPod = translate([sx, sy, sz],
                hull(
                    sphere({ radius: 2, segments: 8 }),
                    translate([
                        (sx - cx) * 0.2,
                        (sy - cy) * 0.2,
                        (sz - height * 0.6) * 0.3
                    ], sphere({ radius: 1.2, segments: 8 }))
                )
            );
            sensors.push(sensorPod);
        }
    }

    // Central processing core (inner glowing element)
    const core = translate([cx, cy, height * 0.6],
        sphere({ radius: 5, segments: 16 })
    );

    // Data tendrils - organic cable-like structures
    const tendrils = [];
    for (let d = 0; d < 4; d++) {
        const angle = d * degToRad(90) + degToRad(45);

        // Create tendril using hulled chain of spheres
        const tendrilPath = [];
        for (let t = 0; t < 4; t++) {
            const progress = t / 3;
            const spread = progress * 15;
            const drop = progress * progress * (height * 0.4);

            tendrilPath.push(
                translate([
                    cx + Math.cos(angle) * spread,
                    cy + Math.sin(angle) * spread * 0.6,
                    height * 0.4 - drop
                ], sphere({ radius: 1.5 - progress * 0.5, segments: 8 }))
            );
        }

        if (tendrilPath.length > 1) {
            tendrils.push(hullChain(tendrilPath));
        }
    }

    // Combine features
    puppet = union(puppet, headCore, headShell, core, ...sensors, ...tendrils);

    // Add clip mechanism
    const clip = createClipMechanism(hexRadius, height, tolerance);
    puppet = union(puppet, clip);

    // Cut magnet slots
    const magnetSlots = createMagnetSlots(hexRadius, height, magnetDiameter, magnetHeight, tolerance);
    puppet = subtract(puppet, magnetSlots);

    return puppet;
};

// ============================================================================
// EXPORTS
// ============================================================================

module.exports = { main, getParameterDefinitions };
