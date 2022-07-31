"""
Various methods of drawing scrolling plots.
"""

import numpy as np
import pyqtgraph as pg
import irsdk
import math

"""import pyqtgraph.examples
pyqtgraph.examples.run()"""

# this is our State class, with some helpful variables
class State:
    ir_connected = False
    last_car_setup_tick = -1

win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('dataaa')

f = open("data.csv", "w")
f.write("Time (s),Laps (#),Speed (m/s),Gear (#),Brake (%),Throttle (%),Steering Angle (rad),Distance around lap (%),X Position (m),Y Position (m)\n")
f.close()

# plots
# speed m/s
plotSpeed = win.addPlot(title="speed (m/s)")
plotSpeed.setYRange(0, 70, padding=0)
dataSpeed = np.random.normal(size=1500)
curveSpeed = plotSpeed.plot(dataSpeed)
ptr1 = 0

win.nextRow()
# steering angle
plotSteering = win.addPlot(title="steering angle (rad)")
dataSteer = np.random.normal(size=1500)
curveSteer = plotSteering.plot(dataSteer)

win.nextRow()
# throttle inputs
plotPedalInputs = win.addPlot(title="pedal inputs (%)")
plotPedalInputs.setYRange(-1, 1, padding=0)
dataThrottle = np.random.normal(size=1500)
curveThrottle = plotPedalInputs.plot(dataThrottle, pen=(0,255,0))
dataBrake = np.random.normal(size=1500)
curveBrake = plotPedalInputs.plot(dataBrake, pen=(255,0,0))

win.nextRow()
# map
#map: pg.PlotItem = win.addPlot(title="track map")
#map.showGrid(x=True, y=True)

# initializing ir and state
ir = irsdk.IRSDK()
ir.startup()
state = State()

xPos = 0
yPos = 0

arrX = []
arrY = []

def update():
    global dataSpeed, ptr1, xPos, yPos, dataSteer, dataThrottle, dataBrake
    dataSpeed[:-1] = dataSpeed[1:]  # shift data in the array one sample left
    dataSteer[:-1] = dataSteer[1:]
    dataThrottle[:-1] = dataThrottle[1:]
    dataBrake[:-1] = dataBrake[1:]
                            # (see also: np.roll)
    
    # get GPS speed (m/s)
    speed = ir['Speed']
    if(abs(speed) < 1):
        dataSpeed[-1] = 0
        speed = 0
    else:
        dataSpeed[-1] = speed

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
    #map.clear()
    #map.plot(arrX, arrY)
    
    f = open("data.csv", "a")
    speed = str(speed)
    time = str(ir['SessionTime'])
    laps = str(ir['LapCompleted'])
    gear = str(ir['Gear'])

    # pedal inputs
    brake = str(ir['Brake'])
    throttle = str(ir['Throttle'])
    dataBrake[-1] = ir['Brake']
    dataThrottle[-1] = ir['Throttle']

    # steering angle
    steering = str(ir['SteeringWheelAngle'])
    dataSteer[-1] = ir['SteeringWheelAngle']

    lapdist = str(ir["LapDistPct"])
    row = time + "," + laps + "," + speed + "," + gear + "," + brake + "," + throttle + "," + steering + "," + lapdist + "," + str(xPos) + "," + str(yPos) + "\n"
    f.write(row)
    f.close()

    
    ptr1 += 1
    curveSpeed.setData(dataSpeed)
    curveSpeed.setPos(ptr1, 0)
    curveSteer.setData(dataSteer)
    curveSteer.setPos(ptr1, 0)
    curveBrake.setData(dataBrake)
    curveBrake.setPos(ptr1, 0)
    curveThrottle.setData(dataThrottle)
    curveThrottle.setPos(ptr1, 0)


timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(20)


pg.exec()