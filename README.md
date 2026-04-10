# MPU6050 Real-Time IMU Sensor Fusion 

This project implements a live orientation estimator using an MPU6050 IMU on an Arduino Uno.
Raw accelerometer and gyroscope data are fused using a **complementary filter** to estimate roll,
pitch, and yaw. A Python tool logs the data and a 3D visualizer replays it with a comparison of raw vs. filtered signals.

## Features
- Complementary filter sensor fusion (α=0.95 gyro, α=0.05 accel)
- Gyroscope auto-calibration on startup
- Raw vs. filtered angle output for comparison
- Serial output in CSV format
- 3D orientation visualizer
- 2D **live** plots comparing raw and filtered roll/pitch/yaw

## Hardware
- Arduino Uno
- MPU6050 sensor module
- Jumper wires
- Mini Breadboard(optional)

## Libraries
### Arduino
- MPU6050_tockn
- Wire

### Python
- PyQt6
- pyqtgraph
- PyOpenGL
- PyOpenGL_accelerate
- numpy

## Running Instructions
1. Upload `MPU_CODE.ino` to the Arduino Uno while wired up.
2. Close Arduino IDE to free the port (if its still open there will be port conflict).
3. Run `pythonterminal.py` in the terminal.
4. Press `Ctrl+C` to stop recording. Data (5 columns) saves to `movement.txt`. (To record data just move the breadboard)
5. Run `visualiser.py` to replay the 3D visualization and view raw vs. filtered plots.

## CSV Data Format
Each row in `movement.txt` contains 5 columns:
## Wiring

![Wiring Diagram](MPU_WIRING.png)


![Wiring](mpu_wiring.png)

## Visualizer Example
![Visualizer](Visualizer_example.png)



