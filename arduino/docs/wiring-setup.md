# Puppet LED Project - Wiring Setup

## Quick Reference: What Connects Where

### Complete Power Flow:
```
BATTERY + → 1H pad → 1F (Switch COM) ──┐
                                        │ Switch ON
BATTERY - → 2H pad → 7H (GND bus)      │
                                        ↓
                              2F (Switch OUT) → 6H → Row 6 bus (~4V)
                                                         │
                                            ┌────────────┴────────────┐
                                            ↓                         ↓
                                        9A (XIAO)                20G (LED power)
                                            │
                                    [XIAO regulates]
                                            ↓
                                        9C (3.3V)
                                            ↓
                                        20A (FSR power)
```

### The Two Power Paths:
1. **Battery (~4V)** → Switch → Row 6 bus → XIAO (9A) + LED (20G)
2. **XIAO 3.3V regulated** → 9C → FSR+ (20A)

### Why Two Paths?
- LEDs need 4V (brighter)
- FSR needs 3.3V (accurate readings)
- Battery voltage ≠ Regulated voltage (don't mix!)

### All Connections Summary:
| From | To | What | Type |
|------|-----|------|------|
| Battery + wire | 1H pad | Power input | External wire |
| 1H | 1F (Switch COM) | To switch | Trace on back |
| 2F (Switch OUT) | 6H (Row 6 bus) | From switch | Trace on back |
| Battery - wire | 2H pad | Ground input | External wire |
| 2H | 7H (Row 7 bus) | To GND bus | Trace on back |
| Row 6 bus | 9A | XIAO power | Trace on back |
| Row 6 bus | 20G | LED power | Trace on back |
| 9C (3.3V) | 20A | FSR power | Trace on back |
| 15B (D1) | 20E | LED data | Trace on back |
| 20B (FSR-) | 16A | FSR signal | Trace on back |
| 16A | 15A (D0) | Read pressure | Trace on back |
| 17A (Resistor) | 7A (GND bus) | Pull-down | Trace on back |

---

## XIAO ESP32-C3 Placement

**Position:** Rows 9 and 15, Columns A through G (7 pins across)
**Orientation:** USB-C port pointing toward board edge (near row 9)

```
        USB-C PORT
          ┌───┐
          │   │ ← Edge of perfboard
    A   B   C   D   E   F   G
  ┌───┬───┬───┬───┬───┬───┬───┐
 9│5V │GND│3V3│D10│D9 │D8 │D7 │  Top pins (near USB)
  │   │   │   │   │   │   │   │
  │        XIAO ESP32-C3       │  Component body
  │   │   │   │   │   │   │   │
15│D0 │D1 │D2 │D3 │D4 │D5 │D6 │  Bottom pins
  └───┴───┴───┴───┴───┴───┴───┘
```

### Complete Pin Mapping

| Position | Pin | Function | Wire Color | Connection |
|----------|-----|----------|------------|------------|
| **9A** | **5V/VBUS** | Power in | **Red** | Battery + (via switch) |
| **9B** | **GND** | Ground | **Black** | Common GND bus |
| **9C** | **3V3** | 3.3V out | **Orange** | FSR power |
| 9D | D10 | GPIO | - | (unused) |
| 9E | D9 | GPIO | - | (unused) |
| 9F | D8 | GPIO | - | (unused) |
| 9G | D7 | GPIO | - | (unused) |
| **15A** | **D0** | Analog in | **Yellow** | FSR signal junction |
| **15B** | **D1** | Digital out | **Green** | LED DIN pad (direct) |
| 15C | D2 | GPIO | - | (unused) |
| 15D | D3 | GPIO | - | (unused) |
| 15E | D4/SDA | I2C Data | - | (future: OLED) |
| 15F | D5/SCL | I2C Clock | - | (future: OLED) |
| 15G | D6 | GPIO | - | (unused) |

---

## Component Placement Plan

### XIAO ESP32-C3 ✓ SOLDERED
- **Rows:** 9 & 15
- **Columns:** A-G
- **USB port:** Facing edge at row 9

### ~~Level Shifter~~ ✗ SKIPPED
- Not needed - 3.3V logic works fine with 4V-powered LEDs
- D1 connects **directly** to LED DIN output pad

### 10K Pull-down Resistor
- **Rows:** 17-18
- **Column:** A
- **Connections:**
  - One leg → 16A (D0)
  - Other leg → GND bus

### FSR Connection Junction
- **Row:** 17
- **Column:** A
- **Meets:** D0 (16A) + 10K resistor + FSR signal wire

---

## Complete Board Layout

```
FULL PERFBOARD MAP (Front View) - Columns A through J
══════════════════════════════════════════════════════════════════════════════

     A    B    C    D    E    F    G    H    I    J
                                                  ┌───┐
 1   -    -    -    -    -    -    -    -    -   [SW1]  ← Switch pin 1 (unused)
                                                  │   │
 2   -    -    -    -    -  [BAT+]━━━━━━━━━━━━━━━[SW2]  ← Battery+ pad → Switch COM
                                                  │   │
 3   -    -    -    -    -    -    -    -    -   [SW3]  ← Switch pin 3 → Row 6
                                                  └─┬─┘
 4   -    -    -    -    -    -    -    -    -    -│-
 5   -    -    -    -    -    -    -    -    -    -│-
                                                   ↓
 6  [══════════════ BATTERY BUS ~4V ══════════════════]  ← Solid wire A-J

 7  [══════════════ GROUND BUS ════════════════════BAT-]  ← Solid wire A-J, black wire at J7

 8   -    -    -    -    -    -    -    -    -    -

 9  [5V][GND][3V3][D10][D9 ][D8 ][D7 ] -    -    -      ← XIAO top pins (row 9)
     ↑    ↑    ↓
    ┌────────────────────────────────┐                    9A = power in (~4V)
    │     XIAO ESP32-C3 (body)       │                    9B = GND
    │       rows 10-14               │                    9C = 3.3V regulated out
    └────────────────────────────────┘

15  [D0 ][D1 ][D2 ][D3 ][D4 ][D5 ][D6 ] -    -    -      ← XIAO bottom pins (row 15)
     ↑    ↓
16  [JCT] -    -    -    -    -    -    -    -    -      ← Junction: D0 + resistor + FSR-

17  [RES] -    -    -    -    -    -    -    -    -      ← 10K resistor other leg
     ↓
    GND

18   -    -    -    -    -    -    -    -    -    -
19   -    -    -    -    -    -    -    -    -    -

20  [FSR+][FSR-] -   -  [DIN][GND][4V ] -    -    -      ← External pads (row 20)
     20A   20B          20E  20F  20G
```


## Understanding the Power System

**KEY CONCEPT: You have TWO separate power sources:**

### Power Path 1: Battery Voltage (≈4V) - Powers LEDs
```
Battery + wire → 1H pad
   ↓
Switch (1F-2F) — turns power on/off
   ↓
2F → 6H trace (to battery bus)
   ↓
Row 6 bus ← (carries battery voltage, ~4V)
   ↓
Splits two ways:
   ├─→ 9A (XIAO's power input)
   └─→ 20G (LED 5V pad) → LED ring VCC
```
**Why:** LEDs are brighter at 4V than 3.3V

### Power Path 2: Regulated 3.3V - Powers FSR
```
9A (XIAO receives ~4V from battery)
   ↓
[XIAO's internal voltage regulator]
   ↓
9C (XIAO outputs regulated 3.3V)
   ↓
20A (FSR+ pad) → FSR sensor
```
**Why:** FSR needs stable 3.3V for accurate readings

### Why NOT Connect 3V3 to Row 6?
- Row 6 = battery voltage (~4V)
- 9C = regulated output (3.3V)
- They're **different voltages** - can't mix them!
- Row 6 powers: XIAO + LEDs (need 4V)
- 9C powers: FSR only (needs 3.3V)

---

## Complete Power & Signal Flow

```
BATTERY (3.7V LiPo, reads ~4V charged)
   │
   ├─ RED (+) ──→ 1H pad ──→ SWITCH (1F-2F) ──→ 2F ──→ 6H (battery bus)
   │                                                      │
   │                                                      ├──→ 9A (XIAO power in)
   │                                                      │     └─→ [regulator] ─→ 9C (3.3V out) ─→ 20A (FSR+)
   │                                                      │
   │                                                      └──→ 20G (LED 5V)
   │
   └─ BLACK (-) ──→ 2H pad ──→ 7H (GND bus)
                                  │
                                  ├──→ 9B (XIAO GND)
                                  ├──→ 16A/17A (resistor to GND)
                                  └──→ 20F (LED GND)

SIGNAL PATHS (data, not power):
   15B (D1) ──→ 20E (LED DIN) ─→ LED ring data input

FSR VOLTAGE DIVIDER (for reading pressure):
   20A (FSR+) ──→ FSR sensor ──→ 20B (FSR-) ──→ 16A (junction)
                                                   ├──→ 15A (D0 reads voltage)
                                                   └──→ 16A-17A (10K resistor to GND)
```

## All Traces You Need to Solder (on BACK of board)

### Power Buses (horizontal wires):
1. **Row 6 (Battery bus):** Solid wire across 6A → 6J (all 10 columns)
2. **Row 7 (Ground bus):** Solid wire across 7A → 7J (all 10 columns)

### Switch & Battery Connections:
3. ✓ **Battery + pad at F2** (red wire soldered here)
4. ✓ **F2 → J2 trace** (connects battery+ to switch COM)
5. ✓ **J3 → 6J trace** (switch output to battery bus)
6. ✓ **Battery - at J7** (black wire soldered directly to GND bus)

### XIAO Power (your actual route):
7. ✓ **6A → 5A bridge** (bus to 5A)
8. ✓ **5A → 8A insulated wire** (crosses over rows 6-7)
9. ✓ **8A → 9A bridge** (to XIAO power input)
10. **7B → 9B** (ground bus to XIAO ground) - still needed?

### LED Ring:
9. **6G → 20G** (battery bus to LED 4V pad)
10. **7F → 20F** (ground bus to LED GND pad)
11. **15B → 20E** (D1 pin to LED DIN pad)

### FSR Sensor:
12. **9C → 20A** (XIAO 3.3V output to FSR+ pad)
13. **20B → 16A** (FSR- pad to junction)
14. **16A → 15A** (junction to D0 analog pin) - may already be connected via resistor leg

### Resistor:
15. **10K resistor:** legs in 16A and 17A
16. **17A → 7A** (resistor bottom leg to ground bus)

---

## How to Build Power Buses

**Row 6 (Battery Bus ~4V) - STEP BY STEP:**
1. Cut a piece of solid wire about 4 inches long
2. Strip ALL the insulation off (you want bare wire)
3. On the BACK of the board, thread it through hole 6A
4. Bend it to lay flat along Row 6
5. Thread through or solder to each hole: 6A, 6B, 6C... all the way to 6J
6. Solder at each hole as you go (or at least at A, G, and J)
7. Trim any excess

**Row 7 (GND Bus) - Same process:**
1. Cut another 4 inch piece of solid wire
2. Strip ALL insulation
3. On BACK of board, lay it across Row 7 from 7A to 7J
4. Solder at multiple points

**Why Row 6 needs to reach column J:**
- Your switch is at J1-J3
- J3 (switch output) needs to connect DOWN to 6J
- Then Row 6 bus carries power across to 6A → 9A (XIAO)

---

## External Wire Pads ✓ PLACED

Row 20 pads - these connect to external components via wires:

| Pad | Position | Purpose | Voltage/Signal | Trace connects to |
|-----|----------|---------|----------------|-------------------|
| FSR + | **20A** | FSR power | **3.3V** | 9C (XIAO's 3V3 output) |
| FSR - | **20B** | FSR signal | Variable | 16A (junction) |
| LED DIN | **20E** | LED data | Signal (3.3V) | 15B (D1 pin) |
| LED GND | **20F** | LED ground | 0V | Row 7 (GND bus) |
| LED 5V | **20G** | LED power | **~4V** | Row 6 (battery bus) |

**Note:** Even though labeled "LED 5V", this pad gets ~4V from your battery, not 5V!

---

## Decisions Log

- [x] XIAO position: Rows 9 & 15, Cols A-G (horizontal, USB out)
- [x] D0 (FSR) at 15A
- [x] D1 (LED) at 15B
- [x] Power pins: 9A (5V), 9B (GND), 9C (3V3)
- [x] Level shifter: SKIPPED (not needed)
- [x] 10K resistor: Rows 16-17, Col A
- [x] External pads at Row 20: A (FSR+), B (FSR-), E (LED DIN), F (LED GND), G (LED 5V)
- [ ] Power buses: Row 6 (5V), Row 7 (GND) - TBD
- [ ] Battery input pads: TBD

---

*Last updated: March 2026*
