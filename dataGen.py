import pandas as pd
import time
from influxdb import InfluxDBClient
import random
import numpy as np
from datetime import datetime
from datetime import timezone

df = pd.read_csv('ubConfig.csv')
client = InfluxDBClient('localhost', 8086, '', '','ubData')
try:
    client.drop_database('ubData')
except:
    pass
client.create_database('ubData')

def insertDB(sensorID,lat,lng,freezer_model,btVal,tempVal,spoc_name,spoc_number):
    lt = datetime.now(timezone.utc)
    timeStr = lt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    json_body = [{ "measurement":'freezer',"time": timeStr,"fields": {"lat":lat, \
                "lng":lng,"bt_value":btVal,"id":sensorID,"freezer_model":freezer_model, \
                "temp_value":tempVal,"spoc_name":spoc_name,"spoc_number":spoc_number}}]
    client.write_points(json_body)
    print(json_body)

tempRange = np.linspace(-10.0,4.0,num=150)
uniqueID = []
i = 1
while True:
    temp_row = df.sample(replace=False)
    sensorID = temp_row['id'].tolist()[0]
    if sensorID in uniqueID:
        continue
    uniqueID.append(sensorID)
    lat = temp_row['lat'].tolist()[0]
    lng = temp_row['lng'].tolist()[0]
    freezer_model = temp_row['freezer_model'].tolist()[0]
    spoc_name = temp_row['spoc_name'].tolist()[0]
    spoc_number = temp_row['spoc_number'].tolist()[0]
    btVal = random.randint(80,100)
    tempVal = random.choice(tempRange)
    insertDB(sensorID,lat,lng,freezer_model,btVal,tempVal,spoc_name,spoc_number)
    print("Iteration: ",i)
    i = i +1
    if i > 3000:
        uniqueID=[]
    print("Unique IDs: ",len(set(uniqueID)))
    time.sleep(0.4) #Data writing overhead for every entry = 0.05s
