#external libraries
import numpy as np

#internal libraries
from classes.node import Node

class Pipe():
    '''
    Generic class for any kind of pipe.

    Arguments:
    - indx: Index of the element. If two pipes have the same indx, they'reconsidered as parallel.    
    - ni: Node object of the first point of the Pipe.
    - nf: Node object of the second point of the Pipe.
    - d: List containing the diameter and its units [value, 'units'] [m].
        - Supported units: 'in', 'mm', 'm'
    - l: Length of the Pipe [m]
    '''
    def __init__(self,  indx: int,
                        ni: Node,
                        nf: Node,
                        d: list,
                        l: float,
                        c: float = 0) -> None:
        #primary attributes
        self.indx = indx;
        self.ni = ni;
        self.nf = nf;
        #properties
        self.d = self.verifyUnits(d);
        self.l = l;
        self.c = c;
        self.q = 0;
        #status attributes
        self.isParallel = False;
        pass

    def verifyUnits(self,   list: list):
        if list[1].lower() == 'in':
            return list[0]*0.0254
        elif list[1].lower() == 'mm':
            return list[0]/1000
        elif list[1].lower() == 'm':
            return list[0]
        else:
            raise ValueError(f'Unsupported units for Pipe {self.indx}.')

    def addParallel(self,   d: list,
                            l: float):
        self.d.append(self.verifyUnits(d))
        self.l.append(l)
