# Hardware Description

## Raspberry Pico W

![Raspberry Pico W Datasheet](../img/Raspberry-Pi-RP2040-Microcontroller-Pico-Board-Pinout-1_1.png)

- [MicroPython](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html)
- [MicroPython UF2](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html)

### Living Room Setup

![Living Room Setup](../img/IMG_7922.jpg)

#### Screen Setup

- Power: Pin 40 on Raspberry Pico
- Ground: Pin 38 on Raspberry Pico
- SDA (Serial Data): Pin 1 on Raspberry Pico
- SCL (Serial Clock): Pin 2 on Raspberry Pico

![Screen Wiring](../img/IMG_7921.jpg)

#### DH11 Sensor Setup

- Pin 1 (GPIO): Any GPIO pin on Raspberry Pico
- Pin 2 (Data): Connect as needed
- Pin 3 (Power): Raspberry Pico Power
- Pin 4 (Ground): Raspberry Pico Ground

![DH11 Sensor Wiring](<../img/dht11 - Copy.png>)

#### Buzzer Setup

![Buzzer Wiring](../img/IMG_7925.jpg)

#### Button Setup

![Button Wiring](<../img/Screenshot 2024-01-11 012012.png>)

#### Red LED Setup

- Short Pin: Raspberry Pico Ground
- Long Pin: GPIO Pin on Raspberry Pico

![Red LED Wiring](../img/R.jpeg)

#### Living Room Prototype

![Living Room Prototype](../img/image0.jpg)

### Kitchen Setup

![Kitchen Setup](../img/IMG_7923.jpg)

#### Analog and DHT11 Setup

- Signal Pin to GPIO: GPIO 14 on Raspberry Pico
- Ground for Signal Pin: Connect to DHT11 Pin 1
- 3V3 Power Supply: Connect to DHT11 Pin 1
- DHT11 Data to GPIO: GPIO 15 on Raspberry Pico
- DHT11 Ground to Raspberry Pi Pico Ground: Pin 23 on Raspberry Pico
- Analog Ground: Pin 3 on the lower part of the circuit board

![Analog and DHT11 Wiring](../img/1.jpg)

#### Kitchen Prototype

![Kitchen Prototype](../img/prototype.jpg)
