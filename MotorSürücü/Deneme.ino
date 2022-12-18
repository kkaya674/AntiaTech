#include <L298N.h> // include the L298N library

// define the pins for the motor driver
#define ENA 6
#define IN1 7
#define IN2 8

// define the pin for the potentiometer
#define POT A0

// create an instance of the L298N class
L298N motor(ENA, IN1, IN2);

void setup() {
  // set the motor driver pins as outputs
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
}

void loop() {
  // read the value of the potentiometer
  int potValue = analogRead(POT);
  
  // map the potentiometer value to a range of speeds
  int speed = map(potValue, 0, 1023, 0, 255);
  
  // set the speed of the motor using the L298N library
  motor.setSpeed(speed);
}
