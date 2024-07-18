import numpy as np
import matplotlib.pyplot as plt





def valid_vortex(S_past, dx, dy, i, j, r):
    x, y = dx*i, dy*j
    x_center, y_center = dx*S_past.shape[0]/2, dy*S_past.shape[1]/2
    return (x - x_center)**2 + (y - y_center)**2 < r**2

def set_border(S_past, dx, dy, r):
    S_new = S_past.copy()
    for i in range(1,S_past.shape[0]-1):
        for j in range(1,S_past.shape[1]-1):
            if not valid_vortex(S_past, dx, dy, i, j, r):
                neighbors = [S_past[i+1, j], S_past[i-1, j], S_past[i, j+1], S_past[i, j-1]]
                neighbors = [n for n in neighbors if n != 0]
                if len(neighbors) > 0:
                    S_new[i, j] = np.mean(neighbors)
                else:
                    S_new[i, j] = 0
    return S_new

def clear_outside(S_past, dx, dy, r):
    S_new = S_past.copy()
    for i in range(1,S_past.shape[0]-1):
        for j in range(1,S_past.shape[1]-1):
            if not valid_vortex(S_past, dx, dy, i, j, r):
                S_new[i, j] = 0
    return S_new

def PermEff(S):
        lamb = 0.52#ajustavel, valor de lambda 
        krg = 0.7737#ajustavel, valor a permeabilidade inicial do gas
        krw = 0.2007#ajustavel, valor a permeabilidade inicial da agua
        Swc = 0.10 #ajustavel, valor da saturação da agua conata no ambiente (menor valor de agua q pode existir)
        Sgr = 0.0 #fixo, valor da saturação do ar no ambiente, pode ser maior que 0, mas vamos deixar assim msm
        if S > Swc and S <= 1:
         Swe = (S-Swc)/(1-Swc-Sgr)
        elif S <= Swc:
         Swe = Swc
        else:
         Swe = 1
        #Swe = (S-Swc)/(1-Swc-Sgr)
        # Swc = 0.99
        # Sgr = 0.0
        # Swe = (S-Swc)/(1-S-Sgr)
        # if Swe < 0:
        #   Swe = 0
        k_w = krw*Swe**lamb
        k_g = krg*(1-Swe)**(3+(2/lamb))
        return k_w,k_g

def Fw(S_past):
    mrf = 1.0 # ajustavel, 1 pra agua e mrf>1 para outros tipos de substancias.
    muw = 1.0 # densidade da agua em g/ml
    mug =  0.0000172 # densidade do vapor de agua em g/ml
    old_F = np.zeros((S_past.shape[0], S_past.shape[1]))
    for i in range(1, S_past.shape[0]-1):
        for j in range(1, S_past.shape[1]-1):
            kw1, kg1 = PermEff(S_past[i,j])
            lambw = (kw1)/(muw)
            lambg = (kg1)/(mug*mrf)
            old_F[i,j] = (lambw)/(lambw+lambg)
        
    ## COLOCAR AQUI O CODIGO PARA CALCULAR FW
    return old_F.copy()

def up_S(S_past, k, vx, vy, dt, dx, dy, r):
    old_F = Fw(S_past)
    S_new = np.zeros_like(S_past)
    for i in range(1, S_past.shape[0]-1):
        for j in range(1, S_past.shape[1]-1):

                d2S_dx2 = (S_past[i+1, j] - 2*S_past[i, j] + S_past[i-1, j]) / (dx**2)
                d2S_dy2 = (S_past[i, j+1] - 2*S_past[i, j] + S_past[i, j-1]) / (dy**2)
                dF_dx = (old_F[i+1, j] - old_F[i-1, j]) / (2*dx)
                dF_dy = (old_F[i, j+1] - old_F[i, j-1]) / (2*dy)

                if valid_vortex(S_past, dx, dy, i, j, r):
                    S_new[i, j] = k * (d2S_dx2 + d2S_dy2) - vx * dF_dx - vy * dF_dy
                    S_new[i, j] = S_past[i, j] + S_new[i, j] * dt
    return S_new

max_T, max_X, max_Y, r = 500, 100, 100, 40
dt, dx, dy = 1, 1, 1
vx, vy = 0.012, 0.012
k = 0.1

S = np.zeros((int(max_T/dt), int(max_X/dx), int(max_Y/dy)))
S[0, 40:60, 15:40] = 1

for t in range(1, S.shape[0]):
    S[t-1] = set_border(S[t-1], dx, dy, r)
    S[t] = up_S(S[t-1], k, vx, vy, dt, dx, dy, r)
    S[t-1] = clear_outside(S[t-1], dx, dy, r)
    S[t, 40:60, 15:40] = 1

import imageio
images = []
for i in range(S.shape[0]):
    plt.imshow(S[i], cmap='viridis')
    x_center, y_center = S.shape[1]/2, S.shape[2]/2
    circle = plt.Circle((x_center, y_center), r, color='r', fill=False)
    plt.gca().add_artist(circle)
    plt.title(f'Time = {i*dt}')
    plt.axis('off')
    plt.savefig('porosity.png')
    images.append(imageio.imread('porosity.png'))
imageio.mimsave('porosity.gif', images)

