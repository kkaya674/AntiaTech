const int in1 = 8;     // Motor sürücümüze bağladığımız pinleri tanımlıyoruz
const int in2 = 9;     
const int in3 =  10;
const int in4 =  11;
void setup() 
{
pinMode(in1, OUTPUT);  //Tüm pinlerden güç çıkışı olacağı için OUTPUT olarak ayarladık.
pinMode(in2, OUTPUT);  
pinMode(in3, OUTPUT);
pinMode(in4, OUTPUT);
}
void loop() 
{
// motor 1
digitalWrite(in1, HIGH);
digitalWrite(in2,  LOW);  
// motor 2
digitalWrite(in3, HIGH);
digitalWrite(in4,  LOW);
}
