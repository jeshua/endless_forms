# Geometry Specification for Form Shards

## Core Principle

When the three shards merge together, they must form a **perfect geometric shape** (triangle or hexagon). The unique character of each shard comes from their **inner edges**, not their outer edges.

## Edge Types

Each shard has two types of edges:

### 1. OUTER EDGE (Perimeter Edge)
- Forms part of the final shape's perimeter
- **MUST be a straight line** following the triangle/hexagon boundary
- When all shards merge, these edges combine to create the perfect outline

### 2. INNER EDGES (Radial Edges)
- Connect from the center to the vertices
- **CAN have interesting shapes**: curves, notches, protrusions, waves
- These edges are shared between neighboring shards
- When merged, inner edges overlap and interlock, hidden from view

## Triangle Mode Geometry

```
                    TOP VERTEX
                        /\
                       /  \
                      /    \
            Inner    /  A   \    Inner
            Edge 1  /        \   Edge 2
                   /    *     \
                  /   center   \
                 /              \
                /   B       C    \
               /                  \
              /____________________\
        BOTTOM-LEFT            BOTTOM-RIGHT
              VERTEX              VERTEX

        <-------- OUTER EDGES -------->
```

### Shard Assignment (Triangle)
- **Shard A**: Top wedge
  - Outer edge: TOP → BOTTOM-LEFT (straight line along triangle perimeter)
  - Inner edges: CENTER → TOP, CENTER → BOTTOM-LEFT (can be shaped)

- **Shard B**: Bottom-left wedge
  - Outer edge: BOTTOM-LEFT → BOTTOM-RIGHT (straight line along bottom)
  - Inner edges: CENTER → BOTTOM-LEFT, CENTER → BOTTOM-RIGHT (can be shaped)

- **Shard C**: Bottom-right wedge
  - Outer edge: BOTTOM-RIGHT → TOP (straight line along triangle perimeter)
  - Inner edges: CENTER → BOTTOM-RIGHT, CENTER → TOP (can be shaped)

## Hexagon Mode Geometry

```
              V1
             /  \
           /      \
         V0   A    V2
         |    *    |
         |  center |
         V5   B    V3
           \      /
             \  /
              V4

    Each shard covers 2 edges of the hexagon perimeter
```

### Shard Assignment (Hexagon)
- **Shard A**: Rhombus covering vertices V0, V1, V2
  - Outer edges: V0→V1, V1→V2 (straight lines along hex perimeter)
  - Inner edges: CENTER→V0, CENTER→V2 (can be shaped)

- **Shard B**: Rhombus covering vertices V2, V3, V4
  - Outer edges: V2→V3, V3→V4 (straight lines along hex perimeter)
  - Inner edges: CENTER→V2, CENTER→V4 (can be shaped)

- **Shard C**: Rhombus covering vertices V4, V5, V0
  - Outer edges: V4→V5, V5→V0 (straight lines along hex perimeter)
  - Inner edges: CENTER→V4, CENTER→V0 (can be shaped)

## Inner Edge Design Principles

The inner edges give each shard its unique character:

### Shard A: "The Organic"
- Inner edges have **smooth curves and bulges**
- Rounded, flowing, organic feel
- Uses bezierCurveTo or quadraticCurveTo

### Shard B: "The Mechanical"
- Inner edges have **angular notches and teeth**
- Geometric, precise, industrial feel
- Uses lineTo with sharp angles

### Shard C: "The Hybrid"
- Inner edges have **mixed curves and points**
- Combination of organic and mechanical
- Protrusions that interlock with neighbors

## Overlapping Mechanism

The key insight: inner edges **extend INTO neighboring shard's territory**. When merged, these extensions **tuck behind** the neighboring shard.

### How Overlapping Works

1. Each shard's inner edges have curves/bulges that extend beyond the basic wedge boundary
2. These extensions go INTO the territory that a neighbor shard occupies
3. Shards are layered in Z-order: A (bottom) → B (middle) → C (top)
4. When merged, the neighbor shard covers the extension, hiding it from view

### Layer Order (Triangle)
```
     C (top - covers A and B's extensions)
    / \
   /   \
  A --- B  (A on bottom, B covers A's extension)
```

### Example
- Shard A's right inner edge bulges INTO Shard C's territory
- When merged, Shard C sits ON TOP of that bulge, covering it
- Result: You only see C's edge, not A's extension underneath

## Visual Result

**Apart**: Each shard displays its unique curved silhouette - you can see the extensions that would normally be hidden

**Merged**: Perfect triangle/hexagon outline with smooth layered interior - extensions are tucked beneath neighboring shards

---

## Triangle Division Styles

The triangle doesn't have to be divided into equal thirds. Here are 5 different division styles:

### Style 1: Classic Thirds
```
        *
       /|\
      / | \
     /  |  \
    / A | C \
   /    *    \
  /   / B \   \
 /___/______\__\
```
- 3 equal wedges from center
- Each robot owns exactly 1 side of the triangle
- Symmetrical, balanced

### Style 2: Big Boss
```
        *
       / \
      / A \________
     /      \  B  |
    /        \____|
   /    A      \C/
  /______________\/
```
- Robot A: Large L-shaped piece, owns 2 sides
- Robot B: Small corner piece
- Robot C: Small corner piece
- Creates hierarchy - one dominant robot

### Style 3: Horizontal Layers
```
        *
       /_\      <- A (apex)
      /___\     <- B (middle band)
     /_____\
    /_______\   <- C (base)
```
- Robot A: Small triangle at apex
- Robot B: Trapezoid band in middle
- Robot C: Wide trapezoid at base
- Each touches 2 edges of the perimeter

### Style 4: Corner Huggers
```
        *
       /|\
      / | \
     /A | C\
    /___|___\
       B
```
- Each robot owns one corner
- They meet with overlapping curves in the center
- Each owns portions of 2 edges meeting at their corner

### Style 5: Spiral/Unequal
```
        *
       /|\
      / | \
     /  |C \
    / A |   \
   /    |    \
  /_____|_____\
      B (wide base)
```
- Wedges from center with UNEQUAL angles
- A: Thin sliver, B: Wide base, C: Medium
- Creates dynamic asymmetry
