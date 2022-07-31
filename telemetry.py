import math

xPos = 0
yPos = 0
def update(ir, file):
    f = open(file, "a")
    global xPos, yPos
    # get GPS speed (m/s)
    speed = ir['Speed']
    if(abs(speed) < 1):
        speed = 0

    # estimate position (m)
    x = ir['VelocityX'] if abs(ir['VelocityX']) > 0.1 else 0
    y = ir['VelocityY'] if abs(ir['VelocityY']) > 0.1 else 0
    yawNorth = ir['YawNorth']
    #print("yaw relative to North (rad): " + str(yawNorth))

    deltaX = x*math.sin(yawNorth) + y*math.cos(yawNorth)
    deltaY = x*math.cos(yawNorth) + y*math.sin(yawNorth)

    xPos += deltaX * .02
    yPos += deltaY * .02
    
    speed = str(speed)
    time = str(ir['SessionTime'])
    laps = str(ir['LapCompleted'])
    gear = str(ir['Gear'])

    # pedal inputs
    brake = str(ir['Brake'])
    throttle = str(ir['Throttle'])

    # steering angle
    steering = str(ir['SteeringWheelAngle'])

    lapdist = str(ir["LapDistPct"])
    row = time + "," + laps + "," + speed + "," + gear + "," + brake + "," + throttle + "," + steering + "," + lapdist + "," + str(xPos) + "," + str(yPos) + "\n"
    f.write(row)
    f.close()

def get_headers():
    return "Time (s),Laps (#),Speed (m/s),Gear (#),Brake (%),Throttle (%),Steering Angle (rad),Distance around lap (%),X Position (m),Y Position (m)\n"