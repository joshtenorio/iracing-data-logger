"""
Various methods of drawing scrolling plots.
"""

from time import perf_counter
import numpy as np
import pyqtgraph as pg
import time
import irsdk
import math

# this is our State class, with some helpful variables
class State:
    ir_connected = False
    last_car_setup_tick = -1

win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('dataaa')

f = open("data.csv", "w")
f.write("Time (s),Laps (#),Speed (m/s),Gear (#),Brake (%),Throttle (%),Steering Angle (rad),X Position (m),Y Position (m)\n")
f.close()

# 1) Simplest approach -- update data in the array such that plot appears to scroll
#    In these examples, the array size is fixed.
p2 = win.addPlot()
p2.setYRange(0, 50, padding=0)
data1 = np.random.normal(size=1500)
curve2 = p2.plot(data1)
ptr1 = 0

win.nextRow()

map: pg.PlotItem = win.addPlot()
map.showGrid(x=True, y=True)

# initializing ir and state
ir = irsdk.IRSDK()
ir.startup()
state = State()

xPos = 0
yPos = 0

arrX = []
arrY = []

def update():
    global data1, ptr1, xPos, yPos
    data1[:-1] = data1[1:]  # shift data in the array one sample left
                            # (see also: np.roll)
    
    # get GPS speed (m/s)
    speed = ir['Speed']
    if(abs(speed) < 1):
        data1[-1] = 0
        speed = 0
    else:
        data1[-1] = speed

    # estimate position (m)
    x = ir['VelocityX'] if abs(ir['VelocityX']) > 0.1 else 0
    y = ir['VelocityY'] if abs(ir['VelocityY']) > 0.1 else 0
    yawNorth = ir['YawNorth']
    #print("yaw relative to North (rad): " + str(yawNorth))

    deltaX = x*math.sin(yawNorth) + y*math.cos(yawNorth)
    deltaY = x*math.cos(yawNorth) + y*math.sin(yawNorth)

    xPos += deltaX * .02
    yPos += deltaY * .02
    arrX.append(xPos)
    arrY.append(yPos)
    map.clear()
    map.plot(arrX, arrY)
    
    f = open("data.csv", "a")
    speed = str(speed)
    time = str(ir['SessionTime'])
    laps = str(ir['LapCompleted'])
    gear = str(ir['Gear'])
    brake = str(ir['Brake'])
    throttle = str(ir['Throttle'])
    steering = str(ir['SteeringWheelAngle'])
    row = time + "," + laps + "," + speed + "," + gear + "," + brake + "," + throttle + "," + steering + "," + str(xPos) + "," + str(yPos) + "\n"
    f.write(row)
    f.close()

    
    ptr1 += 1
    curve2.setData(data1)
    curve2.setPos(ptr1, 0)


timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(20)


pg.exec()