# micropython script for esp32
# Author: Himanshu Tripathi

# This script will make esp32 to connect with the wifi network
# also esp32 will connect with the firebase real-time database
# if button is pressed on the esp32 devkit, it will update the value in RTDB
# also esp32 will read the RTDB and update the state of on-board led
# Ref Link: https://github.com/ckoever/micropython-firebase-realtime-database


import network
import time
import ufirebase as fb
from machine import Pin
import sys

# object for led (output device)
led = Pin(22,Pin.OUT)
# object for button (input device)
button = Pin(5,Pin.IN)
# default led remains off
led.off()

# function to connect with wifi
# esp32 acting as station device 
def connect_wifi(ssid,psk,timeout):
    """restart wifi module and connect with wifi network"""
    # configure esp32 as station device, object for wlan connection 
    wlan = network.WLAN(network.STA_IF)
    # restart wifi module of esp32 
    wlan.active(False)
    time.sleep(1)
    wlan.active(True)
    t = 0
    # connect with wifi
    wlan.connect(ssid,psk)
    # if not connected with wifi wait for given timeout 
    if not wlan.isconnected():
        print("Connecting",end="..")
        while not wlan.isconnected() and t<timeout:
            print(".",end="")
            t += 1
            time.sleep(1)
    # if connected print the IP address of ESP32 
    if wlan.isconnected():
        print("Connected",wlan.ifconfig())
    else:
        print("not connected")

connect_wifi('Galaxy M11','mayank23',10)
# set the database URL 
fb.setURL("https://project1-9f0c3-default-rtdb.firebaseio.com/")
# print for debugging 
print("databse connected")
pressEvent = True
pr=0

# interrupt service routine for button interrupt
def button_isr(pin):
    global pr
    pr=1
    print("button pressed")
    

# enable interrupt request for button pin 
button.irq(trigger=Pin.IRQ_RISING,handler=button_isr)


while True:
    fb.get("testtag1","var1",bg=0)
        # update the led state 
    led.value(fb.var1)
    time.sleep(0.100)
    if pr==1:
        if pressEvent is True:
            fb.put("testtag2",1,bg=0)
            pressEvent = False
            pr=0
        else:
            fb.put("testtag2",0,bg=0)
            pressEvent = True
            pr=0