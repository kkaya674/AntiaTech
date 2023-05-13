
// define the pins for the motor driver

#define ENA 3
#define IN1_1 2
#define IN1_2 4 
#define ENB 6
#define IN2_1 7
#define IN2_2 8

// define the pin for the potentiometer
#define POT A0



void setup() {
  Serial.begin(9600);
  // set the motor driver pins as outputs
  pinMode(ENA, OUTPUT);
  pinMode(IN1_1, OUTPUT);
  pinMode(IN2_1, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(IN1_2, OUTPUT);
  pinMode(IN2_2, OUTPUT);
}

void loop() {
  // read the value of the potentiometer
  int potValue = analogRead(POT);
  
  // map the potentiometer value to a range of speeds
  int speed = map(potValue, 0, 1023, 0, 255);
  
  // set the speed of the motor using the L298N library
  digitalWrite(IN1_1,HIGH);
  digitalWrite(IN1_2,LOW);
  digitalWrite(IN2_1,HIGH);
  digitalWrite(IN2_2,LOW);
  analogWrite(ENA,speed);
  analogWrite(ENB,speed);
}
