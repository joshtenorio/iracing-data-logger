
def corner_header(corner):
    shockdefl = corner + " shock defl (mm),"
    shockvel = corner + " shock vel (mm/s),"
    tiretemp = corner + " tire temperature (C),"
    return shockdefl + shockvel + tiretemp

def corner(ir, corner):
    shockdefl = str(ir[corner + 'shockDefl'] * 1000)
    shockvel = str(ir[corner + 'shockVel'] * 1000)
    tiretemp = str(ir[corner + 'tempCM'])
    return shockdefl + "," + shockvel + "," + tiretemp + ","

def update(ir, file):
    f = open(file, "a")
    # get GPS speed (m/s)
    speed = ir['Speed']
    if(abs(speed) < 1):
        speed = 0

    latAccel = str(ir['LatAccel'] * 0.101972)
    lonAccel = str(ir['LongAccel'] * 0.101972)
    
    speed = str(speed)
    time = str(ir['SessionTime'])
    laps = str(ir['LapCompleted'])
    gear = str(ir['Gear'])

    # pedal inputs
    brake = str(ir['Brake'])
    throttle = str(ir['Throttle'])

    # steering angle
    steering = str(ir['SteeringWheelAngle'])
    
    # gyroscope
    pitch = str(ir['Pitch'] * 57.2958)
    roll = str(ir['Roll'] * 57.2958)
    pitchr = str(ir['PitchRate'] * 57.2958)
    rollr = str(ir['RollRate'] * 57.2958)

    lapdist = str(ir["LapDistPct"])
    row = time + "," + laps + "," + speed + "," + gear + "," + brake + ","
    row += corner(ir, "LF")
    row += corner(ir, "RF")
    row += corner(ir, "LR")
    row += corner(ir, "RR")
    row += pitch + "," + pitchr + "," + roll + "," + rollr + ","
    row += throttle + "," + steering + "," + latAccel + "," + lonAccel + "," + lapdist + "\n"
    f.write(row)
    f.close()

def get_headers():
    header = "Time (s),Lap (#),Speed (m/s),Gear (#),Brake (%),"
    header += corner_header("LF")
    header += corner_header("RF")
    header += corner_header("LR")
    header += corner_header("RR")
    header += "Pitch (deg),Pitch rate (deg/s),Roll (deg),Roll rate (deg/s),"
    header +="Throttle (%),Steering Angle (rad),Lateral Acceleration (g),Longitudinal Acceleration (g),Distance around lap (%)\n"
    return header