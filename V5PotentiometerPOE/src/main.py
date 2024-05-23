# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Akshat Tewari and Andy Teng                                              #
# 	Created:      5/17/2024, 10:10:24 AM                                       #
# 	Description:  A4_VelocityLevelEncoders                                                  #
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
    wait(1, SECONDS)


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
def swingLeft(turnCount):
    rightEncoder.set_position(0, DEGREES)
    # turnCount = encoder count for turn
    # Reset the right encoder to 0.
    while (
        rightEncoder.position(DEGREES) < turnCount
    ):  # Check turn status based on right encoder count
        spinMotors(40, 0)
        # Spin right motor forward (left = off)
    stopMotors()  # Stop the motors


# Right Swing Turn
def swingRight(turnCount):
    leftEncoder.set_position(0, DEGREES)
    # turnCount = encoder count for turn
    # Reset the left encoder to 0.
    while (
        leftEncoder.position(DEGREES) < turnCount
    ):  # Check turn status based on left encoder count
        spinMotors(0, 50)  # Spin left motor forward (right = off)

    stopMotors()
    # Stop the motors


# Left Point Turn
def pointLeft(turnCount):
    rightEncoder.set_position(0, DEGREES)
    ## turnCount = encoder count for turn
    # Reset the right encoder to 0.
    while (
        rightEncoder.position(DEGREES) < turnCount
    ):  # Check turn status based on right encoder count
        spinMotors(60, -60)  # Spin right motor forward and left reverse
    stopMotors()
    # Stop the motors


# Right Point Turn
def pointRight(turnCount):
    leftEncoder.set_position(0, DEGREES)
    ## turnCount = encoder count for turn
    # Reset the left encoder to 0.
    while leftEncoder.position(DEGREES) < turnCount:
        spinMotors(-50, 50)  # Check turn status based on left encoder count
    # Spin left motor forward and right reverse
    stopMotors()  # Stop the motors


def liftArm(velocity, liftDisp):
    # vel = motor velocity, mDisp = angular displacement of motor sha
    # liftDisp = angular displacement for lift
    # Set motor power level
    liftMotor.set_velocity(velocity, PERCENT)
    # Configure the motor to hold its position once the lift arm rotation is complete.
    liftMotor.set_stopping(HOLD)
    GR = 5
    motorDisp = liftDisp * GR
    # Input gear = 12T, output gear = 60T for lift arm
    # Corresponding angular disp. of motor shaft with a GR = 5
    # Print starting potentiometer position (degrees)
    initPos = pot1.angle(DEGREES)   
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Pot. Angle: " + str(initPos))
    # Rotate the lift arm
    liftMotor.spin_for(FORWARD, motorDisp, DEGREES)
    # Print final potentiometer position (degrees)
    finalPos = pot1.angle(DEGREES)
    brain.screen.set_cursor(2, 1)
    brain.screen.print("Pot. Angle: " + str(finalPos))
    # Print liftarm's angular displacement
    brain.screen.set_cursor(3, 1)
    brain.screen.print("Anglular Displacement:" + str(abs(finalPos - initPos)))


def main():
    liftVel = 20
    bump()
    liftArm(liftVel, 55)


main()
# Lift motor velocity in percent
# parami = velocity level
# param2 = desired angular displacement of lift in degrees (+ raise, - lower
