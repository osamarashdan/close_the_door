from mqtt_as import MQTTClient, config
import asyncio
from time import sleep
from machine import Pin, PWM, I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
import dht
import time


config['server'] = '64.225.110.253'
config['port'] = 1883
config['user'] = 'king'
config['password'] = 'arthur'
config['ssid'] = 'osama_wifi'
config['wifi_pw'] = 'osama123456'

dh_sens_pin = Pin(26,Pin.IN)  
dh_sens = dht.DHT11(dh_sens_pin)
red_led = Pin(16, Pin.OUT)
buzzer = PWM(Pin(11))
buttonPin = Pin(18, Pin.IN)
tones = {'G6': 1568, 'C7': 2093}
Alert = ["G6", 0, "C7", 0 ,"G6", 0, "C7", 0 ,"G6", 0, "C7", 0 ,"G6", 0, "C7", 0,"G6", 0, "C7", 0 ,"G6", 0, "C7", 0 ,"G6", 0, "C7", 0 ,"G6", 0, "C7", 0 ]
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20



i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
has_started = False
has_started2 = False
close = 0


def dht_mesure_humid():
        dh_sens.measure()
        humidity = dh_sens.humidity()
        return humidity
        
def dht_mesure_temp():
        dh_sens.measure()
        temperature = dh_sens.temperature()
        return temperature


def message_on_screen():
    lcd.clear()
    lcd.move_to(3,0)
    lcd.putstr("Close  The")
    lcd.move_to(2,1)
    lcd.putstr("Stupide Door")

def message_on_screen2():
    lcd.clear()
    lcd.move_to(3,0)
    lcd.putstr("Thank  You")
    
def message_on_screen3(temperature, humidity):
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr("Temperature: " + str(temperature))
    lcd.move_to(0,1)
    lcd.putstr("Humidity: " + str(humidity))



def playtone(frequency):
    buzzer.duty_u16(10000)
    buzzer.freq(frequency)

def bequiet():
    buzzer.duty_u16(0)


    
def Alarm(Alert):
    for i in range(len(Alert)):
        if (Alert[i] == 0 ):
            bequiet()
         

        elif (Alert[i] == 'G6' or Alert[i] == "C7" ) :
            playtone(tones[Alert[i]])
            sleep(0.25)


    
async def messages(client):
    global close
    async for topic, msg, retained in client.queue:
        close = msg
        print((topic, msg, retained))
        

async def up(client):
    while True:
        await client.up.wait()
        client.up.clear()
        await client.subscribe('close', 1)
        
        
async def main(client):
    global close
    global has_started
    global has_started2
    await client.connect()
    for coroutine in (up, messages):
        asyncio.create_task(coroutine(client))
    await client.publish('open', "1", qos = 1)
    while True:
        await asyncio.sleep(0.25)
        if close == "0":
            while True:
                await asyncio.sleep(0.25)
                if has_started == True:
                    message_on_screen3(dht_mesure_temp(), dht_mesure_humid())
                    red_led.value(0)
                    has_started = False
                    sleep(30)
                    has_started2 = False
                    await client.publish('open', "1", qos = 1)
                    break
                if has_started == False:
                    has_started = True
                break
                

        if close == "1":
            while True:
                await asyncio.sleep(0.25)
                if has_started2 == False:
                    has_started2 = True
                    message_on_screen()
                    red_led.value(1)
                    Alarm(Alert)
                    break
                if buttonPin.value() == 1:
                    bequiet()
                    red_led.value(0)
                    message_on_screen2()
                    sleep(5)
                    has_started = True
                    close = None
                    await client.publish('close', "0", qos = 1)
                    break
                break
            
        


                
                




while True:
    config["queue_len"] = 1  # Use event interface with default queue size
    MQTTClient.DEBUG = True  # Optional: print diagnostic messages
    client = MQTTClient(config)
    try:
        asyncio.run(main(client))
    finally:
        client.close()  # Prevent LmacRxBlk:1 errors
    