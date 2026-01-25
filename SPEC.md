Please make some choices and start designing this system and design for these interlocking puppets. I want to be able to render and see different versions in a webgl based system to share with others but also a legit cade file setup



APPENDIX
Computational Design Architectures for Tripartite Modular Robotic Puppetry: From Algorithmic Geometry to Additive Manufacturing
The development of a modular robotic system comprised of three distinct floating puppets that coalesce into a geometrically perfect hexagon represents a multidisciplinary challenge at the intersection of computational geometry, mechatronics, and additive manufacturing. This objective requires the synthesis of aesthetic character design with rigorous mechanical constraints, specifically focusing on 120-degree rotational symmetry and high-precision interlocking interfaces.1 For a novice designer, the path from conceptualization to a physical, 3D-printed artifact is mediated by a series of software kernels, geometric algorithms, and manufacturing workflows that must be integrated into a cohesive "toolbench" or development environment.4
The Mathematical Foundation of Hexagonal Dissection and Symmetry
The core design constraint involves partitioning a regular hexagon into three congruent figures that maintain individual visual interest while facilitating a perfect combined form. In Euclidean geometry, a regular hexagon is defined by six equal sides and internal angles of 120 degrees. The most efficient and aesthetically balanced method for tripartite division is the rhombic dissection.1 By drawing line segments from the center of the hexagon to every second vertex, the hexagon is divided into three identical rhombi, each possessing internal angles of 60 degrees and 120 degrees.2
This geometric footprint serves as the bounding volume for each of the three puppets. To ensure that the individual puppets have a fun and interesting form, the designer must move beyond the basic rhombus and utilize the available 3D space within that rhombus's extrusion. The total area $A$ of the final hexagonal assembly, given a side length $s$, is defined by the formula:

$$A = \frac{3\sqrt{3}}{2}s^2$$
Consequently, each puppet must occupy an average area of:

$$A_{puppet} = \frac{\sqrt{3}}{2}s^2$$
The puppets are designated as "floating," a term that in robotic puppetry implies a lack of traditional terrestrial locomotion, such as legs or wheels. Instead, these forms often utilize biomimetic or industrial aesthetics, such as thruster housings, simulated rotors, or articulated appendages that suggest movement in a three-dimensional fluid or zero-gravity environment.7 The "clip together in the back" requirement suggests a common central axis where all three puppets interface, requiring a high degree of precision in the design of the rear-facing coupling mechanisms.3
Symmetry and Orientation in Modular Design
The assembly relies on $C_3$ rotational symmetry, where the system is invariant under rotations of $2\pi/3$ radians (120 degrees).2 In a computational modeling environment, this symmetry allows the designer to develop one "Master Puppet" and replicate it twice through 120-degree and 240-degree rotations about the central Z-axis to verify the hexagonal fit.11

Geometric Parameter
Value for Regular Hexagon
Implications for Puppet Design
Interior Angle
120 degrees 2
Defines the corner angles of the outer hexagon shell.
Central Angle
60 degrees 1
Determines the wedge angle for a six-part split.
Tripartite Split Angle
120 degrees 2
The fundamental angle for rotating each puppet module.
Number of Vertices
6 2
Provides the anchor points for the hexagonal vertices.
Internal Partition
3 Rhombi 2
Provides the primary structural footprint for each puppet.

Comparative Analysis of Computational Design Kernels
For a user interested in building a web-based toolbench, the selection of a 3D modeling kernel is the most consequential decision. Traditional "point-and-click" CAD software lacks the iterative power of "Code-to-CAD" systems, which allow for parametric adjustments to be propagated throughout the assembly instantly.4
CSG vs. B-Rep Kernels
The two primary paradigms in computational geometry are Constructive Solid Geometry (CSG) and Boundary Representation (B-Rep). CSG defines objects through Boolean operations (union, subtraction, intersection) on simple primitives like cubes and spheres.5 B-Rep defines objects by their boundaries—surfaces, edges, and vertices—allowing for more complex operations like fillets, sweeps, and revolves.5

