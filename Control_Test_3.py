"""Servomotor Control Version 3

This script defines the functions available for control
and executes a functionality test of the servomotors.

This script is meant to run on a Raspberry Pi with an Adafruit 16-Channel PWM / Servo HAT
and requires `Adafruit ServoKit Library 1.0` be installed in the environment.

File can be imported for use of the following functions:
    * Pan_To_Angle - pans the camera directly to a desired angle given X and Y values.
    * Control - the primary method for controlling the camera using vectors.

If run as main program this script will execute a test of the
cameras diagonal panning and if it can reach all boundaries.
"""

from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)

# this test script uses adafruit_servokit library for controlling 



# hardcoded coords for testing. Would be calculated in real time
# the direction of movement is the vector from initial coordinates to current coordinates
touch_origin = [100, 100]   # <- Coordinate of initial touch, would remain constant until finger is lifted


right = [200, 100]
left = [0, 100]
up = [100, 0]
down = [100, 200]

right_up = [200, 0]
right_down = [200, 200]
left_up = [0, 0]
left_down = [0, 200]


gain = [1/25,-1/25]     # determine through trial and error


def Init():
    # move servos to neutral position at center of boundary
    Pan_To_Angle(90,90)

    print(kit.servo[0].angle, kit.servo[2].angle)

def Pan_To_Angle(x_angle, y_angle):
    # pan directly to a desired angle, needs X and Y coordinates

    x_angle = Check_Angle(x_angle,10, 170)
    y_angle = Check_Angle(y_angle,30, 150)

    angle_current_x = kit.servo[0].angle
    angle_current_y = kit.servo[2].angle

    displacement_x = x_angle - angle_current_x
    displacement_y = y_angle - angle_current_y

    k = 20
    for i in range(1,k+1):
        # discretize camera movement to allow diagonal panning
        kit.servo[0].angle = angle_current_x + i*(displacement_x/k)
        kit.servo[2].angle = angle_current_y + i*(displacement_y/k)
        
        time.sleep(0.05/10) # slows down camera movement, experimenting with this
    print(servo_0.angle, servo_2.angle)



def Check_Angle(value, lower_bound, upper_bound):
    # make sure the desired angle is within boundary conditions
    # if value outside conditions return max or min value

    if value < lower_bound:
        return lower_bound
    elif value > upper_bound:
        return upper_bound
    else:
        return value


def Check_Boundary(value, lower_bound, upper_bound):
    # make sure desired angle is within bounds. Returns Boolean

    if value < lower_bound:
        return True
    elif value > upper_bound:
        return True
    else:
        return False

def Cap_Displacement(value, upper_bound):
    # check that displacement magnitude is below some threshold
    sign = (value > 0) - (value < 0)
    if abs(value) > upper_bound:
        return sign*upper_bound
    else:
        return value

def Control(position):
    # needs origin of touch, and current coordinates
    # the difference (vector) two will be mutiplied by some gain and added onto the current angle
    
    angle_current_x = kit.servo[0].angle
    angle_current_y = kit.servo[2].angle

    displacement_x = (position[0] - touch_origin[0])*gain[0]
    displacement_y = (position[1] - touch_origin[1])*gain[1]

    # displacement capped at 5 degrees per iteration
    displacement_x = Cap_Displacement(displacement_x, 5)
    displacement_y = Cap_Displacement(displacement_y, 5)

    angle_desired_x = angle_current_x + displacement_x
    angle_desired_y = angle_current_y + displacement_y

    # make sure angle is within [0 to 180] by some margin
    if Check_Boundary(angle_desired_x, 10, 170):
        displacement_x = 0

    if Check_Boundary(angle_desired_y, 30, 150):
        displacement_y = 0

    k = 20
    for i in range(1,k+1):
        # an attempt to discretize camera movement to allow diagonal panning
        kit.servo[0].angle = angle_current_x + i*(displacement_x/k)
        kit.servo[2].angle = angle_current_y + i*(displacement_y/k)
        

        time.sleep(0.05/10) # experimenting with this

    print(kit.servo[0].angle, kit.servo[2].angle)


def Pan_To_Boundary(direction):
    # used for testing if servomotors successfully move within their bounds
    x = kit.servo[0].angle
    y = kit.servo[2].angle

    Control(direction)
    while(x != kit.servo[0].angle or y != kit.servo[2].angle):
        x = kit.servo[0].angle
        y = kit.servo[2].angle

        Control(direction)




# _______MAIN________
# run a test of the servomotor movement

if __name__ == '__main__':

    Init()

    # test diagonal panning of camera
    Pan_To_Boundary(left_up)
    Pan_To_Boundary(down)
    Pan_To_Boundary(right_up)
    Pan_To_Boundary(left)
    Pan_To_Boundary(right_down)
    Pan_To_Boundary(up)
    Pan_To_Boundary(left_down)

    Init()

