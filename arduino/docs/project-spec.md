# Pressure-Reactive LED Puppet Project

## Overview

A portable device where squeezing an FSR (Force Sensitive Resistor) controls the brightness of an LED ring. Designed to be embedded in a puppet head - squeeze the puppet's hand/body and its eyes glow brighter.

**Behavior:** Press harder → brighter orange glow. Release → off.

---

## Hardware Components

| Component | Model | Purpose |
|-----------|-------|---------|
| Microcontroller | Seeed Studio XIAO ESP32-C3 | Brain - reads sensor, controls LEDs |
| LED Ring | WS2812B 7-LED Ring | Visual output (eyes) |
| Pressure Sensor | FSR (Force Sensitive Resistor) | Input - detects squeeze |
| Level Shifter | HiLetgo 4-Channel 3.3V-5V | Converts 3.3V signal to 5V for LEDs |
| Resistor | 10K ohm | Pull-down for FSR voltage divider |
| Battery | 3.7V LiPo (Qimoo 803040) | Portable power |
| Switch | SPDT slide switch | On/off control |

---

## Wiring Schematic

```
                                    ┌─────────────────┐
                                    │   7-LED RING    │
                                    │    WS2812B      │
                                    │                 │
                                    │  VCC  GND  DIN  │
                                    └───┬────┬────┬───┘
                                        │    │    │
                                        │    │    │
┌─────────────┐    ┌──────────────┐     │    │    │
│    XIAO     │    │ LEVEL SHIFT  │     │    │    │
│  ESP32-C3   │    │              │     │    │    │
│             │    │  HV ────────────────┼────┼────┘ (5V)
│        3V3 ─┼────┼─ LV          │     │    │
│             │    │              │     │    │
│         D1 ─┼────┼─ LV1    HV1 ─┼─────┼────┘ (LED Data)
│             │    │              │     │
│        GND ─┼────┼─ GND    GND ─┼─────┘
│             │    └──────────────┘
│             │
│         D0 ─┼────────┬─────────────────┐
│             │        │                 │
│        3V3 ─┼────────┼───┐             │
│             │        │   │             │
└─────────────┘        │   │             │
                       │   │             │
                    ┌──┴───┴──┐      ┌───┴───┐
                    │   FSR   │      │ 10K Ω │
                    │ Sensor  │      │  Res  │
                    └────┬────┘      └───┬───┘
                         │               │
                         └───────────────┼──→ GND
                      (same row on       │
                       breadboard)       │
                                         ▼
                                        GND


POWER CIRCUIT:
                    ┌─────────┐
   Battery (+) ────►│ SWITCH  │────► 5V Rail ────► XIAO VIN
                    └─────────┘                    LED VCC
                                                   Level Shifter HV

   Battery (-) ────────────────────► GND Rail ────► All GNDs
```

---

## Pin Reference

| XIAO Pin | GPIO | Connection | Notes |
|----------|------|------------|-------|
| D0 | GPIO2 | FSR signal | Analog input (ADC) |
| D1 | GPIO3 | Level Shifter LV1 | LED data out |
| 3V3 | - | FSR power + Level Shifter LV | 3.3V reference |
| GND | - | Common ground | Connect all grounds |
| VIN | - | Battery + (via switch) | Power input |

---

## Software

### Current Code (led_test.ino)

```cpp
#include <FastLED.h>

#define FSR_PIN     D0
#define LED_PIN     D1
#define NUM_LEDS    7

#define THRESHOLD   50    // Ignore noise below this
#define HUE_ORANGE  32    // Orange-yellow color

CRGB leds[NUM_LEDS];
int smoothedPressure = 0;

void setup() {
  Serial.begin(115200);
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.clear();
  FastLED.show();
  analogReadResolution(12);
}

void loop() {
  int pressure = analogRead(FSR_PIN);

  // Smooth reading to reduce flicker
  smoothedPressure = (smoothedPressure * 3 + pressure) / 4;

  if (smoothedPressure < THRESHOLD) {
    FastLED.clear();
    FastLED.show();
  } else {
    int brightness = map(smoothedPressure, THRESHOLD, 4095, 10, 255);
    brightness = constrain(brightness, 0, 255);
    fill_solid(leds, NUM_LEDS, CHSV(HUE_ORANGE, 255, brightness));
    FastLED.show();
  }

  delay(20);
}
```

### Upload Commands

```bash
# Compile
arduino-cli compile --fqbn esp32:esp32:XIAO_ESP32C3 led_test

# Upload (check port with: ls /dev/cu.usb*)
arduino-cli upload -p /dev/cu.usbmodem1101 --fqbn esp32:esp32:XIAO_ESP32C3 led_test
```

---

## Perfboard Layout

