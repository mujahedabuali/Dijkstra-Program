from vertice import Vertice
from heap import Heap
from stack import Stack
from math import radians, sin, cos, sqrt, atan2

class Dijkstra:
    def __init__(self):
        self.vertic = {}
        self.num_vertices = 0
        self.num_edges = 0

        self.short_path = "Start:\n "
        self.distance = 0
        self.short_path_vert =[]

        self.file = None

    #read from file
    def read(self, file_path):
        
        #make its initial value
        self.vertic = {}
        self.num_vertices = 0
        self.num_edges = 0
        self.distance = 0
        self.short_path_vert =[]

        
        with open(file_path, 'r') as file:
            lines = file.readlines()
            
            first_line = lines[0].strip().split(',')
            self.num_vertices = int(first_line[0].strip())
            self.num_edges = int(first_line[1].strip())

            #read vertice
            for i in range(1, self.num_vertices):
                ver_line = lines[i].strip().split(',')

                name = ver_line[0].strip()
                x=ver_line[1].strip()
                y=ver_line[2].strip()
                st=ver_line[3].strip()

                x = float(x)
                y = float(y)

                ver = Vertice(name, x, y,st)
                self.vertic[name] = ver

            #read edges
            for j in range(self.num_vertices,self.num_edges+self.num_vertices):
                edge_line = lines[j].strip().split(',')
                from_name = edge_line[0].strip()
                to_name = edge_line[1].strip()

                from_ver = self.vertic[from_name]
                to_ver = self.vertic[to_name]
                from_ver.add_edge(to_ver)

          
    #get short path and distance
    def calculate_dijkstra(self, source, dest):
        known = {}
        dis = {}
        prev = {}
        heap = Heap()
        stack = Stack()

        #clear before using
        self.short_path_vert =[]
        self.short_path = "Start:\n"
        self.distance = 0

        srcVert = self.vertic[source]
        desVert = self.vertic[dest]
        
        dis[srcVert] = 0
        prev[srcVert] = None
        heap.push(srcVert,dis[srcVert])

        while not heap.is_empty():
            curnt = heap.pop()
            print("name: ",curnt.name)
            known[curnt]=1
    
            if curnt.name == desVert.name: break

            for i in curnt.getEdges() :
                adj = i.end
                print("adj: ",adj.name)

                if adj not in known:
                    print("!")
                    dis[adj] = float('inf')
                    known[adj]=0
                    prev[adj] = None

                newDis = self.get_Distance(curnt,adj)+dis[curnt]
                print(newDis)
                if newDis<dis[adj]:
                    print("!!")
                    dis[adj] = newDis
                    prev[adj] = curnt
                    heap.push(adj,dis[adj])

                       
        desCurnt=desVert  
        # add path on stack
        while desCurnt is not None:          
                stack.push(desCurnt)
                desCurnt = prev.get(desCurnt)     

        #get vertices path and put it on array
        size = stack.size()
        for i in range(0,size): 
            self.short_path_vert.append(stack.pop()) 
      
        #print path for GUI
        for i in range(0,len(self.short_path_vert)): 
            if(i==len(self.short_path_vert)-1):
                self.short_path+="*"
                self.short_path+=self.short_path_vert[i].name+"*\n -> END!"
            else:self.short_path+=self.short_path_vert[i].name+f"\n\n↓↓↓ {"{:.2f}".format(self.get_Distance(self.short_path_vert[i],self.short_path_vert[i+1]))}KM ↓↓↓\n"  
            self.short_path+="\n"


        #get distance for the short Path   
        for i in range(len(self.short_path_vert)-1):
            ver1 = self.short_path_vert[i]
            ver2=self.short_path_vert[i+1]
            
            d =self.get_Distance(ver1,ver2)
            self.distance+=d 
      

    #Haversine formula for get distance between tow points  
    def get_Distance(self,v1,v2):

        cord = (v1.x,v1.y)    
        cord2 = (v2.x,v2.y) 
        r = 6371.0

        la1, l1 = map(radians, cord)
        la2, l2 = map(radians, cord2)

        dt = la2 - la1
        dn = l2 - l1

        a = sin(dt / 2)**2 + cos(l1) * cos(l2) * sin(dn / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        d = r * c
        return d