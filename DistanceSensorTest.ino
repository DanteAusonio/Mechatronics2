#include <PID_v1.h>

#define TRIG_PIN 9
#define ECHO_PIN 10
#define LED_PIN 11

double desiredDistance = 20;
double realDistance;
double ledOutput;

// PID parameters
double Kp = 2, Ki = 5, Kd = 1;

// PID Object
PID myPID(&realDistance, &ledOutput, &desiredDistance, Kp, Ki, Kd, DIRECT);


  
void setup() {
  Serial.begin(9600);  // Initialize Serial Monitor

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT); 

  myPID.SetTunings(Kp, Ki, Kd);
  myPID.SetMode(AUTOMATIC); // Enable PID control
  myPID.SetOutputLimits(0, 255); // Ensure LED brightness is within valid range

}



void loop() {
  long duration;
  float distance;

  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Measure the echo pulse duration
  duration = pulseIn(ECHO_PIN, HIGH);

  // Convert duration to distance in cm
  distance = duration * 0.034 / 2;

  realDistance = distance;

  myPID.Compute();

 // Adjust LED brightness based on distance
  // if (realDistance <= desiredDistance - 1) {
    
  // } else if (realDistance >= desiredDistance + 1) {
  //   myPID.Compute();
  // }

  // Constrain LED brightness to valid PWM range (0-255)
  ledOutput = constrain(ledOutput, 0, 255);

  // Apply outputs
  analogWrite(LED_PIN, ledOutput); // Control the LED brightness

  // Print values for debugging
  Serial.print("Distance: ");
  Serial.print(realDistance);
  Serial.print(" | LED Intensity: ");
  Serial.println(ledOutput);

  delay(100); // Short delay to stabilize readings


}









