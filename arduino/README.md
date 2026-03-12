# Pressure-Reactive LED Puppet

Arduino project for a pressure-sensitive LED ring controlled by an FSR sensor, designed to be embedded in a puppet.

## Project Structure

```
arduino/
├── README.md                      # This file
├── docs/
│   ├── wiring-diagram.html        # Visual wiring diagram (open in browser)
│   ├── wiring-setup.md            # Detailed perfboard layout decisions
│   ├── project-spec.md            # Complete project specification
│   └── setup.md                   # Arduino IDE/CLI setup instructions
├── led_test/
│   └── led_test.ino              # Current working code (orange brightness control)
├── fsr_test/
│   └── fsr_test.ino              # FSR sensor calibration tool
└── pressure_reactive_leds/
    └── pressure_reactive_leds.ino # Alternative with color shifting
```

## Quick Start

1. **Hardware:** XIAO ESP32-C3, WS2812B 7-LED ring, FSR, 10K resistor, 3.7V LiPo battery
2. **Setup:** See `docs/setup.md` for Arduino IDE/CLI installation
3. **Wiring:** Open `docs/wiring-diagram.html` in your browser
4. **Upload:** `led_test/led_test.ino` is the main working code

## Current Behavior

Press the FSR sensor harder → LED ring glows brighter orange

## Repository

Full project: [endless_forms](https://github.com/jeshua/endless_forms)
