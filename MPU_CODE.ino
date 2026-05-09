#include <MPU6050_tockn.h>  
#include <Wire.h> 
//μερικά references
//https://seanboe.com/blog/complementary-filters
//https://www.youtube.com/watch?v=wTfSfhjhAU0
#include <MPU6050_tockn.h>  
#include <Wire.h>

MPU6050 mpu6050(Wire);

float alpha_comp = 0.92;  //Complementary filter, 0.92 και κάτω->more jitter

float roll = 0, pitch = 0, yaw = 0;
float gx_bias = 0, gy_bias = 0, gz_bias = 0;

unsigned long prevTime;

void calibrateGyroBias() {
  float sum_x = 0, sum_y = 0, sum_z = 0;
  const int samples = 500;
  
  Serial.println("Calibrating gyro... keep sensor still!");
  
  for (int i = 0; i < samples; i++) {
    mpu6050.update();
    sum_x += mpu6050.getGyroX();
    sum_y += mpu6050.getGyroY();
    sum_z += mpu6050.getGyroZ();
    delay(4);
  }
  
  gx_bias = sum_x / samples;
  gy_bias = sum_y / samples;
  gz_bias = sum_z / samples;
  
  Serial.print("Gyro bias: ");
  Serial.print(gx_bias); Serial.print(", ");
  Serial.print(gy_bias); Serial.print(", ");
  Serial.println(gz_bias);
}

void setup() {
  Serial.begin(9600);
  Wire.begin(); 
  mpu6050.begin();
  
  delay(1000);
  calibrateGyroBias(); //Calibrate axes
  
  prevTime = micros();  
}

void loop() {
  mpu6050.update();

  unsigned long currentTime = micros();
  float dt = (currentTime - prevTime) / 1000000.0;  //to seconds
  prevTime = currentTime;

  // Raw angles
  float ax = mpu6050.getAccX();
  float ay = mpu6050.getAccY();
  float az = mpu6050.getAccZ();

  float roll_acc  = atan2(ay, az) * 180.0 / PI;
  float pitch_acc = atan2(-ax, sqrt(ay*ay + az*az)) * 180.0 / PI;

  float gx = mpu6050.getGyroX() - gx_bias;
  float gy = mpu6050.getGyroY() - gy_bias;
  float gz = mpu6050.getGyroZ() - gz_bias;

  // Integrate gyro
  float roll_gyro  = roll  + gx * dt;
  float pitch_gyro = pitch + gy * dt;
  yaw += gz * dt;

  // Complementary filter 
  roll  = alpha_comp * roll_gyro  + (1 - alpha_comp) * roll_acc;
  pitch = alpha_comp * pitch_gyro + (1 - alpha_comp) * pitch_acc;

  // CSV 
  Serial.print(roll_acc);  Serial.print(",");
  Serial.print(pitch_acc); Serial.print(",");
  Serial.print(roll);      Serial.print(",");
  Serial.print(pitch);     Serial.print(",");
  Serial.println(yaw);

  delay(50);
}