Library
Paradigm
Pros
Cons
Manifold 3D
CSG (High Speed)
Extreme performance, guaranteed manifold output.5
Limited advanced surfacing like complex fillets.5
JSCAD
CSG (Web Native)
Easy to learn, JavaScript-based, massive ecosystem.5
Performance can lag with high-resolution meshes.5
CascadeStudio
B-Rep (NURBS)
Engineering precision, exports STEP files, advanced fillets.5
Steeper learning curve, higher computational overhead.5
OpenSCAD
CSG (Classic)
Most popular, huge community, many libraries.4
Uses a custom language, lacks modern web integration.5

For a floating robotic puppet project, Manifold 3D is arguably the most suitable for the core geometry because it is optimized for WebAssembly (WASM), allowing for near-instantaneous updates in a web browser.6 Its "guaranteed manifold" property ensures that the generated models will always be 3D printable, which is a critical safety net for a beginner who might accidentally create "non-manifold" geometry that a 3D printer cannot interpret.6
The Role of WebAssembly (WASM) in Web-Based CAD
Browser-based CAD tools traditionally suffered from the performance bottlenecks of interpreted JavaScript, which struggled with the heavy geometric calculations required for Boolean operations.16 The advent of WebAssembly enables near-native execution of C++ kernels like Manifold or OpenCascade (used in CascadeStudio) directly in the browser.16 This allows the "toolbench" to offer a "Live Preview" experience, where the 3D form of the puppet updates in real-time as the user modifies parameters like arm length, thruster size, or clip tolerance.13
Constructing the Toolbench: Architecture and Integration
An effective toolbench for this project must integrate a geometric kernel, a visualization engine, and an export pipeline. This setup allows the user to iterate on the "interesting forms" of the puppets while maintaining the strict "hexagonal" fit.
Visualization via Three.js and WebGL
While the geometric kernel (like Manifold 3D) handles the "math" of the shapes, Three.js is required to render those shapes on the screen via WebGL.20 Three.js manages the camera, lighting, and materials that give the robotic puppets their "distinctive look".18 The process involves converting the mesh data from the CAD library into a format Three.js can understand, such as BufferGeometry.18
The visualization environment should include:
A Lighting Rig: Standard studio lighting (e.g., an ambient light and a directional light) to highlight the robotic textures and shadows.21
A Perspective Camera: To allow the user to orbit around the puppets and inspect the clip interfaces.21
Material Shaders: Using MeshStandardMaterial to simulate metallic or plastic surfaces, which is appropriate for a robotic aesthetic.21
The Export Pipeline for CAD and 3D Printing
To bridge the gap between web-based modeling and physical manufacturing, the toolbench must export files that can be read by CAD software and 3D printer "slicers."
STL (Stereolithography): The industry standard for 3D printing. It represents the surface of the puppet as a collection of triangles.23 Three.js provides an STLExporter that can generate these files directly from the browser.24
3MF (3D Manufacturing Format): A more modern alternative to STL that is more reliable for complex assemblies and can store material information.5
STEP (Standard for the Exchange of Product Model Data): Necessary if the user wishes to open the models in professional engineering software like Fusion 360 or SolidWorks.27 CascadeStudio is the primary web library capable of generating true STEP files.13

Feature
STL
STEP
Primary Use
3D Printing 23
Professional Engineering/CAD 28
Geometry Representation
Triangulated Mesh 23
Precise Mathematical Curves (NURBS) 29
Editability
Very low (difficult to modify) 29
High (can modify dimensions/radii) 28
File Size
Large for high detail 23
Compact and efficient 29

