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

async def messages(client):  # Respond to incoming messages
    global open 
    async for topic, msg, retained in client.queue:
        open = msg
        print((topic, msg, retained))
    
    
async def up(client):  # Respond to connectivity being (re)established
    while True:
        await client.up.wait()  # Wait on an Event
        client.up.clear()
        await client.subscribe('open', 1)  # renew subscriptions


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









