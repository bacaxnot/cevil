#external libraries
import numpy as np

class Node:
    '''
    Generic class for any kind of node.

    Arguments:
    - indx: Node index
    - h: Heigth [m]
    - hp: Piezometric heigth [m]
    - xq: External flow given (+) or extracted (-).
    '''
    def __init__(self,  indx: int,
                        h: float = 0,
                        hp: float = 0,
                        xq: float = 0) -> None:
        self.indx = indx;
        self.h = h;
        self.hp = hp;
        self.xq = xq;
        pass