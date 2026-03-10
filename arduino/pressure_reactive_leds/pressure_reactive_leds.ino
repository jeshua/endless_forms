/*
 * Pressure-Reactive LED Strip
 *
 * Hardware:
 *   - ESP32 Dev Board
 *   - FSR (Force Sensitive Resistor) on GPIO 34
 *   - WS2812B LED Strip (data on GPIO 4)
 *   - 10K pull-down resistor for FSR
 *   - 330 ohm resistor on LED data line
 *   - 1000uF capacitor across power rails
 *
 * Press harder on the FSR -> brighter colors, more LEDs lit
 */

#include <FastLED.h>

// Pin definitions (XIAO ESP32-C3)
#define FSR_PIN       D0    // A0/D0 - Analog input for pressure sensor
#define LED_PIN       D1    // D1 - Data pin for WS2812B strip
#define NUM_LEDS      30    // Adjust to match your strip length
#define LED_TYPE      WS2812B
#define COLOR_ORDER   GRB

// LED array
CRGB leds[NUM_LEDS];

// Pressure reading variables
int pressureValue = 0;
int smoothedPressure = 0;
const float smoothingFactor = 0.1;  // Lower = more smoothing

// Calibration values (adjust based on your FSR)
const int PRESSURE_MIN = 100;   // Minimum reading when pressed lightly
const int PRESSURE_MAX = 4000;  // Maximum reading when pressed hard

void setup() {
  Serial.begin(115200);
  Serial.println("Pressure-Reactive LED Strip Starting...");

  // Initialize FastLED
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
  FastLED.setBrightness(255);
  FastLED.clear();
  FastLED.show();

  // Configure ADC for ESP32
  analogReadResolution(12);  // 12-bit resolution (0-4095)
  analogSetAttenuation(ADC_11db);  // Full 0-3.3V range

  // Startup animation
  startupAnimation();

  Serial.println("Ready! Press the sensor...");
}

void loop() {
  // Read pressure sensor
  pressureValue = analogRead(FSR_PIN);

  // Apply exponential smoothing
  smoothedPressure = (smoothingFactor * pressureValue) +
                     ((1 - smoothingFactor) * smoothedPressure);

  // Debug output
  Serial.print("Raw: ");
  Serial.print(pressureValue);
  Serial.print(" | Smoothed: ");
  Serial.println(smoothedPressure);

  // Map pressure to LED behavior
  if (smoothedPressure < PRESSURE_MIN) {
    // No pressure - LEDs off or dim idle animation
    idleAnimation();
  } else {
    // Pressure detected - reactive mode
    pressureReactiveMode(smoothedPressure);
  }

  FastLED.show();
  delay(20);  // ~50fps update rate
}

void startupAnimation() {
  // Quick rainbow sweep to confirm LEDs work
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CHSV(i * 255 / NUM_LEDS, 255, 150);
    FastLED.show();
    delay(30);
  }
  delay(500);
  FastLED.clear();
  FastLED.show();
}

void idleAnimation() {
  // Gentle breathing effect when no pressure
  static uint8_t brightness = 0;
  static int8_t direction = 1;

  brightness += direction;
  if (brightness >= 30 || brightness <= 0) {
    direction = -direction;
  }

  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CHSV(160, 255, brightness);  // Soft blue pulse
  }
}

void pressureReactiveMode(int pressure) {
  // Map pressure to 0-255 range
  int mappedPressure = constrain(
    map(pressure, PRESSURE_MIN, PRESSURE_MAX, 0, 255),
    0, 255
  );

  // Calculate how many LEDs to light (pressure = more LEDs)
  int numLit = map(mappedPressure, 0, 255, 1, NUM_LEDS);

  // Calculate color (pressure shifts from blue -> green -> yellow -> red)
  uint8_t hue = map(mappedPressure, 0, 255, 160, 0);

  // Calculate brightness (pressure = brighter)
  uint8_t brightness = map(mappedPressure, 0, 255, 50, 255);

  // Clear all LEDs first
  FastLED.clear();

  // Light up LEDs from center outward (or change to from one end)
  int center = NUM_LEDS / 2;
  for (int i = 0; i < numLit / 2 + 1; i++) {
    int leftIndex = center - i;
    int rightIndex = center + i;

    if (leftIndex >= 0) {
      leds[leftIndex] = CHSV(hue, 255, brightness);
    }
    if (rightIndex < NUM_LEDS) {
      leds[rightIndex] = CHSV(hue, 255, brightness);
    }
  }
}

// Alternative mode: Fill from one end
void pressureReactiveFill(int pressure) {
  int mappedPressure = constrain(
    map(pressure, PRESSURE_MIN, PRESSURE_MAX, 0, 255),
    0, 255
  );

  int numLit = map(mappedPressure, 0, 255, 0, NUM_LEDS);
  uint8_t hue = map(mappedPressure, 0, 255, 160, 0);
  uint8_t brightness = map(mappedPressure, 0, 255, 50, 255);

  for (int i = 0; i < NUM_LEDS; i++) {
    if (i < numLit) {
      leds[i] = CHSV(hue, 255, brightness);
    } else {
      leds[i] = CRGB::Black;
    }
  }
}

// Alternative mode: Uniform color change only
void pressureReactiveColor(int pressure) {
  int mappedPressure = constrain(
    map(pressure, PRESSURE_MIN, PRESSURE_MAX, 0, 255),
    0, 255
  );

  uint8_t hue = map(mappedPressure, 0, 255, 160, 0);
  uint8_t brightness = map(mappedPressure, 0, 255, 30, 255);

  fill_solid(leds, NUM_LEDS, CHSV(hue, 255, brightness));
}
