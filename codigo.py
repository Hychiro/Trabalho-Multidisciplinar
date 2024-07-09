import numpy as np
import math
import matplotlib as plt

class PorositiyProblem():
    def __init__(self):
        self.krw0__ = None # ajustavel
        self.krg0__ = None # ajustavel
        self.lamb__ = None # ajustavel
        self.swc__ = None # ajustavel
        self.sw__ = None # vai variar na conta, mas é o valor inicial da saturação
        self.sg__ = None # constante, sg é o resultado do sw-swc se me lembro bem (saturação de liquido - saturação conata = saturação do gas) já q sgr pode ser considerado 0
        self.mrf__ = None # valor referente ao sufactante 
        self.phi__ = None # valor da porosidade
        self.volW__ = None # volume de agua dentro do experimento (resultado da massaFinal - massaInicial do experimento)
        self.volt__ = None # volume total do ambiente
        
        #Condicao inicial
        self.Sw_0 = 1 #fixo 
        #Condicao de Contorno
        self.sw_a = self.swc__ #gas  e espuma
        #self.sw_a = 1 # agua
    def settingEnviroment(self):
        
        self.h_x=0.01 #step de deslocamento em x
        self.h_y=0.01 #step de deslocamento em y
        self.h_t=0.01 #step de tempo em segundos
        self.xT = 100 #espaço total de deslocamento em x
        self.yT = 100 #espaço total de deslocamento em y
        self.timeT = 100 #tempo total para o deslocamento

        self.x = np.arange(0, self.xT, self.h_x)    
        self.y = np.arange(0, self.yT, self.h_y)
        self.t = np.arange(0, self.timeT, self.h_t)

        self.tamX = len(self.x) #dimensão do sistema
        self.tamY = len(self.y) #dimensão do sistema
        self.steps = len(self.t) #numero de passos de tempo
        self.sol_tempo=[] # primeira fase (agua)
        self.sol_tempo2=[] # segunda fase (ar ou espuma)

        self.Sw = np.zeros([self.tamX,self.tamY])#x,y
        self.Sg = np.zeros([self.tamX,self.tamY])#x,y
        
        for i in range(self.tamX):
            for j in range(self.tamY):
                self.Sw[i,j] = self.Sw_0
                self.Sw[i,j] = self.Sw_0
        self.sol_tempo.append(self.Sw)
        self.sol_tempo2.append(1-self.Sw)
        self.Sw_new=np.zeros(self.tam)

    def calculate(self):
        vx = 0
        vy = 0
        qx = (vx*self.ht)/(self.h_x*self.phi__)
        qy = (vy*self.ht)/(self.h_y*self.phi__)
        Og = 0 
        D = 0 # agua à 25º é 2.299·10−9 m2·s−1
        fw = np.zeros([self.tamX,self.tamY])#x,y
        listOfFw = []
        for i in range(self.tamX):
            for j in range(self.tamY):
                fw[i,j] = fw_(self.Sw[i,j], self.sg__, self.mrf__,self.krw0__,self.krg0__,self.lamb__,self.swc__)
        listOfFw.append(np.copy(fw))

        for k in range(1,self.steps):

            for i in range(1,self.tamX):
                for j in range(1,self.tamY):
                    self.Sw_new[i,j] = self.Sw[i,j]  - qx*(fw[i-1,j]  - fw[i,j] )  -qy*(fw[i,j-1]  - fw[i,j] ) - D*(((self.Sw[i+1,j] - 2*self.Sw[i,j] + self.Sw[i-1,j])/self.h_x)+((self.Sw[i,j+1] - 2*self.Sw[i,j] + self.Sw[i,j-1])/self.h_y)) - Og 
            self.Sw_new[0,0]=self.sw_a
            self.Sw = np.copy(self.Sw_new)
            self.sol_tempo.append(self.Sw)
            self.sol_tempo2.append(1-self.Sw)

            for i in range(0,self.tamX):
                for j in range(0,self.tamY):
                    fw[i,j] = fw_(self.Sw[i,j], self.sg__, self.mrf__,self.krw0__,self.krg0__,self.lamb__,self.swc__)
            listOfFw.append(np.copy(fw))        




    # saber se eles usam qual valor para fazer a conta do 

def fw_(sw,sg, mrf,krw0, krg0,lamb, swc):
    lambw = lambw_(sw,krw0,lamb,swc)
    lambt = lambw_(sw,krw0,lamb,swc)+lambg_(sg,mrf,krg0,lamb,swc,sw)
    return lambw/lambt

def swe_(sw,swc,sgr):
    return (sw - swc)/(1-swc-sgr)

def lambw_(sw,krw0,lamb,swc):
    muw = None # fixo
    krw = krw_(sw,krw0,lamb,swc)
    return (krw*sw)/muw

def lambg_(sg,mrf,krg0,lamb,swc,sw):
    mug = None # fixo
    krg = krg_(krg0,lamb,swc,sw)
    return (krg*sg)/(mug*mrf)

def krw_(sw,krw0,lamb,swc):
    sgr = None # fixo 
    swe = swe_(sw,swc,sgr)
    return krw0*(swe**lamb)

def krg_(sw,krg0,lamb,swc):
    sgr = None # fixo 
    swe = swe_(sw,swc,sgr)
    return krg0*(1-swe**(3-(2/lamb)))

def phi_(volW,volT):
    return volW/volT

