/*  Arduino DC Motor Control - PWM | H-Bridge | L298N
         Example 02 - Arduino Robot Car Control
    by Dejan Nedelkovski, www.HowToMechatronics.com
*/

/* RIGHT SHIT */
#define enA 6
#define in1 A4
#define in2 A5
#define enB 9
#define in3 A6
#define in4 A7

/* LEFT SHIT */
//#define enA 3
//#define in1 16
//#define in2 14
//#define enB 5
//#define in3 15
//#define in4 17

int motorSpeedA = 0;
int motorSpeedB = 0;

void setup() {
//  pinMode(enA, OUTPUT);
//  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  
  delay(50);
  
  Serial.begin(9600);
  
//  int in1Arr[2] = {HIGH, LOW};
//  int in2Arr[2] = {LOW, HIGH};
//  
//  for(int j = 0; j < 2; j++) {
//    digitalWrite(in1, in1Arr[j]);
//    digitalWrite(in2, in2Arr[j]);
//
//    digitalWrite(in3, in1Arr[j]);
//    digitalWrite(in4, in2Arr[j]);
// }
}

void loop() {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);

  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  
  for(int i = 0; i < 1024; i += 32) {
    motorSpeedA = map(i, 0, 1023, 0, 255);
    motorSpeedB = map(i, 0, 1023, 0, 255);
    
    Serial.println(motorSpeedA);
    
    analogWrite(enA, motorSpeedA); // Send PWM signal to motor A
    analogWrite(enB, motorSpeedB); // Send PWM signal to motor B
    
    delay(500);
  }
    
  while(true) {}
}
