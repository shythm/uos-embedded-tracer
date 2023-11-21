// Include the necessary libraries
#include <Arduino.h>

// Define the motor control pins
const int leftMotorPWM = 5;  // PWM pin for the left motor
const int leftMotorDir = 4;  // Direction pin for the left motor
const int rightMotorPWM = 3; // PWM pin for the right motor
const int rightMotorDir = 2; // Direction pin for the right motor

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Set motor control pins as output
  pinMode(leftMotorPWM, OUTPUT);
  pinMode(leftMotorDir, OUTPUT);
  pinMode(rightMotorPWM, OUTPUT);
  pinMode(rightMotorDir, OUTPUT);
}

void loop() {
  // Check if there is data available to read
  if (Serial.available() >= 5) {
    // Read the first character to determine the motor (L or R)
    char motorType = Serial.read();

    // Read the second character to determine the direction (+ or -)
    char direction = Serial.read();

    // Read the next three characters as a string and convert to an integer
    String pwmValueString = Serial.readStringUntil('\n');

    // Convert to forward proportional
    int pwmValue = 0;
    if(motorType == 'L') {
      if(direction == '+'){
        pwmValue = pwmValueString.toInt();
      } else {
        pwmValue = 255 - pwmValueString.toInt();
      }
    } else {
      if(direction == '+'){
        pwmValue = 255 - pwmValueString.toInt();
      } else {
        pwmValue = pwmValueString.toInt();
      }
    }

    // Handle Exceptional Value
    if(pwmValue > 255) {
      pwmValue = 255;
    } else if(pwmValue < 0) {
      pwmValue = 0;
    }

    // Determine which motor to control and set the direction
    if (motorType == 'L') {
      analogWrite(leftMotorPWM, abs(pwmValue));
      digitalWrite(leftMotorDir, (direction == '+') ? LOW : HIGH);
    } else if (motorType == 'R') {
      analogWrite(rightMotorPWM, abs(pwmValue));
      digitalWrite(rightMotorDir, (direction == '+') ? HIGH : LOW);
    }
  }
}
