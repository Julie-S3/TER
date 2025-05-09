from data import Data
import numpy as np
import heapq
import time
import argparse
from random import randint

def mise_a_jour_envoye(data:Data, envoye,v,t):
    dico = {}
    for j in range(data.nb_sommets):
        if(data.w[j,v] != 0):
            dico[j] = min(data.alpha_max[j,v], data.Q[j] + t * data.r[j] - envoye[j])
    
   
    dico_trie =heapq.nlargest(min(data.M,len(dico)), dico.items(), key=lambda x: x[1])  
    somme_vecteur_triee = 0 

    for cle,valeur in dico_trie:
        somme_vecteur_triee += valeur 

    if(somme_vecteur_triee <= data.R):
        for cle, valeur in dico_trie:
            envoye[cle] += valeur
    else:
        somme = 0 
        for cle, valeur in dico_trie:
            while(somme < data.R):
                envoye[cle] += min(valeur, data.R - somme)
                somme += min(valeur, data.R - somme)
    return envoye

def maths_heur(data:Data):
    t = 0 
    ici = 0
    P_ici_v = np.zeros(data.nb_sommets)
    envoye = np.zeros(data.nb_sommets)
    pcc,pred = dijkstra(data)
    #print("T : ",data.nb_pas_de_temps)
    while(data.nb_pas_de_temps - t - pcc[ici] > 0):
        #print(" temps restant ", data.nb_pas_de_temps - t - pcc[ici] )
        #print("ici : ", ici)
        #print("temps t : ",t)
        for v in range(data.nb_sommets):
            if data.h[ici,v] != 0 and  data.nb_pas_de_temps - t - pcc[v] - 1 > 0:
                #print("T : ",data.nb_pas_de_temps, " t :  ",t," v ",v ," pcc ",pcc[v])
                #print("temps restant apres : ",data.nb_pas_de_temps - t - pcc[v] - 1)
                P_ici_v[v] = calcul_P_ici_v(data,ici,v,t,envoye) 
        P_ici_v[ici] = calcul_P_ici_ici(data,ici,t,envoye)
        apres = ici 
        valeur_apres = P_ici_v[ici]
        for v in range(data.nb_sommets):
            if data.h[ici,v] != 0 and  data.nb_pas_de_temps - t - pcc[v] - 1 > 0:
                if(P_ici_v[v] >= valeur_apres):
                    valeur_apres = P_ici_v[v]
                    apres = v 
        if ici == apres :
            t += 1 
        else :
            t += data.h[ici][apres] + 1
        #print("t , ",t," apres : ", apres)
        envoye = mise_a_jour_envoye(data,envoye,apres,t)
        #print("envoye :  ",envoye)
        ici = apres 
    
    
    return sum(envoye) 

def maths_heur_param(data:Data,t,ici,envoye):
    P_ici_v = np.zeros(data.nb_sommets)
    pcc,pred = dijkstra(data)
    #print("T : ",data.nb_pas_de_temps)
    while(data.nb_pas_de_temps - t - pcc[ici] > 0):
        #print(" temps restant ", data.nb_pas_de_temps - t - pcc[ici] )
        #print("ici : ", ici)
        #print("temps t : ",t)
        for v in range(data.nb_sommets):
            if data.h[ici,v] != 0 and  data.nb_pas_de_temps - t - pcc[v] - 1 > 0:
                #print("T : ",data.nb_pas_de_temps, " t :  ",t," v ",v ," pcc ",pcc[v])
                #print("temps restant apres : ",data.nb_pas_de_temps - t - pcc[v] - 1)
                P_ici_v[v] = calcul_P_ici_v(data,ici,v,t,envoye) 
        P_ici_v[ici] = calcul_P_ici_ici(data,ici,t,envoye)
        apres = ici 
        valeur_apres = P_ici_v[ici]
        for v in range(data.nb_sommets):
            if data.h[ici,v] != 0 and  data.nb_pas_de_temps - t - pcc[v] - 1 > 0:
                if(P_ici_v[v] >= valeur_apres):
                    valeur_apres = P_ici_v[v]
                    apres = v 
        if ici == apres :
            t += 1 
        else :
            t += data.h[ici][apres] + 1
        #print("t , ",t," apres : ", apres)
        envoye = mise_a_jour_envoye(data,envoye,apres,t)
        #print("envoye :  ",envoye)
        ici = apres 

    return sum(envoye) 

def maths_heur_ameliore(data:Data):
    voisins = []
    solution_voisins = []  
    for i in range(1,data.nb_sommets) :
        if data.h[0,i] != 0 :
            voisins.append(i)
            solution_voisins.append(0)
    
    for j in range(len(voisins)) :
        envoye = np.zeros(data.nb_sommets)
        ici = voisins[j]
       # print("debut heuristique avec ",ici)
        t = data.h[0,ici] + 1
        envoye = mise_a_jour_envoye(data,envoye,ici,t)
        solution_voisins[j] = maths_heur_param(data,t,ici,envoye)
       # print("envoye : ",solution_voisins[j])
    
    return max(solution_voisins)

    
        

