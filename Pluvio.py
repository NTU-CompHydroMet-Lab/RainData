import serial.tools.list_ports
import serial, time
import binascii
import re
   
a = serial.tools.list_ports.comports()
i=0
for w in a:
    vidn = w.vid if (type(w.vid) is int) else 0
    print('%d)\t%s\t(USB VID=%04X)' % (i, w.device, vidn))
    i = i+1

ser = serial.Serial()
ser.port = "COM3"
   
#9600,N,8,1
ser.baudrate = 9600
ser.bytesize = serial.EIGHTBITS #number of bits per bytes
ser.parity = serial.PARITY_NONE #set parity check
ser.stopbits = serial.STOPBITS_ONE #number of stop bits
   
ser.timeout = 0.5          #non-block read 0.5s
ser.writeTimeout = 0.5     #timeout for write 0.5s
ser.xonxoff = False    #disable software flow control
ser.rtscts = False     #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False     #disable hardware (DSR/DTR) flow control
   
try: 
    ser.open()
except Exception as ex:
    print ("open serial port error " + str(ex))
    exit()
   
if ser.isOpen():
    try:
        ser.flushInput() #flush input buffer
        ser.flushOutput() #flush output buffer
   
        print('Open: ' + ser.portstr)
        
        send_data = 'E ' + '\r' # ask for return of measurements
        ser.write(send_data.encode('ascii')) # encode to ASCII
        
        response = ser.readline()
        print('Sensor reading:', response.decode('ascii'))
		
        message = response.decode('ascii')
        message = message.split()
        print('Sensor reading:', message)
		
        ser.close()
    except Exception as e1:
        print ("communicating error " + str(e1))
   
else:
    print ("open serial port error")
