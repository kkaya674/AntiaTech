int vibr_Pin_4 = 17;
int vibr_Pin_3 = 16;
int vibr_Pin_1 = 14;
int vibr_Pin_2 = 15;
int threshold1 = 5;
int threshold2 = 10;
int threshold0 = 8;
long var1 = 0;
long var2 = 0;
long var3 = 0;
int var4 = 0;
int ct = 0;
long var1_next = 0;
long var2_next = 0;
long var3_next = 0;
long var4_next = 0;
long current_time = 0;

int delay_val = 8;
void setup() {
  // put your setup code here, to run once:
pinMode(vibr_Pin_1, INPUT);
pinMode(vibr_Pin_2, INPUT);
pinMode(vibr_Pin_3, INPUT);
pinMode(vibr_Pin_4, INPUT);
Serial.begin(9600);
}

void loop() {

  var1 = 4*2.5*analogRead(vibr_Pin_1);
  var2 = 4*2.2*analogRead(vibr_Pin_2);
  var3 = 4*2.9*analogRead(vibr_Pin_3);
  var4 = 4*1.5*analogRead(vibr_Pin_4);
  
  if(var1>threshold0 || var2>threshold0 || var3>threshold0 || var4>threshold0){
    current_time = millis(); 
    //Serial.println(current_time);
    while(millis()<current_time+delay_val){
      var1_next += 4*2.5*analogRead(vibr_Pin_1);
      var2_next += 4*2.2*analogRead(vibr_Pin_2);
      var3_next += 4*2.9*analogRead(vibr_Pin_3);
      var4_next += 4*1.5*analogRead(vibr_Pin_4);
      ct += 1; 
    }
     //Serial.println(var1_next);
      var1 = var1_next / ct;
      var2 = var2_next / ct;
      var3 = var3_next / ct;
      var4 = var4_next / ct;
      /*
      Serial.print(var1);
      Serial.print(",");
      Serial.print(var2);
      Serial.print(",");
      Serial.print(var3);
      Serial.print(",");
      Serial.println(var4);
      */
      ct = 0;
      var1_next = 0 ;
      var2_next = 0 ;
      var3_next = 0 ;
      var4_next = 0 ;

  }
  



  if(var1>threshold0){
    if((var1 - var2)>threshold1 && (var1 - var3)>threshold1 && (var1 - var4)>threshold2){
      if((var3-var4)>threshold1 &&(var2-var4)>threshold1){
          Serial.print("1. bölge, 1.sensor= ");
          Serial.println(var1);
          delay(100);
      }
    }
  }

    if(var2>threshold0 || var1>threshold0){
    if(abs(var1 - var2)<threshold1 && abs(var3 - var4)<threshold1){
      if((var1-var4)>threshold1 &&(var2-var4)>threshold2 && (var2-var3)>threshold2 && (var2-var4)>threshold1 ){
          Serial.print("2. bölge, 1.sensor= ");
          Serial.print(var1);
          Serial.print("       2.sensor= ");
          Serial.println(var2);
          delay(100);
      }
    }
  }

    if(var2>threshold0){
    if((var2 - var1)>threshold1 && (var2 - var3)>threshold2 && (var2 - var4)>threshold1){
      if((var4-var3)>threshold1 &&(var1-var3)>threshold1){
          Serial.print("3. bölge, 2.sensor= ");
          Serial.println(var2);
          delay(100);
      }
    }
  }

    if(var3>threshold0){
    if((var3 - var1)>threshold1 && (var3 - var4)>threshold1 && (var3 - var2)>threshold2){
      if((var4-var2)>threshold1 &&(var1-var2)>threshold1){
          Serial.print("4. bölge, 3.sensor= ");
          Serial.println(var3);
          delay(100);
      }
    }
  }


    if(var3>threshold0 || var4>threshold0){
    if(abs(var1 - var2)<threshold1 && abs(var3 - var4)<threshold1){
      if((var3-var1)>threshold1 &&(var3-var2)>threshold2 && (var4-var1)>threshold2 && (var4-var2)>threshold1 ){
          Serial.print("5. bölge, 3.sensor= ");
          Serial.print(var3);
          Serial.print("       4.sensor= ");
          Serial.println(var4);
          delay(100);
      }
    }
  }

    if(var4>threshold0){
    if((var4- var2)>threshold1 && (var4 - var3)>threshold1 && (var4 - var1)>threshold2){
      if((var3-var1)>threshold1 &&(var2-var1)>threshold1){
          Serial.print("6. bölge, 4.sensor= ");
          Serial.println(var4);
          delay(100);
      }
    }
  }
 
}
