from influxdb_client.client.write_api import SYNCHRONOUS
import influxdb_client

from datetime import datetime, timedelta
import serial.tools.list_ports
import serial, time
import binascii
import re

bucket = "Pluvio L 400"
org = "WG"
token = "VDwvoYR1X0NK0-n1Bppm8ehUhnE-RMZCIJ3pO9uK-WTvSKkVgYQI068M7gaUWsPQx39W_mURnf7YZfVDCjqLvw=="
# Store the URL of your InfluxDB instance
url="http://localhost:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

a = serial.tools.list_ports.comports()
i = 0
for w in a:
    vidn = w.vid if (type(w.vid) is int) else 0
    print('%d)\t%s\t(USB VID=%04X)' % (i, w.device, vidn))
    i = i+1

ser = serial.Serial()
ser.port = "COM4"
   
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

        time_now = datetime.utcnow()  # Or .now() for local time
        time_rounded = time_now.replace(second=0, microsecond=0)

        while True:
            # Wait until next 5 minute time
            time_rounded += timedelta(minutes=1)
            time_to_wait = (time_rounded - datetime.utcnow()).total_seconds()
            time.sleep(time_to_wait)
		
            send_data = 'M ' + '\r'
            ser.write(send_data.encode('ascii'))
        
            response = [float(i) for i in ser.readline().decode('ascii').split()]
            print('RT Intensity:', response[0])
        
            write_api = client.write_api(write_options = SYNCHRONOUS)
            p = [influxdb_client.Point("RT Intensity").field("Pluvio L", response[0]),
                 influxdb_client.Point("Accu RT-NRT").field("Pluvio L", response[1]),
                 influxdb_client.Point("Accu NRT").field("Pluvio L", response[2]),
                 influxdb_client.Point("Accu total NRT").field("Pluvio L", response[3]), 
                 influxdb_client.Point("Accu Bucket RT").field("Pluvio L", response[4]),
                 influxdb_client.Point("Accu Bucket NRT").field("Pluvio L", response[5]),]
		
            write_api.write(bucket=bucket, org=org, record=p)   
		
        ser.close()
    except Exception as e1:
        print ("communicating error " + str(e1))
   
else:
    print ("open serial port error")