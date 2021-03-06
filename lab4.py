from serial import Serial
import matplotlib.pyplot as plt
import time
import numpy
    
def is_valid(val,buff):
    if len(buff) <= 3:
        return True
    if val <= ( numpy.mean(buff)+ 2* numpy.std(buff)) and val >= ( numpy.mean(buff)- 2* numpy.std(buff)):
        return True
    else:
        return False

with Serial('COM4',9600) as arduino:
    time.sleep(1)
    xdata=[]
    voltage=[]
    LED_I = []
    LED_R = []
    Photo_I = []
    Photo_R = []
    duty_cycle=[i for i in range(100)]

    with open('lab4logs.txt', 'w') as logFile:
        logFile.writelines("Measurements:\n")

        for k in range(100):
            # get 5 points for each iteration, add to buffer, take average
            buff = []

            for count in range(5):
                arduino.reset_output_buffer()
                arduino.reset_input_buffer()
                arduino.write(b'1') 
                #time.sleep(0.1)
                a = int(arduino.readline().decode("utf-8"))
                v = float(a)*5.0/255.0         # voltage on photocell
                # Error checking, if voltage too large or too small, discard
                if is_valid(v,buff):
                    buff.append(v)
                    #logFile.writelines("Iteration: %d, Arduino: %f, Buff avg: %f. Valid" % (k,a,numpy.mean(buff)))
                    print("Iteration: %d, Arduino: %f, Buff avg: %f. Valid" % (k,a,numpy.mean(buff)))
                else:
                    #logFile.writelines("Iteration: %d, Arduino: %f, Buff avg: %f. InValid" % (k,a,numpy.mean(buff)))
                    print("Iteration: %d, Arduino: %f, Buff avg: %f. InValid" % (k,a,numpy.mean(buff)))
            voltage.append(numpy.mean(buff))
            logFile.writelines("Duty cycle: %d, Average Voltage Photocell: %f \n" %(k, numpy.mean(buff)))
            print ("Duty cycle: %d, Average Voltage Photocell: %f" %(k, numpy.mean(buff)))
            # Photocell circuit
            Photo_I.append(5.0 - numpy.mean(buff)) # mA
            Photo_R.append((numpy.mean(buff)/((5.0 - numpy.mean(buff))/1000.0))/1000.0) # kOhm
            # LED circuit
            vol_R = 5.0-(k*5/100.0)
            LED_I.append(vol_R*1000.0/1000.0)       # mA
            LED_R.append(((k*5/100.0)/(vol_R/1000.0))/1000.0)       #kOhm
        # End iteration

        # Write logFile
        logFile.writelines("Calculations:\n")
        logFile.writelines("Photocell voltage: 5 * Arduino_reading/255\n")
        logFile.writelines("Photocell Current: (5 - Photocell_vol)/1000 Ohm\n")
        logFile.writelines("Photocell Resistance: Photocell_vol/Photocell_current\n")
        logFile.writelines("LED Current: (5 - LED_voltage)/1000 Ohm\n")
        logFile.writelines("LED Resistance: LED_voltage/LED_current\n")
        for idx in range(100):
            logFile.writelines("Photocell Voltage: %f, Photocell current: %f, Photocell Resistance: %f, LED Current: %f, LED Resistance: %f\n" % (voltage[idx], Photo_I[idx], Photo_R[idx], LED_I[idx], LED_R[idx]))
        logFile.close()

    arduino.close()

plot1 = plt.figure(1)
plt.xlabel('Duty Cycle (%)')
plt.ylabel('Photocell Voltage (V)')
plt.grid(True)
plt.xlim(0,100)
plt.ylim(0,5)
plt.plot(duty_cycle,voltage,'bo')

plot2 = plt.figure(2)
plt.xlabel('Duty Cycle (%)')
plt.ylabel('Photocell current (mA)')
plt.grid(True)
plt.xlim(0,100)
plt.ylim(0,5)
plt.plot(duty_cycle,Photo_I,'bo')

plot3 = plt.figure(3)
plt.xlabel('Duty Cycle (%)')
plt.ylabel('Photocell Resistance (kOhm)')
plt.grid(True)
plt.xlim(0,100)
plt.ylim(0,5)
plt.plot(duty_cycle,Photo_R,'bo')

plot4 = plt.figure(4)
plt.xlabel('LED Current (mA)')
plt.ylabel('Photocell Resistance (kOhm)')
plt.grid(True)
plt.xlim(0,5)
plt.ylim(0,5)
plt.plot(LED_I,Photo_R,'bo')

plot5 = plt.figure(5)
plt.xlabel('Duty Cycle (%)')
plt.ylabel('LED current (mA)')
plt.grid(True)
plt.xlim(0,100)
plt.ylim(0,5)
plt.plot(duty_cycle,LED_I,'bo')

plot6 = plt.figure(6)
plt.xlabel('Duty Cycle (%)')
plt.ylabel('LED Resistance (kOhm)')
plt.grid(True)
plt.xlim(0,100)
plt.ylim(0,5)
plt.plot(duty_cycle,LED_R,'bo')

plt.show()