Conceptual Character Design for Robotic Puppetry
A "distinctive look" for three floating puppets requires a strategy that balances variety with structural unity. The designer can use "Procedural Generation" to create unique features while keeping the "back" of the puppet constant for the hexagonal connection.3
Structural Elements of Floating Robots
Robotic puppets often utilize a "central chassis" from which functional modules radiate.31
Appendages and Limbs: For a robotic look, limbs can be designed with articulated "ball and socket" joints or "hinge" joints.34 Modularity can be achieved by using standardized sockets, allowing the designer to swap different arms or sensors between the three puppets.32
Thrusters and Hover Modules: Since the puppets are "floating," the base of each rhombus could feature simulated ion engines, fans, or anti-gravity pads.7
Sensor Clusters: Distinctive looks can be achieved by giving each puppet a different "head" or "sensor array"—for example, one could have a large cyclopean lens, while another has a cluster of insect-like cameras.36
Procedural Modeling for Infinite Variation
The power of a toolbench lies in its ability to generate "interesting forms" algorithmically. By using mathematical functions like noise (Perlin or Simplex), a designer can deform a basic rhombus into an organic, "fun" robotic shape.12
The Hull Function: In libraries like JSCAD, the hull() function can create a smooth skin over a set of points or shapes, resulting in a streamlined, "sci-fi" appearance.14
Boolean Patterning: A robotic look is often defined by "greebles"—small, complex mechanical details added to a surface. In a code-to-CAD system, these can be generated using nested loops that subtract small cubes or cylinders from the main chassis.12
Engineering the Interlocking Hexagonal Interface
The requirement that the three puppets "clip together in the back" to form a hexagon is a problem of mechanical tolerances and joint design.3 Because 3D printers have inherent inaccuracies, a design that is mathematically perfect on screen may not fit together in reality.3
Snap-Fit Mechanisms
Snap-fits use the elasticity of plastic to create a temporary or permanent connection.42
Cantilever Snaps: A flexible arm with a hook that deflects during assembly and "snaps" back into a recess.43 For a robotic puppet, these could be integrated into the rear "spine" of the chassis.44
Annular Snap-Fits: Circular joints that use hoop strain, often found in bottle caps. These could be used for "floating" modules that need to rotate while remaining attached.41
Material Selection: PLA is commonly used by beginners, but PETG or Nylon offers better flexibility for snap-fits, preventing the clips from breaking after repeated use.41
Magnetic Coupling Systems
For a "floating" feel, magnetic connectors are superior to mechanical clips. They allow the puppets to "snap" together effortlessly and provide a satisfying tactile experience.32
Self-Alignment: By carefully orienting the poles of neodymium magnets, the three puppets can be designed to self-align into the hexagon shape.32
Embedding Magnets: The most advanced technique involves pausing the 3D printer mid-process, dropping a magnet into a pre-designed slot, and then printing over it.46 This seals the magnet inside the robotic part, creating a clean, seamless look with no visible hardware.46

Design Parameter
Recommended Tolerance (FDM)
Recommended Tolerance (SLA/SLS)
Press-Fit (Tight)
0.05 mm - 0.1 mm 3
0.02 mm - 0.05 mm 44
Slide-Fit (Loose)
0.2 mm - 0.3 mm 3
0.1 mm - 0.2 mm 10
Magnetic Slot
0.2 mm - 0.4 mm 47
0.1 mm - 0.2 mm 49
Snap-Fit Clearance
0.5 mm 3
0.3 mm 44

