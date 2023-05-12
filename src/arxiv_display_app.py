# Import necessary libraries
import pygame
from PIL import Image
# Define the class for the app
from repeating_timer import*
from const import *
from PIL import Image, ImageDraw, ImageFont
from wifi import*
from display_driver import DisplayDriverFactory
from views import WifiView
import signal


class ArxivDisplayApp:
    def __init__(self):
        # Initialize any necessary variables and parameters here
        self.fetch_timer = RepeatingTimerThread(FETCH_INTERVAL, self.fetch_papers_handler)
        self.render_timer = RepeatingTimerThread(RENDER_INTERVAL, self.render_handler)
        
        # list of all fetched papers
        self.papers = []

        self.wifi = WifiManager(WIFI_SSID, WIFI_PWD)
        
        # register callbacks for connection status
        self.wifi.register_on_connected_cb(self._on_wifi_connected_cb)
        self.wifi.register_on_disconnected_cb(self._on_wifi_disconnected_cb)
        self.wifi.register_on_connection_error_cb(self._on_wifi_connection_failed_cb)

        driver_factory = DisplayDriverFactory()
        self.screen_driver = driver_factory.create_driver('pygame', 400, 300)
        
        self.WifiView = WifiView(self.screen_driver)

        # connect to WIFI
        self.wifi.connect()


    def start(self):
        # Start the app here
        self.fetch_timer.start()
        self.render_timer.start()

        pass
    
    def stop(self):
        # Stop the app here
        
        pass


    def fetch_papers_handler(self):
        
        pass

    def render_handler(self):
        pass

    def _on_wifi_connected_cb(self):
        self.WifiView.update('connecting')
        self.WifiView.render()

    def _on_wifi_disconnected_cb(self):
        self.WifiView.update('disconnected')
        self.WifiView.render()

    def _on_wifi_connection_failed_cb(self, e):
        self.WifiView.update('error', e)
        self.WifiView.render()


adp = ArxivDisplayApp()
adp.render_handler()


def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    pygame.quit()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while 1:
    continue

