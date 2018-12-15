#!/usr/bin/env python

import rospy
import rosparam
import time


class Duckiebus:
	def __init__(self):
		self.sequence=rospy.get_param("~direction")
		self.route = rospy.get_param("~route")
		self.duckiestops = rospy.get_param("~stops")
		self.loop = 0
		print(self.sequence)
		print(self.route)
		print(self.duckiestops)
		self.run()

	def run(self):
		counter = 0
		end = len(self.sequence)
		end_stop = len(self.route)
		num_stop = len(self.duckiestops)
		
		#keep looping as long as rospy is on
		while not rospy.is_shutdown():
			#loop through all the stops
			for stop in self.route:
				print("heading to "+ str(stop))
				bus_stop = [];
				for d in self.duckiestops:
					if d[0] == stop:
						bus_stop.append(int(d[1]))
				sort(bus_stop)
				timer = 0;
				#start to run
				rospy.set_param('/pi/supervisor_node/job', sequence[counter])
				rospy.set_param('/pi/supervisor_node/job_done', False)
				print("turn " + self.sequence[counter])
				
				#test all bus stops in segement
				for ds in bus_stop:
					if ds == -1:
						continue;
					time.sleep(ds-timer) #waiit for a little
					timer = ds
					print("Duckiebus stop reached!")
					#stop the car
					rospy.set_param('/pi/supervisor_node/job_done', True)
					command = raw_input("Press y once every duckie is on the bus (y): ")
					rospy.set_param('/pi/supervisor_node/job_done', False)
					
				#done with in semgment bus stops, wait until the end of segment	
				while not rospy.get_param('/pi/supervisor_node/job_done'):
					pass 
				print("job done")

				#increment counter
				counter = (counter+1)%end
				
				#bus stop is right at the line
				if -1 in bus_stop:
					print("Duckiebus stop reached!")
					command = raw_input("Press y once every duckie is on the bus (y): ")
				
				time.sleep(3) #add delay between each job


if __name__ == "__main__":
	rospy.init_node("duckiebus", anonymous=False)
	Duckiebus()
	rospy.spin()