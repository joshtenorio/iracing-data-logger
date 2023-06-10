# iRacing Logger
iRacing data logger
## Build Instructions
### Windows
```bat
:: Create virtual environment
$ python -m venv venv

:: Start virtual environment
$ call venv/scripts/activate.bat

:: Install required packages
$ pip install -r requirements.txt

:: log data
$ python logger.py

:: Leave the virtual environment
$ deactivate
```