
class Footing:
    '''
    Generic footing parent class

    Arguments:
    - df: footing's depth [m].
    '''
    def __init__(self,  df:float) -> None:
        self.df = df;
        pass

class RectFooting(Footing):
    '''
    Generic footing parent class

    Arguments:
    - b: footing's base [m].
    - l: footing's length [m].
    '''
    def __init__(self,  df: float,
                        b: float,
                        l: float) -> None:
        super().__init__(df)
        self.b = b;
        self.l = l;
    pass

class CircFooting(Footing):
    def __init__(self,  df: float,
                        d: float) -> None:
        super().__init__(df)
        self.d = d;
    pass