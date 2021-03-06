int ledpin = 5;
float temp1=0;
float dutycycle = 0.05;
int photocellPin = 0;       // cell at a0
int photocellReading;
int count = 0;
float volLED = 0.0;
float volphoto = 0.0;
 
void setup() {
  // Timer 3 - Fast PWM
  TCCR3A=0b10000010;
  TCCR3B=0b00011100;
  OCR3A= 1000;
  ICR3 = 1000;
  TCNT3=0;
  pinMode(ledpin,OUTPUT);
  Serial.begin(9600);
  interrupts();
}
void loop() {
    //count += 1;
   for (dutycycle = 0; dutycycle <= 1.0; dutycycle +=0.05){
   temp1 = dutycycle*ICR3;
   OCR3A = (int) temp1;
   delay(2000);
   photocellReading = analogRead(photocellPin);
   Serial.print("duty cycle = "); Serial.println(dutycycle);
   Serial.print("photoread = ");Serial.println(photocellReading);
   volLED = 5 - dutycycle*5;
   Serial.print("voltage resistor LED circuit = "); Serial.println(volLED);
   volphoto = 5 - photocellReading*5.0/255.0;
   Serial.print("voltage resistor photocell circuit= "); Serial.println(volphoto);
   }
//   for (dutycycle = 1.0; dutycycle >= 0.05; dutycycle -=0.05){
//   temp1 = dutycycle*ICR3;
//   OCR3A = (int) temp1;
//   delay(2000);
//   photocellReading = analogRead(photocellPin);
//   Serial.print("photocell reading = ");
//   Serial.println(photocellReading);      // raw analog reading 
//   }
   
}

ISR(TIMER3_COMPA_vect){
  digitalWrite(ledpin, !digitalRead(ledpin));
}
