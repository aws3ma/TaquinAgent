# Taquin Agent
Backend : Django.<br/>
Two classes : 
- Class node : Store current and previous node with heuristics

- Class Taquin : The agent use A* algorithm to calculate steps and achieve the goal

Two methods :
- Post : Sending data from client (Frontend) to server (Backend) in json format<br/>
{"data":{
    "a00":8,
    "a01":7,
    "a02":0,
    "a10":2,
    "a11":4,
    "a12":6,
    "a20":1,
    "a21":5,
    "a22":3},"n":3
}<br/> data refers to the matrix of our puzzle and n refers to number of elements per record in the matrix
- Get : Return the result of the Agent in json format. Every element is the next move of the empty case and the current status of the puzzle

