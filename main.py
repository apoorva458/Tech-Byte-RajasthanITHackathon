
import network
import time
import ufirebase as fb
from machine import Pin
import sys


led = Pin(22,Pin.OUT)

button = Pin(5,Pin.IN)

led.off()


def connect_wifi(ssid,psk,timeout):
    """restart wifi module and connect with wifi network"""
     
    wlan = network.WLAN(network.STA_IF)
     
    wlan.active(False)
    time.sleep(1)
    wlan.active(True)
    t = 0
    
    wlan.connect(ssid,psk)
    
    if not wlan.isconnected():
        print("Connecting",end="..")
        while not wlan.isconnected() and t<timeout:
            print(".",end="")
            t += 1
            time.sleep(1)
    
    if wlan.isconnected():
        print("Connected",wlan.ifconfig())
    else:
        print("not connected")

connect_wifi('Galaxy M11','Mayank23',10)
 
fb.setURL("https://project1-9f0c3-default-rtdb.firebaseio.com/")

print("databse connected")
pressEvent = True
pr=0


def button_isr(pin):
    global pr
    pr=1
    print("button pressed")
    


button.irq(trigger=Pin.IRQ_RISING,handler=button_isr)


while True:
    fb.get("testtag1","var1",bg=0)
    
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