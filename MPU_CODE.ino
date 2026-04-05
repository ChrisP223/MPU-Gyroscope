#include <MPU6050_tockn.h>  
#include <Wire.h> 


MPU6050 mpu6050(Wire, 0.05, 0.95);//τα filter settings μπορούν να αλλάξουν

void setup() {
  Serial.begin(9600);
  Wire.begin(); 
  mpu6050.begin(); 
  delay(2000);//stabilize
  mpu6050.calcGyroOffsets(true);//Calibrate offsets
}

void loop() {
  mpu6050.update();  // Read and process sensor data
  // Get orientation angles
  float roll  = mpu6050.getAngleX();
  float pitch = mpu6050.getAngleY();
  float yaw   = mpu6050.getAngleZ();
  //deadzone για να αποφύγουμε noise
  if (abs(roll)  < 0.5) roll  = 0;
  if (abs(pitch) < 0.5) pitch = 0;
  if (abs(yaw)   < 0.5) yaw   = 0;
  //data in csv format
  Serial.print(roll);
  Serial.print(",");
  Serial.print(pitch);
  Serial.print(",");
  Serial.println(yaw);

  delay(50); 
}