#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def helloworld_t():
	pub=rospy.Publisher('world', String, queue_size=10)
	rospy.init_node('helloworld_t', anonymous=True)
	rate = rospy.Rate(1)
	while not rospy.is_shutdown():
		out_str="Hello world!"
		rospy.loginfo(out_str)
		pub.publish(out_str)
		rate.sleep()
if __name__ == '__main__':
	try:
		helloworld_t()
	except rospy.ROSInterruptException:
		pass
