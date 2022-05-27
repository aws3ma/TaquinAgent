from copy import deepcopy
from home.Node import Node
from home.PriorityQueue import PriorityQueue

class Taquin:
	def __init__(self, l, n, goal):
		self.m = self.array_to_matrix(l, n)
		self.goal = goal
    # convert the inisitial state from list to matrix

	def array_to_matrix(self, l, n):
		b = []
		m = []
		j = 0
		for k in l:
			if j < n:
				m.append(k)
				j += 1
			if j == n:
				b.append(m)
				m = []
				j=0
		return b
    # generate nodes to work with when needed from the algorithm A*
	def get_neighbors(self, v):
		zero_pos=self.pos(v.current_node,0)
		possibilities_pos = self.generate_possibilities(zero_pos,len(self.m)-1)
		possibilities =[]
		for pos in possibilities_pos:
			temp=deepcopy(v.current_node)
			temp[zero_pos[0]][zero_pos[1]]=temp[pos[0]][pos[1]]
			temp[pos[0]][pos[1]]=0
			node = Node(temp,v,v.g+1,self.manhattan_distance(temp,self.goal),pos[2])
			possibilities.append(Node(temp,v,v.g+1,self.manhattan_distance(temp,self.goal),pos[2]))
		return possibilities
    # calculate what kind of moves the blank case is able to
	def generate_possibilities(self,m,n):
		pos=[]
		l=[]
		if m[0]>0:
			l.append(m[0]-1)
			l.append(m[1])
			l.append('U')
			pos.append(l)
			l=[]
		if m[0]<n:
			l.append(m[0]+1)
			l.append(m[1])
			l.append('D')
			pos.append(l)
			l=[]
		if m[1]>0:
			l.append(m[0])
			l.append(m[1]-1)
			l.append('L')
			pos.append(l)
			l=[]
		if m[1]<n:
			l.append(m[0])
			l.append(m[1]+1)
			l.append('R')
			pos.append(l)
			l=[]

		return pos
    # heuristic function calculate manhattan distance
	def manhattan_distance(self, m,a):
		s=0
		for i in range(len(m)):
			for j in range(len(m)):
				if(m[i][j]!=0):
					currentpos=self.pos(m,m[i][j])
					goalpos=self.pos(a,m[i][j])
					s+=abs(currentpos[0]-goalpos[0])+abs(currentpos[1]-goalpos[1])
		return s
    # get pos of k in puzzle
	def pos(self,matrice,k):
		i=0
		j=0
		while i<len(matrice):
			while j<len(matrice):
				if matrice[i][j]==k:
					return (i,j)
				j+=1
			j=0
			i+=1
		return (-1,-1)
    # every node have the direction, we will collect them to define the fastest path as a list of characters
	def build_path(self,closed_set):
		node = closed_set[str(self.goal)]
		branch = list()
		while node.dir:
			branch.append(node.dir)
			node = closed_set[str(node.previous_node.current_node)]
		branch.reverse()
		return branch

	def a_star_search(self):
		closed_set = {}
		frontier = PriorityQueue()
		frontier.put(Node(self.m, self.m, 0, self.manhattan_distance(self.m,self.goal), ""),0)

		while True:
			if frontier.empty():
				return None
			test_node = frontier.get()
			closed_set[str(test_node.current_node)] = test_node
			if test_node.current_node == self.goal:
				return self.build_path(closed_set)

			neighbors = self.get_neighbors(test_node)
			for node in neighbors:
				if str(node.current_node) in closed_set.keys():
					continue        
				frontier.put(node,node.f())