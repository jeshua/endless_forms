/*
 * FSR Sensor Test
 *
 * Reads the Force Sensitive Resistor and prints values to Serial Monitor.
 * Use this to calibrate PRESSURE_MIN and PRESSURE_MAX values.
 *
 * Wiring (ESP32-C3):
 *   - FSR pin 1 -> 3.3V (or VIN rail)
 *   - FSR pin 2 -> GPIO 2 AND 10K resistor to GND
 *
 * Open Serial Monitor at 115200 baud to see values.
 */

#define FSR_PIN D0  // XIAO ESP32-C3 pin D0/A0

void setup() {
  Serial.begin(115200);
  Serial.println("FSR Test Starting...");
  Serial.println("Press the sensor and watch the values!");
  Serial.println("=====================================");

  // Configure ADC
  analogReadResolution(12);       // 0-4095 range
  analogSetAttenuation(ADC_11db); // Full 3.3V range
}

void loop() {
  int value = analogRead(FSR_PIN);

  // Visual bar graph
  int barLength = map(value, 0, 4095, 0, 50);
  Serial.print("Value: ");
  Serial.print(value);
  Serial.print("\t|");
  for (int i = 0; i < barLength; i++) {
    Serial.print("=");
  }
  Serial.println("|");

  delay(100);
}
