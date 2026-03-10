/*
 * FSR Brightness Control - Orange/Yellow
 * Press harder = brighter
 */

#include <FastLED.h>

#define FSR_PIN     D0
#define LED_PIN     D1
#define NUM_LEDS    7

#define THRESHOLD   50    // Ignore noise below this value
#define HUE_ORANGE  32    // Orange-yellow hue (0=red, 32=orange, 64=yellow)

CRGB leds[NUM_LEDS];
int smoothedPressure = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("=== ORANGE BRIGHTNESS ===");

  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.clear();
  FastLED.show();

  analogReadResolution(12);
}

void loop() {
  int pressure = analogRead(FSR_PIN);

  // Smooth the reading to reduce flicker
  smoothedPressure = (smoothedPressure * 3 + pressure) / 4;

  // Below threshold = off (no flicker)
  if (smoothedPressure < THRESHOLD) {
    FastLED.clear();
    FastLED.show();
  } else {
    // Map pressure to brightness
    int brightness = map(smoothedPressure, THRESHOLD, 4095, 10, 255);
    brightness = constrain(brightness, 0, 255);

    // Fixed orange-yellow color
    fill_solid(leds, NUM_LEDS, CHSV(HUE_ORANGE, 255, brightness));
    FastLED.show();
  }

  Serial.print("Pressure: ");
  Serial.print(smoothedPressure);
  Serial.println();

  delay(20);
}