The "Master Assembly" Strategy
To ensure a "perfect combined form," the designer should model the hexagon as a single entity first and then "cut" it into three parts using Boolean subtractions.52
Create a Solid Hexagon.
Define a "Cutting Tool" shape—a plane or a zigzag line that creates an interlocking seam.52
Rotate the "Cutting Tool" three times by 120 degrees.11
Subtract the tools from the hexagon to create three perfect pieces.52
Apply a "Tolerance Offset" to the cuts so they have room to slide together after printing.10
Comprehensive Roadmap for the 3D Printing Novice
Starting with zero knowledge of 3D printing requires an understanding of the entire "digital-to-physical" lifecycle. The puppets must not only look good on a screen but also be "printable".55
Step 1: The Design for Manufacturability (DFM)
When designing the robotic puppets, the user must account for the constraints of FDM (Fused Deposition Modeling), the most common type of home 3D printer.3
Overhangs and Supports: Printers cannot print in mid-air. Any part of the puppet that extends out at an angle greater than 45 degrees will need "support material," which must be broken off after printing.23
Bed Adhesion: The bottom of each puppet must have a flat surface to stick to the build plate. For a floating puppet, this might require a temporary "sacrificial" flat base that is removed after printing.3
Layer Orientation: 3D prints are weakest between layers. Clips and joints should be oriented so the stress doesn't pull the layers apart.3
Step 2: Slicing and G-Code Generation
The "Slicer" is the software that translates the 3D model (STL) into instructions for the printer (G-code).23
Popular Slicers: PrusaSlicer and Cura are free, open-source, and beginner-friendly.23
Key Settings:
Infill: The internal structure of the puppet. 15-20% is typical for decorative or lightweight robotic toys.49
Wall Count: Using 3 or 4 perimeters makes the robotic shell much stronger and improves the finish of the interlocking clips.3
Layer Height: 0.2 mm is the standard for speed, while 0.1 mm or 0.15 mm is better for high-detail puppets and tight-fitting joints.41
Step 3: Hardware Integration for "Floating" Effects
To make the puppets appear "robotic" and "floating," the user can integrate electronics and magnetic levitation.
Servo Motors: Small "micro servos" (like the SG90) can be embedded into the puppets to move arms or heads.33
Arduino/Microcontrollers: A small computer can be programmed to trigger movements or lights, giving the puppets a "robotic" life of their own.31
Display Stands: Since the puppets are floating, they can be mounted on thin clear acrylic rods or "levitated" using powerful neodymium magnets in a base.9
Technical Implementation: The Toolbench Starter Code
To help the user start their project, this section outlines the structure of a toolbench script using JSCAD, which is the most accessible for a beginner because it runs entirely in the browser with no installation.5
Anatomy of a Modular Puppet Script
The following structure allows for the iterative design of three puppets with distinctive looks and a shared hexagonal interface.12

JavaScript


// JSCAD Toolbench Template
const { cube, sphere, cylinder, union, subtract, rotateZ, translate } = require('@jscad/modeling').primitives;
const { hull } = require('@jscad/modeling').operations;

function main(params) {
    const hexRadius = 50; // Total size of the hexagon
    const tolerance = 0.2; // The gap for the clip fit

    // Define the three puppets
    const puppet1 = createPuppetA(hexRadius, tolerance);
    const puppet2 = createPuppetB(hexRadius, tolerance);
    const puppet3 = createPuppetC(hexRadius, tolerance);

    // Arrange them in 120-degree symmetry
    return [
        puppet1,
        rotateZ(Math.PI * 2/3, puppet2),
        rotateZ(Math.PI * 4/3, puppet3)
    ];
}

function createPuppetA(radius, tol) {
    // The 'Back' interface - consistent across all puppets
    let backInterface = cube({size: , center: [radius, 0, 0]});
    
    // The 'Fun' unique body
    let body = hull(
        sphere({radius: 15, center: [radius-20, 0, 10]}),
        sphere({radius: 10, center: [radius-30, 15, -10]})
    );

    return union(body, backInterface);
}
// Repeat createPuppetB and createPuppetC with different body shapes...


