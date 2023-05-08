import network
import time
from machine import Timer

class WifiManager:
    def __init__(self, ssid, password):
        self._ssid = ssid
        self._password = password
        self._wifi = network.WLAN(network.STA_IF)
        self._connected = False
        self._callbacks = {"connected": None, "disconnected": None}

    def connect(self):
        # Connect to the wifi network
        try:
            self._wifi.active(True)
            self._wifi.connect(self._ssid, self._password)
            start = time.time()
            attempt_number = 0 # initializing the number of attempts
            while not self._wifi.isconnected():
                time.sleep(1)
                if time.time() - start > 20: #timeout after 20 seconds
                    # Raise an exception if the number of attempts exceed 49
                    if attempt_number >= 20:
                      raise Exception("Connection attempt timed out")
                    attempt_number += 1
                    start = time.time() # Reset the start timer
                    print("Connection attempt {} timed out. Retrying...".format(str(attempt_number)))
                    self._wifi.disconnect()
                    self._wifi.connect(self._ssid, self._password)
                self._connected = True
                # Call the connected callback function if it exists
                if self._callbacks["connected"] is not None:
                    self._callbacks["connected"]()
        except Exception as e:
            print("Error while connecting to Wi-Fi: ", e)
            if self._callbacks["disconnected"] is not None:
                self._callbacks["disconnected"]()

    def disconnect(self):
        # Disconnect from the wifi network
        self._wifi.disconnect()
        self._connected = False
        # Call the disconnected callback function if it exists
        if self._callbacks["disconnected"] is not None:
            self._callbacks["disconnected"]()

    def on_connected(self, func):
        # Set the connected callback function
        self._callbacks["connected"] = func

    def on_disconnected(self, func):
        # Set the disconnected callback function
        self._callbacks["disconnected"] = func


