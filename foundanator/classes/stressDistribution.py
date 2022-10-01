#internal libraries
from methods.geometry import *

class StressDistribution:
    '''
    ---
    Generic class of a Stress Distribution.

    Arguments:
    - distribution: array containing values of the distribution alongside with its coordinates
    '''
    def __init__(self, distribution: np.ndarray) -> None:
        self.distribution = distribution
        pass

    def graphicDist(self):
        dist = self.distribution
        dist = np.insert(dist, 0, [0, 0], axis = 0)
        dist = np.append(dist, [[dist[-1, 0], 0]], axis = 0)
        return dist

    @property
    def resultant(self):
        pol = Polygon(self.graphicDist());
        return pol.area
    
    @property
    def centroid(self):
        pol = Polygon(self.graphicDist());
        return self.distribution[-1, 0] - pol.xcentroid
        