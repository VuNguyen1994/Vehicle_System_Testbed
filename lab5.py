import serial
import matplotlib.pyplot as plt
import time
import numpy
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plt.close('all')
root = tk.Tk()
root.geometry("1000x600")
root.title("Photoresistor Evaluator")
root.configure(bg='grey')

figure1 = plt.Figure(figsize=(12,6), dpi=100)

ax1 = figure1.add_subplot(231)
fig1 = FigureCanvasTkAgg(figure1,root)
fig1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
figure1.set_facecolor('lightgrey')
line1, = ax1.plot([],[],'bo')
ax1.set_xlabel('Duty Cycle (%)', fontsize=10)
#ax1.set_ylabel('Photocell Voltage (V)', fontsize=10)
ax1.set_title('Photocell Voltage (V)')
ax1.grid(b=True, which='major', color='k', linestyle = '-')
ax1.grid(b=True, which='minor', color='r', linestyle = '-', alpha = 0.2)
ax1.minorticks_on()

ax2 = figure1.add_subplot(232)
line2, = ax2.plot([],[],'bo')
ax2.set_xlabel('Duty Cycle (%)',fontsize=10)
#ax2.set_ylabel('Photocell Current (mA)', fontsize=10)
ax2.set_title('Photocell Current (mA)')
ax2.grid(b=True,which='major',color='k',linestyle='-')
ax2.grid(b=True,which='minor',color='r',linestyle='-',alpha=0.2)
ax2.minorticks_on()

ax3 = figure1.add_subplot(233)
line3, = ax3.plot([],[],'bo')
ax3.set_xlabel('Duty Cycle (%)',fontsize=10)
#ax3.set_ylabel('Photocell Resistance (k\u03A9)', fontsize=10)
ax3.set_title('Photocell Resistance (k\u03A9)')
ax3.grid(b=True,which='major',color='k',linestyle='-')
ax3.grid(b=True,which='minor',color='r',linestyle='-',alpha=0.2)
ax3.minorticks_on()

ax4 = figure1.add_subplot(235)
line4, = ax4.plot([],[],'bo')
ax4.set_xlabel('Duty Cycle (%)',fontsize=10)
#ax4.set_ylabel('LED Voltage (V)', fontsize=10)
ax4.set_title('LED Voltage (V)')
ax4.grid(b=True,which='major',color='k',linestyle='-')
ax4.grid(b=True,which='minor',color='r',linestyle='-',alpha=0.2)
ax4.minorticks_on()

ax5 = figure1.add_subplot(236)
line5, = ax5.plot([],[],'bo')
ax5.set_xlabel('Duty Cycle (%)',fontsize=10)
#ax5.set_ylabel('LED Current (mA)', fontsize=10)
ax5.set_title('LED Current (mA)')
ax5.grid(b=True,which='major',color='k',linestyle='-')
ax5.grid(b=True,which='minor',color='r',linestyle='-',alpha=0.2)
ax5.minorticks_on()

figure1.subplots_adjust(hspace=0.5)
fontStyle= tkFont.Font(family="Lucida Grande", size=14)
var = StringVar()
label= Label( root,textvariable=var,font=fontStyle,bg='lightgrey')
label.place(x=100,y=400)

def get_valid_avg (buff):
    temp_mean = numpy.mean(buff)
    temp_std = numpy.std(buff)
    temp_buff = []
    for val in buff:
        # Error check, only store valid values to new buffer and return new mean
        if val <= (temp_mean + temp_std) and val >= (temp_mean - temp_std):
            temp_buff.append(val)
    return numpy.mean(temp_buff)

def startCallBack():
    arduino=serial.Serial('COM4',9600,timeout=5)
    time.sleep(1)
    DC=[]
    V_res=[]
    V_pc=[]
    I=[]
    R=[]
    LED_I=[]
    LED_V=[]
    print("***********Lab5***************")
    with open('lab5logs.txt', 'w') as logFile:
        logFile.writelines("***********Lab5***************\n")
        logFile.writelines("Measurements:\n")

        for i in range(100):
            buff_V_pc = []
            DC.append(i)
            var.set("Duty Cycle: {:.2f} %".format(DC[-1]))
            for count in range(5):
                arduino.reset_input_buffer()
                arduino.reset_output_buffer()
                #time.sleep(0.01)
                arduino.write(b'1')
                #time.sleep(0.5)
                #a=int(arduino.read(4).decode("ascii"))
                a = int(arduino.readline().decode("utf-8"))
                v = float(a)*5.0/255.0         # voltage on photocell
                buff_V_pc.append(v)
                print("Iteration: %d, Arduino: %f, Pcell Volt: %f" % (i,a,v))
            # Store output to buffers
            V_pc.append(get_valid_avg(buff_V_pc))
            print ("Duty cycle: %d, Average Voltage Photocell: %f" %(i, get_valid_avg(buff_V_pc)))
            logFile.writelines("Duty cycle: %d, Average Voltage Photocell: %f \n" %(i, get_valid_avg(buff_V_pc)))
            V_res.append(5-V_pc[-1])
            I.append(V_res[-1]*1000.0/1000.0) #mA
            R.append(V_pc[-1]/I[-1])           #kOhm
            vol_R = 5.0-(i*5/100.0)
            LED_I.append(vol_R*1000.0/1000.0)       # mA
            LED_V.append(i*5/100.0)

            line1.set_data(DC,V_pc)
            axa = fig1.figure.axes[0]
            axa.set_xlim(0,100)
            axa.set_ylim(0, 5)

            line2.set_data(DC, I)
            axb = fig1.figure.axes[1]
            axb.set_xlim(0, 100)
            axb.set_ylim(0, 5)

            line3.set_data(DC, R)
            axc = fig1.figure.axes[2]
            axc.set_xlim(0,100)
            axc.set_ylim(0,20)
            
            line4.set_data(DC, LED_V)
            axd = fig1.figure.axes[3]
            axd.set_xlim(0, 100)
            axd.set_ylim(0, 5)

            line5.set_data(DC, LED_I)
            axe = fig1.figure.axes[4]
            axe.set_xlim(0, 100)
            axe.set_ylim(0, 5)
            
            fig1.draw()
            plt.pause(0.05)
            plt.show()

        # Write logFile
        logFile.writelines("Calculations:\n")
        logFile.writelines("Photocell voltage: 5 * Arduino_reading/255\n")
        logFile.writelines("Photocell Current: (5 - Photocell_vol)/1000 Ohm\n")
        logFile.writelines("Photocell Resistance: Photocell_vol/Photocell_current\n")
        logFile.writelines("LED Current: (5 - LED_voltage)/1000 Ohm\n")
        logFile.writelines("LED Resistance: LED_voltage/LED_current\n")
        for idx in range(100):
            logFile.writelines("Photocell Voltage: %f, Photocell current: %f, Photocell Resistance: %f, LED Current: %f, LED Resistance: %f\n" % (V_pc[idx], I[idx], R[idx], LED_I[idx], LED_V[idx]))
        logFile.close()

    arduino.close()
    return

# Create Start button
start_button = Button(root, text ="Start", font=fontStyle, height=2, width=5, command = startCallBack)
start_button.place(x=100, y=450)
root.mainloop()



