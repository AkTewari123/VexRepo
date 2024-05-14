# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       A. Tewari and A. Teng                                        #
# 	Created:      5/3/2024, 10:33:45 AM                                        #
# 	Description:  A1 Wait States                                               #
#                                                                              #
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


# Bump Switch - will hold the program until pressed
def bump():
    while bumpSwitch.pressing() == False:
        wait(10, MSEC)
        pass


def spinMotors(vel):
    # Set the velocity as a percentage
    rightMotor.set_velocity(vel, PERCENT)
    leftMotor.set_velocity(vel, PERCENT)
    # Make both the motors spin forward
    rightMotor.spin(FORWARD)
    leftMotor.spin(FORWARD)
    # Clearn the Timer
    brain.timer.clear()
    brain.screen.print("Timer Started")


def stopMotors():  # Stop both motors
    rightMotor.stop()
    leftMotor.stop()


def main():
    motorVelocity = 70
    brain.screen.set_cursor(1, 1)

    bump()

    spinMotors(motorVelocity)
    wait(5000, MSEC)

    stopMotors()

    brain.screen.set_cursor(2, 1)
    brain.screen.print("Time: " + str(brain.timer.time(SECONDS)))


main()
