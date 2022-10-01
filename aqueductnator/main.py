#internal libraries
from classes.opensystem import OpenSystem
from classes.mesh import Mesh
from classes.pipe import Pipe
from classes.node import Node
from classes.tank import Tank
from methods import hazenw as hw

a = Tank(0, 1150)
b = Node(1, xq=-0)
c = Node(2, xq=-0)
d = Tank(3, 1030)

t = [];
t.append(Pipe(0, a, b, [16, 'in'], 1250))
t.append(Pipe(1, b, c, [10, 'in'], 2520))
t.append(Pipe(2, c, d, [14, 'in'], 1350))
t.append(Pipe(3, a, d, [14, 'in'], 1350))

s = Mesh(t)
s.defC(120)
print(s.losses())
#s.solveFlows()
#for pipe in s.pipes:
#    print(pipe.q)
