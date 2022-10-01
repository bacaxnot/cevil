#VIGANATOR 3000 V2.0
# %%
#LIBRERÍAS
import numpy as np
import matplotlib.pyplot as plt
import functions as f
import os

os.system("cls")
# %%
#DECLARACION DE VARIABLES
#Propiedades físico-mecánicas
b = 0.2; h = 0.2;
E = 2000; #Módulo de Young
A = b*h; #Área
I = b*h**3/12; #Inercia
#Geometría: Grados de Libertad [X, Y, Rotación]
NODE = [[3,2,True,False,True],[0,0,False,False,True],[5,2,False,False,True]]; #Nodos: PosX, PosY, RestX, RestY, RestRot
ELM = np.array([[0,1],[1,2]]); #Elementos
L = np.empty([0,]); #Longitudes
AN = np.empty([0,]); #Ángulos (rad) de inclinación en X: Dextrogiro [+]
nn = len(NODE); #Número de nodos
ne = ELM.shape[0]; #Número de elementos
#Cargas: Arriba-Derecha-Levogiro [+]; Abajo-Izquierda-Dextrogiro [-]
 #Dirección: [1:X, 2:Y, 3:M]
CPn = np.zeros([nn,3])#Puntuales (Node): [Fx, Fy, M]
CPe = np.array([[1, -20, 1, 12]]); #Puntuales (Elm): [Elemento, Magnitud, PosX, Tipo/Dirección]
CRe   = np.array([[0, -20, 1, 2, 22]]); #Rectangulares (Elm): [Elemento, Magnitud, PosXi, PosXf, Tipo/Dirección] [[0, -20, 1, 2, 22]]
CTCe = np.empty([0,2]); #Triangulares crecientes (Elm): [Elemento, Magnitud, PosXi, PosXf, Tipo/Dirección]
CTDe = np.empty([0,2]); #Triangulares decrecientes (Elm): [Elemento, Magnitud, PosXi, PosXf, Tipo/Dirección]
#Matricial
GL = np.empty([3*nn,1]) #Grados de libertad (1:Permitidos, 0:Restringidos)
Ki = np.empty([0,6,6]) #Matrices de rigidez individuales (S.Global)
K = np.zeros([3*nn,3*nn]) #Matriz de rigidez ensamblada (S.Global)
FEFi = np.zeros([ne,6,1]) #FEF individuales (S.Global)
FEF = np.zeros([3*nn,1]) #Vector de FEF ensambladas (S.Global)
dx = np.zeros([3*nn,1]) #Vector de desplazamientos (S.Global)
#Reacciones
Rn = np.zeros([nn,3]); #Reacciones (Node): [Fx, Fy, M]
Re = np.zeros([ne,6]) #Reacciones (Elm): [Fx1, Fy1, M1, Fx2, Fy2, M2]
#Funciones de fuerzas internas
X = [0]*ne; #Discretización X
fW = [0]*ne; #Carga
fV = [0]*ne; #Cortante
fM = [0]*ne; #Momento
fN = [0]*ne; #Axial
# %%
#CALCULO DE PROPIEDADES DE ELEMENTOS
 #Todas las propiedades y fuerzas se ordenan según orden de elementos
NODE = np.array(sorted(NODE, key = lambda d : d[0])); #Ordenar nodos según PosX
 #Iterando Elementos
for i,n in enumerate(ELM):
    L = np.append(L,np.linalg.norm(NODE[n[1],0:2] - NODE[n[0],0:2])); #Longitudes
    AN = np.append(AN,np.arcsin((NODE[n[1],1]-NODE[n[0],1])/L[i])); #Ángulos
    Ki = np.append(Ki,[f.MRigL(A,E,I,L[i])],axis=0) if AN[i] == 0 else np.append(Ki,[f.MRigG(A,E,I,L[i],AN[i])],axis=0) #K Individuales
# %%
#CALCULO DE FUERZAS DE EMPOTRAMIENTO PERFECTO (S.GLOBAL)
 #Iterando Puntuales
for n in CPe:
    FEFi[n[0]] += f.FEFL(n[3],n[1],L[n[0]],n[2]) if AN[n[0]] == 0 else f.FEFG(AN[n[0]],n[3],n[1],L[n[0]],n[2])
 #Iterando Rectangulares
