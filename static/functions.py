import numpy as np

#FUNCION DE SINGULARIDAD
'''
x: Discretización de dominio X
a: Punto de aplicación de carga [Izq. a Der.]
n: Grado de carga según EC.SINGULARIDAD.
'''
def sing(x,a,n):
    y = np.zeros_like(x)
    for i,xi in enumerate(x):
        y[i] = ((xi-a)**n, 0)[xi <= a] #Condicional
    return y
#MATRIZ DE TRANSFORMACION
'''
AN: Ángulo (rad) con respecto a X global [+ levogiro]
n: Cantidad de matrices de transformación internas
trans: Tipo de transformación (L2G:Local to Global, G2L:GLobal to Local)
'''
def MTrans(AN,n,trans):
    c = np.cos(AN) #Seno del ángulo
    s = np.sin(AN) #Coseno del ángulo
    T = np.zeros([3*n,3*n]) #Matriz de transformación n-dimensional
    for i in range(n):
        T[3*i:3*(i+1), 3*i:3*(i+1)] = [[c,-s,0],[s,c,0],[0,0,1]]
    return (T, np.transpose(T))[trans == "G2L"]
#MATRIZ DE RIGIDEZ LOCAL
'''
A: Area ST elemento
E: Modulo de Young
I: Inercia ST elemento
L: Longitud elemento
'''
def MRigL(A,E,I,L):
    Q = [A*E/L, 12*E*I/(L**3), E*I/L] #Constantes repetitivas
    K = np.array([[Q[0], 0, 0, -Q[0], 0, 0],\
         [0, Q[1], 6*Q[2]/L, 0, -Q[1], 6*Q[2]/L],\
         [0, 6*Q[2]/L, 4*Q[2], 0, -6*Q[2]/L, 2*Q[2]],\
         [-Q[0], 0, 0, Q[0], 0, 0],\
         [0, -Q[1], -6*Q[2]/L, 0, Q[1], -6*Q[2]/L],\
         [0, 6*Q[2]/L, 2*Q[2], 0, -6*Q[2]/L, 4*Q[2]]])
    return K
#MATRIZ DE RIGIDEZ GLOBAL
'''
AN: Ángulo (rad) con respecto a X [+ levogiro]
'''
def MRigG(A,E,I,L,AN):
    c = np.cos(AN) #Seno del ángulo
    s = np.sin(AN) #Coseno del ángulo
    Q = [A*E/L, 12*E*I/(L**3), E*I/L] #Constantes repetitivas
    K = np.array([[Q[0]*(c**2)+Q[1]*(s**2), s*c*(Q[0]-Q[1]), -s*(6*Q[2]/L), -(Q[0])*c**2-(Q[1])*s**2, -s*c*(Q[0]-Q[1]), -s*(6*Q[2]/L)],\
         [s*c*(Q[0]-Q[1]), (Q[0])*s**2+(Q[1])*c**2, c*(6*Q[2]/L), -s*c*(Q[0]-Q[1]), -(Q[0])*s**2-(Q[1])*c**2, c*(6*Q[2]/L)],\
         [-s*(6*Q[2]/L), c*(6*Q[2]/L), 4*Q[2], s*(6*Q[2]/L), -c*(6*Q[2]/L), (2*Q[2])],\
         [-Q[0]*(c**2)-Q[1]*(s**2), -s*c*(Q[0]-Q[1]), s*(6*Q[2]/L), (Q[0])*c**2+(Q[1])*s**2, s*c*(Q[0]-Q[1]), s*(6*Q[2]/L)],\
         [-s*c*(Q[0]-Q[1]), -Q[0]*(s**2)-Q[1]*(c**2), -c*(6*Q[2]/L), s*c*(Q[0]-Q[1]), Q[0]*(s**2)+Q[1]*(c**2), -c*(6*Q[2]/L)],\
         [-s*(6*Q[2]/L), c*(6*Q[2]/L), 2*Q[2], s*(6*Q[2]/L), -c*(6*Q[2]/L), 4*Q[2]]])
    return K
