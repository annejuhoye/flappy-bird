import requests
import time

esp_ip = "192.168.4.1"  # Replace with the actual IP address of the ESP32 hotspot
url = f"http://{esp_ip}/"

while True:
    try:
        response = requests.get(url)
        voltage = response.text
        print(f"Voltage: {voltage} V")
    except requests.exceptions.ConnectionError:
        print("Connection error")
    
    time.sleep(1)  # Request every second
