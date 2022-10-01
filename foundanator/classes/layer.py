class Layer:
    '''
    ---
    Generic class for a layer of soil with its physical properties.

    Arguments:
    - indx: index of the layer. More depth equals higher index.
    - thick: thickness of the layer.
    - gamma: selfweigth of the layer.
    - phi: drenated friction angle.
    - c: cohesion.
    - saturated: true if the layer is saturated, false if not. 
    '''
    def __init__(self,  indx: int,
                        thick: float,
                        gamma: float,
                        phi: float,
                        c: float = 0,
                        saturated: bool = False) -> None:            
        self.indx = indx;
        self.thick = thick;
        self.gamma = gamma;
        self.phi = phi;
        self.c = c;
        self.ko = None;
        self.ka = None;
        self.kp = None;
        self.saturated = saturated;
        pass
