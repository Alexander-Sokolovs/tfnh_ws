#include <Arduino.h>
#include <AccelStepper.h>
#include <TimedAction.h>

#define trigPinLHS 8 //attach pin D3 Arduino to pin Trig of HC-SR04
#define echoPinLHS 9 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPinRHS 11 //attach pin D3 Arduino to pin Trig of HC-SR04
#define echoPinRHS 10// attach pin D2 Arduino to pin Echo of HC-SR04

#define PUL 8
#define DIR 9
#define MICROSTEP 2 // set with DIP switches on the motor driver

#define ACCEL 500
#define MAXSPEED 1440

float deg = MICROSTEP/1.8;

long duration; // variable for the duration of sound wave travel
int distance; // variable for the distance measurement

AccelStepper motor1(AccelStepper::DRIVER, PUL, DIR);
AccelStepper motor2(AccelStepper::DRIVER, PUL, DIR);

char *ptr = NULL;


void setup() {
  pinMode(trigPinLHS, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPinLHS, INPUT); // Sets the echoPin as an INPUT
  pinMode(trigPinRHS, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPinRHS, INPUT); // Sets the echoPin as an INPUT
  
  motor1.setAcceleration(ACCEL);
  motor1.setMaxSpeed(10000);
  
  motor2.setAcceleration(ACCEL);
  motor2.setMaxSpeed(10000);
  Serial.begin(1000000);
}

// Ultrasonic
int get_us_dist(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
  // Displays the distance on the Serial Monitor
  return distance;
}

void send_us_dist(){
  int left = get_us_dist(trigPinLHS, echoPinLHS);
  int right = get_us_dist(trigPinRHS, echoPinRHS);
  //Serial.print("[");
  Serial.print(left);
  //Serial.print("]");
  //Serial.print("[");
  Serial.println(right);
  //Serial.println("]");
  //update_speed();
}


int get_motor_speed(int percent) {
  return (MAXSPEED/100)*percent;
}


// Updates motor speeds from serial message
int spd;
int spd2;
void update_speed(){

  spd = Serial.readStringUntil(',').toInt();
  spd2 = Serial.readStringUntil('\n').toInt();

  //Serial.flush();
  //Serial.println(spd);
}


TimedAction speed_update_action = TimedAction(100, update_speed);
TimedAction us_update_action = TimedAction(100, send_us_dist);

void loop() {
  motor1.runSpeed(); 
  motor2.runSpeed(); 
  speed_update_action.check();
  
  us_update_action.check();
  
    if(0 < spd <= 100){
      motor1.setSpeed(-get_motor_speed(spd)*deg); 
      //Serial.println(spd);
  }
  if(0 < spd2 <= 100){
      motor2.setSpeed(-get_motor_speed(spd2)*deg); 
      //Serial.println(spd2);
  }
}
