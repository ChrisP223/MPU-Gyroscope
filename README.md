# MPU6050 Real-Time IMU Sensor Fusion
This project implements a live orientation estimator using an MPU6050 IMU on an Arduino Uno.
Raw accelerometer and gyroscope data are processed using a **complementary filter** to estimate roll,
pitch, and yaw. A Python tool logs the data and a 3D visualizer replays it with a comparison of raw vs. filtered signals.

## Features
- Complementary filter sensor fusion (α=0.98 gyro, α=0.02 accel)
- Manual gyro Z bias calibration on startup (500 samples)
- Raw vs. filtered angle output for comparison
- Serial output in CSV format
- 3D visualizer with frame-skip playback
- 2D **live** plots comparing raw and filtered roll/pitch/yaw

## Hardware
- Arduino Uno
- MPU6050 sensor module
- Jumper wires
- Mini Breadboard (optional)

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
2. Keep the sensor **completely still** for 3 seconds on startup ! it's calibrating gyro Z bias.
3. Close Arduino IDE to free the port (if its still open there will be port conflict). **SOS**
4. Run `pythonterminal.py` in the terminal.
5. Press `Ctrl+C` to stop recording. Data saves to `movement.txt`.
6. Run `visualiser.py` to replay the 3D visualization and view raw vs. filtered plots.

**Note that I already have a prefiled movement.txt so you can test the visualizer right away!**

## CSV Data Format
Each row in `movement.txt` contains 5 columns:
- **roll_raw / pitch_raw** — angle from accelerometer only (shaky)
- **roll_filtered / pitch_filtered / yaw_filtered** — angle after filtering (smooth)

## Analysis: Noise, Drift, and Limitations

### Complementary Filter
Combines two imperfect sensors into one good estimate. The gyroscope is smooth but drifts over time.
The accelerometer is stable long term but shaky. Mixing them (98% gyro, 2% accel) gives both smoothness and accuracy.

### Yaw
Yaw has no accelerometer reference, gravity is vertical so it can't tell you which way you're facing.
It's pure gyro integration with a manually measured bias removed at startup. Drift is unavoidable without a magnetometer. :(

The MPU6050_tockn library's `calcGyroOffsets()` was found to overcorrect the Z axis, zeroing out gz entirely.
The fix is to zero the library offsets with `setGyroOffsets(0,0,0)`, then measure gz bias manually

### Noise
Raw accelerometer angles jump around a lot during fast motion. The filter cleans this up but it can be
slightly slow to react to very quick movements.

### Gyroscope Drift
Small measurement errors accumulate over time, causing angle estimates to drift

### Rate
Loop runs at 50ms. Slow movements are captured well. Very fast rotations may be depicted worse.

### Filtered vs. Unfiltered
| Signal | Noise | Drift |
|---|---|---|
| Raw accelerometer (roll/pitch) | High | None |
| Gyroscope integration only | Low | Unbounded |
| Complementary filter output | Low | Minimal (roll/pitch), moderate (yaw) |

## Wiring
![Wiring Diagram](MPU_WIRING.png)
![Wiring](mpu_wiring.png)

## Visualizer Example
![Visualizer](Screenshot111.png)

## Demo Video





