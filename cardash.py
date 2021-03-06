import serial
import matplotlib.pyplot as plt
import time
import sys
import numpy
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from tkinter import messagebox
import math as m
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plt.close('all')

root = tk.Tk()
root.geometry("1000x600")
root.title("Dashboard")
root.configure(bg='grey')

figure1 = plt.Figure(figsize=(12,6), dpi=100)

ax1 = figure1.add_subplot(231)

fig1 = FigureCanvasTkAgg(figure1,root)
fig1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
figure1.set_facecolor('lightgrey')

line1, = ax1.plot([],[],'bo')

ax1.set_xlabel('Iteration', fontsize=10)
ax1.set_ylabel('Velocity (%)', fontsize=10)
ax1.set_title('Velocity (%)')
ax1.grid(b=True, which='major', color='k', linestyle = '-')
ax1.grid(b=True, which='minor', color='r', linestyle = '-', alpha = 0.2)
ax1.minorticks_on()

figure1.subplots_adjust(hspace=0.5)
fontStyle= tkFont.Font(family="Lucida Grande", size=14)

var = StringVar()
var1 = StringVar()

#label= Label( root,textvariable=var,font=fontStyle,bg='lightgrey')
label1 = Label(root,textvariable=var1,font=fontStyle,bg='lightgrey')
#label2 = Label(root,textvariable='LEDs',font=fontStyle,bg='lightgrey')
#frame1 = Frame(width=20, height=20, bg="white",relief=SUNKEN)
#label.place(x=100,y=400)
label1.place(x=100,y=300)
#label2.place(x=600,y=300)
#frame1.place(x=600,y=400)

OnAuthorized = False

#system one-time status var ---------------------------------------------------------------

Temp_Authorized = [100,0]      # order = denied, allowed - denied on start
sys_Authorized = figure1.add_subplot(5,6,19)
sys_Authorized.pie(Temp_Authorized, colors=['red','green'])
sys_Authorized.set_title('Unauthorized')
sys_Authorized.axis('equal')
#----------------------------------------------------------------------------------

