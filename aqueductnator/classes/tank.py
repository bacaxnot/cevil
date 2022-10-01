#internal libraries
from classes.node import Node

class Tank(Node):
    '''
    Generic class for Tank object.

    Arguments:
    - indx: Tank index (take in count also Node indices)
    - h: Heigth [m]
    - xq: External flow given (+) or extracted (-).
    '''
    def __init__(self,  indx: int, 
                        h: float = 0,
                        xq: float = 0) -> None:
        super().__init__(indx, h, h, xq)