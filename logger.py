import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QPushButton, QLineEdit, QGroupBox, QVBoxLayout, QTextEdit
from PyQt5.QtCore import QTimer
import irsdk
import json

class Logger(QWidget):
    def __init__(self) -> None:
        super().__init__()
        super().setWindowTitle("iRacing Data Logger")
        super().setFixedSize(800, 400)
        self.lyt: QVBoxLayout = QVBoxLayout()
        super().setLayout(self.lyt)

        # file setup
        self.lytFile: QGridLayout = QGridLayout()
        self.fileBox: QGroupBox = QGroupBox()
        self.fileBox.setLayout(self.lytFile)
        self.fileBox.setTitle("File Setup")
        self.lyt.addWidget(self.fileBox)
        self.lblDate: QLabel = QLabel("Date")
        self.lblTrack: QLabel = QLabel("Track")
        self.lblCar: QLabel = QLabel("Car")
        self.lblConfig: QLabel = QLabel("Track Config")
        self.lblSessionType: QLabel = QLabel("Session Type")
        self.lblSessionNum: QLabel = QLabel("Session #")
        self.lblSetupNotes: QLabel = QLabel("Setup Notes")
        self.editDate: QLineEdit = QLineEdit()
        self.editTrack: QLineEdit = QLineEdit()
        self.editCar: QLineEdit = QLineEdit()
        self.editConfig: QLineEdit = QLineEdit()
        self.editSessionType: QLineEdit = QLineEdit()
        self.editSessionNum: QLineEdit = QLineEdit()
        self.textEditSetup: QTextEdit = QTextEdit()

        self.lytFile.addWidget(self.lblDate, 0, 0)
        self.lytFile.addWidget(self.editDate, 0, 1)
        self.lytFile.addWidget(self.lblTrack, 1, 0)
        self.lytFile.addWidget(self.editTrack, 1, 1)
        self.lytFile.addWidget(self.lblCar, 2, 0)
        self.lytFile.addWidget(self.editCar, 2, 1)
        self.lytFile.addWidget(self.lblConfig, 3, 0)
        self.lytFile.addWidget(self.editConfig, 3, 1)
        self.lytFile.addWidget(self.lblSessionType, 4, 0)
        self.lytFile.addWidget(self.editSessionType, 4, 1)
        self.lytFile.addWidget(self.lblSessionNum, 5, 0)
        self.lytFile.addWidget(self.editSessionNum, 5, 1)
        self.lytFile.addWidget(self.lblSetupNotes, 6, 0)
        self.lytFile.addWidget(self.textEditSetup, 6, 1)

        # start/stop logging
        self.btnLog: QPushButton = QPushButton("Start Logging")
        self.btnLog.clicked.connect(self.log)
        self.lblStatus: QLabel = QLabel("")
        self.lyt.addWidget(self.btnLog)
        self.lyt.addWidget(self.lblStatus)

        # timer
        self.timer: QTimer = QTimer()
        self.timer.setInterval(5000) # setting to 5 seconds bc all we care about rn is lap times
        self.timer.timeout.connect(self.captureIRData)

        # irsdk setup
        self.ir = irsdk.IRSDK()
        self.ir.startup()

        # data
        self.lapTimes = []
        self.filename = ""

    def log(self):
        if self.btnLog.text() == "Start Logging":
            self.lblStatus.setText("Logging")
            self.btnLog.setText("Stop Logging")
            self.timer.start()
            data = self.getSetupData()
            self.filename = data["track"] + "-" + data["car"] + "-" + data["date"] + "-" + data["session #"]
            f = open(self.filename + ".csv", "w")
            f.write("lap (#), lap time (s)")
            f.close()
            f = open(self.filename + ".json", "w")
            json_obj = json.dumps(data, indent = 4)
            f.write(json_obj)
            f.close()

        else:
            self.lblStatus.setText("")
            self.btnLog.setText("Start Logging")
            self.timer.stop()

            # write data
            i = 0
            f = open(self.filename, "a")
            for time in self.lapTimes:
                f.write( str(i) + "," + str(time))
                i += 1
            f.close()
            
            # clear data
            self.lapTimes.clear()
    
    def captureIRData(self):
        if self.ir["LapLastLapTime"]:
            lastLapTime = self.ir["LapLastLapTime"]
            if len(self.lapTimes) == 0:
                self.lapTimes.append(lastLapTime)
            elif lastLapTime != self.lapTimes[-1]:
                self.lapTimes.append(lastLapTime)

    def getSetupData(self):
        payload = {}
        payload["date"] = (self.editDate.text())
        payload["track"] = (self.editTrack.text())
        payload["car"] = (self.editCar.text())
        payload["config"] = (self.editConfig.text())
        payload["session type"] = (self.editSessionType.text())
        payload["session #"] = (self.editSessionNum.text())
        payload["setup notes"] = (self.textEditSetup.toPlainText())
        return payload


def main():
    app = QApplication(sys.argv)
    logger = Logger()
    logger.show()
    sys.exit(app.exec_())

main()