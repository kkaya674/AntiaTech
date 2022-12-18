#include <Servo.h>

Servo myservo;  // create servo object to control a servo

int val = 0;    // variable to read the value from the analog pin

void setup() {
  Serial.begin(9600);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
}

void loop() {
   if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    Serial.print("You sent me: ");
    Serial.println(data);
    if(data == "H"){
      val = val + 10;
      if(val >= 180){
      val = 0 ;
      }
      myservo.write(val); 
   }
  
//  if(Serial.available() > 0){
//    String a = Serial.readString();
//    Serial.println("Hello"); 
//    if(a == "0"){
//      val = val + 10;
//      if(val >= 180){
//      val = 0 ;
//      }
//      myservo.write(val);                  // sets the servo position according to the scaled value
//    }
 // }

 delay(500);  
  // waits for the servo to get there
}
}

