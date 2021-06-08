import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from graphPlot import plotGraph
from DebugWindow import childWindow
from info import infoWindow


# === below imports from earlier code 

from matplotlib import pyplot as plt
from matplotlib import style
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from time import sleep
import logging
import time
import datetime
import glob
import urllib.request
import io         # used to create file streams
from io import open
import fcntl
import sys
import RPi.GPIO as GPIO
import os
import smbus
import csv
import pandas as pd
from pandas import read_csv
from nsetools import Nse
from pprint import pprint
i2cbus = smbus.SMBus(1)


#log file
logging.basicConfig(filename="newfile.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 
  
#Creating an object 
logger=logging.getLogger() 
  
#Setting the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG)


#sensor_call
regCall  =  0x52
regEC    =  0xF4
regPH    =  0x34
regRTD   =  0x2e
regORP   =  0x35
regDO    =  0x33
PHAdd    =  0x63
RTDAdd   =  0x66
ORPAdd   =  0x62
ECAdd    =  0x64
DOAdd    =  0x61

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

time1 =''
key="N6LN5Q0HQZ124WFU"       # Enter your Write API key from ThingSpeak





def readPH(addr=PHAdd):    
  i2cbus.write_byte_data(addr,regCall,0)
  time.sleep(0.9)
  P1 = i2cbus.read_i2c_block_data(addr, regPH,7)
  time.sleep(0.9)
  PH = ''.join(str(chr(A)) for A in P1[1:6])
  return (str(PH))
  
  
def readRTD(addr=RTDAdd ):    
  i2cbus.write_byte_data(addr,regCall,0)
  time.sleep(0.9)
  P2 = i2cbus.read_i2c_block_data(addr, regRTD,7)
  time.sleep(0.9)
  RTD = ''.join(str(chr(A)) for A in P2[1:6])
  return (str(RTD))

def readORP(addr=ORPAdd ):    
  i2cbus.write_byte_data(addr,regCall,0)
  time.sleep(0.9)
  P3 = i2cbus.read_i2c_block_data(addr, regORP,7)
  time.sleep(0.9)
  ORP = ''.join(str(chr(A)) for A in P3[1:6])
  return (str(ORP))

def readEC(addr=ECAdd ):    
  i2cbus.write_byte_data(addr,regCall,0)
  time.sleep(0.9)
  P4 = i2cbus.read_i2c_block_data(addr, regEC,7)
  time.sleep(0.9)
  EC = ''.join(str(chr(A)) for A in P4[1:5])
  return (str(EC))

def readDO(addr=DOAdd ):    
  i2cbus.write_byte_data(addr,regCall,0)
  time.sleep(0.9)
  P5 = i2cbus.read_i2c_block_data(addr, regDO,7)
  time.sleep(0.9)
  DO = ''.join(str(chr(A)) for A in P5[1:4])
  return (str(DO))




def main():

    URL = 'https://api.thingspeak.com/update?api_key=%s' % key 

    (PH)  = readPH()
    (RTD) = readRTD()
    (ORP) = readORP()
    (EC)  = readEC()
    (DO)  = readDO()

    A = float(PH)
    B = float(RTD)
    C = float(ORP)
    D = float(DO)
    E = float(EC)
    F = 2

    global time1
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    time2=datetime.datetime.now().strftime('%H:%M:%S')

    if time2 != time1:
        time1 = time2
        # curDate.config(text=today)
        # curTime.config(text=time2)
        timeDate.config(text="Date : {}\nTime : {}".format(today, time2))

        # set the text of labels
        data_rtd.config(text="RTD\n=%d °C" % B)
        data_orp.config(text="ORP\n=%d mV" % C)
        data_do.config(text="DO\n=%d mg/L" % D)
        data_ec.config(text="EC\n=%d uS" % E)
        data_ph.config(text="PH\n=%d pH" % A)
        data_tb.config(text="TB\n=%d"%F)

        # writing to a csv file (appending)
        with open('sensor_readings.csv', mode='a') as sensor_readings:
          sensor_write = csv.writer(sensor_readings, delimiter=',', quotechar='”', quoting=csv.QUOTE_MINIMAL)
          write_to_log = sensor_write.writerow([today,time2,A,B,C,D,E,F]) 




        # -------------------------------------------------
        # Chemical_detection_code_part

        if (A <= 6.5):
          chemical_pollutants="Water is Acidic :  "

        elif ( A>= 8.5 ):
          chemical_pollutants="Water is Basic :  "

        PH = A
        EC = E
        ORP = C
        DO = D

        #p1
        if ((0<= PH <= 4) or (11.5<= PH <= 14)):
            p1=1
        elif ((5<= PH <= 6.4) or (8.6<= PH <= 11.4 )):
            p1=2
        else :
            p1=3

        #e1
        if ((EC < 50) or (EC > 350)) :
             e1= 0
        else :
            e1=1

        #o1
        if ((0<= ORP <= 200) or (ORP > 400))  :
            o1 = 0
        else :
            o1 = 1


        # calculating Level (maybe)
        t=o1+p1+e1

        if t==1 :
          level="L5"
        elif t== 2 :
          level="L4"
        elif t== 3 :
          level="L3"
        elif t== 4 :
          level="L2"
        elif t== 5 :
          level="L1"

        txt_chemical="Chemical\nPollutants\n\n\n"+chemical_pollutants+level
        block1.config(text=txt_chemical)
        


        # ----------------------------------
        #Plastic Detection does not exist
        block2.config(text="")
              



        # ----------------------------------
        # Micro_organisms code


        # o2
        if ((ORP <= 150) or (ORP > 400)) :
          o2 = 0
        else :
          o2=1

        # d2
        if ((DO < 4) or (DO > 13)) :
          d2 = 0
        else :
          d2 = 1

        # calculating m 
        m = d2 + o2


        if m==0 :
          micro_organisms="Present"              
        elif m==1 :
          micro_organisms="Present in less amt"
        elif m==2 :
          micro_organisms="Water is safe"

        txt_micro="Micro-\nOrganisms\n\n\n"+micro_organisms
        block3.config(text=txt_micro)





        # --------------------------
        # WATER_QUALITY

        # p3
        if ((0<= PH <= 6.4) or (8.6 <= PH <= 14)) :
            p3=0
        else :
            p3=1


        # e3
        if ((EC < 50) or (EC > 400)) :
           e3= 0
        else :
           e3=1

          
        # o3
        if ((ORP <= 250) or (ORP > 400)) :
          o3 = 0
        else :
           o3=1


        # d3
        if((DO < 4) or (DO > 13)) :
          d3 = 0
        else :
           d3 = 1


        # calculating A
        A=o3+p3+e3+d3


        if A==1 :
          water_quality="Very Bad"

        elif A== 2 :
          water_quality="Bad"

        elif A== 3 :
          water_quality="Moderate"

        elif A== 4 :
          water_quality="Good"

        elif A==0 :
          water_quality="Hazardous"

        txt_water="Water\nQuality\n\n\n"+water_quality
        block4.config(text=txt_water)


            
             

        # ----------------------
        # send data towards cloud
        finalURL = URL +"&field1=%s" %(PH)+"&field2=%s" %(RTD)+"&field3=%s" %(EC)+"&field4=%s" %(ORP)+"&field5=%s" %(DO)

        try:
          s=urllib.request.urlopen(finalURL);
          s.close()
          print("connected")

        except urllib.error.URLError as e:
          print("conection failed")
          print("reconnecting.....")
          logger.critical("Internet is down") 
        time.sleep(10)

    timeDate.after(300000,main)
     
# ================================


def currentTime():
    dt = datetime.datetime.now()
    d = dt.strftime("%Y-%m-%d")
    t = dt.strftime("%H:%M:%S")
    timeDate.config(text="Date : {}\nTime : {}".format(d, t))
    timeDate.after(1000, currentTime)


# reading data
data = pd.read_csv("sensor_readings.csv")
lastIndex = len(data) - 1


window = tk.Tk()

# Configuration of rows
window.config(bg='#272727')
window.rowconfigure([0, 1, 2], weight=1)
window.columnconfigure(0, weight=1, minsize=50)
window.title("Water quality monitoring")
window.geometry("800x480")
# black
BGcolor = "#272727"

# grey
color1 = "#747474"

# red
color2 = "#FF652F"

# yellow
color3 = "#FFE400"

# green
color4 = "#14A76C"

BFSize = 15
BFFamily = "Verdana BOLD"
BFont = (BFFamily, BFSize)

BFont2=(BFFamily,16)
pad = 7
pad2 = 2







# ==========================================================

# frame 1
frame1 = tk.Frame(master=window, width=800, height=140, bg=BGcolor)
frame1.grid(row=0, sticky="nsew", padx=5, pady=5)

frame1.rowconfigure([0, 1, 2, 3, 4, 5], weight=1, minsize=23)
frame1.columnconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                        10, 11], weight=1, minsize=50)




