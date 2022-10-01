#external libraries
import numpy as np

class Polygon():
    def __init__(self,  vertices:np.ndarray) -> None:
        self.vertices = np.append(vertices, [vertices[0]], axis = 0)
        pass

    @property    
    def area(self):
        '''
        Method that returns the area of a given polygon by coordinates.
        '''
        xy = self.vertices;
        n = len(xy) - 1;
        area = 0;
        for i in range(n):
            area += xy[i, 0] * xy[i+1, 1] - xy[i+1, 0] * xy[i, 1];
        return 1/2 * np.abs(area)

    @property
    def xcentroid(self):
        '''
        Method that returns the centroid along the first axis of a given polygon by coordinates.
        '''
        xy = self.vertices;
        n = len(xy) - 1;
        centroid = 0;
        for i in range(n):
            centroid += (xy[i, 0] + xy[i+1, 0])*(xy[i, 0] * xy[i+1, 1] - xy[i+1, 0] * xy[i, 1]);
        area = self.area
        return 1/(6 * area) * np.abs(centroid)