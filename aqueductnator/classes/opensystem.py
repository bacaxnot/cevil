#internal libraries
from classes.system import System
from methods import hazenw as hw
#external libraries
from scipy.optimize import fsolve
from numpy import isclose

class OpenSystem(System):
    '''
    Generic class for an Open Pipes System.

    Arguments:
    - pipes: List of Pipe elements of the system.
    '''
    def __init__(self, pipes: list) -> None:
        super().__init__(pipes)
        self.sortPipes()
        pass

    def eqDiameter(self):
        pass

    def solveFlows(self):
        '''
        Find correspondent flows on Pipes in Open System using Hazen Williams head loss equation.
        '''
        #available energy (difference in piezometric heigth between first and last element)
        dh = self.pipes[0].ni.hp - self.pipes[-1].nf.hp;
        #defining equations system
        def functions(q):
            f = [];
            fhf = - dh;
            for i, pipe in enumerate(self.pipes):
                #continuity control
                if i == 0:
                    pass
                else:
                    f.append(q[i-1] - q[i] + pipe.ni.xq)
                #head loss control
                fhf += hw.hf(q[i], pipe.l, pipe.d, pipe.c)
            f.append(fhf)
            return f
        #solving system    
        q = fsolve(functions, len(self.pipes)*[1])
        #checking solution
        isSolution = isclose(functions(q), len(self.pipes)*[0])
        #assigning flow to each pipe
        if all(isSolution):
            i = 0;
            for pipe in self.pipes:
                pipe.q = q[i];
                i += 1
            return 'Success'
        else:
            raise ValueError("Couldn't solve the system.")
