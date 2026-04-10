#include <MPU6050_tockn.h>  
#include <Wire.h> 

MPU6050 mpu6050(Wire, 0.05, 0.95);

void setup() {
  Serial.begin(9600);
  Wire.begin(); 
  mpu6050.begin(); 
  delay(2000);
  mpu6050.calcGyroOffsets(true);
}

void loop() {
  mpu6050.update();//process sensor data

 
  float roll  = mpu6050.getAngleX();
  float pitch = mpu6050.getAngleY();
  float yaw   = mpu6050.getAngleZ();

  //RAW accel angles(noisy, no gyro, no drift)
  float ax = mpu6050.getAccX();
  float ay = mpu6050.getAccY();
  float az = mpu6050.getAccZ();
  float roll_raw  = atan2(ay, az)*180.0/PI;
  float pitch_raw = atan2(-ax, sqrt(ay*ay+az*az))*180.0/PI;

 //deadzone
  if (abs(roll)< 0.5) roll = 0;
  if (abs(pitch)< 0.5) pitch = 0;
  if (abs(yaw)< 0.5) yaw = 0;

  //CSV
  Serial.print(roll_raw);   Serial.print(",");
  Serial.print(pitch_raw);  Serial.print(",");
  Serial.print(roll);       Serial.print(",");
  Serial.print(pitch);      Serial.print(",");
  Serial.println(yaw);

  delay(50); 
}
