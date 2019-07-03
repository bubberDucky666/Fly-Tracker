#include <Wire.h>
#include <Adafruit_MCP4725.h>
Adafruit_MCP4725 dac;

void setup() {

  // put your setup code here, to run once:
  int volt = 5;
  int pin  = 5;

  int baud = 9600;

  Serial.begin(baud);
  pinMode(pin, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:

  int mes = Serial.read();

  if (mes == 1) {
    dac.setVoltage(volt, false);
  }
  else {
    dac.setVoltage(0, false);
  }
}
