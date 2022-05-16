# -*- coding: utf-8 -*-
from math import pi,sin
import numpy as np
import matplotlib.pyplot as plt
import random 
import copy
# import logging
# logging.basicConfig(level=logging.DEBUG)
# # logging.basicConfig(level=logging.CRITICAL)
# logger = logging.getLogger('main')
from observer import *

class Generator  :
    def __init__(self,name="signal",mag=1.0,freq=1.0,phase=0.0,harmonics=1):
        Subject.__init__(self)
        self.name=name
        self.signal=[]
        self.mag,self.freq,self.phase=mag,freq,phase
        self.harmonics=harmonics
        self.samples=1000
        self.steps=5
    def __repr__(self):
        return "<Generator(mag:{}, freq:{}, phase:{})>".format(self.mag,self.freq,self.phase)

    def get_name(self):
        return self.name
    def set_name(self,name):
        self.name=name
    def get_signal(self):
        # signal=copy.copy(self.signal)
        return self.signal

    def get_magnitude(self):
        return self.mag
    def set_magnitude(self,mag):
        self.mag=mag
    def get_frequency(self):
        return self.freq
    def set_frequency(self,freq):
        self.freq=freq
    def get_phase(self):
        return self.phase
    def set_phase(self,phase):
        self.phase=phase
    def get_samples(self):
        return self.samples
    def set_samples(self,samples):
        self.samples=samples
    def get_steps(self):
        return steps
    def set_steps(self,steps):
        self.steps=steps

    def vibration(self,t):
        a,f,p=self.mag,self.freq,self.phase
        sum=0
        for h in range(1,self.harmonics+1) :
            sum=sum+(a*1.0/h)*sin(2*pi*(f*h)*t-p)
        return sum

    def generate(self):
        del self.signal[0:]
        period=2
        echantillons=range(int(self.samples)+1)
        Tech=period/self.samples
        for t in echantillons :
            self.signal.append([t*Tech,self.vibration(t*Tech)])
        return self.signal
    def delete(self):
        del self.signal[0:]
 


class PreyPredator :
    def __init__(self,alpha=0.8,beta=0.4,gamma=0.6,delta=0.2,preys=3,predators=5) :
        Subject.__init__(self)
        self.a,self.b,self.g,self.d=alpha,beta,gamma,delta
        # self.a,self.b,self.g,self.d=1.5,0.05,0.48,0.05
        self.x,self.y=preys,predators
        self.population=[]
        self.start,self.stop=0.0,100.0
        self.samples=1000

    def preys_evolution(self,x,y):
        """
        x : proies 
        y : predateurs
        """
        return x*(self.a-self.b*y)
    def predators_evolution(self,x,y):
        """
        x : proies 
        y : predateurs
        """
        return y*(-self.g+self.d*x)
    def set_preys(self,alpha=0.8,beta=0.4) :
        """
        a : taux de reproduction des proies
        b : taux de mortalité des proies dû aux prédateurs rencontrés
        """
        self.a,self.b=alpha,beta
    def set_predators(self,gamma=0.6,delta=0.2) :
        """
        g : taux de mortalité des prédateurs
        d : taux de reproduction des prédateurs en fonction des proies rencontrées et mangées'''
        """
        self.g,self.d=gamma,delta

    def generate(self) :
        del self.population[0:]
        h=(self.stop-self.start)/self.samples
        time,preys,predators=[0]*(self.samples+1),[0]*(self.samples+1),[0]*(self.samples+1)
        time[0]=self.start
        preys[0]=self.x
        predators[0]=self.y
        for i in range(self.samples):
            # print("time",time[i])
            time[i+1]=time[0]+h*(i+1)
            # print("preys",preys[i])
            preys[i+1]=preys[i]+h*self.preys_evolution(preys[i],predators[i])
            predators[i+1]=predators[i]+h*self.predators_evolution(preys[i],predators[i])
        self.population=zip(time,preys,predators)
        return self.population

class Logistic(Subject) :
    def __init__(self,r=np.linspace(0,4,1000),trials=50,niteration=100) :
        Subject.__init__(self)
        self.r=r
        self.trials=trials
        self.niteration=niteration

    def iterations(self,r):
        x=random.uniform(0,1)
        i=0
        while i<self.niteration and x<1:
            x=r*x*(1-x)
            i+=1
        return x if x < 1 else -1

    def generate(self):
        r_v=[]
        x_v=[]
        for rr in self.r:
            j=0
            while j < self.trials:
                xx=self.iterations(rr)
                if xx>0:               # Convergence: il s'agit d'une valeur d'équilibre
                    r_v.append(rr)
                    x_v.append(xx)
                j+=1                   # Nouvel essai

        return r_v, x_v

if  __name__ == "__main__" :
    a=1
    while a != 0 :
        a = input('choisir un chiffre entre 1 et 3 (sortie : 0) : ')
        if a in ('0','1','2','3') :
            a=int(a)
            if a==1:
                model=Generator()
                # # logger.debug("{}".format(model))
                print(model)
                signal=model.generate()
                time=[t[0] for t in signal]
                elongation=[e[1] for e in signal]
                plt.plot(time,elongation,".g")
                model.set_steps(2)
                model.set_frequency(2.0)
                signal=model.generate()
                time=[t[0] for t in signal]
                elongation=[e[1] for e in signal]
                plt.plot(time,elongation,"or")
                model.set_samples(200)
                model.set_phase(90.0)
                signal=model.generate()
                time=[t[0] for t in signal]
                elongation=[e[1] for e in signal]
                plt.plot(time,elongation,"+b")
            elif a==2 :
                model=PreyPredator()
                signal=model.generate()
                print(signal)
                signal=list(signal)
                time=[t[0] for t in signal]
                print(len(time))
                preys=[t[1] for t in signal]
                print(len(preys))
                predators=[t[2] for t in signal]
                print(len(predators))
                plt.plot(time,preys,"+g")
                plt.plot(time,predators,"-r")
                plt.plot(preys,predators,".b")
            # r=np.linspace(0,4,100)
            # print(r)
            elif  a==3 :
                model=Logistic()
                x,y=model.generate()
                plt.plot(x, y, 'r,')
                plt.xlabel('r')
                plt.ylabel('x')
            plt.show()
        else :
            print ("Vous devez choisir un chiffre entre 1 et 3 !")