for n in CRe:
    FEFi[n[0]] += f.FEFL(n[4],n[1],L[n[0]],n[2],n[3]) if AN[n[0]] == 0 else f.FEFG(AN[n[0]],n[4],n[1],L[n[0]],n[2],n[3])
 #Iterando Triangulares Crecientes
for n in CTCe:
    FEFi[n[0]] += f.FEFL(n[4],n[1],L[n[0]],n[2],n[3]) if AN[n[0]] == 0 else f.FEFG(AN[n[0]],n[4],n[1],L[n[0]],n[2],n[3])
 #Iterando Triangulares Decrecientes
for n in CTDe:
    FEFi[n[0]] += f.FEFL(n[4],n[1],L[n[0]],n[2],n[3]) if AN[n[0]] == 0 else f.FEFG(AN[n[0]],n[4],n[1],L[n[0]],n[2],n[3])
# %%
#ENSAMBLAJE DE MATRICES (S.GLOBAL)
for i,n in enumerate(ELM):
    K[3*n[0]:3*(n[0]+1), 3*n[0]:3*(n[0]+1)] += Ki[i, 0:3, 0:3] #K11
    K[3*n[0]:3*(n[0]+1), 3*n[1]:3*(n[1]+1)] += Ki[i, 0:3, 3:6] #K12
    K[3*n[1]:3*(n[1]+1), 3*n[0]:3*(n[0]+1)] += Ki[i, 3:6, 0:3] #K21
    K[3*n[1]:3*(n[1]+1), 3*n[1]:3*(n[1]+1)] += Ki[i, 3:6, 3:6] #K22
    FEF[3*n[0]:3*(n[0]+1), :] += FEFi[i, 0:3, :] #FEF1
    FEF[3*n[1]:3*(n[1]+1), :] += FEFi[i, 3:6, :] #FEF2
# %%
#SOLUCION MATRICIAL DE LA ESTRUCTURA (S.GLOBAL)
GL = np.array([x==1 for x in NODE[:, 2:5].flatten()]) #Grados de Libertad (QUITAR BUCLE EN V.FINAL)
GLr = np.logical_not(GL); #Grados de Libertad restringidos
dx[GL] = np.linalg.solve(K[np.ix_(GL,GL)], (CPn.reshape((3*nn,1)) - FEF)[GL]) #Desplazamientos libres
Rn[GLr.reshape((nn,3))] = ((K[np.ix_(GLr,GL)] @ dx[GL]) + FEF[GLr]).flatten() #Reacciones (Node)
# %%
#CALCULO DE FUERZAS NODALES INTERNAS POR ELEMENTO (S.GLOBAL)
for i,n in enumerate(ELM):
    if AN[i] == 0: #Elementos no inclinados
        Re[i] = (Ki[i] @ np.concatenate( (dx[3*n[0]:3*(n[0]+1)], dx[3*n[1]:3*(n[1]+1)]) ) + FEFi[i]).flatten()
    else: #Elementos inclinados
        Re[i] = (f.MTrans(AN[i],2,"G2L") @ (Ki[i] @ np.concatenate( (dx[3*n[0]:3*(n[0]+1)], dx[3*n[1]:3*(n[1]+1)]) ) + FEFi[i]) ).flatten()
# %%
#DIAGRAMAS DE CARGA POR ELEMENTO (S.LOCAL)
'''TODO: Optimizar según ángulos de inclinación y Reacciones que sean 0
         Revisar por qué no cierran algunos diagramas
         Revisar diagramas de cortante
         Se pueden ordenar cargas según elementos'''
 #Discretización de elementos
for i,n in enumerate(ELM):
    X[i] = np.arange(0, L[i]+0.002, 0.001)
 #Iterando Puntuales
for n in CPe:
    if n[3] == 11: #Fuerza longitudinal
        fN[n[0]] += -n[1]*f.sing(X[n[0]], n[2], 0)
    elif n[3] == 12: #Fuerza transversal
        fV[n[0]] += n[1]*f.sing(X[n[0]], n[2], 0)
        fM[n[0]] += n[1]*f.sing(X[n[0]], n[2], 1)
    elif n[3]  == 13: #Momento
        fM[n[0]] += -n[1]*f.sing(X[n[0]], n[2], 0)
 #Iterando Rectangulares
