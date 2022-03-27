from random import shuffle
from math import ceil,floor
from collections import OrderedDict
import time

class Taquin:
	def __init__(self, environment, previous=None, move=None):
		#l’environnement dans lequel évolue l’état
		self.environment = environment
		self.environment.createdTaquins += 1
		#la référence au taquin précédent – parent
		self.previous = previous
		# le nombre d’inversions, c’est-à-dire, le nombre de fois pour chaque élément de la sequence où celui-ci est plus grand que chacun des éléments suivants
		self.inv = None
		#  l’abréviation de l’anglais disorder, désordre, soit le nombre de tuiles qui ne sont pas à la place occupée dans l’état final
		self.dis = None
		#la distance de Manhattan brute, n’ayant subie aucune pondération
		self.man = None
		# : la somme des calculs de chaque heuristique utilisée
		self.h = None
		if previous == None:
			# premier taquin n'a aucun état previous donc path est vide
			self.path = "_"
			# le côut d’un chemin allant de l’état initial à l’état actuel représenté par un entier
			self.g = 0
			self.sequence = self.magic(1)
		else:
			# on a un previous donc n'est pas le premier, alors on va ajouter le move dernier pour contruire le path
			self.path = previous.path + move
			self.g = previous.g + 1
			# l’ordre des tuiles dans le taquin, représenté par une liste, le vide vaut 0 ; à l’état initial la sequence est une liste remplie aléatoirement
			self.sequence = previous.sequence.copy()
			self.moveTile(move)
			self.inv,self.dis,self.man,self.h = self.details()
	 	# la liste des prochains coups possibles à partir de l’état actuel
		self.moves = self.findMoves()
		# fonction d'evaluation f = g + h de la taquin acturel
		self.f = self.h + self.g
	def coordinates(self, content=0):
		width = self.environment.sizes[0]
		if isinstance(content, list):
			return (width * content[1]) + content[0]
		else:
			index = self.sequence.index(content)
			y = ceil((index + 1) / width) - 1
			x = index - (y * width)
			return [x, y]

	def details(self):
		width, length = self.environment.sizes
		weightings = self.environment.weightings
		seq = self.sequence
		inv = 0
		dis = 0
		man = 0
		h = 0
		for weighting in weightings:
			k = 0
			stepH = 0
			for i in range(0,length):
				stepMan = 0
				if weighting == weightings[0]:
					for j in range(i+1,length):
						if seq[i] != 0 and seq[j] != 0 and seq[i] > seq[j]:
							inv += 1
					if seq[i] != 0 and seq[i] != (i+1):
						dis += 1
				if i > 0:
					pos = self.coordinates(i)
					x = i % width
					coords = (((width - 1) if x == 0 else (x - 1)), ceil(i / width) - 1)
					stepMan += (abs(pos[0] - coords[0]) + abs(pos[1] - coords[1]))
					if weighting == weightings[0]:
						man += stepMan
					stepH += weighting[0][k] * stepMan
					k += 1
			if weighting[2] == 7:
				stepH += dis
			stepH = int(stepH / weighting[1])
			h += stepH
		h = int( h / len(weightings) )
		return [inv,dis,man,h]

	def findMoves(self,flex=False):
		limit = self.environment.sizes[0] - 1
		coords = self.coordinates()
		last = self.path[self.g]
		moves = []
		if coords[0] != 0 	  and (last != 'L' or flex): moves.append('R')
		if coords[0] != limit and (last != 'R' or flex): moves.append('L')
		if coords[1] != 0	  and (last != 'U' or flex): moves.append('D')
		if coords[1] != limit and (last != 'D' or flex): moves.append('U')
		return moves
	def moveTile(self, move):
		seq = self.sequence
		width = self.environment.sizes[0]
		x = self.coordinates(self.coordinates())
		if move == 'R': y = x - 1
		if move == 'L': y = x + 1
		if move == 'D': y = x - width
		if move == 'U': y = x + width
		seq[x] = seq[y]
		seq[y] = 0
	def valid(self):
		width = self.environment.sizes[0]
		self.inv,self.dis,self.man,self.h = self.details()
		row = abs(self.coordinates()[1] - width)
		return True if (((width % 2 == 1) and (self.inv % 2 == 0)) or ((width % 2 == 0) and ((row % 2 == 1) == (self.inv % 2 == 0)))) else False
	def children(self):
		childList = []
		for move in self.moves:
			child = Taquin(self.environment,self,move)
			if child.dis == 0:
				return child
			i = 0
			while (i < len(childList)):
				if (child.f < childList[i].f):
					break
				i += 1
			childList.insert(i,child)
		return childList
	def magic(self, rand=0):
		length = self.environment.sizes[1]
		seq = [0]*length
		for i in range(1, length):
			seq[i-1] = i
		if rand == 1:
			shuffle(seq)
			self.sequence = seq
			while not self.valid():
				shuffle(seq)
				self.sequence = seq
		return seq
	def __repr__(self):
		
		return self.path[1:]
