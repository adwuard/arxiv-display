import threading

class RepeatingTimerThread:
    def __init__(self, interval: int, callback_func: callable):
        self.interval = interval
        self.callback_func = callback_func
        self.timer = None
    
    def start(self):
        self.timer = threading.Timer(self.interval, self._run)
        self.timer.start()
    
    def stop(self):
        self.timer.cancel()
    
    def _run(self):
        self.callback_func()
        self.start()

# # Start a `RepeatingTimerThread` instance to invoke `callback_function` every 7200 seconds
# def callback_function():
#     # your code here
#     print(2)
#     pass

# def callback_function2():
#     # your code here
#     print(3)
#     pass

# timer_thread = RepeatingTimerThread(2, callback_function)
# timer_thread2 = RepeatingTimerThread(3, callback_function2)

# timer_thread.start()
# timer_thread2.start()