#include <Arduino.h>
#include <WiFi.h>
#include <DHT.h>

// With my actual wifi credidentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// DHT11 or DHT22 Sensor configuration
#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
void setup() {
  Serial.begin(115200);
  dht.begin();
  
  Serial.print("Connecting to WiFi network: ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  
  Serial.println("\nSuccessfully connected to WiFi!");
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP()); 
}

void loop() {
  // Reading temperature
  float t = dht.readTemperature();
  
  // Check if any reads failed
  if (isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
  } else {
    Serial.print("Current Temperature: ");
    Serial.print(t);
    Serial.println(" *C");
  }
  // The program will wait 5 seconds between measurements 
  delay(5000);
}

