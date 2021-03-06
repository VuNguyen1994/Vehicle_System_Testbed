import matplotlib.pyplot as plt

duty_cycle = [i for i in range(100)]
voltage = [2*i for i in range(100)]
Photo_I = [i**2 for i in range(100)]

plot1 = plt.figure(1)
plt.xlabel('Duty Cycle (%)')
plt.ylabel('Photocell Voltage (V)')
plt.grid(True)
plt.xlim(0,100)
plt.ylim(0,5)
plt.plot(duty_cycle,voltage,'bo')

plot2 = plt.figure(2)
plt.xlabel('Duty Cycle (%)')
plt.ylabel('Photocell current (A)')
plt.grid(True)
plt.xlim(0,100)
plt.ylim(0,5)
plt.plot(duty_cycle,Photo_I,'bo')

plt.show()