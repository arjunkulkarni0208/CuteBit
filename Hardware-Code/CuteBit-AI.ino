#include <Wire.h>
#include <Adafruit_SSD1306.h>
#include <FluxGarage_RoboEyes.h> 

int l1 = 25;
int l2 = 26;
int r1 = 18;
int r2 = 19;
int ir = 4;

int rt = 360;
int lt = 320;

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET     -1 
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
RoboEyes<Adafruit_SSD1306> roboEyes(display); 

void setup() {
  pinMode(l1, OUTPUT);
  pinMode(l2, OUTPUT);
  pinMode(r1, OUTPUT);
  pinMode(r2, OUTPUT);
  Serial.begin(9600);
  Serial.setTimeout(10);

  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3C or 0x3D
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  } // Don't proceed, loop forever
  
  roboEyes.begin(SCREEN_WIDTH, SCREEN_HEIGHT, 100);

  roboEyes.setAutoblinker(ON, 3, 2); // Start auto blinker animation cycle -> bool active, int interval, int variation -> turn on/off, set interval between each blink in full seconds, set range for random interval variation in full seconds
  //roboEyes.setIdleMode(ON, 2, 2); 
  // Start idle animation cycle (eyes looking in random directions) -> turn on/off, set interval between each eye repositioning in full seconds, set range for random time interval variation in full seconds
  


}

void front(int t=0){
  digitalWrite(l1,LOW);
  digitalWrite(r1,HIGH);
  digitalWrite(l2,HIGH);
  digitalWrite(r2,LOW);
  delay(t);
}
void back(int t=0){
  digitalWrite(l1,HIGH);
  digitalWrite(r1,LOW);
  digitalWrite(l2,LOW);
  digitalWrite(r2,HIGH);
  delay(t);
}
void right(int t=0){
  digitalWrite(l1,LOW);
  digitalWrite(r1,LOW);
  digitalWrite(l2,HIGH);
  digitalWrite(r2,HIGH);
  delay(t);
}
void left(int t=0){
  digitalWrite(l1,HIGH);
  digitalWrite(r1,HIGH);
  digitalWrite(l2,LOW);
  digitalWrite(r2,LOW);
  delay(t);
}
void stop(int t=0){
  digitalWrite(l1,LOW);
  digitalWrite(r1,LOW);
  digitalWrite(l2,LOW);
  digitalWrite(r2,LOW);
  delay(t);
}


void loop() {
  roboEyes.update();

  // --- STANDARD SERIAL PARSING ---
  if (Serial.available() > 0) {
    
    // Read first number (Movement)
    int moveVal = Serial.parseInt();
    
    // Read second number (Emotion)
    int emoteVal = Serial.parseInt();

    // Clear buffer (read until newline)
    if (Serial.read() == '\n') {
      
      // Movement
      switch(moveVal){
        case 0: stop(); break;
        case 1: front(); break;
        case 2: right(); break;
        case 3: left(); break;
        case 4: back(); break;
      }

      // Emotion
      switch(emoteVal){
        case 0: roboEyes.setMood(DEFAULT); break;
        case 1: roboEyes.setMood(HAPPY); break;
        case 2: roboEyes.setMood(ANGRY); break;
        case 3: roboEyes.setMood(TIRED); break;
      }
    }
  }
}