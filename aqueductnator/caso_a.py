from numpy import arange, linspace
from classes.node import Node
from classes.pipe import Pipe
from methods import hazenw as hw

c = 120;
d1 = 8*0.0254; #m
l1 = 300; #m

d2 = 6*0.0254; #m
l2 = 250; #m

i=0;
tol = 0.01;
for qb in arange(65, 137, 0.01):
    i += 1
    print(f'Iteracion {i} con Qb = {qb} lps:')

    hdt = 150 - qb**2/125; #m
    hpb = 0 + hdt;

    hf1 = hw.hf(qb/1000, l1, d1, c)
    hpi = hpb - hf1;
    hpc = 80

    hf2 = hw.hf(qb/1000, l2, d2, c)
    dh = hpi - hf2 - hpc;
    if abs(dh) <= tol:
        print(f'CP B = {hpb} [m]')
        print(f'hf 1 = {hf1} [m]')
        print(f'CP I = {hpi} [m]')
        print(f'hf2 I = {hf2} [m]')
        print(f'Error = {dh} [m]')
        break
    