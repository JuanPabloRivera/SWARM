#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

    
#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy


def callback(data):
        #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
	print(data.axes)        
	power=70

	# Knopf A = Turbomodus
	if data.buttons[1] == 1:
        	power=80
        

	# Vorwaertsfahren
	if data.axes[1] > 0.1 and data.axes[3]==0:
        	p1.start(data.axes[1]*power)
        	p2.start(data.axes[1]*power)
	
	else:
        	p1.start(0)
        	p2.start(0)


	#Links lenken
	if data.axes[3] < 0:
        	pwm1_steer=(1-abs(data.axes[3]))*(data.axes[1]*power) #linkes Rad
        	pwm2_steer=abs(data.axes[3])*(data.axes[1]*power) #rechtes Rad
        	p1.start(pwm1_steer)
        	p2.start(pwm2_steer)
		#print(pwm1_steer, pwm2_steer)

	#rechts lenken
	if data.axes[3] > 0:
        	pwm1_steer=abs(data.axes[3])*(data.axes[1]*power) #linkes Rad
        	pwm2_steer=(1-abs(data.axes[3]))*(data.axes[1]*power) #rechtes Rad
        	p1.start(pwm1_steer)
        	p2.start(pwm2_steer)

    
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

    PWM1 =32
    PWM2 =33
    EN1  =15
    EN2  =18


    # set Pin numbers to the board's
    GPIO.setmode(GPIO.BOARD)

    # initialize PWM, EN1 and EN2 as Output
    GPIO.setup(EN1, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(EN2, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(PWM1, GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup(PWM2, GPIO.OUT, initial = GPIO.LOW)

    #define PWM with 100 Hertz
    p1=GPIO.PWM(PWM1, 5000)
    p2=GPIO.PWM(PWM2, 5000)

    try:
        listener()
    except rospy.ROSInterruptException:
        pass