#FUERZAS DE EMPOTRAMIENTO PERFECTO (EJES LOCALES)
'''
W: Magnitud de carga
a: Inicio de aplicación de carga [Izq. a Der.]
b: Fin de aplicación de carga [Izq. a Der.]
L: Longitud elemento
Tipo: Tipo de carga
'''
def FEFL(Tipo,W,L,a,b=0):
    if Tipo == 11: #Carga Puntual Longitudinal
        M2 = 0;
        M1 = 0;
        R2Y = 0;
        R1Y = 0;
        R2X = -(W*a)/L;
        R1X = -W - R2X;
    if Tipo == 12: #Carga Puntual Transversal
        W = -W; #Convención
        M2 = -(W*a**2*(L - a))/L**2;
        M1 = (W*a*(L - a)**2)/L**2;
        R2Y = (W*a - M1 - M2)/L;
        R1Y = W - R2Y;
        R2X = 0;
        R1X = 0;
    elif Tipo == 13: #Momento Puntual
        M2 = (W*a*(2*L - 3*a))/L**2;
        M1 = -(W*(L**2 - 4*L*a + 3*a**2))/L**2;
        R2Y = (-W - M1 - M2)/L;
        R1Y = -R2Y;
        R2X = 0;
        R1X = 0;
    elif Tipo == 21: #Carga Rectangular Longitudinal
        M2 = 0;
        M1 = 0;
        R2Y = 0;
        R1Y = 0;
        R2X = (W*(a**2 - b**2))/(2*L);
        R1X = -W*(b - a) - R2X;
    elif Tipo == 22: #Carga Rectangular Transversal
        W = -W; #Convención
        M2 = -(3*W*a**4 - 3*W*b**4 - 4*L*W*a**3 + 4*L*W*b**3)/(12*L**2);
        M1 = -(3*W*a**4 - 3*W*b**4 + 6*L**2*W*a**2 - 6*L**2*W*b**2 - 8*L*W*a**3 + 8*L*W*b**3)/(12*L**2);
        R2Y = (W*(b**2 - a**2)/2 - M1 - M2)/L;
        R1Y = W*(b - a) - R2Y;
        R2X = 0;
        R1X = 0;
    elif Tipo == 23: #Momento Rectangular
        M2 = (W*a**3 - W*b**3 - L*W*a**2 + L*W*b**2)/L**2;
        M1 = (W*(a - b)*(a*b - 2*L*b - 2*L*a + L**2 + a**2 + b**2))/L**2;
        R2Y = (-W*(b - a) - M1 - M2)/L;
        R1Y = - R2Y;
        R2X = 0;
        R1X = 0;
    elif Tipo == 31: #Carga Triangular Creciente Longitudinal
        M2 = 0;
        M1 = 0;
        R2Y = 0;
        R1Y = 0;
        R2X = (W*(a*b + a**2 - 2*b**2))/(6*L);
        R1X = -W*(b - a)/2 - R2X;
    elif Tipo == 32: #Carga Triangular Creciente Transversal
        W = -W; #Convención
        M2 = -(W*(a - b)*(9*a*b**2 - 15*L*b**2 - 5*L*a**2 + 6*a**2*b + 3*a**3 + 12*b**3 - 10*L*a*b))/(60*L**2);
        M1 = -(W*(a - b)*(10*L**2*a - 10*L*a**2 - 30*L*b**2 + 20*L**2*b + 9*a*b**2 + 6*a**2*b + 3*a**3 + 12*b**3 - 20*L*a*b))/(60*L**2);
        R2Y = (W*(b - a)*(a + 2*b)/6 - M1 - M2)/L;
        R1Y = W*(b - a)/2 - R2Y;
        R2X = 0;
        R1X = 0;
    elif Tipo == 33: #Momento Triangular Creciente
        M2 = (W*(a - b)*(6*a*b - 8*L*b - 4*L*a + 3*a**2 + 9*b**2))/(12*L**2);
        M1 = (W*(a - b)*(6*a*b - 16*L*b - 8*L*a + 6*L**2 + 3*a**2 + 9*b**2))/(12*L**2);
        R2Y = (-W*(b - a)/2 - M1 - M2)/L;
        R1Y = - R2Y;
        R2X = 0;
        R1X = 0;
    elif Tipo == 41: #Carga Triangular Decreciente Longitudinal
        M2 = 0;
        M1 = 0;
        R2Y = 0;
        R1Y = 0;
        R2X = -(W*(a*b - 2*a**2 + b**2))/(6*L);
        R1X = -W*(b - a)/2 - R2X;
    elif Tipo == 42: #Carga Triangular Decreciente Transversal
        W = -W; #Convención
        M2 = -(W*(a - b)*(6*a*b**2 - 5*L*b**2 - 15*L*a**2 + 9*a**2*b + 12*a**3 + 3*b**3 - 10*L*a*b))/(60*L**2);
        M1 = -(W*(a - b)*(20*L**2*a - 30*L*a**2 - 10*L*b**2 + 10*L**2*b + 6*a*b**2 + 9*a**2*b + 12*a**3 + 3*b**3 - 20*L*a*b))/(60*L**2);
        R2Y = (W*(b - a)*(2*a + b)/6 - M1 - M2)/L;
        R1Y = W*(b - a)/2 - R2Y;
        R2X = 0;
        R1X = 0;
    elif Tipo == 43: #Momento Triangular Decreciente
        M2 = (W*(a - b)*(6*a*b - 4*L*b - 8*L*a + 9*a**2 + 3*b**2))/(12*L**2);
        M1 = (W*(a - b)*(6*a*b - 8*L*b - 16*L*a + 6*L**2 + 9*a**2 + 3*b**2))/(12*L**2);
        R2Y = (-W*(b-a)/2 - M1 - M2)/L;
        R1Y = - R2Y;
        R2X = 0;
        R1X = 0;
    
    return np.array([[R1X], [R1Y], [M1], [R2X], [R2Y], [M2]]) #Vector FEF
#FUERZAS DE EMPOTRAMIENTO PERFECTO (L2G)
'''
AN: Ángulo (rad) con respecto a X [+ levogiro]
'''
def FEFG(AN,Tipo,W,L,a,b=0):
    FEF = FEFL(Tipo,W,L,a,b) #FEF locales
    T = MTrans(AN,2,"L2G") #Matriz de transformación
    return T@FEF #FEF globales

