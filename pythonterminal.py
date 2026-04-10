# ΟΔΗΓΙΕΣ:
# 1) ΤΡΕΧΟΥΜΕ ΣΤΟ TERMINAL ΑΦΟΥ ΤΡΕΧΕΙ ΤΟ ARDUINO
# 2) Ctrl-C για να σταματήσουμε το recording
# 3) Αφού σταματήσω να το τρέχω, τρέχω το visualizer.py για να δω το output

python -c "
import serial
PORT = 'COM3'
ser = serial.Serial(PORT, 9600, timeout=1)
print('Recording... press Ctrl+C to stop')
with open('movement.txt', 'w') as f:
    f.write('roll_raw,pitch_raw,roll_filtered,pitch_filtered,yaw_filtered\n')
    try:
        while True:
            line = ser.readline().decode('utf-8').strip()
            if ',' in line:
                parts = line.split(',')
                if len(parts) == 5:
                    f.write(line + '\n')
                    print(line)
    except KeyboardInterrupt:
        print('Stopped.')
        ser.close()
"
