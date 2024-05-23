# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       akshattewari                                                 #
# 	Created:      5/23/2024, 10:36:27 AM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain = Brain()

brain.screen.print("Hello V5")

# Robot Configuration

rightMotor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
leftMotor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
liftMotor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
rightEncoder = Encoder(brain.three_wire_port.a)
leftEncoder = Encoder(brain.three_wire_port.g)
pot1 = PotentiometerV2(brain.three_wire_port.e)
bumpSwitch = Bumper(brain.three_wire_port.d)


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


def encoderValues():
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Right encoder: ")
    brain.screen.print(
        rightEncoder.position(DEGREES)
    )  # Prints out the right encoder values
    brain.screen.set_cursor(1, 25)
    brain.screen.print("Left encoder: ")
    brain.screen.print(
        leftEncoder.position(DEGREES)
    )  # Prints out the left encoder values

    brain.screen.set_cursor(1, 25)


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


# Bump Switch - will hold the program until pressed
def bump():
    while bumpSwitch.pressing() == False:
        wait(10, MSEC)
        pass


# Automatic straightening (driving forward)
def driveStraightFoward(
    distance, overshoot
):  # parame1 = nomial distance, param2 = overshoot correction
    distance -= overshoot  # Correct distance
    count = (360 * distance) / (
        4 * math.pi
    )  # Convert distance in inches to degrees of rotation
    leftEncoder.set_position(0, DEGREES)  # Reset encoders
    rightEncoder.set_position(0, DEGREES)

    #   Normal and slow velocities (tuned for specific robot)
    normal = 50  # Run at normal percent of max speed
    slow = 43  # Run at slow percent of max speed

    while rightEncoder.position(DEGREES) < count:
        encoderValues()

        # Compare the left and right encoders and correct motors as necessary
        if rightEncoder.position(DEGREES) < leftEncoder.position(
            DEGREES
        ):  # if the left encoder is faster
            spinMotors(normal, slow)
        elif leftEncoder.position(DEGREES) < rightEncoder.position(DEGREES):
            spinMotors(slow, normal)
        else:
            spinMotors(normal, normal)
    stopMotors()


def main():
    leftMotor.set_stopping(BRAKE)
    rightMotor.set_stopping(BRAKE)
    driveStraightFoward(48, 7)
    pointLeft(270)
    stopMotors()
    driveStraightFoward(48, 7)
    pointLeft(270)
    stopMotors()
    driveStraightFoward(48, 7)
    pointLeft(270)
    stopMotors()
    driveStraightFoward(48, 7)
    pointLeft(270)
    stopMotors()


main()
