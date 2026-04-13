## NoSleep (Windows only)

Keeps your Windows display awake with a simple ON/OFF toggle. Built with `tkinter` and `ctypes` on Python 3.

Download available at [releases page](https://github.com/mfaridn03/NoSleep/releases).

### Features
- **One-click toggle**: Turn display keep-awake ON/OFF.

### Requirements
- **OS**: Windows 10/11 recommended
- **Python**: 3.x

### Build
- Clone the repository
- [Releases](https://github.com/mfaridn03/NoSleep/releases) are compiled using `pyinstaller`:

```bash
pyinstaller --onefile --windowed --name=NoSleep app.py
```
- executable will be in `dist/NoSleep.exe`