# ----------------



lstRead = tk.Label(master=frame1, text="Last Reading", bg=color2)
lstRead.grid(row=0, column=0, columnspan=2, sticky="nsew", )

d = data["date"][lastIndex]
t = data["time"][lastIndex]
lstRead = tk.Label(
    master=frame1, text="Date : {}\nTime : {}".format(d, t), bg=color2)
lstRead.grid(row=1, column=0, rowspan=2, columnspan=2, sticky="nsew")

info = tk.Button(master=frame1, text="Info", fg=color4,command=lambda: infoWindow(window))
info.grid(row=3, column=3, sticky="nsew")


heading = tk.Label(master=frame1, text="Water Quality Monitoring",
                   bg=BGcolor, fg=color4, borderwidth=0, font=("Verdana", 24))
heading.grid(row=0, column=3, rowspan=2, columnspan=6,
             sticky="nsew", padx=pad, pady=pad)

debug = tk.Button(master=frame1, text="Debug", fg=color4,command=lambda: childWindow(window))
debug.grid(row=3, column=8, sticky="nsew")

logoImg = tk.PhotoImage(file="logo.png")
logo = tk.Label(frame1, image=logoImg, bg=BGcolor)
logo.grid(row=2, column=4, rowspan=4, columnspan=4,
          ipadx=1, ipady=1, sticky="nsew")


