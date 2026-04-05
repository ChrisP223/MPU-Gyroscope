#ΟΔΗΓΙΕΣ:
#1) ΤΡΕΧΟΥΜΕ ΣΤΟ TERMINAL ΑΦΟΥ ΤΡΕΧΕΙ ΤΟ ARDUINO
#2)Ctrl-C για να σταματήσουμε το recording
#3)Αφού σταματήσω να το τρέχω, τρέχω το visualizer.py για να δω το output


python -c "
import serial, time
PORT = 'COM3'#port number
ser = serial.Serial(PORT, 9600, timeout=1)
print('press Ctrl+C to stop')
with open('movement.txt', 'w') as f:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if ',' in line:
            f.write(line + '\n')
            print(line)
"