```
┌──────────────────────────────────────────────┐
│                   PERFBOARD                   │
│                                               │
│   USB PORT THIS EDGE (for reprogramming)      │
│   ┌─────────────┐                             │
│   │    XIAO     │                             │
│   │  ESP32-C3   │                             │
│   │ 3V3 GND D0 D1                             │
│   └──┬───┬──┬──┬┘                             │
│      │   │  │  │                              │
│      │   │  │  └──────┐                       │
│      │   │  │         │                       │
│      │   │  │    ┌────┴─────┐                 │
│      │   │  │    │  LEVEL   │                 │
│      │   │  │    │ SHIFTER  │                 │
│      │   │  │    │LV1   HV1─┼──→ LED DIN      │
│      │   │  │    │LV     HV─┼──→ 5V           │
│      │   │  │    │GND   GND─┼──→ GND          │
│      │   │  │    └────┬─────┘                 │
│      │   │  │         │                       │
│      └───┼──┼─────────┴─── 3V3 bus            │
│          │  │                                 │
│          │  └────────┐                        │
│          │           │                        │
│          │      ┌────┴────┐                   │
│          │      │  10K Ω  │                   │
│          │      └────┬────┘                   │
│          │           │                        │
│          └───────────┴──── GND bus            │
│                                               │
│   EXTERNAL WIRE PADS:                         │
│   ┌─────┬─────┬─────┬─────┬─────┐             │
│   │ FSR │ FSR │ BAT │ BAT │ LED │             │
│   │  +  │  -  │  +  │  -  │ 3pin│             │
│   └─────┴─────┴─────┴─────┴─────┘             │
│                                               │
└──────────────────────────────────────────────┘
```

---

## Assembly Checklist

### Before Soldering
- [ ] Test circuit on breadboard (confirmed working)
- [ ] Plan component placement on perfboard
- [ ] Gather: soldering iron, solder, helping hands, wire

### Soldering Order
1. [ ] Solder XIAO (headers or direct) - USB port at edge
2. [ ] Solder level shifter module
3. [ ] Solder 10K resistor
4. [ ] Create power bus traces (5V, 3.3V, GND)
5. [ ] Solder signal wires (D0→FSR, D1→Level Shifter)
6. [ ] Solder external wire pads/terminals
7. [ ] Test continuity with multimeter
8. [ ] Connect external components and test

### External Wires (to puppet)
- [ ] FSR: 2 wires (signal + 3.3V) - route to squeeze point
- [ ] LED Ring: 3 wires (5V, GND, DIN) - route to puppet head
- [ ] Battery: 2 wires (or JST connector)
- [ ] Switch: inline with battery positive

---

## Customization Options

### Change Color
In code, modify `HUE_ORANGE`:
```cpp
#define HUE_ORANGE  32   // Current: orange-yellow

// Other options:
// 0   = Red
// 32  = Orange
// 64  = Yellow
// 96  = Green
// 128 = Cyan
// 160 = Blue
// 192 = Purple
// 224 = Pink
```

### Adjust Sensitivity
```cpp
#define THRESHOLD   50   // Higher = need more pressure to activate
```

### Change Smoothing
```cpp
// More smoothing (slower response, less flicker):
smoothedPressure = (smoothedPressure * 7 + pressure) / 8;

// Less smoothing (faster response, may flicker):
smoothedPressure = (smoothedPressure + pressure) / 2;
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| LEDs don't light | Check level shifter wiring, verify shared ground |
| LEDs flicker when idle | Increase THRESHOLD value |
| No response to pressure | Check FSR wiring, verify 10K resistor to GND |
| Dim at max pressure | Check 5V power to LED ring |
| Can't upload code | Check USB cable, try different port |

---

## Parts List for Replication

| Item | Search Term | ~Price |
|------|-------------|--------|
| XIAO ESP32-C3 | "Seeed Studio XIAO ESP32C3 pre-soldered" | $8 |
| LED Ring | "WS2812B 7 LED ring" | $7 |
| FSR | "Force sensitive resistor FSR" | $6 |
| Level Shifter | "HiLetgo 4 channel logic level converter 3.3V 5V" | $7 |
| 10K Resistors | "10K ohm resistor pack" | $5 |
| LiPo Battery | "3.7V LiPo battery 500mAh JST" | $8 |
| Perfboard | "Prototype PCB board 5x7cm" | $6 |
| Slide Switch | "SPDT slide switch" | $5 |

---

## Project Repository

GitHub: https://github.com/jeshua/endless_forms

Files in `arduino/` directory:
- `led_test/led_test.ino` - Main working code
- `fsr_test/fsr_test.ino` - FSR calibration tool
- `pressure_reactive_leds/pressure_reactive_leds.ino` - Alternative with color shift
- `SETUP.md` - Setup instructions

---

*Last updated: March 2026*