# time 
current = tk.Label(master=frame1, text="Current Time", bg=color2)
current.grid(row=0, column=10, columnspan=2, sticky="nsew")

timeDate = tk.Label(master=frame1, bg=color2)
timeDate.grid(row=1, column=10, rowspan=2, columnspan=2, sticky="nsew")
currentTime()










# =================================================================

# frame 2
frame2 = tk.Frame(master=window, width=800, height=140, borderwidth=5, bg=color1)
frame2.grid(row=1, sticky="nsew", padx=5, pady=5)

frame2.rowconfigure([0], weight=1, minsize=80)
frame2.columnconfigure([0, 1, 2, 3, 4, 5], weight=1, minsize=120)





#------------------------------

# p = data["PH"][lastIndex]
# txt = "PH\n{}".format(p)
data_ph = tk.Button(master=frame2, fg=color4, font=BFont, command=lambda: plotGraph("PH"))
data_ph.grid(row=0, column=0, sticky="nsew", padx=pad, pady=pad, ipadx=5, ipady=5)



# p = data["RTD"][lastIndex]
# txt = "RTD\n{}".format(p)
data_rtd = tk.Button(master=frame2, fg=color4, font=BFont, command=lambda: plotGraph("RTD"))
data_rtd.grid(row=0, column=1, sticky="nsew", padx=pad, pady=pad, ipadx=5, ipady=5)



# p = data["ORP"][lastIndex]
# txt = "ORP\n{}".format(p)
data_orp = tk.Button(master=frame2, fg=color4, font=BFont, command=lambda: plotGraph("ORP"))
data_orp.grid(row=0, column=2, sticky="nsew", padx=pad, pady=pad, ipadx=5, ipady=5)



