# DataDrain

DataDrain is a Python desktop application running from a local virtual environment (`.venv`).

## Folder Structure

```text
DataDrain/
├── ui.py
├── icon.ico
├── run.bat
├── run_hidden.vbs
└── .venv/
```

## Running DataDrain

### Normal launch

Double-click:

```text
run_hidden.vbs
```

This launches DataDrain using the Python interpreter inside `.venv` without opening a terminal window.

### Debug launch

If DataDrain doesn't start or you need to see Python errors, open PowerShell in the DataDrain folder:

```powershell
.\.venv\Scripts\Activate.ps1
py ui.py
```

The terminal will remain visible so errors can be inspected.

## Launcher

`run.bat`:

```bat
@echo off
cd /d "E:\workspace\DataDrain"
".venv\Scripts\pythonw.exe" "ui.py"
```

`run_hidden.vbs`:

```vbscript
Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "E:\workspace\DataDrain"
WshShell.Run """E:\workspace\DataDrain\.venv\Scripts\pythonw.exe"" ""E:\workspace\DataDrain\ui.py""", 0, False
```

## Desktop Shortcut

For a normal app-like experience:

1. Create a shortcut to `run_hidden.vbs`.
2. Rename the shortcut to **DataDrain**.
3. Right-click → **Properties**.
4. Select **Change Icon**.
5. Choose:

```text
E:\workspace\DataDrain\icon.ico
```

Then use the **DataDrain desktop shortcut** to launch the application.

## Virtual Environment

The application uses:

```text
.venv\Scripts\python.exe
```

and:

```text
.venv\Scripts\pythonw.exe
```



## Reinstalling the Environment

If the virtual environment is deleted or corrupted:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Then test:

```powershell
py ui.py
```

---

# ⚠️ IMPORTANT: If DataDrain Will Be Used by Other People

**The current setup is intended for my own computer.**

It depends on:

* My local Python installation
* My `.venv`
* My local file paths
* My installed Python packages
* The local `E:\workspace\DataDrain` directory
* `run_hidden.vbs`

### Before sharing DataDrain with other users

Do **not** simply copy the current folder and expect it to work on another computer.

Before distributing the application, change the project to a proper standalone distribution.

### Distribution checklist

* [ ] Remove hard-coded paths such as `E:\workspace\DataDrain`
* [ ] Make all application paths relative to the application directory
* [ ] Make sure all required files/resources are bundled
* [ ] Make sure configuration files don't contain my personal paths or information
* [ ] Test on a clean Windows computer
* [ ] Create a proper installer
* [ ] Build a standalone executable with PyInstaller or another packaging method
* [ ] Use the correct architecture for the target computers
* [ ] Test antivirus/Windows security behavior
* [ ] **Code-sign the installer/executable** for distribution
* [ ] Consider an application updater if regular updates are needed

### Remember

For personal use:

```text
Desktop Shortcut
      ↓
run_hidden.vbs
      ↓
.venv
      ↓
ui.py
```

For other users:

```text
Installer
    ↓
Standalone DataDrain Application
    ↓
No Python installation required
    ↓
No .venv required
```

**TODO before distribution:** Revisit the launcher, packaging, installer, paths, dependencies, and code signing.

> **Do not delete this note.** This is the reminder to switch from the personal-development setup to a proper distributable application when DataDrain is ready for other users.

---

## Important

The PyInstaller `.exe` is not required for normal personal use.

The current launcher runs:

```text
Desktop Shortcut
      ↓
run_hidden.vbs
      ↓
.venv\Scripts\pythonw.exe
      ↓
ui.py
      ↓
DataDrain
```

This avoids the unsigned PyInstaller executable and prevents the extra terminal window from appearing.
