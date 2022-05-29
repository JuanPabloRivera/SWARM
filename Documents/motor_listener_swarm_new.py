#!/usr/bin/env python
import RPi.GPIO as GPIO
import time


#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy


def callback(data):
        #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        power=70

	# Knopf A = Turbomodus
        if data.buttons[1] == 1:
            power=80

        dir = 0 if data.axes[1] >= 0 else 1
        GPIO.output(EN1, dir)
        GPIO.output(EN2, dir)

        speed = abs(data.axes[1])

        if data.axes[3] > 0:
            pwm1_steer = (speed*power) * abs(data.axes[3]) 
            pwm2_steer = (speed*power) * (1-abs(data.axes[3]))

        elif data.axes[3] < 0:
            pwm1_steer = (speed*power) * (1-abs(data.axes[3]))
            pwm2_steer = (speed*power) * abs(data.axes[3])

        else:
            pwm1_steer = pwm2_steer = speed*power

        print(pwm1_steer, pwm2_steer, dir)
        p1.ChangeDutyCycle(pwm1_steer)
        p2.ChangeDutyCycle(pwm2_steer)


def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.

    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("joy",Joy, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()



if __name__ == '__main__':

    # Pin definition
    PWM1 = 32
    PWM2 = 33
    EN1  = 15
    EN2  = 18

    # Motor direction, 0 forward 1 backward
    global dir
    dir = 0

    # set Pin numbers to the board's
    GPIO.setmode(GPIO.BOARD)

    # initialize PWM, EN1 and EN2 as Output
    GPIO.setup(EN1, GPIO.OUT, initial=dir)
    GPIO.setup(EN2, GPIO.OUT, initial=dir)
    GPIO.setup(PWM1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(PWM2, GPIO.OUT, initial=GPIO.LOW)

    #define PWM with 100 Hertz
    p1 = GPIO.PWM(PWM1, 5000)
    p2 = GPIO.PWM(PWM2, 5000)
    p1.start(0)
    p2.start(0)

    try:
        listener()
    except rospy.ROSInterruptException:
        print("ROS interrupt")
