# Pressure-Reactive LED Ring - Setup Guide

## Hardware

- **Microcontroller:** Seeed Studio XIAO ESP32-C3
- **LEDs:** WS2812B 7-LED Ring (or any WS2812B strip)
- **Sensor:** FSR (Force Sensitive Resistor)
- **Level Shifter:** 3.3V to 5V logic level converter (required for reliable LED communication)
- **Resistor:** 10K ohm pull-down for FSR voltage divider
- **Power:** 3.7V LiPo battery or USB

## Wiring

### LED Ring
```
LED Ring VCC    →  5V power rail
LED Ring GND    →  Ground rail
LED Ring DIN    →  Level Shifter HV1 output

Level Shifter:
  LV            →  3.3V from XIAO
  HV            →  5V power rail
  GND           →  Ground (both sides)
  LV1           →  D1 on XIAO
  HV1           →  LED Ring DIN
```

### FSR Pressure Sensor
```
FSR Leg 1       →  3.3V (3V3 pin on XIAO)
FSR Leg 2       →  Breadboard row (e.g., Row 20)

In same row:
  10K resistor  →  other end to GND
  Wire          →  D0 on XIAO
```

### Critical: Shared Ground
The XIAO and LED ring MUST share a common ground connection. If powered separately (USB + battery), connect XIAO GND directly to LED GND.

## Pin Reference (XIAO ESP32-C3)

| Component  | XIAO Pin | GPIO | Notes |
|------------|----------|------|-------|
| FSR Signal | D0       | GPIO2 | Analog input |
| LED Data   | D1       | GPIO3 | Through level shifter |
| 3.3V Out   | 3V3      | -    | Power for FSR + level shifter LV |
| Ground     | GND      | -    | Common ground |

## Software Setup

### Option 1: Arduino CLI (Recommended)

```bash
# Install
brew install arduino-cli

# Setup ESP32 support
arduino-cli core update-index
arduino-cli core install esp32:esp32

# Install FastLED library
arduino-cli lib install "FastLED"

# Compile
arduino-cli compile --fqbn esp32:esp32:XIAO_ESP32C3 led_test

# Upload (check your port with: ls /dev/cu.usb*)
arduino-cli upload -p /dev/cu.usbmodem1101 --fqbn esp32:esp32:XIAO_ESP32C3 led_test
```

### Option 2: Arduino IDE

1. Download from: https://www.arduino.cc/en/software
2. Add ESP32 board URL in Settings:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
3. Install "esp32 by Espressif Systems" in Boards Manager
4. Install "FastLED" in Library Manager
5. Select board: **XIAO_ESP32C3**
6. Select port: `/dev/cu.usbmodem*`

## Project Files

| File | Description |
|------|-------------|
| `led_test/led_test.ino` | Main project - FSR controls LED brightness (orange) |
| `fsr_test/fsr_test.ino` | Test FSR sensor readings via Serial Monitor |
| `pressure_reactive_leds/pressure_reactive_leds.ino` | Alternative with color shifting |

## Troubleshooting

### LEDs don't light up
1. **Check level shifter** - 3.3V logic often doesn't work directly with 5V LEDs
2. **Check ground** - XIAO and LEDs must share common ground
3. **Check direction** - LED strip has input/output ends (look for arrows)
4. **Try different GPIO** - Some pins may have conflicts

### LEDs show random colors
- Usually means no data signal reaching LEDs
- Check level shifter wiring
- Verify shared ground connection

### FSR reads constant 0 or 4095
- Check 10K pull-down resistor connection
- Verify FSR legs are in separate breadboard rows
- Check D0 connection

### LEDs flicker at low pressure
- Increase `THRESHOLD` value in code (default: 50)
- Check for loose connections

### Upload fails
- Check USB cable (some are charge-only)
- Try: `ls /dev/cu.*` to find correct port
- Hold BOOT button during upload if needed
