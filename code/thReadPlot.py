#!/usr/bin/python

# Import Libraries
import matplotlib.pyplot as plt
import sys
import Adafruit_DHT as dht
import time as tm
import datetime as dt
import numpy as np
import array as arr
from oledDevice import get_device
from luma.core.render import canvas

# FUNCTIONS ####################################################################

# displays the current time, and pasues execution untill interval reached
def dispUpdate(timeData, tempFmt, humidFmt):

    # reading interval length (min)
    intLen = 5

    # last time sec
    lastTimeSec = 0

    # gets the current minute reading
    timeStamp = dt.datetime.now()
    timeStampMin = int(timeStamp.strftime("%M"))

    # calculates the next minute reading
    nxtTimeStamp = timeStampMin + intLen
    if nxtTimeStamp > 59:
        nxtTimeStamp = nxtTimeStamp - 60 

    # last time / temp / humid readings
    lstRdTime = timeData.strftime("%H:%M")
    lstRdTemp = str(np.around(tempFmt, decimals=1))  
    lstRdHumid = str(np.around(humidFmt, decimals=1)) 

    # while loop that prints the current time, exits
    # when the interval is up
    while timeStampMin != nxtTimeStamp: 

        # keeps getting the current minute reading
        timeStamp = dt.datetime.now()
        timeStampMin = int(timeStamp.strftime("%M"))

        # formats time and date for the display
        dispTimeFmt = timeStamp.strftime("%H:%M:%S")
        dispDateFmt = timeStamp.strftime("%d %b %y")

        timeStampSec = int(timeStamp.strftime("%S"))

        # only updates oled when delta time = 1s
        if timeStampSec != lastTimeSec:
            lastTimeSec = timeStampSec          
            
            with canvas(device) as draw:
                draw.text((1, 0), "Date:  " + dispDateFmt, fill="yellow")
                draw.text((1, 9), "Time:  " + dispTimeFmt, fill="yellow") 
                draw.text((32, 24), "Last Reading", fill="yellow")
                draw.text((1, 35), "Time:  " + lstRdTime, fill="yellow")
                draw.text((1, 44), "Temp:  " + lstRdTemp + " degC", fill="yellow")
                draw.text((1, 53), "Humid: " + lstRdHumid + " %", fill="yellow") 



# read temp and humidity from sensor
def readData():
    # Try to grab a sensor reading.  Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    humidData, tempData = dht.read_retry(22, 4)

    if humidData is not None and humidData > 10 and humidData < 100 and tempData is not None and tempData > 5 and tempData < 60:   	
        timeData = dt.datetime.now()
        return (timeData, tempData, humidData)
    else:
        print('Failed to get reading, or over limits. Trying again!')
        tm.sleep(2)
        return readData()


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


# convert data to a better format and then print to display
def fmtData(timeVal, tempVal, humidVal):
    
    timeFmt = timeVal.strftime("%d %m %y %H:%M")  
    tempFmt = np.around(tempVal, decimals=1)
    humidFmt = np.around(humidVal, decimals=1) 

    # formats time for command line output
    timeFmtTmp = timeVal.strftime("%H:%M")

    print("Time:",timeFmtTmp," Temp:",tempFmt," Humid:",humidFmt)

    return timeFmt, tempFmt, humidFmt

    

# MAIN #############################################################################

# creates the figure window and axes for the plots
plt.ion()
fig, axes = plt.subplots(nrows=2, ncols=1)

# global variables
timeArr = []
tempArr = []
humidArr = []

# max data elements to store
# 4032 = 2 weeks worth of data at 5 min intervals
dataLenMax = 4032

# get the oled device info??
device = get_device()

# inf loop
while True: 

    # read the temp / humid sensor and record the time
    timeData, tempData, humidData = readData()

    # format time / temp / humid and print result to screen
    timeFmt, tempFmt, humidFmt = fmtData(timeData, tempData, humidData)

    # saves the data into a global array
    timeArr.append(timeFmt)
    tempArr.append(tempFmt)
    humidArr.append(humidFmt)

    # limits data length
    if len(tempArr) > dataLenMax:
        timeArr = timeArr[1:(dataLenMax+1)]
        tempArr = tempArr[1:(dataLenMax+1)]
        humidArr = humidArr[1:(dataLenMax+1)]

    # plot the data and pause
    plotData(fig, axes, timeArr, tempArr, humidArr)

    # displays the current time on the oled, pauses
    # execution until an interval time length has been
    # reached
    dispUpdate(timeData, tempFmt, humidFmt)


    