# p = data["DO"][lastIndex]
# txt = "DO\n{}".format(p)
data_do = tk.Button(master=frame2, fg=color4, font=BFont, command=lambda: plotGraph("DO"))
data_do.grid(row=0, column=3, sticky="nsew", padx=pad, pady=pad, ipadx=5, ipady=5)



# p = data["EC"][lastIndex]
# txt = "EC\n{}".format(p)
data_ec = tk.Button(master=frame2, fg=color4, font=BFont, command=lambda: plotGraph("EC"))
data_ec.grid(row=0, column=4, sticky="nsew", padx=pad, pady=pad, ipadx=5, ipady=5)



# p = data["TB"][lastIndex]
# txt = "TB\n{}".format(p)
data_tb = tk.Button(master=frame2, fg="#14A76C", font=BFont, command=lambda: plotGraph("TB"))
data_tb.grid(row=0, column=5, sticky="nsew", padx=pad, pady=pad, ipadx=5, ipady=5)








# ================================================================


# frame 3
frame3 = tk.Frame(master=window, width=800, height=200, bg=color1)
frame3.grid(row=2, sticky="nsew", padx=10, pady=10)

frame3.rowconfigure([0], weight=1, minsize=200)
frame3.columnconfigure([0, 1, 2, 3], weight=1, minsize=200)



# chemical_pollutants="Water is Acidic"
# plastic_detection="\t"
# micro_organisms="Present"
# water_quality="Very Bad"

# -------------


# Chemical Pollutants
block1 = tk.Label(master=frame3, bg=color2, font=BFont2)
block1.grid(row=0, column=0, padx=pad2, pady=pad2, sticky="nsew")



# Plastic Detection
block2 = tk.Label(master=frame3, bg=color3,  font=BFont2)
block2.grid(row=0, column=1, padx=pad2, pady=pad2, sticky="nsew")



# Micro-Organisms
block3 = tk.Label(master=frame3, bg=color2,  font=BFont2)
block3.grid(row=0, column=2, padx=pad2, pady=pad2, sticky="nsew")



# Water Quality
block4 = tk.Label(master=frame3, bg=color3,  font=BFont2)
block4.grid(row=0, column=3, padx=pad2, pady=pad2, sticky="nsew")

main()
window.mainloop()

# ------------





































# tried and refused

# block1 = tk.Frame(master=frame3, bg=color2)
# block1.grid(row=0, column=0, padx=pad2, pady=pad2, sticky="nsew")
# block1.columnconfigure([0], weight=1,minsize=200)
# block1.rowconfigure([0, 1], weight=1, minsize=100)

# head1=tk.Label(master=block1,fg=BGcolor,bg=color2, text="Chemical \nPollutant" ,font=BFont2)
# head1.grid(row=0, padx=pad2, pady=pad2, sticky="nsew")

# chemical=tk.Label(master=block1,fg="white",bg=color2, text="Water is Acidic" ,font=BFont)
# chemical.grid(row=1, padx=pad2, pady=pad2, sticky="nsew")





# def plotRTD():
#   x =[]
#   y =[]
#   file = open("sensor_readings.csv")
#   reader = csv.reader(file)
#   lines= len(list(reader))
#   linesm = lines - 5
#   with open('sensor_readings.csv','r') as csvfile:
#     plots = csv.reader(csvfile, delimiter=',')
#     for row in plots:
#         x.append(str(row[1]))
#         y.append(float(row[3])) 
#   plt.figure(figsize=(10,7))
#   ax = plt.axes()
#   # Setting the background color
#   ax.set_facecolor("black")
#   plt.plot(x,y,'-wo',label='RTD')
#   plt.xlim(linesm,lines)
#   plt.ylim(15,45)
#   #plt.xticks(rotation=45)
#   plt.xlabel(row[0])
#   plt.ylabel('°C')
#   plt.title('RTD')
#   plt.grid()
#   plt.legend()
#   plt.show()
  
