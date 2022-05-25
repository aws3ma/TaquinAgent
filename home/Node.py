class Node:
    def __init__(self, current_node, previous_node, g, h, dir):
        self.current_node = current_node
        self.previous_node = previous_node
        self.g = g
        self.h = h
        self.dir = dir

    def f(self):
        return self.g + self.h
    def __eq__(self, other):
        return (self.f() == other.f())

    def __lt__(self, other):
        return (self.f() < other.f())

    def __gt__(self, other):
        return (self.f() > other.f())
