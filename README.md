## NoSleep (Windows only)

Keeps your Windows display awake with a simple ON/OFF toggle. Built with `tkinter` and `ctypes` on Python 3.

Download available at [releases page](https://github.com/mfaridn03/NoSleep/releases).

### Features
- **One-click toggle**: Turn display keep-awake ON/OFF.
- **Native Windows behavior**: Uses `ES_CONTINUOUS` and `ES_DISPLAY_REQUIRED` flags via `ctypes`.

### Requirements
- **OS**: Windows 10/11 recommended
- **Python**: 3.x

### Build
- Clone the repository
- [Releases](https://github.com/mfaridn03/NoSleep/releases) are compiled using `pyinstaller`:

```bash
pyinstaller --onefile --windowed app.py
```


