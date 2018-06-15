#python -c "execfile('Dynamixel_python.py'); function(var...)"
import serial
import crcmod
import struct
import numpy as np
import time

	#EEPROM AREA  ///////////////////////////////////////////////////////////
AX_MODEL_NUMBER_L           =0
AX_MODEL_NUMBER_H           =1
AX_VERSION                  =2
AX_ID                       =3
AX_BAUD_RATE                =4
AX_RETURN_DELAY_TIME        =5
AX_CW_ANGLE_LIMIT_L         =6
AX_CW_ANGLE_LIMIT_H         =7
AX_CCW_ANGLE_LIMIT_L        =8
AX_CCW_ANGLE_LIMIT_H        =9
AX_SYSTEM_DATA2             =10
AX_LIMIT_TEMPERATURE        =11
AX_DOWN_LIMIT_VOLTAGE       =12
AX_UP_LIMIT_VOLTAGE         =13
AX_MAX_TORQUE_L             =14
AX_MAX_TORQUE_H             =15
AX_RETURN_LEVEL             =16
AX_ALARM_LED                =17
AX_ALARM_SHUTDOWN           =18
AX_OPERATING_MODE           =19
AX_DOWN_CALIBRATION_L       =20
AX_DOWN_CALIBRATION_H       =21
AX_UP_CALIBRATION_L         =22
AX_UP_CALIBRATION_H         =23

	#RAM AREA  //////////////////////////////////////////////////////////////
AX_TORQUE_ENABLE            =24
AX_LED                      =25
AX_CW_COMPLIANCE_MARGIN     =26
AX_CCW_COMPLIANCE_MARGIN    =27
AX_CW_COMPLIANCE_SLOPE      =28
AX_CCW_COMPLIANCE_SLOPE     =29
AX_GOAL_POSITION_L          =30
AX_GOAL_POSITION_H          =31
AX_GOAL_SPEED_L             =32
AX_GOAL_SPEED_H             =33
AX_TORQUE_LIMIT_L           =34
AX_TORQUE_LIMIT_H           =35
AX_PRESENT_POSITION_L       =36
AX_PRESENT_POSITION_H       =37
AX_PRESENT_SPEED_L          =38
AX_PRESENT_SPEED_H          =39
AX_PRESENT_LOAD_L           =40
AX_PRESENT_LOAD_H           =41
AX_PRESENT_VOLTAGE          =42
AX_PRESENT_TEMPERATURE      =43
AX_REGISTERED_INSTRUCTION   =44
AX_PAUSE_TIME               =45
AX_MOVING                   =46
AX_LOCK                     =47
AX_PUNCH_L                  =48
AX_PUNCH_H                  =49

    #Status Return Levels ///////////////////////////////////////////////////////////////
AX_RETURN_NONE              =0
AX_RETURN_READ              =1
AX_RETURN_ALL               =2

    #Instruction Set ///////////////////////////////////////////////////////////////
AX_PING                     =1
AX_READ_DATA                =2
AX_WRITE_DATA               =3
AX_REG_WRITE                =4
AX_ACTION                   =5
AX_RESET                    =6
AX_SYNC_WRITE               =131

	#Specials ///////////////////////////////////////////////////////////////
