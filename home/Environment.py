from random import shuffle
from math import ceil,floor
from collections import OrderedDict
import time
from .Taquin import Taquin
import math
class Environment:
	def __init__(self,width,choices=None):
		self.createdTaquins = 0
		self.sizes = (width,width*width)
		self.choices = choices
		self.weightings = self.getWeightings(choices)
		self.moves = [Taquin(self)]
		self.end = []
	def getWeightings(self,choices):
		width = self.sizes[0]
		length = self.sizes[1] - 1
		if (choices == None):
			choices = [5]
		weightings = []
		weight = length
		for index in choices:
			rho = (4 if index % 2 != 0 else 1)
			pi = [0] * length
			if index == 1:
				if width == 3:
					pi = [36, 12, 12, 4, 1, 1, 4, 1]
				else:
					for y in range(0,width):
						for x in range(0,width):
							if x == y == width-1:
								pass
							else:
								if x == y == 0:
									pi[0] = width * (width*3)
									x += 1
								if y == 0:
									while x < width:
										pi[x] = width * 3
										x += 1
								else:
									if (x == 0):
										pi[y*width] = width * 2
									else:
										pi[y*width+x] = width - y
			if index == 2 or index == 3:
				pi = [(length+1) - i for i in range(1,length+1)]
			if index == 4 or index == 5:
				pi = [0] * length
				weight = length
				for i in range(width-1):
					j = 0
					while pi[j] != 0:
						j += 1
					k = 0
					while k < width-i:
						pi[j] = weight
						j += 1
						weight -= 1
						k += 1
					j += i
					pi[j] = weight
					weight -= 1
					j += width
					while j < length - 1 :
						pi[j] = weight
						weight -= 1
						j += width
			if index == 6:
				pi = [1] * length
				rho = 1 / ((width - 3) + 1)
			if index == 7:
				pass
			if index == 8:
				mid = floor(length/2)
				for i in range(0,mid):
					pi[i] = mid - i
				if length % 2 == 1:
					pi[mid] = length
					mid += 1
				for i in range(mid,length):
					pi[i] = i+1
				rho = 2.5
			if index == 9:
				rho = 2
				j = 1
				for i in range(0,length):
					pi[i] = abs(floor(length/2) - (floor((j-1)/2)))
					if i < length-1:
						i += 1
						pi[i] = abs(floor(length/2) - (floor((j-1)/2)))
					j+=1
				if length % 2 == 1:
					pi[length-1] = 1
				shuffle(pi)

			weightings.append((pi,rho,index))
		return weightings
	@staticmethod
	def inArray(taquin,array):
		for element in array:
			if element.sequence == taquin.sequence:
				return True
		return False

	def idaStar(self):
		root = self.moves[-1]
		print(root)
		bound = root.h
		path = [root]
		Infinity = math.inf
		def search(path,g,bound):
			node = path[-1]
			f = g + node.h
			if f > bound: return f
			minimum = Infinity
			children = node.children()
			if isinstance(children,Taquin):
				path.append(children)
				return children
			else:
				for child in children:
					if not child.environment.inArray(child,path):
						path.append(child)
						t = search(path,g+1,bound)
						if isinstance(t,Taquin): return t
						if t < minimum: minimum = t
						path.pop()
			return minimum
		while (True):
			t = search(path,0,bound)
			if isinstance(t,Taquin):
				print(t)
				self.end.append(t)
				return t
			if t == Infinity: return False
			bound = t


	def expand(self,function):
		self.createdTaquins = 1
		result = function()
		return result



	# def play(self,move):
	# 	self.moves.append(Taquin(self,self.moves[-1],move))
	# 	return self.moves[-1]




