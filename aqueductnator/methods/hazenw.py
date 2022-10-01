'''
Series of functions using Hazen-Williams theory.

Units:
- flow (q) [m3/s]
- hf  [m]
- l [m]
- diameter (d) [m]

'''
def flow(   hf:float,
            l:float,
            d:float,
            c:float):
    q = c * (hf * d**4.87 / (10.67 * l)) ** (1/1.85);
    return q

def hf( q:float,
        l:float,
        d:float,
        c:float):
    if q < 0:
        hf = -10.67 * l * (-q/c)**1.85 / (d**4.87);
    else:
        hf = 10.67 * l * (q/c)**1.85 / (d**4.87);
    return hf

def diameter(   q:float,
                l:float,
                hf:float,
                c:float):
    d = (10.67 * l * (q/c)**1.85 / hf) ** (1/4.87);
    return d