OFF                         =0
ON                          =1
LEFT			    =0 #CW
RIGHT                       =1 #CCW
WHEEL			    =0
SERVO			    =1
AX_BYTE_READ                =1
AX_BYTE_READ_POS            =2
AX_RESET_LENGTH	            =2
AX_ACTION_LENGTH	    =2
AX_ID_LENGTH                =4
AX_LR_LENGTH                =4
AX_SRL_LENGTH               =4
AX_RDT_LENGTH               =4
AX_LEDALARM_LENGTH          =4
AX_SALARM_LENGTH            =4
AX_TL_LENGTH                =4
AX_VL_LENGTH                =6
AX_CM_LENGTH                =6
AX_CS_LENGTH                =6
AX_CCW_CW_LENGTH            =8
AX_BD_LENGTH                =4
AX_TEM_LENGTH               =4
AX_MOVING_LENGTH            =4
AX_RWS_LENGTH               =4
AX_VOLT_LENGTH              =4
AX_LED_LENGTH               =4
AX_TORQUE_LENGTH            =4
AX_POS_LENGTH               =4
AX_GOAL_LENGTH              =5
AX_MT_LENGTH                =5
AX_PUNCH_LENGTH             =5
AX_SPEED_LENGTH             =5
AX_GOAL_SP_LENGTH           =7
AX_ACTION_CHECKSUM	    =250
BROADCAST_ID                =254
AX_START                    =255
AX_CCW_AL_L                 =255 
AX_CCW_AL_H                 =3
TIME_OUT 		    =10         #Este parametro depende de la velocidad de transmision
TX_DELAY_TIME               =400        #Este parametro depende de la velocidad de transmision - pero pueden ser cambiados para mayor velocidad.
Tx_MODE 		    =1
Rx_MODE 		    =0
LOCK 			    =1


serial_port = serial.Serial('/dev/ttyUSB0', baudrate=500000, timeout=0.05)


def dyn_ping(ID):
	checksum = (~(ID + AX_READ_DATA + AX_PING))&0xFF
	print('checksum: ' + ":".join("{:08b}".format(checksum)))
	packet = bytearray([0xff, 0xff, ID, 0x02, 0x01, checksum])
	print('Packet: ' + ":".join("{:08b}".format(c) for c in packet))
	print('Packet: ' + ":".join("{:02x}".format(c) for c in packet))
	serial_port.write(packet)
	header = serial_port.read(3)
	print('Received header: ' + ":".join("{:02x}".format(ord(c)) for c in header))
	body = serial_port.read(4)
	print('Received body: ' + ":".join("{:02x}".format(ord(c)) for c in body))
	return


def move(ID, Angle):
	Position = int(3.41*Angle)
	Position_H = Position >> 8;
	Position_L = Position;
	
	checksum = (~(ID + AX_GOAL_LENGTH + AX_WRITE_DATA + AX_GOAL_POSITION_L + Position_L + Position_H))&0xFF
	print('checksum: ' + ":".join("{:08b}".format(checksum)))
	
	packet = np.array((
				(int("0xFF", 16)),
				(int("0xFF", 16)),
				(int(str(ID), 16)),
				(int(str(AX_GOAL_LENGTH), 16)),
				(int(str(AX_WRITE_DATA), 16)), 
				(int(str(AX_GOAL_POSITION_L), 10)),
				(int(str(Position_L), 10)),
				(int(str(Position_H), 10)),
				(int(str(checksum), 10))
	)) 
	z = np.int8(packet)
	print('Packet: ' + ":".join("{:08b}".format(c) for c in packet))
	print('Packet: ' + ":".join("{:02x}".format(c) for c in packet))
	
	serial_port.write(z.tobytes())
	header = serial_port.read(3)
	print('Received header: ' + ":".join("{:02x}".format(ord(c)) for c in header))
	body = serial_port.read(4)
	print('Received body: ' + ":".join("{:02x}".format(ord(c)) for c in body))
	return

def setID(ID, newID):
	checksum = (~(ID + AX_ID_LENGTH + AX_WRITE_DATA + AX_ID + newID))&0xFF
	print('checksum: ' + ":".join("{:08b}".format(checksum)))
	packet = bytearray([0xff, 0xff, ID, AX_ID_LENGTH, AX_WRITE_DATA, AX_ID, newID, checksum])
	print('Packet: ' + ":".join("{:08b}".format(c) for c in packet))
	print('Packet: ' + ":".join("{:02x}".format(c) for c in packet))
	serial_port.write(packet)
	header = serial_port.read(3)
	print('Received header: ' + ":".join("{:02x}".format(ord(c)) for c in header))
	body = serial_port.read(4)
	print('Received body: ' + ":".join("{:02x}".format(ord(c)) for c in body))
	return

