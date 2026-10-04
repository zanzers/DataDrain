import socket
import threading
import time


class PingMonitor:
    def __init__(self, host="1.1.1.1", port=53, interval=2.0, timeout=1.0):
        self.host = host
        self.port = port
        self.interval = interval
        self.timeout = timeout
        self.latest = None          # milliseconds, or None = timeout / no data
        self._running = False

    def start(self):
        if self._running:
            return
        self._running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def stop(self):
        self._running = False
        self.latest = None

    def _measure(self):
        start = time.perf_counter()
        try:
            with socket.create_connection((self.host, self.port), timeout=self.timeout):
                pass
        except OSError:
            return None
        return (time.perf_counter() - start) * 1000

    def _loop(self):
        while self._running:
            self.latest = self._measure()
            time.sleep(self.interval)