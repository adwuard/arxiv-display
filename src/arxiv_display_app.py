# Define the class for the app
import timer
import wifi
import const


class ArxivDisplayApp:
    def __init__(self):
        # Initialize any necessary variables and parameters here
        self.fetch_timer = TimerThread(FETCH_INTERVAL, self.fetch_papers_handler)
        self.render_timer = TimerThread(RENDER_INTERVAL, self.render_handler)
        
        # list of all fetched papers
        self.papers = []

        self.wifi = WifiManager(WIFI_SSID, WIFI_PWD)
        
        # register callbacks for connection status
        self.wifi.on_connected(self.start)
        self.wifi.on_disconnected(self.stop)



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


