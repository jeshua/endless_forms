# Puppet LED Project - Wiring Setup

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
FULL PERFBOARD MAP (Front View)
═══════════════════════════════════════════════════════════════

     A    B    C    D    E    F    G    H
 1   -    -    -    -    -    -    -   [BAT+]  ← Battery + input (via switch)
 2   -    -    -    -    -    -    -   [BAT-]  ← Battery - input
 3   -    -    -    -    -    -    -    -
 4   -    -    -    -    -    -    -    -
 5   -    -    -    -    -    -    -    -
 6  [5V][5V][5V][5V][5V][5V][5V][5V]  ← 5V BUS (battery power)
     ║                             ║
 7  [GND][GND][GND][GND][GND][GND][GND][GND]  ← GND BUS
     ║    ║                         ║
 8   -    -    -    -    -    -    -    -
     ║    ║
 9  [5V][GND][3V3][D10][D9 ][D8 ][D7 ] -   ← XIAO top pins
     ║    ║    ║
    ┌────────────────────────────────┐
    │     XIAO ESP32-C3 (body)       │
    └────────────────────────────────┘
     ║    ║
15  [D0 ][D1 ][D2 ][D3 ][D4 ][D5 ][D6 ] -   ← XIAO bottom pins
     ║    ║
16  [RES] -    -    -    -    -    -    -   ← 10K resistor leg 1
     ║                                      (+ FSR signal junction)
17  [RES] -    -    -    -    -    -    -   ← 10K resistor leg 2
     ║
18   -    -    -    -    -    -    -    -
19   -    -    -    -    -    -    -    -
20  [FSR+][FSR-][LED5V][LEDGND][LEDDIN] -  ← External wire pads
```

## Power Flow Diagram

```
BATTERY (3.7V LiPo)
   │
   ├─ RED (+) ──→ SWITCH ──→ Row 6 Col H (5V bus) ──→ Row 9A (XIAO 5V)
   │                          │                         │
   │                          └──→ Row 20C (LED 5V pad)─┘
   │
   └─ BLACK (-) ───────────→ Row 7 Col H (GND bus)
                              │
                              ├──→ Row 9B (XIAO GND)
                              ├──→ Row 17A (10K resistor)
                              └──→ Row 20D (LED GND pad)

XIAO 3V3 OUTPUT
   Row 9C ────────────────→ Row 20A (FSR + pad)


SIGNAL PATHS

FSR SENSOR:
   FSR + ──→ Row 20A pad ──→ (wire to sensor)
   FSR - ──→ Row 20B pad ──→ (wire to sensor)
                └──→ Row 16A (junction) ──→ Row 15A (D0 analog read)
                       └──→ Row 17A (10K to GND)

LED RING:
   LED 5V ──→ Row 20C pad ──→ (wire to LED VCC)
   LED GND ──→ Row 20D pad ──→ (wire to LED GND)
   LED DIN ──→ Row 20E pad ──→ (wire to LED data)
              └──→ Row 15B (D1 output)
```

## Power Buses - How to Build

**Row 6 (5V Bus):**
1. Strip a ~3 inch piece of solid wire
2. On BACK of board, solder it across holes 6A through 6H
3. Add trace from Row 6H → Row 1H (battery + pad)
4. Add trace from Row 6A → Row 9A (XIAO 5V pin)

**Row 7 (GND Bus):**
1. Strip a ~3 inch piece of solid wire
2. On BACK of board, solder it across holes 7A through 7H
3. Add trace from Row 7H → Row 2H (battery - pad)
4. Add trace from Row 7A → Row 9B (XIAO GND pin)

---

## External Wire Pads ✓ PLACED

Row 20 pads:

| Pad | Position | Wire To | Color | Connects To |
|-----|----------|---------|-------|-------------|
| FSR + | **20A** | FSR leg 1 (power) | Orange/Red | From 9C (3V3) |
| FSR - | **20B** | FSR leg 2 (signal) | Yellow | To 16A junction |
| LED DIN | **20E** | LED ring data | Green | From 15B (D1) |
| LED GND | **20F** | LED ring GND | Black | From GND bus |
| LED 5V | **20G** | LED ring VCC | Red | From 5V bus |

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
