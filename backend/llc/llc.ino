#include <ros.h>
#include <std_msgs/Float64MultiArray.h>
#include <std_msgs/Float32MultiArray.h>

#include <Servo.h>

ros::NodeHandle nh;

//int ledPin = 13;

int frontLeft = 6;
int frontRight = 3;  
int backLeft = 7;
int backRight = 5;

float frontLeftVal = 0.0;
float frontRightVal = 0.0;
float backLeftVal = 0.0;
float backRightVal = 0.0;

/* RIGHT SHIT */     //The logic pins are the in* pins, these take a low or high value
#define enA 6        //to turn the motor, the enable pins are pwm driven and take 0-255
#define in1 A4       //Most of the logic is here and done correctly, I just need to make 
#define in2 A5       //the proper adjustments so the proper pins are being written to
#define enB 9
#define in3 7
#define in4 8

/* LEFT SHIT */
#define enC 3
#define in5 16
#define in6 14
#define enD 5
#define in7 15
#define in8 17

struct Motor {
  int en;
  int p1;
  int p2;
};

struct Motor bleft = {enC,in5,in6};
struct Motor fleft = {enD,in8,in7};
struct Motor fright = {enA,in2,in1};
struct Motor bright = {enB,in4,in3};

const unsigned int MIN_MOTOR_SPEED = 50;
const unsigned int MAX_MOTOR_SPEED = 254;

const unsigned int WHEEL = 0;

const unsigned int NUM_TYPES = 7;

const unsigned int PIN_MAP_SZ = 4;

struct Motor pinMapping[PIN_MAP_SZ] = {fleft,fright,bleft,bright};

//int pinMap[PIN_MAP_SZ] = {frontLeft, frontRight, backLeft, backRight};
int pinTypes[PIN_MAP_SZ] = {WHEEL, WHEEL, WHEEL, WHEEL};
float pinMapVals[PIN_MAP_SZ] = {0.0, 0.0, 0.0, 0.0};

//const unsigned int LIMIT_MAP_SZ = 2;
//int limitMap[LIMIT_MAP_SZ] = {dumperLimit, tiltLimit};

int typeMins[NUM_TYPES] = {  MIN_MOTOR_SPEED, // WHEEL
                             MIN_MOTOR_SPEED, // AUGER_SPIN
                             MIN_MOTOR_SPEED, // AUGER_TILT
                             MIN_MOTOR_SPEED, // DUMPER
                             MIN_MOTOR_SPEED, // CAMERA
                             MIN_MOTOR_SPEED, // AUGER_OUT
                             MIN_MOTOR_SPEED  // SERVO
};

int typeMaxes[NUM_TYPES] = { 254, // WHEEL
                             254, // AUGER_SPIN
                             254, // AUGER_TILT
                             254, // DUMPER
                             254, // CAMERA
                             254, // AUGER_OUT
                             254  // SERVO
};

void runCustomPWM(float val, int pinIndex, int mini, int maxi) {
  float newVal = mini;
  //int pin = pinMap[pinIndex]; 
  int pin = pinMapping[pinIndex].en;
  
  pinMapVals[pinIndex] = val;

  float range = maxi - mini;
  
  // -1 to 0
  if(val >= -1 && val < 0){
    newVal = ((val * -1) * range) + mini;
    digitalWrite(pinMapping[pinIndex].p1,HIGH);
    digitalWrite(pinMapping[pinIndex].p2,LOW);
  }
  // 0 to 1
  if(val <= 1 && val > 0){
    newVal = (val * range) + mini;
    digitalWrite(pinMapping[pinIndex].p2,HIGH);
    digitalWrite(pinMapping[pinIndex].p1,LOW);
  }
  
  analogWrite(pin, newVal);
}

int lastLedVal = LOW;

// TODO: Gets the message, but does not always call the callback function. Spin-once is likely terminating early.
void messageCallback( const std_msgs::Float32MultiArray& message){
  for(int i = 0; i < PIN_MAP_SZ; i++) {
    if(i < message.data_length) {
      //runPWM(message.data[i], pinMap[i]);
        int type = pinTypes[i];
      
        runCustomPWM(message.data[i], i, typeMins[type], typeMaxes[type]);
    }
  }
  
//  digitalWrite(ledPin, lastLedVal);
//  
//  if(lastLedVal == HIGH) lastLedVal = LOW;
//  else                   lastLedVal = HIGH;
}

int getIndex(int pin) {
  for(int i = 0; i < PIN_MAP_SZ; i++) {
    if(pinMapping[i].p1 == pin) {
      return i;
    }
    //if(pinMap[i] == pin) {
    //  return i;
    //}
  }
  
  return -1;
}

ros::Subscriber<std_msgs::Float32MultiArray> sub("a", &messageCallback);

void setup() {
  Serial.begin(57600);
  for(int i = 0; i < PIN_MAP_SZ; i++) {
      pinMode(pinMapping[i].p1,OUTPUT);
      pinMode(pinMapping[i].p2,OUTPUT);   
  }
  
  nh.initNode();
  nh.subscribe(sub);
}

void loop(){
  nh.spinOnce();

  delay(1);
}