def startCallBack():
    global OnAuthorized
    arduino=serial.Serial('COM4',9600,timeout=10)
    time.sleep(1)
    DC=[]
    V_pc=[]
    velo=[50,0,50]
    print("***********Lab5***************")

    #system long-term status var ---------------------------------------------------------------
    Authorized = [100,0]
    HL_status = [100,0,0]      # order = off,dim,full - off on start
    #----------------------------------------------------------------------------------

    
    with open('lab5logs.txt', 'w') as logFile:
        logFile.writelines("***********Lab5***************\n")
        logFile.writelines("Measurements:\n")

        for i in range(1000):
            DC.append(i)
            distance=0
            arduino.reset_input_buffer()
            arduino.reset_output_buffer()
            time.sleep(0.1)
            arduino.write(b'1')
            data = arduino.readline().decode("utf-8").strip()
            # Handle data collected from Arduino: 
            # null, distance, "low coolant" or "high temperature"
            
            #system short-term status var ---------------------------------------------------------------
            CoolantLED = [100,0,0]     # order = off, normal, critical - off on start
            TemperatureLED = [100,0,0] # order = off, normal, critical - off on start
            #----------------------------------------------------------------------------------
            
            if data:
                print(data)
                if data == "C":
                    a = 0
                    CoolantLED = [0,0,100] #coolant low
                    # Set Coolant LED
                else:
                    CoolantLED = [0,100,0]
                    if data == "T":
                        a = 0
                        TemperatureLED = [0,0,100] #over heat
                        # Set Temperature LED
                    else:
                        TemperatureLED = [0,100,0]
                        if data == "A":
                            OnAuthorized = True
                            a = 0
                            Authorized = [0,100] #authorized
                        # Set Authorized LED
                        elif data == "F":
                            HL_status = [100,0,0]
                            # set Headlight LED off
                        elif data == "D":
                            HL_status = [0,100,0]
                            # Set headlight lED dim
                        elif data =="O":
                            HL_status = [0,0,100]
                            # setheadlight LED ON
                        else:
                            a= int(data)
                            OnAuthorized = True
                            Authorized = [0,100] #authorized
            else:
                a = 0
            distance = a/1000.0  # in meters, a in cm
            
            
            velo[1] = distance*100/0.03
            V_pc.append(velo[1])

            
            print("Iteration: %d, Distance: %f m, Velo: %f " % (i,distance,velo[1]))
            logFile.writelines("Iteration: %d, Distance: %f m, Velo: %f \n" % (i,distance,velo[1]))
            var1.set("Distance: {:.3f} m".format(distance))
            #var.set("Velocity: {:.3f} %".format(velo[1]))
            # Figure
            line1.set_data(DC,V_pc)
            axa = fig1.figure.axes[0]
            axa.set_xlim(0,1000)
            axa.set_ylim(0, 100)

            # Speedometer
            realvelo = velo[1]
            velo[1] = velo[1]/2
            velo[0] = 50-velo[1] # Only draw half of the circle for the speedometer
            Rounded_velo = round(realvelo*10)/10  #round num
            percentage_speed = str(Rounded_velo) #convert to string
            ax2 = figure1.add_subplot(233)
            ax2.pie(velo,colors=['white','red','gray'])
            ax2.set_title('Velocity ' + percentage_speed +'%')
            ax2.axis('equal')

            # system status LEDs -----------------------------------------------------------

            sys_coolant = figure1.add_subplot(5,6,17)
            
            sys_coolant.pie(CoolantLED, colors=['gray','green','red'])
            sys_coolant.set_title('Coolant Status')
            sys_coolant.axis('equal')

            sys_temperature = figure1.add_subplot(5,6,18)
            sys_temperature.pie(TemperatureLED, colors=['gray','green','red'])
            sys_temperature.set_title('Temperature')
            sys_temperature.axis('equal')

            sys_Authorized = figure1.add_subplot(5,6,19)
            sys_Authorized.pie(Authorized, colors=['red','green'])
            if OnAuthorized:
                sys_Authorized.set_title('Authorized')
            else:
                sys_Authorized.set_title('Unauthorized')
            sys_Authorized.axis('equal')

            sys_HeadLight = figure1.add_subplot(5,6,23)
            sys_HeadLight.pie(HL_status, colors=['gray','pink','red'])
            if HL_status[0] == 100: 
                sys_HeadLight.set_title('HeadLight Off')
            if HL_status[1] == 100: 
                sys_HeadLight.set_title('HeadLight Dim')
            if HL_status[2] == 100: 
                sys_HeadLight.set_title('HeadLight Full')
            sys_HeadLight.axis('equal')
            
            # --------------------------------------------------------------------------
            # LEDs --------------------------------------------------------------------
            if distance <= 5/1000:
                LED1 = [100,0]
            else:
                LED1 = [0,100]
            if distance <= 4/1000:
                LED2 = [100,0]
            else:
                LED2 = [0,100]
            if distance <= 3/1000:
                LED3 = [100,0]
            else:
                LED3 = [0,100]
            if distance <= 2/1000:
                LED4 = [100,0]
            else:
                LED4 = [0,100]
                
            ax3 = figure1.add_subplot(5,1,1)
            ax3.pie(LED1, colors = ['blue','gray'])
            ax3.set_title('Blue LED')
            ax3.axis('equal')
            
            ax4 = figure1.add_subplot(5,1,2)
            ax4.pie(LED2, colors=['green','gray'])
            ax4.set_title('Green LED')
            ax4.axis('equal')
            
            ax5 = figure1.add_subplot(5,1,3)
            ax5.pie(LED3, colors=['orange','gray'])
            ax5.set_title('Orange LED')
            ax5.axis('equal')
            
            ax6 = figure1.add_subplot(5,1,4)
            ax6.pie(LED4, colors=['red','gray'])
            ax6.set_title('Red LED')
            ax6.axis('equal')
            # --------------------------------------------------------------------------
            # Draw tools -  Do not touch
            fig1.draw()
            plt.pause(0.05)
            plt.show()
 
        logFile.close()

    arduino.close()
    sys.exit(0)
    return

# Create Start button
start_button = Button(root, text ="Start", font=fontStyle, height=2, width=5, command = startCallBack)
start_button.place(x=100, y=450)
root.mainloop()
