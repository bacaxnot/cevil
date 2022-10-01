#OUTER LIBRARIES

#INNER LIBRARIES

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