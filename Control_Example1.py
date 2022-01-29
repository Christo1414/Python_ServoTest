import time

class Servo:    
    angle = 0

servo_0 = Servo()
servo_2 = Servo()

# This script uses a mock class
# demonstrates how the functions below should behave by printing out values it would send to adafruit_servokit

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

    servo_0.angle = 90
    servo_2.angle = 90

    print(servo_0.angle, servo_2.angle)

def Check_Boundary(value, lower_bound, upper_bound):
    #make sure value is within bounds
    if value < lower_bound:
        return True
    elif value > upper_bound:
        return True
    else:
        return False

def Cap_Displacement(value, upper_bound):

    sign = (value > 0) - (value < 0)
    if abs(value) > upper_bound:
        return sign*upper_bound
    else:
        return value

def Control(position):
    # needs origin of touch, and current coordinates
    # the difference between the two will be mutiplied by some gain and added onto the current angle

    angle_current_x = servo_0.angle
    angle_current_y = servo_2.angle

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

    k = 10
    for i in range(1,k+1):
        # discretize camera movement to allow diagonal panning
        servo_0.angle = angle_current_x + i*(displacement_x/k)
        servo_2.angle = angle_current_y + i*(displacement_y/k)
        
        time.sleep(0.05/10) # experimenting with this

    print(servo_0.angle, servo_2.angle)


def Pan_To_Boundary(direction):
    # used for testing
    x = servo_0.angle
    y = servo_2.angle

    Control(direction)
    while(x != servo_0.angle or y != servo_2.angle):
        x = servo_0.angle
        y = servo_2.angle

        Control(direction)


# ________MAIN________

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








