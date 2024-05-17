# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Akshat Tewari and Andy Teng                                              #
# 	Created:      5/14/2024, 10:10:24 AM                                       #
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
    normal = 60  # Run at normal percent of max speed
    slow = 50  # Run at slow percent of max speed

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


# Automatic straightening (driving forward)
def driveStraightReverse(
    distance, overshoot
):  # param 1 = normal distance, param 2 = overshoot correction
    distance -= overshoot  # Correct distance
    count = -(360 * distance) / (
        4 * math.pi
    )  # Convert distance in inches to degrees of rotation
    leftEncoder.set_position(0, DEGREES)  # Reset encoders
    rightEncoder.set_position(0, DEGREES)

    #   Normal and slow velocities (tuned for specific robot)
    normal = -60  # Run at normal percent of max speed
    slow = -50  # Run at slow percent of max speed

    while rightEncoder.position(DEGREES) > count:
        encoderValues()

        # Compare the left and right encoders and correct motors as necessary
        if rightEncoder.position(DEGREES) < leftEncoder.position(
            DEGREES
        ):  # if the left encoder is faster
            spinMotors(slow, normal)
        elif leftEncoder.position(DEGREES) > rightEncoder.position(DEGREES):
            spinMotors(normal, slow)
        else:
            spinMotors(normal, normal)
    stopMotors()


def main():
    bump() # Call bump and wait for a button press
    driveStraightFoward(120, 7.5) # Drive the robot straight forward
    wait(3, SECONDS)
    driveStraightReverse(120, 7.5) # Drive the robot straight forward
main()