def setBD(ID, baud):
	Baud_Rate = (2000000/baud) - 1
	checksum = (~(ID + AX_BD_LENGTH + AX_WRITE_DATA + AX_BAUD_RATE + Baud_Rate))&0xFF
	print('checksum: ' + ":".join("{:08b}".format(checksum)))
	packet = bytearray([0xff, 0xff, ID, AX_BD_LENGTH, AX_WRITE_DATA, AX_BAUD_RATE, Baud_Rate, checksum])
	print('Packet: ' + ":".join("{:08b}".format(c) for c in packet))
	print('Packet: ' + ":".join("{:02x}".format(c) for c in packet))
	serial_port.write(packet)
	header = serial_port.read(3)
	print('Received header: ' + ":".join("{:02x}".format(ord(c)) for c in header))
	body = serial_port.read(4)
	print('Received body: ' + ":".join("{:02x}".format(ord(c)) for c in body))
	return

def moveSpeed(ID, Angle, Speed):
	Position = int(3.41*Angle)
	Position_H = Position >> 8;
	Position_L = Position;
	Speed_H = Speed >> 8;
	Speed_L = Speed;
	checksum = (~(ID + AX_GOAL_SP_LENGTH + AX_WRITE_DATA + AX_GOAL_POSITION_L + Position_L + Position_H + Speed_L + Speed_H))&0xFF
	print('checksum: ' + ":".join("{:08b}".format(checksum)))
	packet = np.array((
				(int("0xff",16)),
				(int("0xff",16)),
				(int(str(ID),16)),
				(int(str(AX_GOAL_SP_LENGTH),16)),
				(int(str(AX_WRITE_DATA),16)),
				(int(str(AX_GOAL_POSITION_L),10)),
				(int(str(Position_L),10)),
				(int(str(Position_H),10)),
				(int(str(Speed_L),10)),
				(int(str(Speed_H),10)),
				(int(str(checksum),10))
	))
	z = np.int8(packet)
	print('Packet: ' + ":".join("{:08b}".format(c) for c in packet))
	print('Packet: ' + ":".join("{:02x}".format(c) for c in packet))
	
	serial_port.write(z.tobytes())
	header = serial_port.read(3)
	print('Received header: ' + ":".join("{:02x}".format(ord(c)) for c in header))
	body = serial_port.read(4)
	print('Received body: ' + ":".join("{:02x}".format(ord(c)) for c in body))
	return

def mode(ID, MODE): #wheel=0, servo=1
	if(MODE == 0):
		AX_CCW_AL_LT=0
		checksum = (~(ID + AX_GOAL_LENGTH + AX_WRITE_DATA + AX_CCW_ANGLE_LIMIT_L))&0xFF
		packet = np.array((
					(int("0xff",16)),
					(int("0xff",16)),
					(int(str(ID),16)),
					(int(str(AX_GOAL_LENGTH),16)),
					(int(str(AX_WRITE_DATA),16)),
					(int(str(AX_CCW_ANGLE_LIMIT_L),16)),
					(int(str(AX_CCW_AL_LT),16)),
					(int(str(AX_CCW_AL_LT),16)),
					(int(str(checksum), 10))
		))
		z = np.int8(packet)
		print('Packet: ' + ":".join("{:08b}".format(c) for c in packet))
		print('Packet: ' + ":".join("{:02x}".format(c) for c in packet))
		
		serial_port.write(z.tobytes())
		header = serial_port.read(3)
		print('Received header: ' + ":".join("{:02x}".format(ord(c)) for c in header))
		body = serial_port.read(4)
		print('Received body: ' + ":".join("{:02x}".format(ord(c)) for c in body))
		return

	if(MODE == 1):
		wheel(ID, 0, 0)
		checksum = (~(ID + AX_GOAL_LENGTH + AX_WRITE_DATA + AX_CCW_ANGLE_LIMIT_L + AX_CCW_AL_L + AX_CCW_AL_H))&0xFF
		packet = np.array((
					(int("0xff",16)),
					(int("0xff",16)),
					(int(str(ID),16)),
					(int(str(AX_GOAL_LENGTH),16)),
					(int(str(AX_WRITE_DATA),16)),
					(int(str(AX_CCW_ANGLE_LIMIT_L),10)),
					(int(str(AX_CCW_AL_L),10)),
					(int(str(AX_CCW_AL_H),10)),
					(int(str(checksum), 10))
		))
		z = np.int8(packet)
		print('Packet: ' + ":".join("{:08b}".format(c) for c in packet))
		print('Packet: ' + ":".join("{:02x}".format(c) for c in packet))
		
		serial_port.write(z.tobytes())
		header = serial_port.read(3)
		print('Received header: ' + ":".join("{:02x}".format(ord(c)) for c in header))
		body = serial_port.read(4)
		print('Received body: ' + ":".join("{:02x}".format(ord(c)) for c in body))
		return
	return

