from mqtt_as import MQTTClient, config
import asyncio
import dht
from machine import Pin
from time import sleep
from machine import ADC



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
yellow = Pin(17, Pin.OUT)
open = None
time_exceeded = False
def dht_mesure():
        dh_sens.measure()
        temperature = dh_sens.temperature()
          
        sensor_value = machine.ADC(analog_pin).read_u16()
        temp2 = round(-34.0 + (sensor_value / 65535.0) * 120.0)
        
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
    green_led.value(1)
    yellow.value(0)
    await client.connect()
    for coroutine in (up, messages):
        asyncio.create_task(coroutine(client))
    await client.publish('close', "0" , qos = 1)
    
    while True:
        await asyncio.sleep(0.25)
        differince = dht_mesure()
        print(differince)     
        while True:
            if differince in range(5,100):
                yellow.value(1)
                sleep(30)
                if differince in range(5,100):
                    green_led.value(0)
                    await client.publish('close', '1', qos = 1)
                    break
                elif differince in range(-100,5):
                    green_led.value(1)
                    await client.publish('open', '1', qos = 1)
                    break
            
            
        if open == "0":
            yellow.value(0)
            green_led.value(1)
            await client.publish('close', "0", qos=1)
                
                
            open = None
        




config["queue_len"] = 1  # Use event interface with default queue size
MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
try:
    asyncio.run(main(client, dht_mesure))
except KeyboardInterrupt:
    print("Stopped")    
finally:
    client.close()




