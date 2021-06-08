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

#GUI  
root = Tk()
root.title("Water quality monitoring")
root.configure(background = "white")
root.geometry("800x480")
canvas2 = Canvas(root, width = 797, height = 480,bg ='black')
canvas2.place(x=0,y=0)
canvas = Canvas(root, width = 95, height = 95)
canvas.place(x=60,y=4)     
img = PhotoImage(file="2.png")
photoimg = img.subsample(2,2)
canvas.create_image(1,1, anchor=NW, image=photoimg)
img3 = PhotoImage(file="3.png")
img2 = img3.subsample(4,4)
canvas2.create_line(0, 105, 800, 105,width = 4,fill='white')
canvas2.create_line(320, 105, 320, 480,width = 4,fill='white')
canvas2.create_line(570, 105, 570, 480,width = 4,fill='white')
canvas2.create_line(320, 260, 800, 260,width = 4,fill='white')
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
        curDate.config(text=today)
        curTime.config(text=time2)
        curTEMP.config(text="RTD=%d °C" % B)
        curORP.config(text="ORP=%d mV" % C)
        curDO.config(text="DO=%d mg/L" % D)
        curEC.config(text="EC=%d uS" % E)
        curPH.config(text="PH=%d pH" % A)
        curTB.config(text="Turbudity=%d"%F)
        with open('sensor_readings.csv', mode='a') as sensor_readings:
          sensor_write = csv.writer(sensor_readings, delimiter=',', quotechar='”', quoting=csv.QUOTE_MINIMAL)
          write_to_log = sensor_write.writerow([today,time2,A,B,C,D,E,F]) 
        #Chemical_detectio_code_part
         
        if ( A<= 6.5 ):
          a=Label(root, text="water is Acidic",bg="orange",fg="black",font="none 14 bold")
          a.place(x=360,y=160)
        elif ( A>= 8.5 ):
          a=Label(root, text="water is Basic",bg="orange",fg="black",font="none 14 bold")
          a.place(x=380,y=160)
        PH = A
        EC = E
        ORP = C
        DO = D
        if 0<= PH <= 4 or 11.5<= PH <= 14 :
            p1=1
        elif 5<= PH <= 6.4 or 8.6<= PH <= 11.4 :
            p1=2
        else :
            p=3
        if EC < 50 or EC > 350 :
             e1= 0
        else :
            e1=1
        if 0<= ORP <= 200 or ORP > 400  :
            o1 = 0
        else :
            o1 = 1
        t=o1+p1+e1
        if t==1 :
              k=Label(root, text="L5",bg="red",fg="black",font="none 12 bold")
              k.place(x=375,y=225)
        elif t== 2 :
              k=Label(root, text="L4",bg="orange",fg="black",font="none 12 bold")
              k.place(x=375,y=225)
              
        elif t== 3 :
              k=Label(root, text="L3",bg="yellow",fg="black",font="none 12 bold")
              k.place(x=375,y=145)
              
        elif t== 4 :
              k=Label(root, text="L2",bg="green",fg="black",font="none 12 bold")
              k.place(x=375,y=145)
             
        elif t== 5 :
              k=Label(root, text="L1",bg="blue",fg="black",font="none 12 bold")
              k.place(x=375,y=145)

        #Micro_organismi code

        if  ORP <= 150 or ORP > 400  :
            o2 = 0
        else :
             o=1
        if DO < 4 or DO > 13 :
               d2 = 0
        else :
                d2 = 1
        m = d2 + o2
        if m==0 :
            a=Label(root, text="Micro-organisms are present",bg="magenta",fg="black",font="none 12 bold")
            a.place(x=325,y=345)
              
        elif m==1 :
            a=Label(root, text="Less Amount of Micro-organisms are present",bg="magenta",fg="black",font="none 12 bold")
            a.place(x=325,y=345)
              
        elif m==2 :
            a=Label(root, text="Water is safe",bg="magenta",fg="black",font="none 12 bold")
            a.place(x=325,y=345)

        #WATER_QUALITY
        w= Label(root,text = "Water Quality",bg = "white",fg="black",font="none 13 bold")
        w.place(x=600,y=270)
      
        if 0<= PH <= 6.4 or 8.6 <= PH <= 14 :
            p3=0
        else :
            p3=1
        if EC < 50 or EC > 400 :
           e3= 0
        else :
           e3=1
        if  ORP <= 250 or ORP > 400  :
          o3 = 0
        else :
           o3=1
        if DO < 4 or DO > 13 :
          d3 = 0
        else :
           d3 = 1
        A=o3+p3+e3+d3
        if A==1 :
            w= Label(root,text = " Very Bad",bg = "white",fg="black",font="none 13 bold")
            w.place(x=600,y=350)
        elif A== 2 :
            w= Label(root,text = " Bad",bg = "white",fg="black",font="none 13 bold")
            w.place(x=600,y=350)
            
        elif A== 3 :
            w= Label(root,text = " Modrate",bg = "white",fg="black",font="none 13 bold")
            w.place(x=600,y=350)
            
        elif A== 4 :
            w= Label(root,text = "Good",bg = "white",fg="black",font="none 13 bold")
            w.place(x=600,y=350)
            
        elif A==0 :
            w= Label(root,text = "Hazardous",bg = "white",fg="black",font="none 13 bold")
            w.place(x=600,y=350)
            
             

        #send data towards cloud
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
    curTime.after(300000,main)
     
     


