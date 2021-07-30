from WS_UMB_EN import WS_UMB
from influxdb_client.client.write_api import SYNCHRONOUS
import influxdb_client
from datetime import datetime, timedelta
import time

bucket = "WS100"
org = "WG"
token = "VDwvoYR1X0NK0-n1Bppm8ehUhnE-RMZCIJ3pO9uK-WTvSKkVgYQI068M7gaUWsPQx39W_mURnf7YZfVDCjqLvw=="
# Store the URL of your InfluxDB instance
url="http://localhost:8086"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
 
with WS_UMB() as umb:

    time_now = datetime.utcnow()  # Or .now() for local time
    time_rounded = time_now.replace(second=0, microsecond=0)
    
    while True:
        # Wait until next 1 minute time
        time_rounded += timedelta(minutes=1)
        time_to_wait = (time_rounded - datetime.utcnow()).total_seconds()
        time.sleep(time_to_wait)
        
        response, status = umb.onlineDataQuery(820)
        if status != 0:
            print(umb.checkStatus(status))
        else:
            print('Precipitation Intensity:', response)

            p = [influxdb_client.Point("Precipitation Intensity").field("mm/h", response)]
            
            write_api = client.write_api(write_options = SYNCHRONOUS)
            write_api.write(bucket=bucket, org=org, record=p)