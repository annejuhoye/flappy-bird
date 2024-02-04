import requests
import time
import csv
from datetime import datetime

esp_ip = "192.168.4.1"  # Replace with the actual IP address of the ESP32 hotspot
url = f"http://{esp_ip}/"
csv_file_path = "voltage_readings.csv" 

with open(csv_file_path, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Voltage (V)"])

while True:
    try:
        response = requests.get(url)
        voltage = response.text
        print(f"Voltage: {voltage} V")
        
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), voltage])
    except requests.exceptions.ConnectionError:
        print("Connection error")
    
    time.sleep(1)  # Request every second
