int ledpin[] = {13,11,5,6};
int i;
int pass;
int a,b,c,d;
int ina,inb,inc,ind;
int f0 = 2560;
int f1 = 1;
int f3 = 1;
int f4 = 1;
int flag0 =0, flag1=0, flag3=0, flag4 = 0; //init = 0, no impact
int count0 = 0;
int attempt = 0;
int cycle8bit = 245; // 245/1000 ms


void setup() {

  pass = random(10000);
  a = pass/1000;
  b = (pass%1000)/100;
  c = (pass%100)/10;
  d = pass%10;
  
  Serial.begin(9600);
  Serial.println(pass);
  
  for (i = 0; i <= 3; i++){
    pinMode(ledpin[i],OUTPUT);
    digitalWrite(ledpin[i],LOW);
  }
  
  noInterrupts();
  
  // Timer 0
  TCCR0A = 0;
  TCCR0B = 0;
  TCNT0 = 0;
  TCCR0B |= (1 << WGM02);   // CTC mode
  TCCR0B |= (1 << CS02);    // 256 prescaler 
  TIMSK0 |= (1 << OCIE0A);
  OCR0A= 16000000 / (256 * f0);
  
  // Timer 1
  TCCR1A = 0;
  TCCR1B = 0;
  TCNT1 = 0;
  TIMSK1=0;
  TCCR1B |= (1 << WGM12);   // CTC mode
  TCCR1B |= (1 << CS12) | (0<<CS11) | (0<<CS10);    // 256 prescaler 
  TIMSK1 |= (1 << OCIE1A);
  OCR1A= 16000000 / (256 * f1);
  
  // Timer 3
  TCCR3A=0;
  TCCR3B=0;
  TCNT3=0;
  TIMSK3=0;
  TCCR3B |= (1<<WGM32);
  TCCR3B |= (1<<CS32) | (0<<CS31) | (0<<CS30);
  TIMSK3 |= (1<<OCIE3A);
  OCR3A= 16000000 / (256 * f3);

   //Timer 4
  TCCR4A = 0;
  TCCR4B = 0;
  TCNT4 = 0;
  TCCR4B |= (1 << WGM42);   // CTC mode
  TCCR4B |= (1 << CS42)| (0<<CS41) | (0<<CS40);    // 256 prescaler 
  TIMSK4 |= (1 << OCIE4A);
  OCR4A= 16000000 / (256 * f4);
  
  interrupts();
  
}

void loop() {
  if(Serial.available() > 0) {
    int inpass = Serial.parseInt();
    attempt++;
    
    if (attempt > 5){
      Serial.println("Max attempt reached. Please reload!");
    }
    else if (attempt == 5){
      Serial.println("Max attempt reached: 5. LEDs solid!");
      flag0=2; flag1=2; flag3=2; flag4 = 2; // 2 to solid LED
    }
    else{     //only for attempt < 5
      Serial.print("I received: "); Serial.println(inpass,DEC);
      Serial.print("No. attempt: "); Serial.println(attempt,DEC);
      
      ina = inpass/1000;
      inb = (inpass%1000)/100;
      inc = (inpass%100)/10;
      ind = inpass%10;
      
      if(a != ina){
        f0 +=100;
        cycle8bit /= 2;
      }
      else{
        flag0 = 1;
      }
        
      if(b != inb){
        f1 += 2;
        OCR1A= 16000000 / (256 * f1);
      }
      else{
        flag1 = 1;
      }
        
      if(c != inc){
        f3 += 2;
        OCR3A= 16000000 / (256 * f3);  
      }
      else{
        flag3=1;
      }   
         
      if(d != ind){
        f4 += 2;
        OCR4A= 16000000 / (256 * f4);  
      }
      else{
        flag4=1;
      }
    }
  }  
}

ISR(TIMER0_COMPA_vect){
 if (flag0 == 0){
  count0 += 1;
  if (count0 >= cycle8bit){
    count0 = 0;
    digitalWrite(ledpin[0],!digitalRead(ledpin[0]));
  }
 }
 else if (flag0 == 1) {
  digitalWrite(ledpin[0],LOW);
  detachInterrupt(digitalPinToInterrupt(ledpin[0]));
 }
 else if (flag0 == 2) {
  digitalWrite(ledpin[0],HIGH);
  detachInterrupt(digitalPinToInterrupt(ledpin[0]));
 }
}

ISR(TIMER1_COMPA_vect){
  if (flag1 == 0){
   digitalWrite(ledpin[1],!digitalRead(ledpin[1]));
  }
  else if (flag1 == 1)
  {
   digitalWrite(ledpin[1],LOW);
   detachInterrupt(digitalPinToInterrupt(ledpin[1])); 
  }
  else if (flag1 == 2) {
  digitalWrite(ledpin[1],HIGH);
  detachInterrupt(digitalPinToInterrupt(ledpin[1]));
 }
}

ISR(TIMER3_COMPA_vect){
  if (flag3 == 0){
   digitalWrite(ledpin[2],!digitalRead(ledpin[2]));
  }
  else if (flag3 == 1)
  {
   digitalWrite(ledpin[2],LOW);
   detachInterrupt(digitalPinToInterrupt(ledpin[2])); 
  }
  else if (flag3 == 2) {
  digitalWrite(ledpin[2],HIGH);
  detachInterrupt(digitalPinToInterrupt(ledpin[2]));
 }
}

ISR(TIMER4_COMPA_vect){
  if (flag4 == 0){
   digitalWrite(ledpin[3],!digitalRead(ledpin[3]));
  }
  else if (flag4 == 1)
  {
   digitalWrite(ledpin[3],LOW);
   detachInterrupt(digitalPinToInterrupt(ledpin[3])); 
  }
  else if (flag4 == 2) {
  digitalWrite(ledpin[3],HIGH);
  detachInterrupt(digitalPinToInterrupt(ledpin[3]));
 }
}
