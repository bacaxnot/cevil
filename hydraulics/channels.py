#LIBRERIAS EXTERNAS
import numpy as np
from abc import ABC, abstractmethod
#LIBRERIAS PROPIAS
from sections import *

#BASE CLASS
class Channel(ABC):
    """
    Abstract class for any kind of Channel.
    
    - Primitive Attributes:
        - flow = flow rate [L^3/t].
        - section = section associated to channel.
        - coriolis = Coriolis Coefficient.
    - Derivated Attributes:
        - 
    """
    #CONSTRUCTOR
    def __init__(self, Section : Section,
                       Coriolis : bool = False,
                       Inclination : float = 0) -> "Channel":
        self.section = Section;
        self.omega = Inclination;
        self.coriolis = Coriolis; 
        pass
    #ATTRIBUTES
    @property
    def flow(self):
        return self.__flow
    @flow.setter
    def flow(self, flow):
        self.__flow = flow
    @property
    def coriolis(self):
        return self.__coriolis
    @coriolis.setter
    def coriolis(self, boolean):
        if not boolean:
            self.__coriolis = 1
        else:
            #Missing implementation
            pass

#CLASS INSTANCES
class OpenChannel(Channel):
    pass
