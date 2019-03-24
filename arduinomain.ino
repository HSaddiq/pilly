// Include the library

#include "Arduino.h"
#include <CheapStepper.h>
#include "Servo.h"

// Declare the stepper and connect pins 
CheapStepper stepper1 (8,9,10,11);
Servo pusher;
Servo sorter;


String pill_string;
int pill_array[] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

void push_pill(int n) {
  while(n>0) {
    pusher.write(80);
    delay(300);
    pusher.write(100);
    delay(100);
  }
}

void setup() {
  // Set speed, ideal range between 10rpm and 22rpm
  stepper1.setRpm(9); //lower = more torque
  pusher.attach(9);
  sorter.attach(10);

  // Set up a serial connection and print some stepper info to the console
  Serial.begin(9600);

  //set the stepper to the home position
  stepper1.moveToDegree(true, 0);
  
}

void loop() {
  
  //blocking read on the terminal until a newline comes through
  pill_string = Serial.readStringUntil("\n");
  for(int i=0;i<18;i++){
    pill_array[i] = atoi(pill_string[i]);
  }

  //test that serial connection was made successfully
  for(int s = 0; s < sizeof(pill_array)/sizeof(pill_array[0]);s++) {
    Serial.println(pill_array[s]);
  }

  //go through each pill type and put in in the boxes it needs to go in
  for (int p = 0; p<6; p++) {
    sorter.write(80);//box1pos
    push_pill(pill_array[p]);
    sorter.write(90);//box2pos
    push_pill(pill_array[p+6]);
    sorter.write(100); //box3pos
    push_pill(pill_array[p+12]);
    stepper1.moveDegreesCW (60);
  }
  stepper1.moveToDegree(true, 0); //return to home

  delay(100);
  digitalWrite(8,LOW); //turn off motors - might get rid of this if not needed
  digitalWrite(9,LOW);
  digitalWrite(10,LOW);
  digitalWrite(11,LOW); 
  delay(300);
  
}

