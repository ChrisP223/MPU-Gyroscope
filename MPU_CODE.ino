#include <MPU6050_tockn.h>  
#include <Wire.h> 


//μερικά references
//https://seanboe.com/blog/complementary-filters
//https://www.youtube.com/watch?v=wTfSfhjhAU0
MPU6050 mpu6050(Wire);

float alpha_acc = 0.9;  //lowpass για accelerometer(μείωση noise)
float alpha_comp = 0.98;

float roll = 0, pitch = 0, yaw = 0;
float roll_raw = 0, pitch_raw = 0;
float roll_acc = 0, pitch_acc = 0;
float prev_roll_acc = 0, prev_pitch_acc = 0;// για low-pass


unsigned long prevTime;

void setup() {
  Serial.begin(9600);
  Wire.begin(); 
  mpu6050.begin(); 

  delay(2000); 
  mpu6050.calcGyroOffsets(true);
  prevTime = millis();
}

void loop() {
  mpu6050.update();

 
  unsigned long currentTime = millis();
  float dt = (currentTime - prevTime) / 1000.0;
  prevTime = currentTime;

 
  float ax = mpu6050.getAccX();
  float ay = mpu6050.getAccY();
  float az = mpu6050.getAccZ();


  roll_acc  = atan2(ay,az) *180.0/PI;
  pitch_acc = atan2(-ax, sqrt(ay*ay + az *az)) *180.0/PI;

// Lowpass για να μειωσει τρέμουλο
  roll_raw  = alpha_acc*prev_roll_acc +(1 - alpha_acc) * roll_acc;
  pitch_raw = alpha_acc *prev_pitch_acc+(1 - alpha_acc)*pitch_acc;

  prev_roll_acc  = roll_raw;
  prev_pitch_acc = pitch_raw;

  
  float gx = mpu6050.getGyroX(); 
  float gy = mpu6050.getGyroY();
  float gz = mpu6050.getGyroZ();

// deg/sec
  float roll_gyro  =roll+gx*dt;
  float pitch_gyro =pitch+gy*dt;
  yaw += gz * dt;


  roll =alpha_comp*roll_gyro +(1 -alpha_comp) *roll_raw;
  pitch= alpha_comp *pitch_gyro+(1 -alpha_comp) * pitch_raw;

 //deadzone
  if (abs(roll)< 0.5) roll  = 0;
  if (abs(pitch)< 0.5) pitch = 0;
  if (abs(yaw) < 0.5) yaw   = 0;

//csv
  Serial.print(roll_raw);
  Serial.print(",");
  Serial.print(pitch_raw);
  Serial.print(",");
  Serial.print(roll);
  Serial.print(",");
  Serial.print(pitch);
  Serial.print(",");
  Serial.println(yaw);

  delay(50);
}
