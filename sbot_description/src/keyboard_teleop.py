#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

msg = """

keyboard teleop sbot control
---------------------------
Moving around:
   1    w    2
   a    s    d
        x    

x : stop

1/2 : increase/ decrease speed +/- 0.1 m/s
w/s : forward/ backward
a/d : turn left/ turn right

"""

e = """
	!!!communication error!!!
"""

def teleop():
	
	print(msg)

	#init ros node
	rospy.init_node('sbot_key_teleop_node') 

	#sent command type twist to cmd_vel --> that control differencial drive plug-in
	p = rospy.Publisher('cmd_vel', Twist, queue_size=10)
	rate = rospy.Rate(5)

	#init all parameters that we want to use
	twist = Twist()
	speed = 0.0
	twist.linear.x = speed; twist.linear.y = 0; twist.linear.z = 0;           
	twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0; 

	#wait for input key then change the linear and angular velocity and sent to ros master to use in topic cmd_vel
	while(True):
		#Get 1 key from keyboard as input
		key = input("Controller command: ")

		if key == "1" and speed > 0:
			speed -= 0.1
			print("Your command (1) current speed: %.2f" %speed)
		elif key == "2":
			speed += 0.1
			print("Your command (2) current speed: %.2f" %speed)
		elif key == "a": 
			twist.angular.z = -speed
			print("Your command (a) Moving State: LEFT Current speed: %.2f, Linear velocity: %.2f, Angular velocity: %.2f" %(speed, twist.linear.x, twist.angular.z))
		elif key == "d":
			twist.angular.z = speed
			print("Your command (d) Moving State: RIGHT Current speed: %.2f, Linear velocity: %.2f, Angular velocity: %.2f" %(speed, twist.linear.x, twist.angular.z))
		elif key == "w":
			twist.linear.x = speed
			print("Your command (w) Moving State: FORWARD Current speed: %.2f, Linear velocity: %.2f, Angular velocity: %.2f" %(speed, twist.linear.x, twist.angular.z))
		elif key == "s":
			twist.linear.x = -speed
			print("Your command (s) Moving State: BACKWARD Current speed: %.2f, Linear velocity: %.2f, Angular velocity: %.2f" %(speed, twist.linear.x, twist.angular.z))
		elif key == "x":
			twist.linear.x = 0.0
			twist.angular.z = 0.0		
			print("Your command (x) Moving State: STOP!")
		else:
			twist.linear.x = 0.0
			twist.angular.z = 0.0		
			print("Q")
			break

		#sent twist to topic cmd_vel 
		p.publish(twist)	


if __name__=="__main__":

	try:
		rospy.loginfo("SBOT_Mobile_Robot Activated!")
		teleop()

	except rospy.ROSInterruptException:
		pass