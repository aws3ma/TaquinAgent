from copy import deepcopy
import numpy as np
import math
# from .Nodes import Node
import time

DIRECTIONS = {"D": [-1, 0], "U": [1, 0], "R": [0, -1], "L": [0, 1]}
n = 0

# END = [[0,1, 2], [3,4, 5], [6,7, 8]]
END = [[1,2,3], [4, 5,6], [7, 8,0]]

#it is the node which store each state of puzzle
class Node:
    def __init__(self, current_node, previous_node, g, h, dir):
        self.current_node = current_node
        self.previous_node = previous_node
        self.g = g
        self.h = h
        self.dir = dir

    def f(self):
        return self.g + self.h


def get_pos(current_state, element):
    for row in range(len(current_state)):
        if element in current_state[row]:
            return (row, current_state[row].index(element))


#it is a distance calculation algo
def euclidianCost(current_state):
    cost = 0
    for row in range(len(current_state)):
        for col in range(len(current_state[0])):
            pos = get_pos(END, current_state[row][col])
            cost += abs(row - pos[0]) + abs(col - pos[1])
    return cost


def getAdjNode(node):
    listNode = []
    emptyPos = get_pos(node.current_node, 0)

    for dir in DIRECTIONS.keys():
        newPos = (emptyPos[0] + DIRECTIONS[dir][0], emptyPos[1] + DIRECTIONS[dir][1])
        if 0 <= newPos[0] < len(node.current_node) and 0 <= newPos[1] < len(node.current_node[0]):
            newState = deepcopy(node.current_node)
            newState[emptyPos[0]][emptyPos[1]] = node.current_node[newPos[0]][newPos[1]]
            newState[newPos[0]][newPos[1]] = 0
            # listNode += [Node(newState, node.current_node, node.g + 1, euclidianCost(newState), dir)]
            listNode.append(Node(newState, node.current_node, node.g + 1, euclidianCost(newState), dir))

    return listNode


#get the best node available among nodes
def getBestNode(openSet):
    firstIter = True

    for node in openSet.values():
        if firstIter or node.f() < bestF:
            firstIter = False
            bestNode = node
            bestF = bestNode.f()
    return bestNode

#this functionn create the smallest path
def buildPath(closedSet):
    node = closedSet[str(END)]
    branch = list()

    while node.dir:
        branch.append({
            'dir': node.dir,
            'node': node.current_node
        })
        node = closedSet[str(node.previous_node)]
    branch.append({
        'dir': '',
        'node': node.current_node
    })
    branch.reverse()

    return branch

def makegoal(br):
    br=deepcopy(br)
    goal = []

    for k in range(len(br)):
        l=[]
        for i in range(len(br)):
            lindex_min=0
            cindex_min=0
            minn=math.inf
            maxx=-math.inf

            for n in range(len(br)):
                if(minn>min(br[n])):
                    lindex_min=np.argmin(br[n])
                    cindex_min=n
                    minn=min(br[n])
                if(maxx<max(br[n])):
                    maxx=max(br[n])
            br[cindex_min][lindex_min]=maxx
            l.append(minn)
        goal[n-1][n-1]=0
        goal.append(l)
    return goal

#main function of node
def main(puzzle,n):
    # END = makegoal(puzzle)
    # print(END)
    open_set = {str(puzzle): Node(puzzle, puzzle, 0, euclidianCost(puzzle), "")}
    print(open_set)
    closed_set = {}
    timeout = time.time() + 20*n
    while True:
        if time.time() > timeout:
            break
        test_node = getBestNode(open_set)
        closed_set[str(test_node.current_node)] = test_node

        if test_node.current_node == END:
            return buildPath(closed_set)

        adj_node = getAdjNode(test_node)
        for node in adj_node:
            if str(node.current_node) in closed_set.keys() or str(node.current_node) in open_set.keys() and open_set[
                str(node.current_node)].f() < node.f():
                continue
            open_set[str(node.current_node)] = node

        del open_set[str(test_node.current_node)]



