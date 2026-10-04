import tkinter as tk
from monitor import Monitor, list_adapters
from utils import format_bytes

print(list_adapters())
mon = Monitor("Wi-Fi", 3 * 1000**3)   
root = tk.Tk()
root.withdraw()                        # hide the empty window


def update():

    used, speed, remaining = mon.tick()
    print(f"{format_bytes(int(speed))}/s | {format_bytes(remaining)}")
    root.after(1000, update)       
    

root.after(1000, update)
root.mainloop()