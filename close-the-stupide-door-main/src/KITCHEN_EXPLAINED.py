from mqtt_as import MQTTClient, config
import asyncio
import dht
from machine import Pin
from time import sleep
from machine import ADC
import urequests as requests


config['server'] = '64.225.110.253'
config['port'] = 1883
config['user'] = 'king'
config['password'] = 'arthur'
config['ssid'] = 'osama_wifi'
config['wifi_pw'] = 'osama123456'


green_led = Pin(16, Pin.OUT)
dh_sens_pin = machine.Pin(28, machine.Pin.IN)  
dh_sens = dht.DHT11(dh_sens_pin)
analog_pin = 27
yellow_led = Pin(17, Pin.OUT)
open = None
time_exceeded = False
started = False
def dht_mesure():
        dh_sens.measure()
        temperature = dh_sens.temperature()
          
        sensor_value = machine.ADC(analog_pin).read_u16()
        temp2 = round(-27.0 + (sensor_value / 65535.0) * 120.0)
        
        differince = (temperature - temp2)
       
        return differince
#This code snippet defines a function named dht_mesure().

#Inside the function, it calls dh_sens.measure() to measure the
 #temperature using a DHT sensor.

#Then, it reads the sensor value from an analog pin using
 #the machine.ADC(analog_pin).read_u16() method and calculates #the temperature in degrees Celsius.

#Finally, it calculates the difference between the measured
 #temperature and the calculated temperature and returns the #difference.

async def messages(client):  # Respond to incoming messages
    global open 
    async for topic, msg, retained in client.queue:
        open = msg
        print((topic, msg, retained))
#This code defines an asynchronous function called messages that 
#takes a client argument. It uses a global variable called close.
#Inside the function, it starts an asynchronous loop that continuously
#retrieves messages from the client.queue.
#For each retrieved message, it assigns the message to 
#he close variable and prints the topic, message, and retention status.
    #This code snippet defines a function named dht_mesure().

    
async def up(client):  # Respond to connectivity being (re)established
    while True:
        await client.up.wait()  # Wait on an Event
        client.up.clear()
        await client.subscribe('open', 1)  # renew subscriptions
#This code defines an async function called up that takes
# a client parameter. It enters an infinite loop and waits for a signal 
#from client.up. Once the signal is received, it clears the signal flag, 
#subscribes to an event called 'OPEN' with a priority of 1, and then
#continues to the next iteration of the loop.   

async def main(client,dht_mesure):
    global open
    await client.connect()
    for coroutine in (up, messages):
        asyncio.create_task(coroutine(client))
    await client.publish('close', "0" , qos = 1)
    await client.publish('open', "1" , qos = 1)
    
    while True:
        await asyncio.sleep(0.25)
        while True:
            if open == "1":
                green_led.value(1)
                differince = dht_mesure()
                print(differince)
                await client.publish('temp-diff', str(differince), qos = 1)
                if differince in range(15,100):
                    green_led.value(1)
                    yellow_led.value(1)
                    sleep(30)
                    if differince in range(15,100):
                        green_led.value(0)
                        yellow_led.value(1)
                        await client.publish('close', '1', qos = 1)
                        while True:
                            requests.post("https://ntfy.sh/close-the-stupied-door",
                                            data="door open detected by sensor",
                                            headers={
                                                "Title": "ALERT: frys door is open",
                                                "Priority": "5",
                                                "Tags": "rotating_light",
                                                })
                            print("door is open, notification sent")
                            sleep(10)
                            break
                        break 
                    elif differince in range(-100,14):
                        green_led.value(1)
                        yellow_led.value(0)
                        await client.publish('close', '0', qos = 1)
                        
                        break
                elif differince in range(-100,14):
                    green_led.value(1)
                    yellow_led.value(0)
                    await client.publish('close', '0', qos = 1)
                    break
            
                    
            open = None



#This code defines an asynchronous function called main that takes
#two arguments: client and dht_mesure. Inside the function, it
#connects the client to some remote service. Then, it creates two
#tasks using asyncio.create_task() to run
#the up and messages coroutines concurrently with the client as an
#argument. Next, it publishes two messages using
#the client.publish() method. After that, it enters an infinite loop that
#sleeps for a quarter of a second on each iteration. Inside the loop, it
#checks the value of a global variable called open. If the value is "1",
#it performs some actions, such as turning on LEDs, measuring a
#difference, printing the difference, and publishing a message with
#the difference. Based on the value of the difference, it takes different
#actions and publishes more messages. The loop continues until the
#value of open is changed. Additionally, if certain conditions are met (specifically,
# if the temperature difference remains in a predefined critical range), 
# the script uses the requests library to send an HTTP POST request to https://ntfy.sh/close-the-stupied-door. 
# This request is a notification mechanism, which includes details like the title of the alert, priority level, 
# and tags in the headers. This part of the script is crucial for sending real-time alerts about the door's status, 
# enhancing the responsiveness of the system in critical situations.
        


while True:

    config["queue_len"] = 1  # Use event interface with default queue size
    MQTTClient.DEBUG = True  # Optional: print diagnostic messages
    client = MQTTClient(config)
    try:
        asyncio.run(main(client, dht_mesure))
    except KeyboardInterrupt:
        print("Stopped")    
    finally:
        client.close()








