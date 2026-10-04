import os
import sys
import tkinter as tk
from tkinter import ttk
from ui_logic import AppLogic, UNIT_CHOICES
from gauge import CircleGauge

COLORS = {
    "bg": "#1e1e2e",
    "text": "#cdd6f4",
    "dim": "#a6adc8",
    "error": "#f38ba8",
    "good": "#a6e3a1",
    "ok": "#f9e2af",
    "bad": "#f38ba8",
}


def resource_path(name: str) -> str:
    """Finds a bundled file both as a script and as an exe."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.logic = AppLogic()
        self.after_id = None

        root.title("DataDrain")
        try:
            root.iconbitmap(resource_path("icon.ico"))
        except tk.TclError:
            pass

        root.geometry("400x470")
        root.config(bg=COLORS["bg"])
        root.protocol("WM_DELETE_WINDOW", self.on_close)

        ttk.Style().theme_use("clam")
        self._build_widgets()

        saved = self.logic.saved_amount()
        if saved:
            self.data_entry.insert(0, saved[0])
            self.unit_box.set(saved[1])

    def _label(self, parent, text="", size=11, color=None):
        return tk.Label(parent, text=text, bg=COLORS["bg"],
                        fg=color or COLORS["text"], font=("Segoe UI", size))

    # ---------- layout only ----------
    def _build_widgets(self):
        r = self.root

        self.gauge = CircleGauge(r, size=200, bg=COLORS["bg"])
        self.gauge.pack(pady=(16, 8))

        stats = tk.Frame(r, bg=COLORS["bg"])
        stats.pack(fill="x", padx=16)

        self.speed_label = self._label(stats, "Speed: --", size=8)
        self.speed_label.pack(anchor="w")
        self.ping_label = self._label(stats, "Ping: --", size=8)
        self.ping_label.pack(anchor="w")
        self.used_label = self._label(stats, "Used: --", size=8, color=COLORS["dim"])
        self.used_label.pack(anchor="w")

        inputs = tk.Frame(r, bg=COLORS["bg"])
        inputs.pack(pady=(14, 0))

        left = tk.Frame(inputs, bg=COLORS["bg"])
        left.grid(row=0, column=0, sticky="n")
        self._label(left, "Remaining data:", size=8, color=COLORS["dim"]).pack(anchor="w")
        entry_row = tk.Frame(left, bg=COLORS["bg"])
        entry_row.pack(anchor="w")
        self.data_entry = ttk.Entry(entry_row, width=8)
        self.data_entry.pack(side="left", padx=(0, 4))
        self.unit_box = ttk.Combobox(entry_row, values=UNIT_CHOICES,
                                     state="readonly", width=4)
        self.unit_box.set("GB")
        self.unit_box.pack(side="left")

        right = tk.Frame(inputs, bg=COLORS["bg"])
        right.grid(row=0, column=1, sticky="n", padx=(12, 0))
        self._label(right, "Adapter:", size=8, color=COLORS["dim"]).pack(anchor="w")
        self.adapter_box = ttk.Combobox(right, values=self.logic.adapters(),
                                        state="readonly", width=16)
        self.adapter_box.pack(anchor="w")

        self.error_label = self._label(r, "", size=9, color=COLORS["error"])
        self.error_label.pack(pady=4)

        self.toggle_btn = ttk.Button(r, text="Start", command=self.on_toggle)
        self.toggle_btn.pack(pady=(4, 10))

    # ---------- helpers ----------
    def _set_inputs_enabled(self, enabled: bool):
        self.data_entry.config(state="normal" if enabled else "disabled")
        self.unit_box.config(state="readonly" if enabled else "disabled")
        self.adapter_box.config(state="readonly" if enabled else "disabled")

    def _reset_display(self):
        self.gauge.reset()
        self.speed_label.config(text="Speed: --")
        self.ping_label.config(text="Ping: --", fg=COLORS["text"])
        self.used_label.config(text="Used: --")
        self.error_label.config(text="")

    # ---------- events ----------
    def on_toggle(self):
        if self.logic.running:
            self.on_stop()
        else:
            self.on_start()

    def on_start(self):
        error = self.logic.start(
            self.data_entry.get(), self.unit_box.get(), self.adapter_box.get()
        )
        if error:
            self.error_label.config(text=error)
            return
        self._reset_display()
        self._set_inputs_enabled(False)
        self.toggle_btn.config(text="Stop")
        self.after_id = self.root.after(1000, self.update)

    def update(self):
        try:
            info = self.logic.tick()
        except KeyError:
            self.on_stop("Adapter not found")
            return

        self.gauge.set(info["percent"], info["remaining"],
                       f"{info['percent']:.0f}% left")
        self.speed_label.config(text=f"Speed: {info['speed']}")
        self.used_label.config(text=f"Used: {info['used']}")

        text, level = info["ping"]
        self.ping_label.config(text=f"Ping: {text}", fg=COLORS[level])

        if info["finished"]:
            self.on_stop("Data used up!")
        else:
            self.after_id = self.root.after(1000, self.update)

    def on_stop(self, message: str = ""):
        if not self.logic.running:
            return
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.logic.stop()
        self._reset_display()
        self.error_label.config(text=message)
        self._set_inputs_enabled(True)
        self.toggle_btn.config(text="Start")

    def on_close(self):
        self.on_stop()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()