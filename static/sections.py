#OUTER LIBRARIES
from abc import ABC, abstractmethod
#INNER LIBRARIES

#CROSS SECTION OBJECTS
class CrossSection(ABC):
    """
    Base class for any type of CrossSection of an Element.

    - Primitive Attributes:
        - Depends on the CrossSection subclass
    - Derivated Attributes:
        - area : Area associated to the CrossSection
        - inertia_z : Moment of Inertia around Z axis.
    """
    def __init__(self) -> "CrossSection":
        pass
    @property
    @abstractmethod
    def area(self):
        pass
    @property
    @abstractmethod
    def inertia_z(self):
        pass
    @property
    @abstractmethod
    def inertia_y(self):
        pass
#CLASS INSTANCES
class SquareSection(CrossSection):
    """
    Base class for any type of CrossSection of an Element.

    - Primitive Attributes:
        - Depends on the CrossSection subclass
    - Derivated Attributes:
        - area : Area associated to the CrossSection
        - inertia_z : Moment of Inertia around Z axis.
    """
    def __init__(self, b : float = 0.2,
                       h : float = 0.2) -> "CrossSection":
        self.base = b;
        self.heigth = h;
    @property
    def area(self):
        return self.base*self.heigth
    @property
    def inertia_z(self):
        return self.base*(self.heigth^3)/12