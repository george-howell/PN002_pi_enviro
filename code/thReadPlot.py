#!/usr/bin/python

# Import Libraries
import matplotlib.pyplot as plt
import sys
import subprocess
import Adafruit_DHT as dht
import time as tm
import datetime as dt
import numpy as np
import array as arr
from oledDevice import get_device
from luma.core.render import canvas

# FUNCTIONS ####################################################################

# read temp and humidity from SHT-21
def readSht21():

    # call sht21ctl function and read stdout
    try:
        data = subprocess.check_output("./sht21ctl readall -nhm", shell=True)                       
    except subprocess.CalledProcessError:
        print("ERROR: with sht-21 sensor")
        sys.exit()

    # convert byte to string
    dataTmp = data.decode("utf-8")

    # split string
    p1, tempTmp, humidTmp = dataTmp.split(':', 3)

    # get data from full string
    tempData = tempTmp[1:5]
    humidData = humidTmp[1:5]

    return (tempData, humidData)

# update oled display
def dispRefresh(timeStamp, lstRdTime, lstRdTemp, lstRdHumid):

    # formats time and date for the display
    currTime = timeStamp.strftime("%H:%M:%S")
    currDate = timeStamp.strftime("%d %b %y")         
    
    with canvas(device) as draw:
        draw.text((1, 0), "Date:  " + currDate, fill="yellow")
        draw.text((1, 9), "Time:  " + currTime, fill="yellow") 
        draw.text((32, 24), "Last Reading", fill="yellow")
        draw.text((1, 35), "Time:  " + lstRdTime, fill="yellow")
        draw.text((1, 44), "Temp:  " + lstRdTemp + " degC", fill="yellow")
        draw.text((1, 53), "Humid: " + lstRdHumid + " %", fill="yellow")


# plot data
def plotData(fig, axes, timeArr, tempArr, humidArr): 

    # clears the data on each axis
    axes[0].clear()
    axes[1].clear()
    
    # plots data to each axes
    axes[0].plot(timeArr, tempArr)
    axes[1].plot(timeArr, humidArr)

    # temp plot labels
    axes[0].set_title('Temperature')
    axes[0].set_ylabel('Temp [degC]')

    # humid plot labels
    axes[1].set_title('Humidity')
    axes[1].set_xlabel('Date-Time')
    axes[1].set_ylabel('RH [%]')

    # grid
    axes[0].grid()
    axes[1].grid()

    # update the plot and pause for x seconds
    plt.pause(0.01)

# MAIN #############################################################################

# max data elements to store
# 4032 = 2 weeks worth of data at 5 min intervals
dataLenMax = 4032

# global variables
timeArr = []
tempArr = []
humidArr = []

# initialise variables
readFlg = True
lastSec = 0
lastRdTime = '--:--'
tempData = '--'
humidData = '--'

# creates the figure window and axes for the plots
plt.ion()
fig, axes = plt.subplots(nrows=2, ncols=1)

# print info
print('PI-ENVIRO')
print('-'*50)
print('TH Sensor')
print('\tDevice     : sht-21')
print('\tInterface  : i2c')
print('Display')

# opens the oled device and print some sys info
device = get_device()

# inf loop
while True: 

    # current time
    timeStamp = dt.datetime.now()

    # current second and min values
    currSec = int(timeStamp.strftime("%S"))
    currMin = int(timeStamp.strftime("%M"))       

    # only updates oled display when delta time = 1s
    if currSec != lastSec:
        
        # updates lastSec with current second value
        lastSec = currSec 
        dispRefresh(timeStamp,lastRdTime,tempData,humidData)

    # only read the sensor once every x minutes
    if (currMin % 2)==0: 
        if (readFlg==True):
            # read data from sensor
            tempData, humidData = readSht21()

            # formats date and time for command line output and display
            lastRdTime = timeStamp.strftime("%H:%M")

            # display time, temp and humid reading to console window
            print("Time:",lastRdTime," Temp [degC]:",tempData," RH [%]:",humidData)

            # set the flag to false so it doesn't read twice in the same minute
            readFlg=False

            # formats time for plots
            timePlotFmt = timeStamp.strftime("%d %m %y %H:%M")

            # saves the data into a global array
            timeArr.append(timePlotFmt)
            tempArr.append(float(tempData))
            humidArr.append(float(humidData))

            # limits data length
            if len(tempArr) > dataLenMax:
                timeArr = timeArr[1:(dataLenMax+1)]
                tempArr = tempArr[1:(dataLenMax+1)]
                humidArr = humidArr[1:(dataLenMax+1)]

            # plot the data
            plotData(fig, axes, timeArr, tempArr, humidArr)
    else:
        readFlg=True
