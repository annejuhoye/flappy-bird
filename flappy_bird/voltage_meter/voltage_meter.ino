#include <Arduino.h>

#define ANALOG_PIN 4  // Connect analog signal to GPIO4
#define ADC_RESOLUTION 4095  // ADC resolution for ESP32 is 12 bits

void setup() {
  Serial.begin(115200);  // Start serial communication with a baud rate of 115200
  analogReadResolution(12);  // Set ESP32 ADC resolution to 12 bits
}

void loop() {
  int adcValue = analogRead(ANALOG_PIN);  // Read analog value
  float voltage = adcValue * (3.3 / ADC_RESOLUTION);  // Convert analog value to voltage

  Serial.print("ADC Value: ");
  Serial.print(adcValue);  // Output ADC raw value
  Serial.print(" - Voltage: ");
  Serial.print(voltage);  // Output voltage value
  Serial.println(" V");

  delay(10);  // Read once per second
}
