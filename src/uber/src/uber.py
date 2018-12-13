#!/usr/bin/env python

import rospy
import rosparam
from graph import Graph, Node

class Uber:

	def __init__(self):
		# get user input
		self.graph = rospy.get_param("uber_node")
		self.mode = rospy.get_param("~mode")
		if self.mode == "taxi":
			self.start = rospy.get_param("~start")
			self.end = rospy.get_param("~end")
		else:
			self.start == None
			self.end == None
		rospy.loginfo("[Start] %s, [End] %s, [Mode] %s Initialized ",self.start, self.end,self.mode)
		self.run()

	#set all visit status to a certain value
	def all_nodes_visit(self,value):
		for k in self.graph.keys():
			self.visited[k] = value
			for o in self.graph[k]:
				if len(o)>0:
					self.visited[o] = value

	def previsit(self,node):
		print("previsit " + str(node) )
	
	def postvisit(self,node):
		print("postvisit "+str(node))
	#visited is set to true for 
	#all nodes reachabe from input node
	def explore(self,node):
		self.visited[node] = True
		print("visited " + str(node))
		self.previsit(node)
		for v in self.graph[node]:
			if len(v) > 0 and self.visited[v] is False:
				self.explore(v)
		self.postvisit(node)

	def dfs(self):
		self.all_nodes_visit(False)
		print(self.visited)
		for v in self.visited.keys():
			if not self.visited[v]:
				self.explore(v)
		print(self.visited)

	def path(self):
		print(self.start)
		print(self.end)
		town_map = Graph()
		for k in self.graph.keys():
			if k == "start" or k == "end" or k == "mode":
				continue
			node = Node(k,self.graph[k])
			town_map.add_node(node)
		town_map.dijkstra(self.start)
		path =town_map.shortest_path(self.start,self.end) 
		directions = town_map.direction(path)
		print(directions)
		for direct in directions:
			rospy.set_param('/pi/supervisor_node/job', direct)
			rospy.set_param('/pi/supervisor_node/job_done', False)
			print("turn " + direct)
			while not rospy.get_param('/pi/supervisor_node/job_done'):
				pass #waiting for supervisor to get job done
			print("job done")
			time.sleep(2) #add delay between each job
		
	def run(self):
		if self.mode == "taxi":
			self.path()
		elif self.mode == "bus":
			print("bus mode")


if __name__ == "__main__":
	rospy.init_node("uber", anonymous=False)
	Uber()
	rospy.spin()