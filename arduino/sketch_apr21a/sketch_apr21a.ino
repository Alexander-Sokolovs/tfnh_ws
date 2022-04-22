#include <Arduino.h>
#include <AccelStepper.h>
#include <TimedAction.h>

#define PUL 8
#define DIR 9
#define MICROSTEP 2 // set with DIP switches on the motor driver

#define ACCEL 500
#define MAXSPEED 1440

float deg = MICROSTEP/1.8;

AccelStepper motor1(AccelStepper::DRIVER, PUL, DIR);
AccelStepper motor2(AccelStepper::DRIVER, PUL, DIR);

char *ptr = NULL;


void setup() {
  motor1.setAcceleration(ACCEL);
  motor1.setMaxSpeed(10000);
  
  motor2.setAcceleration(ACCEL);
  motor2.setMaxSpeed(10000);
  Serial.begin(1000000);
}


int get_motor_speed(int percent) {
  return (MAXSPEED/100)*percent;
}

void update_speed(){
  Serial.println("Update");  
  char* spd;
  while (Serial.available()){
    int c = Serial.read();
    //Serial.println(c);
    spd += c;
  }
  ptr = strtok(spd, ",");
  Serial.println(ptr);
  int m1 = get_motor_speed(int(ptr[0]));
  int m2 = get_motor_speed(int(ptr[1]));
  motor1.setSpeed(m1*deg); 
  motor2.setSpeed(m2*deg); 
}

TimedAction speed_update = TimedAction(100, update_speed);


void loop() {
  motor1.runSpeed(); 
  motor2.runSpeed(); 
  speed_update.check();
}
