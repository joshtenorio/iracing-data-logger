# iracing-lap-analyzer
iRacing telemetry viewer using PyQt5 and pyqtgraph
## Build Instructions
### Windows
```bat
:: Create virtual environment
$ python -m venv venv

:: Start virtual environment
$ call venv/scripts/activate.bat

:: Install required packages
$ pip install -r requirements.txt

:: Run the lap analyzer
$ python main.py

:: Leave the virtual environment
$ deactivate
```