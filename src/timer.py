import threading

class TimerThread:
    def __init__(self, time: int, callback_func: callable):
        self.time = time
        self.callback_func = callback_func
        self.timer = None
    
    def start(self):
        self.timer = threading.Timer(self.time, self.callback_func)
        self.timer.start()
    
    def stop(self):
        self.timer.cancel()

# Start a `TimerThread` instance to invoke `callback_function` every 7200 seconds
def callback_function():
    # your code here
    pass



timer_thread = TimerThread(7200, callback_function)
timer_thread.start()


