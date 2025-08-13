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
config['ssid'] = 'Mutagir'
config['wifi_pw'] = '12345678'

dh_sens_pin = Pin(20,Pin.IN)  
dh_sens = dht.DHT11(dh_sens_pin)
red_led = Pin(16, Pin.OUT)
buzzer = PWM(Pin(11))
buttonPin = Pin(18, Pin.IN)
buzzer = PWM(Pin(11))
buzzer.duty_u16(80000)
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
count = 1
has_started = False
has_started2 = False
close = 0
temp = 0

def dht_mesure_humid():
        dh_sens.measure()
        humidity = dh_sens.humidity()
        return("Humidity: {}%".format(humidity))
        
def dht_mesure_temp():
        dh_sens.measure()
        temperature = dh_sens.temperature()
        return("Temperature: {}°C".format(temperature))

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
    
def message_on_screen3():
    lcd.clear()
    lcd.move_to(3,0)
    lcd.putstr("abo adam")


def buzzer_sound_fast(duration):
    buzzer = Pin(11, Pin.OUT)
    while True:
        buzzer.value(1) 
        time.sleep_ms(50) 
        buzzer.value(0) 
        time.sleep_ms(50)


    
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
    global temp
    global has_started
    global has_started2
    await client.connect()
    for coroutine in (up, messages):
        asyncio.create_task(coroutine(client))
    await client.publish('open', "1", qos = 1)
    while True:
        await asyncio.sleep(0.25)
        if close == "1":
            while True:
                has_started2 = False
                await asyncio.sleep(0.25)
                if has_started2 == False:
                    has_started2 = True
                    red_led.value(1)
                    message_on_screen()
                if buttonPin.value() == 1:
                    red_led.value(0)
                    message_on_screen2()
                    sleep(5)
                    message_on_screen3()
                    await client.publish('open', "1", qos = 1)
                    await client.publish('close', "0", qos = 1)
                    



while True:
    config["queue_len"] = 1  # Use event interface with default queue size
    MQTTClient.DEBUG = True  # Optional: print diagnostic messages
    client = MQTTClient(config)
    try:
        asyncio.run(main(client))
    finally:
        client.close()  # Prevent LmacRxBlk:1 errors
