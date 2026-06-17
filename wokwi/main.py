import network  # connects to wifi
import urequests  # Allows sending and receiving data over the internet, simpler for http requests
import json  # Parses data from Flask
from machine import Pin   #Controls pins
import time    # We need this for the time pause

#Set up the LED pins
red =  Pin(25, Pin.OUT)
green =  Pin(26, Pin.OUT)
blue =  Pin(27, Pin.OUT)

#Wifi details
SSID = 'Wokwi-GUEST'   # Built in wifi network on Wokwi
PASSWORD =  ''      # No password needed

# Connect to wifi
def online():
  wifi = network.WLAN(network.STA_IF)   # The ESP32 as wifi client
  wifi.active(True)    # Wifi ON
  wifi.connect(SSID, PASSWORD)  # Connects to the network

  print("Trying to connect to wifi...")
  for _ in range(20):  # retry for 20 seconds
    if wifi.isconnected():
        print("Connected! IP:", wifi.ifconfig()[0])
        return
    time.sleep(1)
  print("Failed to connect to WiFi")

# Lights up an LED color according to the sign detected
def set_led(r, g, b):
  red.value(r)  # ON = 1, OFF = 0
  green.value(g)
  blue.value(b)

# Main program starts
online()  # Connect to wifi first

print('Identifying signs...')
while True:
  try:
      # Check Wifi before making request
      if not network.WLAN(network.STA_IF).isconnected():
        online()    # Reconnect when disconnected to wifi
      response = urequests.get(   # Communicates through Flask for latest result
        'YOUR_NGROK_url/latest',
        headers={"ngrok-skip-browser-warning": "true"}  # Bypasses ngrok browser warning page
      )
      result = response.json()   # Converts to Python dictionary
      label = result.get('label')   # Gets the traffic sign label
      confidence = result.get('confidence')   # Get the confidence score
      print('Sign: ', label, '| Confidence:', confidence)

      if label == 'Stop':
          set_led(1, 0, 0)   # Red LED
      elif label == 'Pedestrian Crossing':
          set_led(0, 1, 0)   # Green LED
      elif label == 'No Entry':
          set_led(0, 0, 1)   # Blue LED
      elif label == 'Speed Limit': 
          set_led(1, 1, 0)   # Yellow LED
      elif label == 'Unknown':
        set_led(0, 0, 0)     # OFF for unknown
      else:
          set_led(1, 0, 1)   # Magenta LED
    
  except Exception as e:
    print('Error occured:', e)   # Prints and error while running
    

  time.sleep(1)    # Waits for 1 second before rechecking

        



 