# def plotPH():
#   x =[]
#   y =[]
#   file = open("sensor_readings.csv")
#   reader = csv.reader(file)
#   lines= len(list(reader))
#   linesm = lines - 5
#   with open('sensor_readings.csv','r') as csvfile:
#     plots = csv.reader(csvfile, delimiter=',')
#     for row in plots:
#         x.append(str(row[1]))
#         y.append(float(row[2])) 
#   plt.figure(figsize=(10,7))
#   ax = plt.axes()
#   # Setting the background color
#   ax.set_facecolor("black")
#   plt.plot(x,y,'-ro',label='PH')
#   plt.xlim(linesm,lines)
#   plt.ylim(2,13)
#   plt.xlabel(row[0])
#   plt.ylabel('y')
#   plt.title('PH')
#   plt.grid()
#   plt.legend()
#   plt.show()

# def plotDO():
#   x =[]
#   y =[]
#   file = open("sensor_readings.csv")
#   reader = csv.reader(file)
#   lines= len(list(reader))
#   linesm = lines - 5
#   with open('sensor_readings.csv','r') as csvfile:
#     plots = csv.reader(csvfile, delimiter=',')
#     for row in plots:
#         x.append(str(row[1]))
#         y.append(float(row[4])) 
#   plt.figure(figsize=(10,7))
#   ax = plt.axes()
#   # Setting the background color
#   ax.set_facecolor("black")
#   plt.plot(x,y,'-yo',label='DO')
#   plt.xlim(linesm,lines)
#   plt.ylim(0,15)
#   plt.xlabel(row[0])
#   plt.ylabel('mg/l')
#   plt.title('Disolved Oxygen')
#   plt.grid()
#   plt.legend()
#   plt.show()

# def plotORP():
#   x =[]
#   y =[]
#   file = open("sensor_readings.csv")
#   reader = csv.reader(file)
#   lines= len(list(reader))
#   linesm = lines - 5
#   with open('sensor_readings.csv','r') as csvfile:
#     plots = csv.reader(csvfile, delimiter=',')
#     for row in plots:
#         x.append(str(row[1]))
#         y.append(float(row[5])) 
#   plt.figure(figsize=(10,7))
#   ax = plt.axes()
#   # Setting the background color
#   ax.set_facecolor("black")
#   plt.plot(x,y,'-bo',label='ORP')
#   plt.xlim(linesm,lines)
#   plt.ylim(100,500)
#   plt.xlabel(row[0])
#   plt.ylabel('mv')
#   plt.title('ORP')
#   plt.grid()
#   plt.legend()
#   plt.show()

# def plotEC():
#   x =[]
#   y =[]
#   file = open("sensor_readings.csv")
#   reader = csv.reader(file)
#   lines= len(list(reader))
#   linesm = lines - 5
#   with open('sensor_readings.csv','r') as csvfile:
#     plots = csv.reader(csvfile, delimiter=',')
#     for row in plots:
#         x.append(str(row[1]))
#         y.append(float(row[6])) 
#   plt.figure(figsize=(10,7))
#   ax = plt.axes()
#   # Setting the background color
#   ax.set_facecolor("black")
#   plt.plot(x,y,'-go',label='EC')
#   plt.xlim(linesm,lines)
#   plt.ylim(0,600)
#   plt.xlabel(row[0])
#   plt.ylabel('us')
#   plt.title('Electronic_conductivity')
#   plt.grid()
#   plt.legend()
#   plt.show()
  
# def helloCallBack():
#   x =[]
#   y =[]
#   file = open("sensor_readings.csv")
#   reader = csv.reader(file)
#   lines= len(list(reader))
#   linesm = lines - 5
#   with open('sensor_readings.csv','r') as csvfile:
#     plots = csv.reader(csvfile, delimiter=',')
#     for row in plots:
#         x.append(str(row[1]))
#         y.append(float(row[2])) 
#   plt.figure(figsize=(10,7))
#   ax = plt.axes()
#   # Setting the background color
#   ax.set_facecolor("black")
#   plt.plot(x,y,'-ro',label='PH')
#   plt.xlim(linesm,lines)
#   plt.ylim(2,7)
#   plt.xlabel(row[0])
#   plt.ylabel('y')
#   plt.title('PH')
#   plt.grid()
#   plt.legend()
#   plt.show()