def plotRTD():
  x =[]
  y =[]
  file = open("sensor_readings.csv")
  reader = csv.reader(file)
  lines= len(list(reader))
  linesm = lines - 5
  with open('sensor_readings.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(str(row[1]))
        y.append(float(row[3])) 
  plt.figure(figsize=(10,7))
  ax = plt.axes()
  # Setting the background color
  ax.set_facecolor("black")
  plt.plot(x,y,'-wo',label='RTD')
  plt.xlim(linesm,lines)
  plt.ylim(15,45)
  #plt.xticks(rotation=45)
  plt.xlabel(row[0])
  plt.ylabel('°C')
  plt.title('RTD')
  plt.grid()
  plt.legend()
  plt.show()
  
def plotPH():
  x =[]
  y =[]
  file = open("sensor_readings.csv")
  reader = csv.reader(file)
  lines= len(list(reader))
  linesm = lines - 5
  with open('sensor_readings.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(str(row[1]))
        y.append(float(row[2])) 
  plt.figure(figsize=(10,7))
  ax = plt.axes()
  # Setting the background color
  ax.set_facecolor("black")
  plt.plot(x,y,'-ro',label='PH')
  plt.xlim(linesm,lines)
  plt.ylim(2,13)
  plt.xlabel(row[0])
  plt.ylabel('y')
  plt.title('PH')
  plt.grid()
  plt.legend()
  plt.show()

def plotDO():
  x =[]
  y =[]
  file = open("sensor_readings.csv")
  reader = csv.reader(file)
  lines= len(list(reader))
  linesm = lines - 5
  with open('sensor_readings.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(str(row[1]))
        y.append(float(row[4])) 
  plt.figure(figsize=(10,7))
  ax = plt.axes()
  # Setting the background color
  ax.set_facecolor("black")
  plt.plot(x,y,'-yo',label='DO')
  plt.xlim(linesm,lines)
  plt.ylim(0,15)
  plt.xlabel(row[0])
  plt.ylabel('mg/l')
  plt.title('Disolved Oxygen')
  plt.grid()
  plt.legend()
  plt.show()

def plotORP():
  x =[]
  y =[]
  file = open("sensor_readings.csv")
  reader = csv.reader(file)
  lines= len(list(reader))
  linesm = lines - 5
  with open('sensor_readings.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(str(row[1]))
        y.append(float(row[5])) 
  plt.figure(figsize=(10,7))
  ax = plt.axes()
  # Setting the background color
  ax.set_facecolor("black")
  plt.plot(x,y,'-bo',label='ORP')
  plt.xlim(linesm,lines)
  plt.ylim(100,500)
  plt.xlabel(row[0])
  plt.ylabel('mv')
  plt.title('ORP')
  plt.grid()
  plt.legend()
  plt.show()

def plotEC():
  x =[]
  y =[]
  file = open("sensor_readings.csv")
  reader = csv.reader(file)
  lines= len(list(reader))
  linesm = lines - 5
  with open('sensor_readings.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(str(row[1]))
        y.append(float(row[6])) 
  plt.figure(figsize=(10,7))
  ax = plt.axes()
  # Setting the background color
  ax.set_facecolor("black")
  plt.plot(x,y,'-go',label='EC')
  plt.xlim(linesm,lines)
  plt.ylim(0,600)
  plt.xlabel(row[0])
  plt.ylabel('us')
  plt.title('Electronic_conductivity')
  plt.grid()
  plt.legend()
  plt.show()
  
def helloCallBack():
  x =[]
  y =[]
  file = open("sensor_readings.csv")
  reader = csv.reader(file)
  lines= len(list(reader))
  linesm = lines - 5
  with open('sensor_readings.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(str(row[1]))
        y.append(float(row[2])) 
  plt.figure(figsize=(10,7))
  ax = plt.axes()
  # Setting the background color
  ax.set_facecolor("black")
  plt.plot(x,y,'-ro',label='PH')
  plt.xlim(linesm,lines)
  plt.ylim(2,7)
  plt.xlabel(row[0])
  plt.ylabel('y')
  plt.title('PH')
  plt.grid()
  plt.legend()
  plt.show()



#GUI


curwp = Label(root,text="Water Quality index meter",bg = "blue",fg = "white", font = "none 20 bold")
curwp.place(x=220,y=25)

curC = Label(root,text="Chemical Pollutants",bg = "orange",fg = "black", font = "none 16 bold")
curC.place(x=323,y=108)

#a1=Label(root, text="Water is pure",bg="orange",fg="black",font="none 12 bold")
#a1.place(x=375,y=200)


curM = Label(root,text=" Micro-Organizms ",bg = "magenta",fg = "black", font = "none 16 bold")
curM.place(x=323,y=263)

#a1=Label(root, text="Water is pure",bg="magenta",fg="black",font="none 12 bold")
#a1.place(x=375,y=345)

curTime = Label(root,bg = "black",fg = "white", font = "none 10 bold")
curTime.place(x=700,y=10)
curDate = Label(root,bg = "black",fg = "white", font = "none 10 bold")
curDate.place(x=700,y=30)

#temp
curTEMP = Label(root,bg = "grey",fg="white",font="none 20 bold")
curTEMP.place(x=10,y=110)
b1= Button(root,image = img2,bg="grey",fg="black",font="none 15 bold", command =plotRTD)
b1.place(x=270,y=110)

#ph
curPH = Label(root, bg = "red",fg="black",font="none 20 bold")
curPH.place(x=10,y=160)
b2= Button(root,image = img2,bg="red",fg="black",font="none 15 bold", command =plotPH)
b2.place(x=270,y=160)

#orp
curORP = Label(root, bg = "skyblue",fg="white",font="none 20 bold")
curORP.place(x=10,y=210)
b3= Button(root,image = img2,bg="skyblue",fg="black",font="none 15 bold", command =plotORP)
b3.place(x=270,y=210)

#DO
curDO = Label(root,bg = "yellow",fg="black",font="none 20 bold")
curDO.place(x=10,y=260)
b4= Button(root,image = img2,bg="yellow",fg="black",font="none 15 bold", command =plotDO)
b4.place(x=270,y=260)

#EC
curEC = Label(root,bg = "green",fg="white",font="none 20 bold")
curEC.place(x=10,y=310)
b5= Button(root,image = img2,bg="green",fg="black",font="none 15 bold", command =plotEC)
b5.place(x=270,y=310)

#TB
curTB = Label(root,bg = "white",fg="black",font="none 20 bold")
curTB.place(x=10,y=360)
b6= Button(root,image = img2,bg="white",fg="black",font="none 15 bold", command =helloCallBack)
b6.place(x=270,y=360)

#sp

curs = Label(root,text = "Plastic_Detection",bg = "white",fg="black",font="none 13 bold")
curs.place(x=600,y=110)

main()
root.mainloop()
