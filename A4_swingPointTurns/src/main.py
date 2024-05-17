# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Akshat Tewari and Andy Teng                                              #
# 	Created:      5/17/2024, 10:10:24 AM                                       #
# 	Description:  A3_VelocityLevelEncoders                                                  #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain = Brain()
# Robot Configuration

rightMotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
leftMotor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
liftMotor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
rightEncoder = Encoder(brain.three_wire_port.a)
leftEncoder = Encoder(brain.three_wire_port.g)
pot1 = PotentiometerV2(brain.three_wire_port.e)
bumpSwitch = Bumper(brain.three_wire_port.d)


# Bump Switch - will hold the program until pressed
def bump():
    while bumpSwitch.pressing() == False:
        wait(10, MSEC)
        pass


def spinMotors(rightMotorVelocity, leftMotorVelocity):
    # Set the velocity as a percentage
    rightMotor.set_velocity(rightMotorVelocity, PERCENT)
    leftMotor.set_velocity(leftMotorVelocity, PERCENT)
    # Make both the motors spin forward
    rightMotor.spin(FORWARD)
    leftMotor.spin(FORWARD)


def stopMotors():  # Stop both motors
    rightMotor.stop()
    leftMotor.stop()


# Print out the encoder values on the screen
def encoderValues():
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Right encoder: ")
    brain.screen.print(rightEncoder.position(DEGREES))
    brain.screen.set_cursor(1, 25)
    brain.screen.print("Left encoder: ")
    brain.screen.print(leftEncoder.position(DEGREES))

    brain.screen.set_cursor(1, 25)


# Left Swing Turn
def swingLeft(turnCount) :
    rightEncoder.set_position (0, DEGREES)
    # turnCount = encoder count for turn
    # Reset the right encoder to 0.
    while (rightEncoder.position(DEGREES) < turnCount): # Check turn status based on right encoder count
        spinMotors (50, 0)
        # Spin right motor forward (left = off)
    stopMotors()       # Stop the motors
    
    
# Right Swing Turn
def swingRight(turnCount) :
    leftEncoder.set_position(0, DEGREES)
    # turnCount = encoder count for turn
    # Reset the left encoder to 0.
    while(leftEncoder.position(DEGREES) < turnCount) : # Check turn status based on left encoder count
        spinMotors (0, 50) # Spin left motor forward (right = off)
        
    stopMotors ( )
    # Stop the motors

# Left Point Turn
def pointLeft(turnCount):
    rightEncoder.set_position (0, DEGREES)
    ## turnCount = encoder count for turn
    # Reset the right encoder to 0.
    while(rightEncoder.position (DEGREES) < turnCount): # Check turn status based on right encoder count
        spinMotors (50, -50) # Spin right motor forward and left reverse
    stopMotors ()
    # Stop the motors
# Right Point Turn
def pointRight(turnCount) :
    leftEncoder.set_position (0, DEGREES)
    ## turnCount = encoder count for turn
    # Reset the left encoder to 0.
    while(leftEncoder.position(DEGREES) < turnCount):
        spinMotors (-50, 50)   # Check turn status based on left encoder count
    # Spin left motor forward and right reverse
    stopMotors ( )   # Stop the motors

def main() :
    bump()  # Wait for bump switch to be pressed to start motors
    swingLeft(1800) # 90-degree swing turn (count value specific to robot)
    #Count for 90 deg. Left turn may not be equal count for 90-deg. right turn

    #pointLeft(320) # 90-degree point turn (count value specific to robot)
    #Count for 90 deg. Left turn may not be equal count for 90-deg. right turn

main()