This code snippet represents the "logic" of the toolbench. By editing the createPuppet functions, the user can experiment with different "floating" robotic forms while the main function ensures they are always positioned for a hexagonal assembly.11
Advanced Learning Path: Improving Computational Design Skills
For a user who "knows nothing about 3D design," the transition to an expert-level project involves mastering specific domain competencies.55
Level 1: Geometric Primitives and Booleans
The user should begin by learning how to add and subtract basic shapes. Mastering the "Boolean Difference" is essential for creating the slots where magnets or clips will reside.12
Level 2: Parametric Scripting
Instead of using fixed numbers (e.g., "10mm"), the user should use variables (e.g., puppet_height = 50). This allows for global changes—such as resizing the entire hexagonal assembly—by changing a single line of code.14
Level 3: Physics-Aware Design
Learning to design for 3D printing involves understanding how plastic behaves. This includes "chamfering" edges to prevent the "elephant's foot" (where the bottom layer squishes out) and using "fillets" to reduce stress concentrations in robotic joints.3
Level 4: Assembly Simulation in WebGL
The toolbench should eventually include "Kinematics," allowing the user to click and drag the robotic limbs in the WebGL preview to see how they move before printing.28 This is particularly useful for puppets, where the "range of motion" is a key part of the "fun".33
Analysis of Emerging Trends in Modular Robotics
The concept of hexagonal modular robots is currently a subject of active research. For example, the HEXEL system developed by the Max Planck Institute uses hexagonal modules that snap together and use artificial muscles to change shape.9 These modules can jump, crawl, and roll, demonstrating the versatility of the hexagonal form factor in modular robotics.9
Furthermore, the "ModBots" project on platforms like Thangs demonstrates a community-driven approach to modular robot figures with "magnet-ready joints," allowing users to swap parts between different robot series.32 This "Toy System" approach aligns perfectly with the user's desire for three distinctive puppets that can interlock.

Robotic Platform
Primary Locomotion
Modularity Method
Application
HEXEL
Electrohydraulic Muscles 9
Magnetic Snap-On 9
Reconfigurable Research 66
InMoov
Servos and Cables 38
3D Printed Joints 38
Open-Source Humanoid 38
ModBots
Static/Articulated 32
5x2mm Magnets 32
Collectible/Modular Toy 32
Poppy
Dynamixel Actuators 38
Modular Shells 38
AI and Interaction Research 38

