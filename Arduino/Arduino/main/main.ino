/* Include the standard Arduino SPI library */
#include <SPI.h>
#include <IRremote.h>
/* Include the RFID library */
#include <RFID.h>
#include "DHT.h"
#define DHTPIN 7     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11
#define speedup 0xFF906F    //Value of Up button
#define speeddown 0xFFE01F  // Value of Down button
#define button1 0xFF30CF 
#define button2 0xFF18E7
#define button3 0xFF7A85

const int trigPin = 5;
const int echoPin = 4;
int motorPin = 6;
int RECV_PIN = 2;
int ledpin = 2;
int i = 0;
unsigned long key_value = 0;
int headlight = 0;        // 0 = OFF, 1 = DIM, 2 = ON

float duration;
int distance;
int newdistance;
int velo = 0;
int authorized = 0;

/* Define the DIO used for the SDA (SS) and RST (reset) pins. */
#define SDA_DIO 9
#define RESET_DIO 8
/* Create an instance of the RFID library */
RFID RC522(SDA_DIO, RESET_DIO); 

IRrecv irrecv(RECV_PIN); 
decode_results results;
DHT dht(DHTPIN, DHTTYPE); // Initialize DHT sensor.

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(motorPin, OUTPUT);
  pinMode(ledpin, OUTPUT);
  Serial.begin(9600);
  
  /* Enable the SPI interface */
  SPI.begin(); 
  /* Initialise the RFID reader */
  RC522.init();
  // Start the receiver
  irrecv.enableIRIn();
  irrecv.blink13(true); 
  
  dht.begin();
}

void loop() {
  /* Has a card been detected? */
  if (RC522.isCard()){
    /* If so then get its serial number */
    RC522.readCardSerial();
    //Serial.println("Card detected:");
    if (strcmp(RC522.serNum,"D9667B9D59")){ //Correct card, authorized
      authorized = 1;
      Serial.println("A");
    }
    else{
      authorized = 0;
      return;
    }
  }
 if (authorized == 1){ //Valid Card, operate as normal
    // Read water level into value var
  int value = analogRead(A0);
  // Read temperature in Fahrenheit into f var
  float f = dht.readTemperature(true);
  // Locking until water level is higher or temperature < 85oF
  if (value < 300 or f > 90){
    value = analogRead(A0);
    // Water level is low, sending 0 distance to signal system for 
    // shutdown, shutdown everything
    distance = 0;
    velo = 0;
    analogWrite(motorPin, velo);
    if (value < 300){
      Serial.println("C");    // Low Coolant   
    }
    if (f > 85){
      Serial.println("T");    // High Temperature
    }
  }
  else{ //Good coolant and temperature, move on normally
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
  
    duration = pulseIn(echoPin, HIGH); //in us
    distance = (duration*.0343)/2;      // in cm
    if (distance >30){ //Max distance to handle is 30
      distance = 30;
    }
    // Handle velocity
    if (distance <= 5){
      velo = 0;
      analogWrite(motorPin, velo);
      Serial.println(distance);
    }
    else if(velo == 0 && distance > 5){ 
      // Safe distance, but just start the engine, 
      // velo will determined by distance
      velo = map(distance, 0 ,30, 0 ,255);
      newdistance = distance;
      Serial.println(distance);
      analogWrite(motorPin, velo);
    }
    else{ //Safe distance and has some initial velo, so user can control speed
      // check if any button pressed and send it to PythonUI
        if (irrecv.decode(&results)) {
          
          if (results.value == 0XFFFFFFFF){
            results.value = key_value;
          }  
          //Serial.println(results.value, HEX); //Debug
          key_value = results.value;
          
          if (key_value == speedup){
            newdistance = newdistance + 3; // 10% of max distance is 3. Control the velo
            velo = map(newdistance, 0, 30,0, 255); //map distance to velo
            Serial.println(newdistance);
            analogWrite(motorPin, velo);
          }
          else if (key_value == speeddown){
            newdistance = newdistance - 3;
            velo = map(newdistance, 0, 30,0, 255); //map distance to velo
            Serial.println(newdistance);
            analogWrite(motorPin, velo);
          }
          else if (key_value == button1 ){
            Serial.println("F"); // Turn off headlight LED
          }
          else if (key_value == button2){
            Serial.println("D"); //Dim headlight LED
          }
          else if (key_value == button3){
            Serial.println("O"); // Turn on high headlight LED
          } 
          irrecv.resume(); // Receive the next value
      }
      else{
        Serial.println(newdistance);
      }
    }
  }
 }
 delay(100);
}
