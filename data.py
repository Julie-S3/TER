#! usr/bin/python
# -*- coding: utf-8 -*-

from numpy import ndarray
import re
from typing import List
import numpy as np
from collections import deque

# ----------------------------------------------------------------------------
#  data structure
# ----------------------------------------------------------------------------
class Data:
    
    #_______________________ Attributs _______________________
    
    # nb_sommets : nombre total de sommets
    # nb_pas_de_temps : nombre de pas de temps
    # M : Nombre maximal de capteurs pouvant simultanément transmettre de l'information au véhicule à chaque pas de temps.
    # R : Quantité maximale d'information que le véhicule peut collecter par pas de temps.
    # r : Quantité d'information générée par chaque capteur à chaque pas de temps.
    # Q : Quantité initiale d'information stockée par chaque capteur.'
    # d : Distance entre chaque paire de sommets.
    # h : Temps nécessaire pour parcourir la distance entre deux sommets.
    # alpha : Paramètre physique définissant la quantité d'information transmissible par voie sans fil à chaque pas de temps. La quantité maximale transmissible entre deux sommets i et j est donnée par : 1/(alpha_{ij}(1+d_{ij}^2))
    # wir : w_{ij} = 1 si le capteur i peut envoyer de l'information au véhicule quand il est stationné au sommet j, 0 sinon



    #_______________________ Méthodes _______________________

    def __init__(self, nb_sommets:int = 0, nb_pas_de_temps:int = 0, M:int = 0, R:int = 0, r:List[int] = None, Q:List[int] = None, d:ndarray = None, h:ndarray = None, alpha:ndarray = None, w:ndarray = None,alpha_max:ndarray = None):
        self.nb_sommets = nb_sommets 
        self.nb_pas_de_temps = nb_pas_de_temps
        self.M = M
        self.R = R
        self.r = r 
        self.Q = Q
        self.d = d
        self.h = h
        self.alpha = alpha
        self.w = w
        self.alpha_max = alpha_max
        
    def lireData(self, filename) :
        try :

            with open(filename, "r") as file:

                # lecture de la 1ère ligne et séparation des éléments de la ligne
                # dans un tableau en utilisant l'espace comme séparateur
                line = file.readline()
                lineTab = re.split(r'[\n=;]+', line)

                self.nb_sommets = int(lineTab[1])
                line = file.readline()
                lineTab = re.split(r'[\n=;]+', line)
                self.nb_pas_de_temps = int(lineTab[1])
                line = file.readline()
                lineTab = re.split(r'[\n=;]+', line)
                self.M = int(lineTab[1])
                line = file.readline()
                lineTab = re.split(r'[\n=;]+', line)
                self.R = int(lineTab[1])

                #ignore N v e
                for i in range(3):
                    file.readline()

                line = file.readline()
                lineTab = line.split()
                lineTab = re.split(r'[,\s\[\]=;]+', line)

                self.r = [] 
                
                
                for i in range(len(lineTab)-2) :
                    self.r.append(int(lineTab[i+1]))

                line = file.readline()
                lineTab = line.split()
                lineTab = re.split(r'[,\s\[\]=;]+', line)

                self.Q = [] 
                
                for i in range(len(lineTab)-2) :
                    self.Q.append(int(lineTab[i+1]))

                line = file.readline()
                lineTab = line.split()
                lineTab = re.split(r'[,\s\[\]=;]+', line)
                
                self.d = np.zeros((self.nb_sommets,self.nb_sommets))
                for i in range(len(lineTab)-2) :
                    self.d[0,i] = int(lineTab[i+1])

                for i in range(1,self.nb_sommets):
                    line = file.readline()
                    lineTab = line.split()
                    lineTab = re.split(r'[,\s\[\]=;]+', line)
                    for j in range(len(lineTab)-2):
                        self.d[i,j] = int(lineTab[j+1]) 
                        
                line = file.readline()
                lineTab = line.split()
                lineTab = re.split(r'[,\s\[\]=;]+', line)
                
                self.h = np.zeros((self.nb_sommets,self.nb_sommets))
                for i in range(len(lineTab)-2) :
                    self.h[0,i] = int(lineTab[i+1])

                for i in range(1,self.nb_sommets):
                    line = file.readline()
                    lineTab = line.split()
                    lineTab = re.split(r'[,\s\[\]=;]+', line)
                    for j in range(len(lineTab)-2):
                        self.h[i,j] = int(lineTab[j+1]) 
                        
                line = file.readline()
                lineTab = line.split()
                lineTab = re.split(r'[,\s\[\]=;]+', line)
                        
                self.alpha_max = np.zeros((self.nb_sommets,self.nb_sommets))
                for i in range(len(lineTab)-2) :
                    self.alpha_max[0,i] = float(lineTab[i+1])

                for i in range(1,self.nb_sommets):
                    line = file.readline()
                    lineTab = line.split()
                    lineTab = re.split(r'[,\s\[\]=;]+', line)
                    for j in range(len(lineTab)-2):
                        self.alpha_max[i,j] = float(lineTab[j+1]) 
                
                line = file.readline()
                lineTab = line.split()
                lineTab = re.split(r'[,\s\[\]=;]+', line)
                
                self.w = np.zeros((self.nb_sommets,self.nb_sommets))
                for i in range(len(lineTab)-2) :
                    self.w[0,i] = int(lineTab[i+1])

                for i in range(1,self.nb_sommets):
                    line = file.readline()
                    lineTab = line.split()
                    lineTab = re.split(r'[,\s\[\]=;]+', line)
                    for j in range(len(lineTab)-2):
                        self.w[i,j] = int(lineTab[j+1]) 

                # print(self.nb_sommets)
                #print(self.nb_pas_de_temps)
                #print(self.M)
                #print(self.R)
                #print(self.r)
                #print(self.Q)
                #print(self.d)
                #print(self.h)
                #print(self.alpha)
                #print(self.w)
                #self.calcul_alpha_max()
        except FileNotFoundError :
            print("erreur fichier n'existe pas")
            
    # def calcul_alpha_max(self):
    #     self.alpha_max = np.zeros((self.nb_sommets,self.nb_sommets))
    #     for i in range(self.nb_sommets):
    #         for j in range(self.nb_sommets):
    #             self.alpha_max[i,j] = 1/(self.alpha[i,j]*(1+(self.d[i,j]**2)))
        
                    
