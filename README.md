# Taquin Agent
Backend : Django.<br/>
Three classes : 
- Class node : Store current and previous node with heuristics

- Class Taquin : The agent use A* algorithm to calculate steps and achieve the goal

- Class PriorityQueue : Store states ordered in heapq
One methods :
- Post : Sending data from client (Frontend) to server (Backend) in json format<br/>
{"data": [1,7,3,6,4,8,2,5,0]}
<br/> data refers to the matrix of our puzzle. This method will return pattern of characters for moving : U : UP, D : Down, R : Right, L : Left <br/>

To start django server execute this commande in the root (same level of manager.py) : python manager.py runserver
