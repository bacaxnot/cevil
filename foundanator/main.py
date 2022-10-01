#internal libraries
from methods.lateralPressure import *
from classes.layer import Layer
from classes.soil import Soil  
#data
l1 = Layer(indx=1, thick=3, phi=30, gamma=18, c=10 ,saturated=False)
l2 = Layer(indx=2, thick=4, phi=30, gamma=20.1, c=10 , saturated=True)
l3 = Layer(indx=3, thick=2, phi=25, gamma=18.4, c=20 , saturated=True)
#l4 = Layer(indx=4, thick=2, phi=25, gamma=18.4, saturated=True)
#l5 = Layer(indx=5, thick=4, phi=26, gamma=19.5, saturated=True)

s = Soil([l2, l1, l3], overload=50)


method = RankineMethod(s);
stress = StressDistribution(method.active());
print(stress.resultant, stress.centroid)