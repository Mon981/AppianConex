import threading
import time

class ConnectingAnimator:
    def __init__(self, max_dots=5, interval=0.5):
        self.max_dots = max_dots
        self.interval = interval
        self._running = False
        self._thread = None

    def _animate(self):
        count = 0
        while self._running:
            count = (count + 1) % (self.max_dots + 1)
            dots = "." * count
            print(f"\rConectando{dots:<{self.max_dots}}", end="", flush=True)
            time.sleep(self.interval)

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()        
        print("\rConexión establecida", flush=True)


class ProgressBarAnimator:
    def __init__(self, max_hashes=20, interval=0.5):
        self.max_hashes = max_hashes
        self.interval = interval
        self._running = False
        self._thread = None

    def _animate(self):
        count = 0
        while self._running:
            count = (count + 1) % (self.max_hashes + 1)
            bar = "#" * count
            print(f"\r{bar:<{self.max_hashes}}", end="", flush=True)
            time.sleep(self.interval)

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self._thread.start()

    def stop(self, message=None):
        self._running = False
        if self._thread:
            self._thread.join()
        if message:
            print("\r" + message)
