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
buzzer = PWM(Pin(17))
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
#This code snippet defines a function called dht_mesure_humid
#that measures the humidity using a DHT sensor.
#It calls the measure method of the sensor to obtain the humidity value,
#which is then stored in the humidity variable. 
#Finally, the function returns the humidity value.
        
def dht_mesure_temp():
        dh_sens.measure()
        temperature = dh_sens.temperature()
        return temperature
#This code snippet defines a function called dht_mesure_temp that
 #measures the temperature using a DHT sensor. It first calls
 #the measure() function on the sensor object dh_sens, then assigns
 #the temperature value returned by the temperature() function to the 
#variable temperature, and finally returns the temperature value.

def message_on_screen():
    lcd.clear()
    lcd.move_to(3,0)
    lcd.putstr("Close  The")
    lcd.move_to(2,1)
    lcd.putstr("Stupide Door")
#This code defines a function called message_on_screen. Inside the 
    #function, it clears the LCD screen, moves the cursor to position (3,0) 
    #on the screen, and writes the string "Close The". Then it moves the 
    #cursor to position (2,1) and writes the string "Stupide Door" on the 
    #screen.

def message_on_screen2():
    lcd.clear()
    lcd.move_to(3,0)
    lcd.putstr("Thank  You")
    #This code snippet defines a function called message_on_screen2 that 
    #clears the LCD screen, moves the cursor to position (3,0), and 
    #displays the message "Thank You" on the LCD screen.
    
def message_on_screen3(temperature, humidity):
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr("Temperature: " + str(temperature))
    lcd.move_to(0,1)
    lcd.putstr("Humidity: " + str(humidity))
#This code defines a function message_on_screen3 that takes in two 
    #parameters: temperature and humidity. Inside the function, it clears 
    #the LCD screen, moves the cursor to the top-left corner, and displays
     #the temperature and humidity readings on separate lines.


def playtone(frequency):
    buzzer.duty_u16(50000)
    buzzer.freq(frequency)
#This code defines a function called playtone that takes 
    #a frequency parameter. Inside the function, it sets the duty cycle of a 
    #buzzer to 50000 and then sets the frequency of the buzzer to the #given frequency.


def bequiet():
    buzzer.duty_u16(0)
#This code defines a function called bequiet that sets the duty cycle of
#a buzzer to 0.

    
def Alarm(Alert):
    for i in range(len(Alert)):
        if (Alert[i] == 0 ):
            bequiet()
         

        elif (Alert[i] == 'G6' or Alert[i] == "C7" ) :
            playtone(tones[Alert[i]])
            sleep(0.25)
#This code defines a function called Alarm that takes in a list 
#called Alert as an argument. It loops through each element in 
#the Alert list and performs different actions based on the element's
 #value. If the element is 0, it calls a function called bequiet(). If the
#element is either 'G6' or 'C7', it calls a function called playtone() with
#the corresponding tone from a dictionary called tones and then
#pauses for 0.25 seconds.

    
async def messages(client):
    global close
    async for topic, msg, retained in client.queue:
        close = msg
        print((topic, msg, retained))
        
#This code defines an asynchronous function called messages that 
#takes a client argument. It uses a global variable called close.
#Inside the function, it starts an asynchronous loop that continuously
#retrieves messages from the client.queue.
#For each retrieved message, it assigns the message to 
#he close variable and prints the topic, message, and retention status.
        

async def up(client):
    while True:
        await client.up.wait()
        client.up.clear()
        await client.subscribe('close', 1)
#This code defines an async function called up that takes
# a client parameter. It enters an infinite loop and waits for a signal 
#from client.up. Once the signal is received, it clears the signal flag, 
#subscribes to an event called 'close' with a priority of 1, and then
#continues to the next iteration of the loop.     
        
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
#This code snippet defines an asynchronous main function that takes a 
#client parameter. It performs the following actions:
#1-Connects to the client asynchronously using await client.connect().
#2-Creates two tasks, up and messages, using asyncio.create_task() 
#and executes them concurrently with the client as a parameter.
#3-Publishes a message with the topic 'open' and payload '1' to the
# client with Quality of Service (QoS) set to 1 using await client.publish('open', "1", qos=1).
#4-Enters an infinite loop and repeats the following steps:
# A- Waits for 0.25 seconds using await asyncio.sleep(0.25).
# B- Checks the value of the close variable. If it is equal to "0", 
            

#it enters another loop and repeats the following steps:
#1-Waits for 0.25 seconds using await asyncio.sleep(0.25).
#2-Checks the value of the has_started variable. If it is True, 
# it calls the message_on_screen3 function with the results of the #dht_mesure_temp and dht_mesure_humid functions,
# sets the red_led value to 0, sets has_started to False, 
#sleeps for 30 seconds, sets has_started2 to False,
# and publishes a message with the topic 'open' and 
#payload '1' to the client with QoS set to 1.
#3- If has_started is False, it sets has_started to True and breaks the loop.
            

#If the value of close is "1", it enters another loop and repeats the following steps:
#1- Waits for 0.25 seconds using await asyncio.sleep(0.25).
#2- Checks the value of the has_started2 variable. 
#If it is False, it sets has_started2 to True, calls the message_on_screen #function, sets the red_led value to 1, and triggers an 
#alarm using the Alarm function with the Alert parameter.
#3- If the value of the buttonPin is 1, it calls the bequiet function, 
#sets the red_led value to 0, calls the message_on_screen2 function,
#sleeps for 5 seconds, sets has_started to True, sets close to None,
#and publishes a message with the topic 'close' and payload '0' to the client #with QoS set to 1.
#4- Breaks the loop.

           
        


                
                




while True:
    config["queue_len"] = 1  # Use event interface with default queue size
    MQTTClient.DEBUG = True  # Optional: print diagnostic messages
    client = MQTTClient(config)
    try:
        asyncio.run(main(client))
    finally:
        client.close()  # Prevent LmacRxBlk:1 errors
    