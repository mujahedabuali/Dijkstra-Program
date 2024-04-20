class Vertice:
    def __init__(self, name, x, y,st=None):
        self.name = name
        self.x = x
        self.y = y
        self.st=st
        self.edges = []

    def add_edge(self, to):
        self.edges.append(Edge(self, to))

    def num_edge(self) :
        return len(self.edges)   

    def getEdges(self):
        return self.edges
    

class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end    