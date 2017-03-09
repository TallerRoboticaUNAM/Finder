#!/usr/bin/env python

import roslib
import rospy
from geometry_msgs.msg import Twist
import sys,select,termios,tty

msg="""
Control your turtlebot
Moving around:
 u i o
 j k l 
 m , .
 
q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease omly angular speed by 10%
space key,k : force stop
anything else: stop smoothly

CTRL C to quit
"""

moveBindings={
	'i':(1,0),
	'o':(1,-1),
	'j':(0,1),
	'l':(0,-1),
	'u':(1,1),
	',':(-1,0),
	'.':(-1,1),
	'm':(-1,-1),
				}

speedBindings={
	'q':(1.1,1.1),
	'z':(.9,.9),
	'w':(1.1,1),
	'x':(.9,1),
	'e':(1,1.1),
	'c':(1,.9),
 				}
 				
def getKey():
	tty.setraw(sys.stdin.fileno())
	rlist, _, _ =select.select([sys.stdin], [],[],0.1)	
	if rlist:
		key=sys.stdin.read(1)
	else:
		key=''
	
	termios.tcsetattr(sys.stdin,termios.TCSADRAIN,settings)
	return key

speed = 1
turn = 1

def vels(speed,turn):
	return  "currently:\tspeed %s \t turn %s" % (speed,turn)

if __name__=="__main__":
	settings=termios.tcgetattr(sys.stdin)
	rospy.init_node('chefbot teleop')
	pub=rospy.Publisher('~cmd_vel',Twist,queue_size=5)
	
	x=0
	th=0
	status=0
	count=0
	acc=0.1
	target_speed=0
	target_turn=0
	control_speed=0
	control_turn=0
	try:
		print msg
		print vels(speed,turn)
		while(1):
			key=getKey()
			if key in moveBindings.keys():
				x=moveBindings[key][0]
				th=moveBindigs[key][1]
				count=0
			elif key in speedBindings.keys():
				speed=speed*speedBindigns[key][0]
				turn=turn*speedBindings[keys][1]
				count=0
				
				print vels(speed,turn)
				if(status==14):
					print msg
				status=(status+1)%15
			elif key==' ' or key=='k':
				x=0
				th=0
				control_speed=0
				control_turn=0
			else:
				count=count+1
				if count>4:
					x=0
					th=0
				if(key=='\x03'):
					break
			target_speed=speed*x
			target_turn=turn*th
			
			if target_speed>control_speed:
				control_speed=min(target_speed,control_speed+.02)
			elif target_speed<control_speed:
				control_speed=max(target_speed,control_speed-.02)
			else:
				control_speed=target_speed
			
			if target_turn>control_turn:
				control_turn=min(target_turn,control_turn+.1)
			elif target_turn<control_turn:
				control_turn=max(target_turn,control_turn-.1)
			else:
				control_turn=target_turn
				
			twist=Twist()
			twist.linear.x=control_speed;twist.linear.y=0;twist.linear.z=0
			twist.angular.x=0;twist.angular.y=0;twist.angular.z=control_turn
			pub.publish(twist)
	except:
		print e
	finally:
		twist=Twist()
		twist.linear.x=0;twist.linear.y=0;twist.linear.z=0
		twist.angular.x=0;twist.angular.y=0;twist.angular.z=0
		pub.publish(twist)

	termios.tcsetattr(sys.stdin,termios.TCSADRAIN,settings)