def wheel(ID, SIDE, Speed):
	if (SIDE == 0):  #LEFT(CW)
		Speed_H = Speed >> 8;
		Speed_L = Speed;
		checksum = (~(ID + AX_SPEED_LENGTH + AX_WRITE_DATA + AX_GOAL_SPEED_L + Speed_L + Speed_H))&0xFF
		packet = bytearray((
					(int("0xff",16)), 
					(int("0xff",16)), 
					(int(str(ID),16)),
					(int(str(AX_SPEED_LENGTH),16)),
					(int(str(AX_WRITE_DATA),16)),
					(int(str(AX_GOAL_SPEED_L), 10)),
					(int(str(Speed_L),10)),
					(int(str(Speed_H),10)),
					(int(str(checksum),10))
		))
		z = np.int8(packet) 
		print('Packet: ' + ":".join("{:08b}".format(c) for c in packet))
		print('Packet: ' + ":".join("{:02x}".format(c) for c in packet))
		
		serial_port.write(z.tobytes())
		header = serial_port.read(3)
		print('Received header: ' + ":".join("{:02x}".format(ord(c)) for c in header))
		body = serial_port.read(4)
		print('Received body: ' + ":".join("{:02x}".format(ord(c)) for c in body))
		return
	
	else: #RIGHT (CCW)
		Speed_H = (Speed >> 8) + 4
		Speed_L = Speed;
		checksum = (~(ID + AX_SPEED_LENGTH + AX_WRITE_DATA + AX_GOAL_SPEED_L + Speed_L + Speed_H))&0xFF
		packet = bytearray((
					(int("0xff",16)), 
					(int("0xff",16)), 
					(int(str(ID),16)),
					(int(str(AX_SPEED_LENGTH),16)),
					(int(str(AX_WRITE_DATA),16)),
					(int(str(AX_GOAL_SPEED_L), 10)),
					(int(str(Speed_L),10)),
					(int(str(Speed_H),10)),
					(int(str(checksum),10))
		))
		z = np.int8(packet) 
		print('Packet: ' + ":".join("{:08b}".format(c) for c in packet))
		print('Packet: ' + ":".join("{:02x}".format(c) for c in packet))
		
		serial_port.write(z.tobytes())
		header = serial_port.read(3)
		print('Received header: ' + ":".join("{:02x}".format(ord(c)) for c in header))
		body = serial_port.read(4)
		print('Received body: ' + ":".join("{:02x}".format(ord(c)) for c in body))
		return

def ledStatus(ID, Status):
	checksum = (~(ID + AX_LED_LENGTH + AX_WRITE_DATA + AX_LED + Status))&0xFF
	packet = bytearray([0xff, 0xff, ID, AX_LED_LENGTH, AX_WRITE_DATA, AX_LED, Status, checksum])
	print('Packet: ' + ":".join("{:08b}".format(c) for c in packet))
	print('Packet: ' + ":".join("{:02x}".format(c) for c in packet))
	serial_port.write(packet)
	header = serial_port.read(3)
	print('Received header: ' + ":".join("{:02x}".format(ord(c)) for c in header))
	body = serial_port.read(4)
	print('Received body: ' + ":".join("{:02x}".format(ord(c)) for c in body))
	return

