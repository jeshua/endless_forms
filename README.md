# Hexagonal Modular Puppet Toolbench

A WebGL-based design system for three floating robotic puppets that clip together to form a geometrically perfect hexagon. Each puppet occupies a rhombic footprint (1/3 of the hexagon) and features unique robotic aesthetics.

## Quick Start

### WebGL Viewer (Share with Others)

1. Start a local server:
   ```bash
   npx serve .
   # or
   npm start
   ```

2. Open `http://localhost:3000` in your browser

3. Use the controls to:
   - Adjust hexagon size, puppet height, and tolerances
   - Toggle between assembled and exploded views
   - Change puppet colors and styles
   - Export STL files for 3D printing

### JSCAD CAD System (Proper CAD Files)

For full parametric CAD capabilities:

1. Go to [https://openjscad.xyz/](https://openjscad.xyz/)
2. Click "File" > "Open" and select `puppets.jscad.js`
3. Use the parameter sliders to customize
4. Export as STL, DXF, or other formats

## The Three Puppets

### Puppet 1: "The Scout"
- Cyclopean sensor dome with lens ring
- Three hover thrusters at base
- Communication antenna

### Puppet 2: "The Lifter"
- Industrial central body housing
- Dual articulated arms with grippers
- Utility pack on top

### Puppet 3: "The Swarm Mind"
- Multi-sensor array head (dodecahedral)
- Distributed sensor pods
- Data tendrils for organic look

## Hexagonal Assembly

The puppets use **C3 rotational symmetry** (120-degree rotations):
- Each puppet is rotated 0°, 120°, or 240° from center
- Central clip mechanism provides mechanical connection
- Magnet slots (5x2mm) for magnetic coupling

## 3D Printing Guide

### Recommended Settings (FDM)
- **Layer Height**: 0.15-0.2mm
- **Infill**: 15-20%
- **Wall Count**: 3-4 perimeters
- **Supports**: Yes, for overhangs >45°

### Tolerances
- **Clip fit**: 0.2mm (adjustable in UI)
- **Magnet slots**: 0.2-0.4mm clearance
- **Material**: PETG recommended for clip durability

### Magnet Installation
1. Print with pause at magnet layer height
2. Insert 5x2mm neodymium magnets
3. Resume print to seal magnets inside

## File Structure

```
endless_forms/
├── index.html          # WebGL viewer (Three.js)
├── puppets.jscad.js    # JSCAD parametric model
├── package.json        # npm configuration
└── README.md           # This file
```

## Technical Details

### Geometry
- Regular hexagon partitioned into 3 congruent rhombi
- Each rhombus: 60° and 120° internal angles
- Hexagon area: A = (3√3/2)s² where s = side length
- Each puppet area: A_puppet = (√3/2)s²

### Export Formats
| Format | Use Case |
|--------|----------|
| STL | 3D printing (universal) |
| 3MF | 3D printing (modern, preserves color) |
| STEP | Professional CAD software |
| DXF | 2D laser cutting |

## Dependencies

The WebGL viewer uses:
- Three.js (loaded via CDN)
- OrbitControls for camera manipulation
- STLExporter for file export

The JSCAD model uses:
- @jscad/modeling (loaded by openjscad.xyz)
