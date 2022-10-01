#LIBRERIAS PROPIAS
from sections import *
from channels import *

#PROBLEMA 2.1
K = TrapezoidSection(b = 3, m = 2, y = 1)

Q = 2; Yo = 0.1; Yf = 2; E = 1
yc = K.cDepth(Q)
print(f"Profundidad critica: {yc}")
print(f"Energía mínima: {K.specificEnergy(Q, yc)}")
print(f"Caudal máximo: {K.flowRate(E, yc)}")
print(f"Profundidades alternas: {K.alternDepths(Q, E)}")
K.drawSpecificEnergyCurve(Q, Yo, Yf, Step =0.001)
K.drawFlowRateCurve(E, Yo, E)