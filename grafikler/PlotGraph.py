import numpy as np 
import matplotlib.pyplot as plt


def plotSth(x,y,title,xlabel,ylabel):
    fig, ax = plt.subplots()
    ax.plot(x,y)
    plt.grid()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    # Show the plot
    plt.savefig("{}.png".format(title))




x = [1,1.25,1.5,1.75,2.0]
y = [1.28,1.39,1.52,1.77,1.98]
plotSth(x, y, "Speed vs Current", "Current (A)", "Speed (m/s)")

x = [1,1.25,1.5,1.75,2.0]
y = [45,51,63,67,70]
plotSth(x, y, "Temperature vs Current for 1 Minute of Operation", "Current (A)", "Temperature(C)")


x = [1,2,3,4,5,6,7,8]
y = [4.5,8.5,9,9,10,9,5,1] 
plotSth(x, y, "Number of Ball per 15 Seconds vs Motor Voltage", "Voltage (V)", "Number of Ball")