Conclusion and Actionable Recommendations
To successfully launch this project, the user should build their development environment on a foundation of high-performance web kernels and standardized hardware. The tripartite hexagonal assembly is a rigorous geometric problem that is best solved through procedural, code-based modeling rather than manual sculpting.1
The following steps provide a strategic path for the project:
Software Selection: Utilize JSCAD for the initial toolbench prototype due to its ease of use for beginners, or Manifold 3D if high-speed live iteration is the priority.5
Geometry Strategy: Define a master hexagon and partition it into three rhombi using 120-degree rotational symmetry. Use the hull() function to generate "distinctive looks" for each puppet within its rhombic boundaries.2
Mechanical Coupling: Design for Neodymium Magnets (5x2mm or 6x3mm). This avoids the high-precision fatigue issues of plastic snap-fits and provides the most "robotic" and "floating" assembly experience.32
Manufacturing Tuning: Account for a 0.2 mm to 0.4 mm tolerance in all interlocking parts to ensure they fit together regardless of minor 3D printing errors.3
Iteration Cycle: Use the WebGL toolbench to visualize the "Hexagon Form" and the "Individual Form" side-by-side. Export small "test clips" for 3D printing before committing to the full puppet prints.3
By following this architecture, the user can create a professional-grade set of modular robotic puppets that are both aesthetically compelling and mechanically sound, even without prior experience in 3D design or additive manufacturing.55
Works cited
How to draw 3 equal circles inside a hexagon touching two sides and two other circles - TD, accessed January 15, 2026, https://www.youtube.com/watch?v=Lbn5fmnigIQ
Geometry POW Solution, October 11 (part 3) - Google Groups, accessed January 15, 2026, https://groups.google.com/g/geometry.pre-college/c/E5Bg3chQbFc
How to 3D Print Interlocking Parts and Assemblies - QIDI Tech, accessed January 15, 2026, https://qidi3d.com/blogs/news/how-to-3d-print-interlocking-parts-and-assemblies
OpenSCAD - The Programmers Solid 3D CAD Modeller, accessed January 15, 2026, https://openscad.org/
Irev-Dev/curated-code-cad - GitHub, accessed January 15, 2026, https://github.com/Irev-Dev/curated-code-cad
manifold-3d - NPM, accessed January 15, 2026, https://www.npmjs.com/package/manifold-3d
Pro mode example puppets - Adobe Illustrator, accessed January 15, 2026, https://pages.adobe.com/character/en/puppets
3D printable octopus-inspired tentacle robots : r/Damnthatsinteresting - Reddit, accessed January 15, 2026, https://www.reddit.com/r/Damnthatsinteresting/comments/1iauqa5/3d_printable_octopusinspired_tentacle_robots/
Hexagonal Electrohydraulic Modules Shape-Shift into Versatile Robots - Tech Briefs, accessed January 15, 2026, https://www.techbriefs.com/component/content/article/51905-hexagonal-electrohydraulic-modules-shape-shift-into-versatile-robots
How to 3D Print Interlocking Parts and Assemblies - Formlabs, accessed January 15, 2026, https://formlabs.com/blog/how-to-3d-print-interlocking-joints/
How to visualize a $120^\circ$ (or $240^\circ$) rotation of a cube about its body diagonal? - Mathematics Stack Exchange, accessed January 15, 2026, https://math.stackexchange.com/questions/1736129/how-to-visualize-a-120-circ-or-240-circ-rotation-of-a-cube-about-its-bod
Make 3D Printable Models with JavaScript | Inspired To Educate, accessed January 15, 2026, http://inspiredtoeducate.net/inspiredtoeducate/make-3d-printable-models-with-javascript/
CascadeStudio | Open CASCADE Technology, accessed January 15, 2026, https://dev.opencascade.org/project/cascadestudio
JSCAD - JavaScript CAD, accessed January 15, 2026, https://openjscad.xyz/
en:jscad_design_guide [JSCAD V2 User Guide], accessed January 15, 2026, https://openjscad.xyz/dokuwiki/doku.php?id=en:jscad_design_guide
WebAssembly for CAD Applications: When JavaScript Isn't Fast Enough - AlterSquare, accessed January 15, 2026, https://altersquare.medium.com/webassembly-for-cad-applications-when-javascript-isnt-fast-enough-56fcdc892004
Hyper Links And Hyperfunctional Text CAD - Hackaday, accessed January 15, 2026, https://hackaday.com/2020/09/30/hyper-links-and-hyperfunctional-text-cad/
Manifold Examples - ManifoldCAD, accessed January 15, 2026, https://manifoldcad.org/jsdocs/documents/Manifold_Examples.html
weianweigan/manifold-csharp: Geometry library for topological robustness - GitHub, accessed January 15, 2026, https://github.com/weianweigan/manifold-csharp
How to Use WebGL for 3D Printing Previews on the Web - PixelFreeStudio Blog, accessed January 15, 2026, https://blog.pixelfreestudio.com/how-to-use-webgl-for-3d-printing-previews-on-the-web/
How to Load 3D Models in WebGL? - GeeksforGeeks, accessed January 15, 2026, https://www.geeksforgeeks.org/javascript/how-to-load-3d-models-in-webgl/
Export a three.js scene to STL / Fil - Observable, accessed January 15, 2026, https://observablehq.com/@fil/export-a-three-js-scene-to-stl
CAD to 3D Print: Software, File Export & Workflow Guide - JLC3DP, accessed January 15, 2026, https://jlc3dp.com/blog/cad-to-3d-print
STLExporter – three.js docs, accessed January 15, 2026, https://threejs.org/docs/pages/STLExporter.html
How to Use Three.js STL Exporter: A Step-by-Step Guide - Modelo, accessed January 15, 2026, https://www.modelo.io/damf/article/2024/08/03/2007/how-to-use-three.js-stl-exporter--a-step-by-step-guide
How to convert Three.js to .stl files for 3D printing? - Stack Overflow, accessed January 15, 2026, https://stackoverflow.com/questions/48072408/how-to-convert-three-js-to-stl-files-for-3d-printing
How to export STEP/STP files from AutoCAD and AutoCAD Toolsets - Autodesk, accessed January 15, 2026, https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/How-to-export-STEP-STP-files-from-AutoCAD-and-AutoCAD-Toolsets.html
STEP Files Simplified: Open, Convert & Edit | 3D Cloud, accessed January 15, 2026, https://3dcloud.com/step-files/
3D STEP File Compatible: For supports export and import file - Formlabs Forum, accessed January 15, 2026, https://forum.formlabs.com/t/3d-step-file-compatible-for-supports-export-and-import-file/14332
Design for interlocking parts | Endeavor 3D, accessed January 15, 2026, https://endeavor3d.com/wp-content/uploads/2024/12/Design-for-Interlocking-Parts-Inovative-Designs.pdf
ROBOPuppet: Low-Cost, 3D Printed Miniatures for Teleoperating Full-Size Robots - Intelligent Motion Lab, accessed January 15, 2026, https://motion.cs.illinois.edu/papers/IROS2014-RoboPuppet.pdf
Been designing a series of modular robot figures you can print and snap together with magnets — here's the heavy lifter, Torque : r/3Dprinting - Reddit, accessed January 15, 2026, https://www.reddit.com/r/3Dprinting/comments/1ms7p8x/been_designing_a_series_of_modular_robot_figures/
Ultron 3D Printed Puppet Concept : 3 Steps - Instructables, accessed January 15, 2026, https://www.instructables.com/Ultron-3D-printed-puppet-concept/
How to Create Articulating Joints in Flexible 3D Printed Toys! - YouTube, accessed January 15, 2026, https://www.youtube.com/watch?v=-6M8x-yEO2Q
"articulated puppet" 3D Models to Print - Yeggi, accessed January 15, 2026, https://www.yeggi.com/q/articulated+puppet/
12 Cool 3D Printed Robot Models to Build at Home - Gambody, accessed January 15, 2026, https://www.gambody.com/blog/3d-printed-robot/
"robot character" 3D Models to Print - Yeggi, accessed January 15, 2026, https://www.yeggi.com/q/robot+character/
15 Best 3D Printed Robots Projects - An Ultimate Guide! - Creality Store, accessed January 15, 2026, https://store.creality.com/blogs/basics/3d-printed-robot
JSCAD — JavaScript CAD in your browser - Prusa3D Forum, accessed January 15, 2026, https://forum.prusa3d.com/forum/english-forum-general-discussion-announcements-and-releases/jscad-javascript-cad-in-your-browser/
First time all the way from CAD design to 3D print attempt. - Reddit, accessed January 15, 2026, https://www.reddit.com/r/BambuLab_Community/comments/196h7ha/first_time_all_the_way_from_cad_design_to_3d/
How to Design and 3D Print Snap-Fit Joints for Enclosures, Boxes, Lids, and More, accessed January 15, 2026, https://formlabs.com/blog/designing-3d-printed-snap-fit-enclosures/
3D Printed Joinery: Simplifying Assembly - Markforged, accessed January 15, 2026, https://markforged.com/resources/blog/joinery-onyx
Guide to 3D Printed Snap Fits +[Design Tips] - Unionfab, accessed January 15, 2026, https://www.unionfab.com/blog/2025/06/3d-print-snap-fit
How do you design snap-fit joints for 3D printing? - Protolabs Network, accessed January 15, 2026, https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing/
How to design interlocking joints for fastening 3D printed parts - Protolabs Network, accessed January 15, 2026, https://www.hubs.com/knowledge-base/how-design-interlocking-joints-fastening-3d-printed-parts/
How to use magnets in 3D printed models - SOVOL, accessed January 15, 2026, https://www.sovol3d.com/blogs/news/how-to-use-magnets-in-3d-printed-models
Magnets for 3d printing, how to Embed Magnets into 3D Prints - Kingroon, accessed January 15, 2026, https://kingroon.com/blogs/3d-printing-guides/how-to-embed-magnets-into-3d-prints
Embed Magnets into 3D Prints - YouTube, accessed January 15, 2026, https://www.youtube.com/shorts/2miPeY4Qsd4
Creative 3D Printing Ideas: Embedding Magnets for Fun and Function - Creality Store, accessed January 15, 2026, https://store.creality.com/blogs/all/magnets-in-3d-printing
How to Make Your 3D Printed Projects Magnetic - Instructables, accessed January 15, 2026, https://www.instructables.com/How-to-Make-Your-3D-Printed-Projects-Magnetic/
3D Printed Puzzles: 35 Mind-Boggling STL Files - All3DP, accessed January 15, 2026, https://all3dp.com/2/3d-printed-puzzle-stl/
Designing and Printing Interlocking Parts - First time - advice, please? - Prusa3D Forum, accessed January 15, 2026, https://forum.prusa3d.com/forum/english-forum-general-discussion-announcements-and-releases/designing-and-printing-interlocking-parts-first-time-advice-please/
Break a model into parts for 3d printing - SketchUp Forums, accessed January 15, 2026, https://forums.sketchup.com/t/break-a-model-into-parts-for-3d-printing/38251
How to split a body into parts that can interlock with each other? : r/Fusion360 - Reddit, accessed January 15, 2026, https://www.reddit.com/r/Fusion360/comments/1iv27i8/how_to_split_a_body_into_parts_that_can_interlock/
Beginner's Guide to 3D Printing Software - PAACADEMY.com, accessed January 15, 2026, https://paacademy.com/blog/beginners-guide-to-3d-printing-software
Beginners Guide to CAD Design for 3D Printing with Fusion 360 | Learn, accessed January 15, 2026, https://www.learneverythingaboutdesign.com/p/cad-design-for-3d-printing-with-fusion-360
3d Modeling Roadmap - A Complete Guide - GeeksforGeeks, accessed January 15, 2026, https://www.geeksforgeeks.org/blogs/3d-modeling-roadmap/
How to make pieces that snap together? : r/3Dprinting - Reddit, accessed January 15, 2026, https://www.reddit.com/r/3Dprinting/comments/1jjkzuv/how_to_make_pieces_that_snap_together/
Slic3r - Open source 3D printing toolbox, accessed January 15, 2026, https://slic3r.org/
Hexagon Logic Puzzle - Free 3D Print Model - MakerWorld, accessed January 15, 2026, https://makerworld.com/en/models/633351-hexagon-logic-puzzle
Magnetic Ball and Socket Joint Robot - 3D Printing, Servos, Arduino and Magnets! Version 6, accessed January 15, 2026, https://www.youtube.com/watch?v=woVBqcJtyD0
Hexglyph Print-in-place Puzzle Box by 3d-printy - Thingiverse, accessed January 15, 2026, https://www.thingiverse.com/thing:6579685
Build a 3D Printed Rotational Platform : 7 Steps - Instructables, accessed January 15, 2026, https://www.instructables.com/Build-a-3D-Printed-Rotational-Platform/
JSCAD experiments - Applied JavaScript - Frido Verweij, accessed January 15, 2026, https://library.fridoverweij.com/codelab/JSCAD/
OpenJSCAD User Guide - Wikibooks, open books for an open world, accessed January 15, 2026, https://en.wikibooks.org/wiki/OpenJSCAD_User_Guide
This robot system is made of modular hexagons - YouTube, accessed January 15, 2026, https://www.youtube.com/shorts/KW10BGG0h_Y