for n in CRe:
    if n[4] == 21: #Fuerza longitudinal
        fN[n[0]] += -n[1]*(f.sing(X[n[0]], n[2], 1) - f.sing(X[n[0]], n[3], 1))
    elif n[4] == 22: #Fuerza transversal
        fV[n[0]] += n[1]*(f.sing(X[n[0]], n[2], 1) - f.sing(X[n[0]], n[3], 1))
        fM[n[0]] += n[1]*(f.sing(X[n[0]], n[2], 2) - f.sing(X[n[0]], n[3], 2))/2
    elif n[4]  == 23: #Momento
        fM[n[0]] += -n[1]*(f.sing(X[n[0]], n[2], 1) - f.sing(X[n[0]], n[3], 1))
 #Iterando Triangulares Crecientes
for n in CTCe:
    k = n[1]/(n[3] - n[2]) #Pendiente
    if n[4] == 21: #Fuerza longitudinal
        fN[n[0]] += -n[1]*(f.sing(X[n[0]], n[2], 1) - f.sing(X[n[0]], n[3], 1))
    elif n[4] == 22: #Fuerza transversal
        fV[n[0]] += n[1]*(f.sing(X[n[0]], n[2], 1) - f.sing(X[n[0]], n[3], 1))/(2*(n[3]-n[2]))
        fM[n[0]] += n[1]*(f.sing(X[n[0]], n[2], 2) - f.sing(X[n[0]], n[3], 2))/2
    elif n[4]  == 23: #Momento
        fM[n[0]] += -n[1]*(f.sing(X[n[0]], n[2], 1) - f.sing(X[n[0]], n[3], 1))
 #Iterando Triangulares Decrecientes
for n in CTDe:
    k = n[1]/(n[3] - n[2]) #Pendiente
    if n[4] == 21: #Fuerza longitudinal
        fN[n[0]] += -n[1]*(f.sing(X[n[0]], n[2], 1) - f.sing(X[n[0]], n[3], 1))
    elif n[4] == 22: #Fuerza transversal
        fV[n[0]] += n[1]*(f.sing(X[n[0]], n[2], 1) - f.sing(X[n[0]], n[3], 1))
        fM[n[0]] += n[1]*(f.sing(X[n[0]], n[2], 2) - f.sing(X[n[0]], n[3], 2))/2
    elif n[4]  == 23: #Momento
        fM[n[0]] += -n[1]*(f.sing(X[n[0]], n[2], 1) - f.sing(X[n[0]], n[3], 1))
 #Iterando Reacciones
for i,n in enumerate(Re):
    #Fuerzas longitudinales
    fN[i] += -n[0]*f.sing(X[i], 0, 0) -n[3]*f.sing(X[i], L[i], 0)
    #Fuerzas transversales
    fV[i] += n[1]*f.sing(X[i], 0, 0) +n[4]*f.sing(X[i], L[i], 0)
    fM[i] += n[1]*f.sing(X[i], 0, 1) +n[4]*f.sing(X[i], L[i], 1)
    #Momentos
    fM[i] += -n[2]*f.sing(X[i], 0, 0) -n[5]*f.sing(X[i], L[i], 0)
# %%
#GRAFICA DE DIAGRAMAS
fig, ax = plt.subplots(3,ne)
 #Axial
ax[0,0].set_title("Axial 1")
ax[0,0].plot(X[0],np.zeros_like(X[0]),X[0],fN[0])
ax[0,1].set_title("Axial 2")
ax[0,1].plot(X[1],np.zeros_like(X[1]),X[1],fN[1])
 #Cortante
ax[1,0].set_title("Cortante 1")
ax[1,0].plot(X[0],np.zeros_like(X[0]),X[0],fV[0])
ax[1,1].set_title("Cortante 2")
ax[1,1].plot(X[1],np.zeros_like(X[1]),X[1],fV[1])
 #Momento
ax[2,0].set_title("Momento 1")
ax[2,0].plot(X[0],np.zeros_like(X[0]),X[0],fM[0])
ax[2,1].set_title("Momento 2")
ax[2,1].plot(X[1],np.zeros_like(X[1]),X[1],fM[1])
# %%