# class Taquin:
#     def __init__(self,br):
#         self.br=br
#         self.DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}
#         self.goal=[]
#         self.makegoal()
#         print("AI is working!!!")
#     #create a goal for the AI by sorting the matrix element by element
    # def makegoal(self):
    #     br=deepcopy(self.br)
    #     for k in range(len(br)):
    #         l=[]
    #         for i in range(len(br)):
    #             lindex_min=0
    #             cindex_min=0
    #             minn=math.inf
    #             maxx=-math.inf

    #             for n in range(len(br)):
    #                 if(minn>min(br[n])):
    #                     lindex_min=np.argmin(br[n])
    #                     cindex_min=n
    #                     minn=min(br[n])
    #                 if(maxx<min(br[n])):
    #                     maxx=max(br[n])
    #             br[cindex_min][lindex_min]=maxx
    #             l.append(minn)
                
    #         self.goal.append(l)
#     def get_pos(self,current_state, element):
#         for row in range(len(current_state)):
#             if element in current_state[row]:
#                 return (row, current_state[row].index(element))
#     #it is a distance calculation algo
#     def euclidianCost(self,current_state):
#         cost = 0
#         for row in range(len(current_state)):
#             for col in range(len(current_state[0])):
#                 pos = self.get_pos(self.goal, current_state[row][col])
#                 print(pos)
#                 cost += abs(row - pos[0]) + abs(col - pos[1])
#         return cost
#     def getAdjNode(self,node):
#         listNode = []
#         emptyPos = self.get_pos(node.current_node, 0)

#         for dir in self.DIRECTIONS.keys():
#             newPos = (emptyPos[0] + self.DIRECTIONS[dir][0], emptyPos[1] +self.DIRECTIONS[dir][1])
#             if 0 <= newPos[0] < len(node.current_node) and 0 <= newPos[1] < len(node.current_node[0]):
#                 newState = deepcopy(node.current_node)
#                 newState[emptyPos[0]][emptyPos[1]] = node.current_node[newPos[0]][newPos[1]]
#                 newState[newPos[0]][newPos[1]] = 0
#                 listNode.append(Node(newState, node.current_node, node.g + 1, self.euclidianCost(newState), dir))

#         return listNode
#     #get the best node available among nodes
#     def getBestNode(self,openSet):
#         firstIter = True

#         for node in openSet.values():
#             if firstIter or node.f() < bestF:
#                 firstIter = False
#                 bestNode = node
#                 bestF = bestNode.f()
#         return bestNode
#     #this functionn create the smallest path
#     def buildPath(self,closedSet):
#         node = closedSet[str(self.goal)]
#         branch = list()

#         while node.dir:
#             branch.append({
#                 'dir': node.dir,
#                 'node': node.current_node
#             })
#             node = closedSet[str(node.previous_node)]
#         branch.append({
#             'dir': '',
#             'node': node.current_node
#         })
#         branch.reverse()

#         return branch
#     #main function of node A* algorithm
#     def main(self,n):
#         open_set = {str(self.br): Node(self.br, self.br, 0, self.euclidianCost(self.br), "")}
#         closed_set = {}
#         timeout = time.time() + 20*n
#         while True:
#             if time.time() > timeout:
#                 break
#             test_node = self.getBestNode(open_set)
#             closed_set[str(test_node.current_node)] = test_node

#             if test_node.current_node == self.goal:
#                 return self.buildPath(closed_set)

#             adj_node = self.getAdjNode(test_node)
#             for node in adj_node:
#                 if str(node.current_node) in closed_set.keys() or str(node.current_node) in open_set.keys() and open_set[
#                     str(node.current_node)].f() < node.f():
#                     continue
#                 open_set[str(node.current_node)] = node

#             del open_set[str(test_node.current_node)]