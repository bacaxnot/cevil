class Soil:
    '''
    ---
    Generic class of a soil composed by various layers.

    Arguments:
    - layers: list containing layer objects of the soil.
    - alpha: horizontal soil slope, from right to left.
    - beta: vertical soil slope, from left to right.
    - overload: magnitude of overload applied to the soil.
    '''
    def __init__(self,  layers: list,
                        alpha: float = 0,
                        beta: float = 90,
                        overload: float = 0) -> None:
        self.layers = layers;
        self.overload = overload;
        self.alpha = alpha;
        self.beta = beta;
        self.sortLayers()
        pass

    def sortLayers(self):
        self.layers.sort(key = lambda x: x.indx);
        pass