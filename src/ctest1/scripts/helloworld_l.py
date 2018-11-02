#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def callback(data):
	rospy.loginfo("I heard%s", data.data)


def helloworld_l():
	rospy.init_node('helloworld_l', anonymous=True)
	rospy.Subscriber("world", String, callback)
	rospy.spin()
	
