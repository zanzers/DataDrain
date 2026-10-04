import time
import psutil
from storage import save_state

SAVE_EVERY = 5   


def list_adapters() -> list[str]:
    return list(psutil.net_io_counters(pernic=True).keys())


class Monitor:
    def __init__(self, adapter: str, remaining: int, save_every: int = SAVE_EVERY):
        self.adapter = adapter
        self.total = remaining
        self.remaining = remaining
        self.speed = 0.0
        self.save_every = save_every

        self._last_bytes = self._read()
        self._last_time = time.monotonic()
        self._last_save = self._last_time

    def _read(self) -> int:
        stats = psutil.net_io_counters(pernic=True)[self.adapter]
        return stats.bytes_sent + stats.bytes_recv

    def tick(self):
        now_bytes = self._read()
        now_time = time.monotonic()

        used = now_bytes - self._last_bytes if now_bytes >= self._last_bytes else 0
        elapsed = now_time - self._last_time
        self.speed = used / elapsed if elapsed > 0 else 0.0
        self.remaining = max(0, self.remaining - used)

        self._last_bytes = now_bytes
        self._last_time = now_time

        if now_time - self._last_save >= self.save_every:
            save_state(self.remaining)
            self._last_save = now_time

        return used, self.speed, self.remaining

    def stop(self):
        save_state(self.remaining)