"""
Various methods of drawing scrolling plots.
"""

from time import perf_counter
import numpy as np
import pyqtgraph as pg
import time
import irsdk

# this is our State class, with some helpful variables
class State:
    ir_connected = False
    last_car_setup_tick = -1

win = pg.GraphicsLayoutWidget(show=True)
win.setWindowTitle('speed')

f = open("data.csv", "w")
f.write("Time (s),Laps (#),Speed (m/s),Gear (#),Brake (%),Throttle (%),SteeringAngle (rad)\n")
f.close()

# 1) Simplest approach -- update data in the array such that plot appears to scroll
#    In these examples, the array size is fixed.
p2 = win.addPlot()
p2.setYRange(0, 50, padding=0)
data1 = np.random.normal(size=1500)
curve2 = p2.plot(data1)
ptr1 = 0

# initializing ir and state
ir = irsdk.IRSDK()
ir.startup()
state = State()

def update():
    global data1, ptr1
    data1[:-1] = data1[1:]  # shift data in the array one sample left
                            # (see also: np.roll)
    speed = ir['Speed']
    if(abs(speed) < 1):
        data1[-1] = 0
        speed = 0
    else:
        data1[-1] = speed
    
    f = open("data.csv", "a")
    speed = str(speed)
    time = str(ir['SessionTime'])
    laps = str(ir['RaceLaps'])
    gear = str(ir['Gear'])
    brake = str(ir['Brake'])
    throttle = str(ir['Throttle'])
    steering = str(ir['SteeringWheelAngle'])
    row = time + "," + laps + "," + speed + "," + gear + "," + brake + "," + throttle + "," + steering + "\n"
    f.write(row)
    f.close()
    x = ir['VelocityX']
    y = ir['VelocityY']
    z = ir['VelocityZ']
    print(str(x) + "\t" + str(y) + "\t" + str(z))
    
    ptr1 += 1
    curve2.setData(data1)
    curve2.setPos(ptr1, 0)


timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(20)

# here we check if we are connected to iracing
# so we can retrieve some data
def check_iracing():
    if state.ir_connected and not (ir.is_initialized and ir.is_connected):
        state.ir_connected = False
        # don't forget to reset your State variables
        state.last_car_setup_tick = -1
        # we are shutting down ir library (clearing all internal variables)
        ir.shutdown()
        print('irsdk disconnected')
    elif not state.ir_connected and ir.startup() and ir.is_initialized and ir.is_connected:
        state.ir_connected = True
        print('irsdk connected')

    

pg.exec()
try:
    # infinite loop
    while True:
        # check if we are connected to iracing
        check_iracing()
        # if we are, then process data
        if state.ir_connected:
            pass
        # sleep for 1 second
        # maximum you can use is 1/60
        # cause iracing updates data with 60 fps
        time.sleep(1/60)
except KeyboardInterrupt:
    # press ctrl+c to exit
    pass