def calcul_P_ici_v(data:Data, ici, voisin, t, envoye):
    vec = np.zeros(data.nb_sommets)
    P_ici_v = 0
    for j in range(data.nb_sommets):
        if data.w[j,voisin] != 0 :
            vec[j] = min(data.alpha_max[j,voisin], data.Q[j]+t*data.r[j] - envoye[j])
    vec = sorted(vec, reverse=True)
    for i in range (data.M):
        P_ici_v += vec[i]
        
    return min(P_ici_v, data.R)/data.h[ici, voisin]




def calcul_P_ici_ici(data:Data, ici, t, envoye):
    vec = np.zeros(data.nb_sommets)
    P_ici_ici = 0
    for j in range(data.nb_sommets):
        if data.w[j,ici] != 0 :
            vec[j] = min(data.alpha_max[j,ici], data.Q[j]+t*data.r[j] - envoye[j])
    vec = sorted(vec, reverse=True)
    for i in range (data.M):
        P_ici_ici += vec[i]

    return min(P_ici_ici, data.R)


def dijkstra(data: Data):
    Perm = []
    Temp = list(range(data.nb_sommets))
    pcc = np.zeros(data.nb_sommets)
    pred = np.zeros(data.nb_sommets)

    for i in range(1,data.nb_sommets):
        pcc[i] = 2**63 - 1
        pred[i] = -1
    
    while(len(Temp) != 0):
        x = Temp[0]
        valeur_x = pcc[Temp[0]]
        for i  in range(1,len(Temp)):
            if(valeur_x > pcc[Temp[i]]) :
                valeur_x = pcc[Temp[i]]
                x = Temp[i]
        Temp.remove(x)
        Perm.append(x)
        for j in range(data.nb_sommets):
            if(data.h[j,x] != 0):
                if(pcc[j] > pcc[x] + data.h[j,x]):
                    pcc[j] = pcc[x] + data.h[j,x]
                    pred[j] = x
    
    return pcc,pred


def maths_heur_stoch(data:Data):
    t = 0 
    ici = 0
    P_ici_v = np.zeros(data.nb_sommets)
    envoye = np.zeros(data.nb_sommets)
    pcc,pred = dijkstra(data)
    #print("T : ",data.nb_pas_de_temps)
    it = 0 
    while(data.nb_pas_de_temps - t - pcc[ici] > 0):
        #print(" temps restant ", data.nb_pas_de_temps - t - pcc[ici] )
        #print("ici : ", ici)
        #print("temps t : ",t)
        voisin = []
        for v in range(data.nb_sommets):
            if data.h[ici,v] != 0 and  data.nb_pas_de_temps - t - pcc[v] - 1 > 0:
                #print("T : ",data.nb_pas_de_temps, " t :  ",t," v ",v ," pcc ",pcc[v])
                #print("temps restant apres : ",data.nb_pas_de_temps - t - pcc[v] - 1)
                voisin.append(v)
                P_ici_v[v] = calcul_P_ici_v(data,ici,v,t,envoye) 
        P_ici_v[ici] = calcul_P_ici_ici(data,ici,t,envoye)
        apres = ici 
        valeur_apres = P_ici_v[ici]
        for v in range(data.nb_sommets):
            if data.h[ici,v] != 0 and  data.nb_pas_de_temps - t - pcc[v] - 1 > 0:
                if(P_ici_v[v] >= valeur_apres):
                    valeur_apres = P_ici_v[v]
                    apres = v
        if  it == int(np.sqrt(data.nb_pas_de_temps))  and len(voisin) != 0 :
            if len(voisin) < 2 :
                apres = voisin[0]
            else :
                k = randint(0,len(voisin)-1) 
                apres = voisin[k]
            it = 0 
        if ici == apres :
            t += 1 
        else :
            t += data.h[ici][apres] + 1
        #print("t , ",t," apres : ", apres)
        envoye = mise_a_jour_envoye(data,envoye,apres,t)
        #print("envoye :  ",envoye)
        ici = apres 
        it += 1 
    return sum(envoye) 

