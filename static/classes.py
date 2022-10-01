import numpy as np
import matplotlib.pyplot as plt

#MATERIAL OBJECTS
class Material:
    '''
    Material class for any type of Element.
    
    - Primitive Attributes:
        - weigth : Volumetric Weigth (W)
        - modulusYoung: Young Modulus (E)
        - modulusPoisson: Poisson Modulus (v)
    - Derivated Attributes:
        - modulusShear: Shear Modulus (G)
    '''
    def __init__(self, W: float = 24,
                       E : float = 24e+3,
                       v : float = 0) -> "Material":
        self.weigth = W;
        self.modulusYoung = E;
        self.modulusPoisson = v;
    @property
    def modulusShear(self):
        return self.modulusYoung/(2*(1+self.modulusPoisson))
#CROSS SECTION OBJECTS
class CrossSection:
    '''
    Base class for any type of CrossSection of an Element.

    - Primitive Attributes:
        - Depends on the CrossSection subclass
    - Derivated Attributes:
        - area : Area associated to the CrossSection
        - inertia_z : Moment of Inertia around Z axis.
    '''
    def __init__(self) -> "CrossSection":
        pass
    @property
    def area(self):
        pass
    @property
    def inertia_z(self):
        pass
class SquareSection(CrossSection):
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
#NODE OBJECTS
class Node:
    '''
    Base class for any type of Node of an Element.

    - Primitive attributes:
        - x: Coordinate on X axis (Global),
        - y: Coordinate on Y axis (Global).
        - freeDeg: Freedom degrees associated to Node (Must be a boolean np.array: [[dX], [dY], [thetha]],
        where True equals to allowed degree, and False to not-allowed degree).
    - Derivated attributes:
        - restrDeg: Restricted freedom degreees associated to Node (Logical opposite to freeDeg).
    '''
    def __init__(self, x : float,
                       y : float) -> "Node":
        self.x = x;
        self.y = y;
        self.freeDeg = np.array([[True],[True],[True]]);
    @property
    def restrDeg(self):
        return np.logical_not(self.freeDeg);
#ELEMENT OBJECTS
class Element:
    '''
    Base class for any type of Element of a Structure.

    - Primitive Attributes:
        - iNode: Initial Node of the Element
        - fNode: Final Node of the Element
        - material: Material of the Element
        - section: CrossSection of the Element
    - Derivated Attributes:
        - stiffness: SMatrix of the Element
    '''
    def __init__(self, iN : Node,
                       fN : Node,
                       material : Material = Material(),
                       section : CrossSection = SquareSection()) -> "Element":
        self.iNode = iN;
        self.fNode = fN;
        self.material = material;
        self.section = section;

A = Node(0,0)
B = Node(1,1)
k = Element(A,B)
