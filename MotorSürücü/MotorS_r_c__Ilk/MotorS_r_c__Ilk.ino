
int Enable_B = 11;
int inputB1 = 6;
int inputB2 = 9;
int i;
int k;
void setup()
{

Serial.begin(9600);
pinMode(Enable_B, OUTPUT);
pinMode(inputB1, OUTPUT);
pinMode(inputB2, OUTPUT);
}
void loop()
{
 
for (i=0; i<120; i++) {
Serial.println(i);
analogWrite(Enable_B,i);
digitalWrite(inputB1,HIGH);
digitalWrite(inputB2,LOW);
delay(100);
}

for(k=120;k>0;k--){
  analogWrite(Enable_B,k);
  digitalWrite(inputB1,HIGH);
  digitalWrite(inputB2,LOW);
  delay(100);
}


}
