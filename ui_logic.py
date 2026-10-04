from parser import parse_data
from utils import format_bytes
from monitor import Monitor, list_adapters
from ping import PingMonitor
from storage import load_state

UNIT_CHOICES = ["KB", "MB", "GB", "TB"]


def describe_ping(ms):
    """Returns (text, level). The UI picks the color from the level."""
    if ms is None:
        return "timeout", "bad"
    if ms < 50:
        return f"{ms:.0f} ms", "good"
    if ms < 100:
        return f"{ms:.0f} ms", "ok"
    return f"{ms:.0f} ms", "bad"


class AppLogic:
    def __init__(self):
        self.mon = None
        self.pinger = PingMonitor()

    def adapters(self) -> list[str]:
        return list_adapters()

    def saved_amount(self):
        state = load_state()
        if not state:
            return None
        n = state.get("remaining", 0)
        if n <= 0:
            return None
        for unit, size in [("TB", 1000**4), ("GB", 1000**3), ("MB", 1000**2), ("KB", 1000)]:
            if n >= size:
                return f"{n / size:.3f}".rstrip("0").rstrip("."), unit
        return f"{n / 1000:.3f}".rstrip("0").rstrip("."), "KB"

    def start(self, amount_text: str, unit: str, adapter: str):
        """Returns an error message, or None if started OK."""
        if not adapter:
            return "Pick an adapter"
        try:
            remaining = parse_data(f"{amount_text.strip()} {unit}")
        except ValueError:
            return "Enter a number like 2.5"
        self.mon = Monitor(adapter, remaining)
        self.pinger.start()
        return None

    def tick(self) -> dict:
        used, speed, remaining = self.mon.tick()
        return {
            "remaining": format_bytes(remaining),
            "speed": format_bytes(int(speed)) + "/s",
            "used": format_bytes(self.mon.total - remaining),
            "percent": remaining / self.mon.total * 100,
            "ping": describe_ping(self.pinger.latest),
            "finished": remaining <= 0,
        }

    def stop(self):
        self.pinger.stop()
        if self.mon is not None:
            self.mon.stop()
            self.mon = None

    @property
    def running(self) -> bool:
        return self.mon is not None