/*
Analog Pin Operation. Lab 1 Experiment 2
 */

int led = 5;           // the pin that the LED is attached to
String brightness = ""; // how bright the LED is
int intensity = 0;
float duty = 0.0;

// the setup routine runs once when you press reset:
void setup() {
  // declare pin 13 to be an output:
  pinMode(led, OUTPUT);
  Serial.begin(9600); 
}

// the loop routine runs over and over again forever:
void loop() {
  if(Serial.available()) {
  brightness = Serial.readString();
  Serial.println("Brightness:" + brightness);
  intensity = brightness.toInt();
  // reverse the direction of the fading at the ends of the fade:
  if (intensity >= 0 && intensity <= 255) {   
    // set the brightness of pin 13:
    analogWrite(led, intensity);
  }
  else{
    Serial.println("Invalid. Enter a number from 0-255");
  }
  }
  duty = 0.05;
  if (duty <= 1.0 and duty >= 0.05){
    duty += 0.05;
  }
  else{
    duty = 0.05;
  }
  intensity = (int) (duty * 255);
  analogWrite(led,intensity);
  delayMicroseconds(100);
  
}
