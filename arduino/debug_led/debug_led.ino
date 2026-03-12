/*
 * Debug - Simple LED test
 */

#include <FastLED.h>

#define LED_PIN     D1
#define NUM_LEDS    7

CRGB leds[NUM_LEDS];

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("=== LED TEST ===");

  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(255);

  fill_solid(leds, NUM_LEDS, CRGB::Red);
  FastLED.show();
  Serial.println("LEDs should be RED");
}

void loop() {
  delay(1000);
}
