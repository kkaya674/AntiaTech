// Define the pins that the L298N is connected to
int enablePin = 9;
int in1Pin = 8;
int in2Pin = 7;

// Define the pin that the potentiometer is connected to
int potPin = A0;

void setup() {
  // Set the enable, in1, and in2 pins as outputs
  pinMode(enablePin, OUTPUT);
  pinMode(in1Pin, OUTPUT);
  pinMode(in2Pin, OUTPUT);
}

void loop() {
  // Read the value of the potentiometer
  int potValue = analogRead(potPin);

  // Convert the potentiometer value to a motor speed
  int motorSpeed = map(potValue, 0, 1023, 0, 255);

  // Set the motor speed
  analogWrite(enablePin, motorSpeed);

  // Turn the motor on in forward direction
  digitalWrite(in1Pin, HIGH);
  digitalWrite(in2Pin, LOW);
}
