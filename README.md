# How to control Turnigy TGY-S518D servo motor 


This datasheet was created for those who want to use this cheap Chineese clone of Robotis Dynamixel MX-28. 

Actually, there aren't any official datasheet for this servo motor on the Internet (at least in non-Chineese segment). The only info about the "Chinamixel" that I could find is provided [here]. 

<img src="https://cdn-global-hk.hobbyking.com/media/catalog/product/cache/1/image/660x415/17f82f742ffe127f42dca9de82fb58b1/legacy/catalog/41219.jpg" width="400" height="300"><img src="https://cdn-global-hk.hobbyking.com/media/catalog/product/cache/1/image/660x415/17f82f742ffe127f42dca9de82fb58b1/legacy/catalog/41216s_2__2.jpg" width="400" height="300">

Some useful features and specifications from that website are:
1. **Features**:
- High torque
- Double end installation, suitable for installation in robot joints
- High precision double bearing
- Good heat dissipation
- Rotation scope: 0~300°
- Can be 360° continuous rotation
- Bus connection, theoretically, 254 units can be in series connection
- 0.25Khz servo update rate
- Compatible with Robotis Dynamixel communication protocols
- Feedback of position, temperature, speed and voltage.
2. **Specifications**:
- Output: Single
- Operating Voltage: 6.0 / 7.4V
- Operating Speed: 0.22 Sec/60° / 0.19 Sec/60°
- Stall Torque: 13.9kg.cm / 16.5kg.cm
- Rotation scope: 0~300°
- Size: 35.5X36X51mm
- Weight: 75g
- Motor: Brushed
- Ball Bearing: 2BB
- Gear: Metal
- Spline Count: 20
- Wire Length: 20cm


"Compatible with Robotis Dynamixel communication protocols" means that it has to support RS-485 via USB2Dynamixel adapter and can be controlled using Dynamixel Wizard. However, it is impossible since the original software always checks for originality of a motor. Being more specific, Dynamixel Wizard is able to find it, thereby prompting the baud rate (500kHz), but do not allow any further actions with TGY-S518D. 

**The method of solving this problem**
It is possible to control TGY-S518D using Arduino board (Mega 2560). However, it will require an additional transceiver module to interface Arduino to RS-458 protocol. I've used this [MAX485 RS485 transiever module]

<img src="https://hobbycomponents.com/1655-home_default/max485-rs485-transceiver-module.jpg" width="250" height="200">

### 1. Wiring connection

|**Arduino**|**MAX485**|**TGY-S518D**|
|:---------:|:--------:|:-----------:|
| Pin 2     | DE       |  -          |
| Pin 2     | RE       |  -          |
| TX0       | DI       |  -          |
| RX0       | RO       |  -          |
| GND       | GND      |  GND        |
| 5V        | VCC      |  -          |
| -         | A        |  Data +     |
| -         | B        |  Data -     |


- Pin 2 - direction pin - controls the MAX485's "enable"
-	Remember: there is a common ground for all connect devices; set current limit to ~1A.
- Only TX0 and RX0 can handle 500K bps (with a 16MHz clock the serial port can handle 1Mbps). Other serial ports are limited to 115200 bps. To use them, firstly, change baud rate with *“Dynamixel.setBD()”* function. (*some TGY-S518D can’t store new baud rate! Every time when power supply turned off, motor's baud rate changes to initial 500k bps*) 
-	RS-485 supports up to 32 independent channels, so you can control many servos with nothing more than an Arduino and one MAX485 module! Just remember to give your servo a unique ID.

[here]: https://hobbyking.com/en_us/turnigy-tgy-s518d-300-digital-metal-gear-intelligent-robot-servo-16-5kg-0-19s.html?___store=en_us
[MAX485 RS485 transiever module]: https://hobbycomponents.com/wired-wireless/663-max485-rs485-transceiver-module
Files:

1. "Dynamixel_python.py" - the python code itself

2. "chinamixel readme.docx" - detailed HowTo for connection and getting started

