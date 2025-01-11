#include <Arduino.h>
#include <HardwareSerial.h>
#include <string.h>

// Function prototypes
void stringToHex(const char* str, char* hexOutput);
uint8_t calculateChecksum(uint8_t lengthByte, uint8_t* payload, int payloadLength);
void stopDataSubscription(HardwareSerial& serial);

HardwareSerial serial(1);

void setup() {
    // Serial configuration
    serial.begin(19200, SERIAL_8N1, 17, 16); // TX=17, RX=16
    delay(2000);

    // Example payloads
    uint8_t payload[] = {0x08, 0x00, 0x0D, 0x08, 0x00, 0x46};
    uint8_t lengthByte = 0x0A; // Example length byte

    // Calculate checksum
    uint8_t checksum = calculateChecksum(lengthByte, payload, sizeof(payload));

    // Assemble the packet
    char packet[256];
    sprintf(packet, "{MC%02X%02X%02X%02X%02X%02X}", lengthByte, checksum, payload[0], payload[1], payload[2], payload[3]);

    // Send the packet
    serial.write((uint8_t*)packet, strlen(packet));

    // Print the response
    while (serial.available()) {
        char response = serial.read();
        Serial.print(response);
    }

    // Stop data subscription
    stopDataSubscription(serial);
}

void loop() {
    // Continuous listening loop
    if (serial.available()) {
        char response = serial.read();
        Serial.print(response);
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
