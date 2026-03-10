# ESP32 Pressure-Reactive LED Strip - Setup Guide

## 1. Install Arduino IDE

Download from: https://www.arduino.cc/en/software

Or install via Homebrew:
```bash
brew install --cask arduino-ide
```

## 2. Add ESP32 Board Support

1. Open Arduino IDE
2. Go to **Arduino IDE > Settings** (Mac) or **File > Preferences** (Windows)
3. In "Additional boards manager URLs", add:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
4. Click OK
5. Go to **Tools > Board > Boards Manager**
6. Search for "esp32"
7. Install **"esp32 by Espressif Systems"** (latest version)

## 3. Install FastLED Library

1. Go to **Sketch > Include Library > Manage Libraries**
2. Search for "FastLED"
3. Install **"FastLED by Daniel Garcia"**

## 4. Configure Board Settings

1. Connect your ESP32 via USB-C
2. Go to **Tools > Board** and select **"ESP32 Dev Module"**
3. Go to **Tools > Port** and select the USB port (usually `/dev/cu.usbserial-*` on Mac)

If no port appears:
- On Mac: Install CH340/CP210x drivers (most ESP32 boards use these)
- Try a different USB cable (some are charge-only)
- Try a different USB port

## 5. Test Sequence

Run these sketches in order:

### Step 1: LED Test (verify strip works)
1. Open `led_test/led_test.ino`
2. **IMPORTANT**: Change `NUM_LEDS` to match your strip length
3. Click Upload (→ button)
4. You should see a rainbow animation

### Step 2: FSR Test (verify sensor works)
1. Open `fsr_test/fsr_test.ino`
2. Upload to ESP32
3. Open **Tools > Serial Monitor** (set baud rate to 115200)
4. Press the FSR and watch values change
5. Note the min/max values for calibration

### Step 3: Full Project
1. Open `pressure_reactive_leds/pressure_reactive_leds.ino`
2. Update these values based on your FSR test:
   - `NUM_LEDS` - your strip length
   - `PRESSURE_MIN` - value when lightly pressed
   - `PRESSURE_MAX` - value when pressed hard
3. Upload and enjoy!

## Troubleshooting

### "No port available"
- Install USB-Serial drivers:
  - CH340: https://www.wch.cn/downloads/CH341SER_MAC_ZIP.html
  - CP210x: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
- Try: `ls /dev/cu.*` in Terminal to see available ports

### Upload fails / times out
- Hold BOOT button on ESP32 while uploading
- Try lower upload speed: **Tools > Upload Speed > 115200**

### LEDs don't light up
- Check capacitor polarity (long leg = positive)
- Verify 330Ω resistor is on data line
- Confirm LED strip VCC wire goes to 5V, not 3.3V
- Try GPIO 2 instead of GPIO 4

### FSR reads 0 or 4095 constantly
- Check 10KΩ pull-down resistor connection
- Verify FSR legs are in separate breadboard rows
- Try GPIO 35 or 36 (other ADC pins)

### Colors are wrong (RGB order)
- Change `GRB` to `RGB` or `BRG` in the code

## Pin Reference (ESP32-C3)

| Component | ESP32-C3 Pin | Notes |
|-----------|--------------|-------|
| FSR Signal | GPIO 2 | Analog input (ADC1, pins 0-5) |
| LED Data | GPIO 4 | Through 330Ω resistor |
| VIN | Battery + | Via toggle switch |
| GND | Battery - | Common ground |

**Note:** Your board is an ESP32-C3. GPIO 34 from the original instructions doesn't exist on the C3. Use GPIO 2 instead for the FSR sensor.

## Arduino CLI (Optional)

For command-line programming:
```bash
# Install
brew install arduino-cli

# Setup
arduino-cli config init
arduino-cli core update-index
arduino-cli core install esp32:esp32

# Install library
arduino-cli lib install "FastLED"

# Compile
arduino-cli compile --fqbn esp32:esp32:esp32 pressure_reactive_leds

# Upload (replace PORT with your port)
arduino-cli upload -p /dev/cu.usbserial-0001 --fqbn esp32:esp32:esp32 pressure_reactive_leds
```
