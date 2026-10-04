import tkinter as tk


class CircleGauge(tk.Canvas):
    def __init__(self, parent, size=200, thickness=16, bg="#1e1e2e", track="#313244"):
        super().__init__(parent, width=size, height=size, bg=bg, highlightthickness=0)
        pad = thickness // 2 + 2
        box = (pad, pad, size - pad, size - pad)

        self.create_arc(*box, start=0, extent=359.99, style="arc",outline=track, width=thickness)
        self.arc = self.create_arc(*box, start=90, extent=0, style="arc", outline="#a6e3a1", width=thickness)
        self.main_text = self.create_text(size / 2, size / 2 - 10, text="--",fill="white", font=("Segoe UI", 22, "bold"))
        self.sub_text = self.create_text(size / 2, size / 2 + 20, text="",fill="#a6adc8", font=("Segoe UI", 10))

    def set(self, percent: float, main: str, sub: str = ""):
        percent = max(0, min(100, percent))

        if percent > 50:
            color = "#a6e3a1"   # green
        elif percent > 20:
            color = "#f9e2af"   # yellow
        else:
            color = "#f38ba8"   # red

        self.itemconfig(self.arc, extent=-min(359.99, percent * 3.6), outline=color)
        self.itemconfig(self.main_text, text=main)
        self.itemconfig(self.sub_text, text=sub)
    
    def reset(self):
        self.itemconfig(self.arc, extent=0, outline="#a6e3a1")
        self.itemconfig(self.main_text, text="--")
        self.itemconfig(self.sub_text, text="")