#internal libraries
from classes.system import System
from methods import hazenw as hw
#external libraries
from scipy.optimize import fsolve
from numpy import isclose

class Mesh(System):
    '''
    Generic class for a Mesh System.

    Arguments:
    - pipes: List of Pipe elements of the system.
    '''
    def __init__(self, pipes: list) -> None:
        super().__init__(pipes)

    def losses(self):
        '''
        Calculate losses inside mesh system (clockwise?)
        '''
        hf = 0;
        for i, pipe in enumerate(self.pipes):
            loss = hw.hf(pipe.q, pipe.l, pipe.d, pipe.c);
            #evaluate first pipe
            if i == 0:
                hf += loss;
            #checking continuity between points
            else:
                prvPipe = self.pipes[i-1];
                #case: pipe is in the rigth flow-direction
                if pipe.ni == prvPipe.nf:
                    hf += loss;
                    pass
                #case: pipe is in the opposite flow-direction
                elif pipe.nf == prvPipe.nf:
                    hf -= loss;
                    pass
                #case: wtf, there's no continuity between pipes
                else:
                    raise ValueError(f'No continuity between Pipes {i-1} & {i}.')
            pass
        #finished iterations
        return hf

    def solveFlows(self):
        '''
        Find correspondent flows on Pipes in Mesh System using Hazen Williams head loss equation.
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