#include <Arduino.h>
#include <HardwareSerial.h>
#include <TFT_eSPI.h> // Include the TFT library
#include <string.h>

// Function prototypes
void stringToHex(const char* str, char* hexOutput);
uint8_t calculateChecksum(uint8_t lengthByte, uint8_t* payload, int payloadLength);
void stopDataSubscription(HardwareSerial& serial);
void updateDisplay(float boilerTemp, float pufferladezustandTemp, float abgasTemp);

// Initialize TFT display
TFT_eSPI tft = TFT_eSPI();

HardwareSerial serial(1);

void setup() {
    // Initialize TFT display
    tft.init();
    tft.setRotation(1);
    tft.fillScreen(TFT_BLACK);
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.setTextSize(2);

    // Serial configuration
    serial.begin(19200, SERIAL_8N1, 17, 16); // TX=17, RX=16
    delay(2000);

    // Example payloads for Boiler, Pufferladezustand, and Abgas
    uint8_t payload[] = {0x08, 0x00, 0x0D, 0x08, 0x00, 0x4B, 0x08, 0x00, 0x0F};
    uint8_t lengthByte = 0x0A; // Example length byte

    // Calculate checksum
    uint8_t checksum = calculateChecksum(lengthByte, payload, sizeof(payload));

    // Assemble the packet
    char packet[256];
    sprintf(packet, "{MC%02X%02X%02X%02X%02X%02X%02X%02X%02X%02X}", lengthByte, checksum,
            payload[0], payload[1], payload[2],
            payload[3], payload[4], payload[5],
            payload[6], payload[7], payload[8]);

    // Send the packet
    serial.write((uint8_t*)packet, strlen(packet));
}

void loop() {
    // Read response
    if (serial.available()) {
        char response = serial.read();
        Serial.print(response);

        // Parse the response to get the temperatures (pseudo-parsing here, actual implementation depends on the protocol)
        float boilerTemp = 60.0; // Example value, replace with parsed data
        float pufferladezustandTemp = 45.0; // Example value, replace with parsed data
        float abgasTemp = 120.0; // Example value, replace with parsed data

        // Update the display with the parsed temperatures
        updateDisplay(boilerTemp, pufferladezustandTemp, abgasTemp);
    }
    delay(30000); // Sleep for 30 seconds
}

void stringToHex(const char* str, char* hexOutput) {
    while (*str) {
        sprintf(hexOutput, "%02X", *str++);
        hexOutput += 2;
    }
}

uint8_t calculateChecksum(uint8_t lengthByte, uint8_t* payload, int payloadLength) {
    uint8_t checksum = lengthByte;
    for (int i = 0; i < payloadLength; ++i) {
        checksum += payload[i];
    }
    return checksum % 256;
}

void stopDataSubscription(HardwareSerial& serial) {
    char stopCommand[] = "{ME00}";
    serial.write((uint8_t*)stopCommand, strlen(stopCommand));
    serial.end();
}

void updateDisplay(float boilerTemp, float pufferladezustandTemp, float abgasTemp) {
    tft.fillScreen(TFT_BLACK);

    // Display Boiler Temperature
    tft.setCursor(10, 30);
    tft.printf("Boiler Temp: %.2f C", boilerTemp);

    // Display Pufferladezustand Temperature
    tft.setCursor(10, 70);
    tft.printf("Pufferlade: %.2f C", pufferladezustandTemp);

    // Display Abgas Temperature
    tft.setCursor(10, 110);
    tft.printf("Abgas Temp: %.2f C", abgasTemp);
}
