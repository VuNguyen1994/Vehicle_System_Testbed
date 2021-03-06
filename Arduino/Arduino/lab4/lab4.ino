int photo_pin = A0;
int val1 = 0;
unsigned int val = 0;
float counter = 0.0;
unsigned int retry = 0;

void setup(){
  Serial.begin(9600);
  pinMode(5,OUTPUT);
}

void loop(){
  if (Serial.available() >0){
    val=Serial.parseInt();
    analogWrite(5,counter);
    //delay(100);
    val1 = analogRead(photo_pin);
    Serial.println(val1);
    if (retry > 4){
      counter +=2.55;
      retry = 0;
    }
    retry += 1;
  }
}
