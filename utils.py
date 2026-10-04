def format_bytes(n: int) -> str:
    
    for unit, size in [("TB", 1000**4), ("GB", 1000**3), ("MB", 1000**2), ("KB", 1000)]:
        if n >= size:
            return f"{n / size:.2f} {unit}"
    return f"{n} B"



def format_duration(seconds) -> str:
    if seconds is None:
        return "--"
    seconds = int(seconds)
    days, rest = divmod(seconds, 86400)
    hours, rest = divmod(rest, 3600)
    minutes, _ = divmod(rest, 60)

    if days:
        return f"{days}d {hours}h"
    if hours:
        return f"{hours}h {minutes}m"
    if minutes:
        return f"{minutes}m"
    return "< 1m"