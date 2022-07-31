# iracing-lap-analyzer
iRacing telemetry viewer using PyQt5 and pyqtgraph
## TODO
- [ ] inertial navigation for estimating position (we dont get GPS data in real-time)
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

:: Or log data
$ python logger.py

:: Leave the virtual environment
$ deactivate
```