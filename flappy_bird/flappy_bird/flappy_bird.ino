#include <WiFi.h>
#include <WiFiClient.h>
#include <WebServer.h>

// Replace with your settings
const char *ssid = "ESP32-Access-Point";
const char *password = "12345678";

WebServer server(80);

#define ANALOG_PIN 4
#define ADC_RESOLUTION 4095

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);

  WiFi.softAP(ssid, password); // Start ESP32 as an access point
  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);

  server.on("/", HTTP_GET, []() {
    int adcValue = analogRead(ANALOG_PIN);
    float voltage = adcValue * (3.3 / ADC_RESOLUTION);
    server.send(200, "text/plain", String(voltage));
  });

  server.begin();
}

void loop() {
  server.handleClient();
}
