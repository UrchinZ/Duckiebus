
class Node(object):
	"""docstring for Node"""
	def __init__(self, id, info):
		self.id = id
		self.neighbor = {}
		self.cost = {}
		self.process_info(info)
	
	def process_info(self,info):
		directions = ["left","forward","right"]
		for i in range(0,len(directions)):
			node = info[0][i]
			if(len(node) > 0):
				self.neighbor[node] = directions[i]
				self.cost[node] = info[1][i]
		
	def value(self):
		return str(self.id) + ":\nneighbor|"+str(self.neighbor) + "\ncost:"+str(self.cost) 


class Graph:
	def __init__(self):
		self.nodes = {}
		self.dist = {}
		self.parent = {}

	def add_node(self,node):
		self.nodes[node.id] = node

	def value(self):
		v = "====== graph nodes: =====\n"
		for n in self.nodes.keys():
			v += self.nodes[n].value() + "\n"
		v += "===== dist ===== \n" + str(self.dist) + "\n===========\n===== min parent ====== \n" + str(self.parent) + "\n=========="
		return v

	def min_distance(self,queue):
		minimum = float("inf")
		min_node= None
		for node_id in queue:
			d = self.dist[node_id]
			if(d < minimum):
				minimum = d
				min_node = node_id
		return min_node

	#find distance of all nodes to start
	def dijkstra(self,start):
		#initialize distance for all nodes
		for node_id in self.nodes.keys():
			self.dist[node_id] = float("inf")
			if node_id == start:
				self.dist[node_id] = 0

		#Add all vertices in queue
		queue = self.nodes.keys()

		#find shortest path for all vertices
		while queue:
			#pick the minimum dist vertex 
			#from the set of vertices
			#still in queue
			u = self.min_distance(queue)
			#remove min element
			queue.remove(u)
			#update distance value and path
			node = self.nodes[u]
			for neighbor in node.cost.keys():
				if neighbor in queue:
					new_cost = self.dist[u] + node.cost[neighbor]
					if(new_cost < self.dist[neighbor]):
						self.dist[neighbor] = new_cost
						self.parent[neighbor] = u
	#back track to find shortest path
	def shortest_path(self,start,end):
		path = []
		node = end
		while not node == start:
			path.append(node)
			node = self.parent[node]
		path.append(start)
		path.reverse()
		return path

	def direction(self,path):
		d = []
		for i in range(len(path)-1):
			node_id = path[i]
			next_id = path[i+1]
			node = self.nodes[node_id]
			d.append(node.neighbor[next_id])
		return d