def setVoltageLimit(ID, DVoltage, UVoltage):
	checksum = (~(ID + AX_VL_LENGTH +AX_WRITE_DATA+ AX_DOWN_LIMIT_VOLTAGE + DVoltage + UVoltage))&0xFF
	packet = bytearray([0xff, 0xff, ID, AX_VL_LENGTH, AX_WRITE_DATA, AX_DOWN_LIMIT_VOLTAGE, DVoltage, UVoltage, checksum])
	print('Packet: ' + ":".join("{:08b}".format(c) for c in packet))
	print('Packet: ' + ":".join("{:02x}".format(c) for c in packet))
	serial_port.write(packet)
	header = serial_port.read(3)
	print('Received header: ' + ":".join("{:02x}".format(ord(c)) for c in header))
	body = serial_port.read(4)
	print('Received body: ' + ":".join("{:02x}".format(ord(c)) for c in body))
	return
	
def lock(ID):
	checksum = (~(ID + AX_LR_LENGTH + AX_WRITE_DATA + AX_LOCK + LOCK))&0xFF
	packet = bytearray([0xff, 0xff, ID, AX_LR_LENGTH, AX_WRITE_DATA, AX_LOCK, LOCK, checksum])
	print('Packet: ' + ":".join("{:08b}".format(c) for c in packet))
	print('Packet: ' + ":".join("{:02x}".format(c) for c in packet))
	serial_port.write(packet)
	header = serial_port.read(3)
	print('Received header: ' + ":".join("{:02x}".format(ord(c)) for c in header))
	body = serial_port.read(4)
	print('Received body: ' + ":".join("{:02x}".format(ord(c)) for c in body))
	return

def reset(ID):
	checksum = (~(ID + AX_RESET_LENGTH + AX_RESET))&0xFF
	packet = bytearray([0xff, 0xff, ID, AX_RESET_LENGTH, AX_RESET, checksum])
	print('Packet: ' + ":".join("{:08b}".format(c) for c in packet))
	print('Packet: ' + ":".join("{:02x}".format(c) for c in packet))
	serial_port.write(packet)
	header = serial_port.read(3)
	print('Received header: ' + ":".join("{:02x}".format(ord(c)) for c in header))
	body = serial_port.read(4)
	print('Received body: ' + ":".join("{:02x}".format(ord(c)) for c in body))
	return

#######################    R E A D S

def readTemperature(ID):
	checksum = (~(ID + AX_TEM_LENGTH  + AX_READ_DATA + AX_PRESENT_TEMPERATURE + AX_BYTE_READ))&0xFF;
	packet = bytearray([0xff, 0xff, ID, AX_TEM_LENGTH, AX_READ_DATA, AX_PRESENT_TEMPERATURE, AX_BYTE_READ, checksum])
	print('Packet: ' + ":".join("{:08b}".format(c) for c in packet))
	print('Packet: ' + ":".join("{:02x}".format(c) for c in packet))
	serial_port.write(packet)
	header = serial_port.read(3)
	print('Received header: ' + ":".join("{:02x}".format(ord(c)) for c in header))
	body = serial_port.read(4)
	print('Received body: ' + ":".join("{:02x}".format(ord(c)) for c in body))
	return

def readPosition(ID):
	checksum = (~(ID + AX_POS_LENGTH  + AX_READ_DATA + AX_PRESENT_POSITION_L + AX_BYTE_READ_POS))&0xFF
	packet = bytearray((
				(int("0xff",16)), 
				(int("0xff",16)), 
				(int(str(ID),16)),
				(int(str(AX_POS_LENGTH),16)),
				(int(str(AX_READ_DATA),16)),
				(int(str(AX_PRESENT_POSITION_L), 10)),
				(int(str(AX_BYTE_READ_POS),10)),
				(int(str(checksum),10))
	))
	z = np.int8(packet) 
	print('Packet: ' + ":".join("{:08b}".format(c) for c in packet))
	print('Packet: ' + ":".join("{:02x}".format(c) for c in packet))
		
	serial_port.write(z.tobytes())
	header = serial_port.read(3)
	print('Received header: ' + ":".join("{:02x}".format(ord(c)) for c in header))
	body = serial_port.read(4)
	print('Received body: ' + ":".join("{:02x}".format(ord(c)) for c in body))
	return




