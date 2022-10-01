
class System():
    '''
    Generic class for any Pipes System.

    Arguments:
    - pipes: List of Pipe elements of the system.
    '''
    def __init__(self,  pipes:list) -> None:
        self.pipes = pipes;
        pass

    def sortPipes(self):
        '''
        Just a method to sort the Pipes using their index.
        '''
        self.pipes.sort(key = lambda x: x.indx);
        pass

    def defC(self,  c: float):
        '''
        Sets uniform C value to all Pipe elements.
        '''
        for pipe in self.pipes:
            pipe.c = c;
    
    def solveFlows(self):
        '''
        Find correspondent flows on Pipes in the
        given System using Hazen Williams head loss equation.
        '''
        pass