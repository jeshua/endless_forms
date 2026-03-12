# Wiring Checklist - Your Actual Layout

## Your Current Progress
- [x] Switch soldered at J1, J2, J3
- [x] Battery + pad at F2
- [x] Trace F2 → J2 (battery to switch COM)
- [ ] Battery - pad at F3 (suggested)
- [ ] Power buses not done yet

---

## Step-by-Step Build Order

### STEP 1: Build the Power Buses (Row 6 and Row 7)

**Row 6 (Battery Bus ~4V):**
1. Cut a 4-inch piece of solid wire
2. Strip ALL the insulation off
3. On the BACK of the board, lay it across Row 6 from hole A to hole J
4. Solder at each hole (or at least A, G, and J)

**Row 7 (Ground Bus):**
1. Same process - solid wire from 7A to 7J
2. Solder at multiple points

### STEP 2: Connect Switch to Battery Bus
- [ ] **J3 → 6J**: Trace from switch output (J3) down to battery bus (6J)
  - This is just 3 rows straight down in column J

### STEP 3: Connect Battery - (Ground)
- [ ] **Battery - wire → F3**: Solder black wire to F3 pad
- [ ] **F3 → 7F**: Trace from F3 to ground bus at 7F

### STEP 4: Connect XIAO Power
- [ ] **6A → 9A**: Battery bus to XIAO power input
- [ ] **7B → 9B**: Ground bus to XIAO ground

### STEP 5: Connect LED Ring Pads
- [ ] **6G → 20G**: Battery bus to LED 4V pad
- [ ] **7F → 20F**: Ground bus to LED GND pad
- [ ] **15B → 20E**: D1 pin to LED DIN pad

### STEP 6: Connect FSR Pads
- [ ] **9C → 20A**: XIAO 3.3V output to FSR+ pad
- [ ] **20B → 16A**: FSR- pad to junction

### STEP 7: Connect Resistor to Ground
- [ ] **17A → 7A**: Resistor bottom to ground bus

---

## Your Board Layout

```
     A    B    C    D    E    F    G    H    I    J
                                                  ┌───┐
 1   -    -    -    -    -    -    -    -    -   [SW1] unused
                                                  │   │
 2   -    -    -    -    -  [BAT+]═══════════════[SW2] COM
                                                  │   │
 3   -    -    -    -    -  [BAT-] -    -    -   [SW3] → to Row 6
                                                  └───┘
 4-5  (empty)

 6  [═══════════════ BATTERY BUS 4V ════════════════════]

 7  [═══════════════ GROUND BUS ════════════════════════]

 8   (empty)

 9  [5V][GND][3V3][D10][D9][D8][D7] -   -   -    XIAO top

10-14    XIAO body

15  [D0][D1][D2][D3][D4][D5][D6] -   -   -       XIAO bottom

16  [JCT] -   -   -   -   -   -   -   -   -      Junction + resistor

17  [10K] -   -   -   -   -   -   -   -   -      Resistor to GND

18-19 (empty)

20  [FSR+][FSR-] -  - [DIN][GND][4V] -  -  -     External pads
     A     B          E    F    G
```

---

## Power Flow Summary

```
Battery + (red)
    ↓
   F2 pad
    ↓ (trace you already did)
   J2 (Switch COM)
    ↓ (when switch is ON)
   J3 (Switch OUT)
    ↓ (trace needed: J3 → 6J)
   Row 6 Bus ══════════════════════════════════
    ↓                    ↓
   6A → 9A (XIAO)       6G → 20G (LED 4V)
    ↓
   XIAO regulates
    ↓
   9C (3.3V out) → 20A (FSR+)


Battery - (black)
    ↓
   F3 pad
    ↓ (trace needed: F3 → 7F)
   Row 7 GND Bus ══════════════════════════════
    ↓           ↓              ↓
   7B → 9B    7A → 17A       7F → 20F
   (XIAO)     (resistor)     (LED GND)
```

---

## What to Do Right Now

1. **Build Row 6 bus** (solid wire 6A to 6J)
2. **Build Row 7 bus** (solid wire 7A to 7J)
3. **Trace J3 → 6J** (switch output to battery bus)
4. Then continue with remaining traces

---

*Last updated: March 2026*