def maths_heur_stoch2(data:Data):
    t = 0 
    ici = 0
    P_ici_v = np.zeros(data.nb_sommets)
    envoye = np.zeros(data.nb_sommets)
    pcc,pred = dijkstra(data)
    #print("T : ",data.nb_pas_de_temps)
    nb_change = 0
    nb_change_max = int(np.sqrt(data.nb_pas_de_temps))
    while(data.nb_pas_de_temps - t - pcc[ici] > 0):
        #print(" temps restant ", data.nb_pas_de_temps - t - pcc[ici] )
        #print("ici : ", ici)
        #print("temps t : ",t)
        voisin = []
        random = randint(0,4)
        for v in range(data.nb_sommets):
            if data.h[ici,v] != 0 and  data.nb_pas_de_temps - t - pcc[v] - 1 > 0:
                #print("T : ",data.nb_pas_de_temps, " t :  ",t," v ",v ," pcc ",pcc[v])
                #print("temps restant apres : ",data.nb_pas_de_temps - t - pcc[v] - 1)
                voisin.append(v)
                P_ici_v[v] = calcul_P_ici_v(data,ici,v,t,envoye) 
        P_ici_v[ici] = calcul_P_ici_ici(data,ici,t,envoye)
        apres = ici 
        valeur_apres = P_ici_v[ici]
        for v in range(data.nb_sommets):
            if data.h[ici,v] != 0 and  data.nb_pas_de_temps - t - pcc[v] - 1 > 0:
                if(P_ici_v[v] >= valeur_apres):
                    valeur_apres = P_ici_v[v]
                    apres = v
        if  random == 0 and nb_change <= nb_change_max and len(voisin) != 0 :
            if len(voisin) < 2 :
                apres = voisin[0]
            else :
                k = randint(0,len(voisin)-1) 
                apres = voisin[k]
            nb_change += 1 
        if ici == apres :
            t += 1 
        else :
            t += data.h[ici][apres] + 1
        #print("t , ",t," apres : ", apres)
        envoye = mise_a_jour_envoye(data,envoye,apres,t)
        #print("envoye :  ",envoye)
        ici = apres 

    return sum(envoye) 

def k_iter(k,data:Data):
    max = 0 
    for i in range(k):
        envoye = maths_heur_stoch(data)
        if envoye > max :
            max = envoye
    return max

def k_iter2(k,data:Data):
    max = 0 
    for i in range(k):
        envoye = maths_heur_stoch2(data)
        if envoye > max :
            max = envoye
    return max

# data = Data()
# data.lireData("../DataVAP/ejemplo_10_40_72_5_4.dat")
# envoye = maths_heur(data)
# print("valeur heur : ",envoye)

# maxxx = maths_heur_ameliore(data)
# print("valeur heur ameliore : ",maxxx)

# maxx = k_iter(10,data)
# print("valeur heur stochastique : ",maxx)

def calculer_glouton_et_temps(data: Data):
    start_time = time.time()  # Début du chronométrage
    envoye = maths_heur(data)  # Appel de l'algorithme glouton
    end_time = time.time()  # Fin du chronométrage
    
    # Temps écoulé
    temps_glouton = end_time - start_time
    
    return envoye, temps_glouton

def calculer_am_et_temps(data: Data):
    start_time = time.time()  # Début du chronométrage
    envoye = maths_heur_ameliore(data)  # Appel de l'algorithme glouton
    end_time = time.time()  # Fin du chronométrage
    
    # Temps écoulé
    temps_glouton = end_time - start_time
    
    return envoye, temps_glouton

def calculer_st1_et_temps(data: Data):
    start_time = time.time()  # Début du chronométrage
    envoye = k_iter(1000,data)  # Appel de l'algorithme glouton
    end_time = time.time()  # Fin du chronométrage
    
    # Temps écoulé
    temps_glouton = end_time - start_time
    
    return envoye, temps_glouton

def calculer_st2_et_temps(data: Data):
    start_time = time.time()  # Début du chronométrage
    envoye = k_iter2(10000,data)  # Appel de l'algorithme glouton
    end_time = time.time()  # Fin du chronométrage
    
    # Temps écoulé
    temps_glouton = end_time - start_time
    
    return envoye, temps_glouton


def main():
    parser = argparse.ArgumentParser(description='Solver script')
    parser.add_argument('-d', '--cheminVersInstance', required=True, help='Path to the instance')
    parser.add_argument('-t', '--tempsLimite', type=int, required=True, help='Solver time limit in seconds')
    parser.add_argument('-r', '--fichierResultat', required=True, help='Fichier où écrire les résultats')

    args = parser.parse_args()

    data = Data()
    data.lireData(args.cheminVersInstance)

    envoye, temps_glouton = calculer_glouton_et_temps(data)
    envoye_am,temps_am = calculer_am_et_temps(data)
    envoye_st2,temps_st2 = calculer_st2_et_temps(data)



    # Ouvrir le fichier pour écrire les résultats
    with open(args.fichierResultat, 'a') as f:
        # Écrire les informations de l'instance dans le fichier
        f.write(f"{data.nb_sommets} {data.nb_pas_de_temps} {data.M} {data.R} ")
        f.write(f"{envoye} {temps_glouton} {envoye_am} {temps_am} {envoye_st2} {temps_st2}\n")



if __name__ == "__main__":
    main()
