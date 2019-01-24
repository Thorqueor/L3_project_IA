'''
Created on 03 mar. 2017

@author: Denou Julien
python version 2.7.13
'''
#!/usr/bin/python
# -*- coding: latin-1 -*-
import os, sys
import random
from random import randint
import copy
import time
from Tkinter import *



class Solution:
        """ La classe Solution est defini par :
        - L'etat courant du Taquin
        - Les differentes heuristiques et leurs valeurs de cout
        - L'affichage du Taquin courant
        - On defini la classe Solution de la facon suivante : """
        def __init__(self, taquin):
                self.restaquin = taquin

        def SolutionH(self):
                """ On defini les differentes heuristiques utilisees de la facon suivante :
                Ces heuristiques utilisent la Distance de Manhattan totale
                c'est la distance de chaque piece entre sa place actuelle et sa position finale en nombre de places.
                Nous utiliserons 6 heuristiques differentes avec des couts differents. """
                tq = self.restaquin
                #print("Affichage du taquin dans Solution")
                #tq.afficherEtat()
                

                """ On teste les 6 heuristiques dans une boucle while """
                distance = 1
                numeroHeuristique = []
                complexiteTemps = []
                nbmouv = []
                nbEtat = []
                complexite = list()
                while distance < 7:
                        """
                        Pour une distance inferieure a 7 car nous avons 6 heuristiques
                        On creer l'arbre binaire de recherche (abr) qui prendra en parametre le Taquin courant et
                        un autre parametre pour le calcul de l'heuristique
                        """
                        abr = Arbre(tq, distance)
                        abr.noeudCourant.taquin

                        """ Creation du timer pour definir la complexite en Temps """
                        start_time = time.time()

                        """ On boucle la recherche tant qu'on a pas atteint un Etat du But """
                        while abr.noeudCourant.heuristique != 0:
                                """On selectionne la meilleure Heuristique dans la Frontiere"""
                                indice = abr.choisirH()
                                meilleur = abr.frontiere[indice]
                                abr.noeudCourant = copy.deepcopy(meilleur)
                                abr.creerFils(abr.noeudCourant.directPrec, distance)

                                """On retire le Noeud courant de la Frontiere"""
                                del abr.frontiere[indice]

                                """On insert le Noeud courant dans l'ensemble des Explores"""
                                tmp = copy.deepcopy(meilleur)
                                insertion = True
                                for i in abr.explore:
                                        if abr.comparerTaquin(i.taquin.taq, tmp.taquin.taq):
                                                insertion = False
                                                break
                                if insertion:
                                        abr.explore.append(tmp)


                        indice = copy.deepcopy(abr.noeudCourant.g)
                        mouv = []
                        
                        """ 
                        Une fois trouvee la solution, on remonte l'arbre de recherche,
                        tout en inserant dans la liste des mouvements, les directions empruntees
                        """

                        while indice != 0:
                                mouv.append(copy.deepcopy(abr.noeudCourant.directPrec))
                                tmp = copy.deepcopy(abr.noeudCourant.noeudPapa)  
                                abr.noeudCourant = copy.deepcopy(tmp)
                                indice -= 1

                        
                        
                        
                        numeroHeuristique.append(distance)
                        nbEtat.append(len(abr.explore))
                        nbmouv.append(len(mouv))
                        complexiteTemps.append(time.time()-start_time)
                        complexite.append(time.time()-start_time)
                        print 'Pour Heuristique = {} Nb Etats = {} Solution en {} mouvements et Complexite en Temps : {} secondes'.format(repr(numeroHeuristique[distance-1]), repr(nbEtat[distance-1]), repr(nbmouv[distance-1]), repr(complexiteTemps[distance-1]))
                        
                        """ On reprends l'etat initial """
                        taquinDebut = copy.deepcopy(tqInit)
                        
                        indice=0
                        mouv.reverse()
                        """ Pour cela on applique les differentes directions enregistrees pour arriver a la Solution en sens inverse """
                        while indice != len(mouv):
                                if mouv[indice] == 0:
                                        taquinDebut.depN()
                                elif mouv[indice] == 1:
                                        taquinDebut.depE()
                                elif mouv[indice] == 2:
                                        taquinDebut.depS()
                                elif mouv[indice] == 3:
                                        taquinDebut.depO()
                                
                                time.sleep(3)
                                
                                indice += 1
                        distance+=1

                        """ On reprend l'Etat Initial pour essayer une autre Heuristique """
                        tq = copy.deepcopy(tqInit)

                a = min(complexiteTemps)
                print 'La complexite en Temps minimum est : {} pour heuristique {}'.format(a ,complexiteTemps.index(a)+1)
                
                
        def afficher(self, taquin):
                i=0
                for y in range(0,3,1):
                        for x in range(0,3,1):
                                if self.taquin.taq[i] != 0:
                                        self.can.create_rectangle ((5+100*x),(5+100*y),(100+100*x),(100+100*y),fill='white')
                                        self.can.create_text((50+100*x),(50+100*y),text=self.taquin.taq[i])
                                else:
                                        self.can.create_rectangle ((5+100*x),(5+100*y),(100+100*x),(100+100*y),fill='black')
                                i=i+1





                

class Interface(Frame):
        """
        Interface principale on affiche le taquin
        et que l'on ajoute les boutons Quitter et Solution
        Il faudrait ajouter le tableau recapitulatif
        """
            
        def __init__(self, fenetre, taquinInit, **kwargs):
                Frame.__init__(self, fenetre, width=350, height=350, **kwargs)
                self.pack(fill=BOTH)
                self.can = Canvas(fenetre, width=300, height=300,bg='black')
                self.can.pack(side="top" , padx=20, pady=70)
                self.taquin = taquinInit

                """ Affichage du taquin """
                i=0
                for y in range(0,3,1):
                        for x in range(0,3,1):
                                if self.taquin.taq[i] != 0:
                                        self.can.create_rectangle ((5+100*x),(5+100*y),(100+100*x),(100+100*y),fill='white')
                                        self.can.create_text((50+100*x),(50+100*y),text=self.taquin.taq[i])
                                i=i+1
                
                """ Affichage des boutons """
                self.bouton_quitter = Button(self, text="Quitter", command=self.quit)
                self.bouton_quitter.pack(side="bottom")
                
                self.bouton_cliquer = Button(self, text="Solution", fg="blue", command=self.cliquer)
                self.bouton_cliquer.pack(side="top")
            
        def cliquer(self):
                """S'il y a eu un clic sur Solution,
                on creer l'objet Solution en lui donnant le Taquin courant en parametre
                et enfin on lance la fonction de resolution"""
                rsd = Solution(self.taquin)
                rsd.SolutionH()
                fenetre2 = Tk()
                champ_label = Label(fenetre2, text="Resultats des Heuristiques ")
                champ_label.pack()

                """
                Ici a ajouter le tableau avec les solution et le comparatif des heuristiques A FAIRE
                print("Solutions des heuristiques : ")
                print(self.complexiteTemps)
                print(self.numeroHeuristique)
                min.complexiteTemps
                """
                


        def afficher(self, taquin):
                """ Permet d'afficher le taquin actuel """
                i=0
                for y in range(0,3,1):
                        for x in range(0,3,1):
                                if self.taquin.taq[i] != 0:
                                        self.can.create_rectangle ((5+100*x),(5+100*y),(100+100*x),(100+100*y),fill='white')
                                        self.can.create_text((50+100*x),(50+100*y),text=self.taquin.taq[i])
                                else:
                                        self.can.create_rectangle ((5+100*x),(5+100*y),(100+100*x),(100+100*y),fill='black')
                                i=i+1


        """ Les fonctions suivantes permetent de deplacer la case
        vide selon la touche directionnelle choisie. Ces boutons ont ete extrait d'Internet les sources sont en fichier Readme """
        def monter(self, event):
                print("HAUT")
                self.taquin.depN()
                self.afficher(self.taquin)
                self.taquin.afficherEtat()
        def descendre(self, event):
                print("BAS")
                self.taquin.depS()
                self.afficher(self.taquin)
                self.taquin.afficherEtat()
        def gauche(self, event):
                print("GAUCHE")
                self.taquin.depO()
                self.afficher(self.taquin)
                self.taquin.afficherEtat()
        def droite(self, event):
                print("DROITE")
                self.taquin.depE()
                self.afficher(self.taquin)
                self.taquin.afficherEtat()

class Taquin :
        
        """
        La classe Taquin est definie par :
        - Les valeurs 0 a 8 servant de cases du Taquin
        - La position des valeurs en parametres
        - Les methodes permettant de retrouver la position d'une case
        - Les methodes permettant de connaitre la distance entre une valeur et sa place ideale
        - Les methodes permettant de permuter les cases
        Cette classe permet d'enregistrer un Etat du Taquin
        """
        def __init__(self):
                self.xvide = 0
                self.yvide = 0
                self.precedent = 0
                self.taq = [0,1,2,3,4,5,6,7,8]
                
        
        def xPosition(self, valeur):
                """ Cette methode renvoie la position x de la valeur """
                n = self.taq.index(valeur)/3 - self.taq.index(valeur)//3
                m = 0
                if n == 0 :
                        m = 0
                elif n < 0.5 :
                        m = 1
                else:
                        m = 2
                return m
        
        def yPosition(self, valeur):
                """ Cette methode renvoie la position x de la valeur """
                return self.taq.index(valeur)//3

        def distanceSolution(self, valeur):
                """ Cette methode retourne la distance de Manhattan entre la valeur en parametre et
                la position ou elle devrait etre dans l'Etat du but"""
                xA = self.xPosition(valeur)
                xB = self.xPosition(self.taq[valeur])
                yA = self.yPosition(valeur)
                yB = valeur//3
                return abs(xA - xB) + abs(yA - yB)

        def heuristique(self, j):
                """ methode qui renvoie l'heuristique du taquin"""
                poids = [
                        [36,12,12,4,1,1,4,1,0],
                        [8,7,6,5,4,3,2,1,0],
                        [8,7,6,5,4,3,2,1,0],
                        [8,7,6,5,3,2,4,1,0],
                        [8,7,6,5,3,2,4,1,0],
                        [1,1,1,1,1,1,1,1,0],
                        ]
                if j==2 or j==4 or j==6:
                        p=1
                else:
                        p=4
                pi=j-1
                i=0
                res=0
                while i<8:
                        res += poids[pi][i]*self.distanceSolution(i)/p
                        i+=1
                return res
        

        def valeurPosition(self, X, Y):
                """ Retourne la valeur aux position X et Y """
                return self.taq[(X * 3) + Y]
        
        
        def deplacement(self, mouv):
                """Cette methode effectue un deplacement selon un mouvement donne"""
                x = xPosition(0)
                y = yPosition(0)

                if mouv == 0 :
                        self.depN(self, x, y)
                elif mouv == 1 :
                        self.depE(self, x, y)
                elif mouv == 2 :
                        self.depS(self, x, y)
                elif mouv == 3 :
                        self.depO(self, x, y)
                else:
                        return 0


        """ Les 4 fonctions suivantes verifient la possibilite d'un deplacement """
        def nordPossible(self):
                if self.xvide == 0 :
                        return False
                else :
                        return True

        def sudPossible(self):
                if self.xvide == 2:
                        return False
                else:
                        return True

        def estPossible(self):
                if self.yvide == 2:
                        return False
                else:
                        return True

        def ouestPossible(self):
                if self.yvide == 0 :
                        return False
                else :
                        return True


        """ Les 4 fonctions suivantes deplacent le 0 """
        def depN(self):
                if self.nordPossible() :
                        temp = self.taq[(self.xvide * 3) + self.yvide]
                        self.taq[(self.xvide * 3) + self.yvide] = self.taq[((self.xvide - 1) * 3) + self.yvide]
                        self.taq[((self.xvide - 1) * 3) + self.yvide] = temp
                        self.xvide = self.xvide - 1

        def depS(self):
                if self.sudPossible() :
                        temp = self.taq[(self.xvide * 3) + self.yvide]
                        self.taq[(self.xvide * 3) + self.yvide] = self.taq[((self.xvide + 1) * 3) + self.yvide]
                        self.taq[((self.xvide + 1) * 3) + self.yvide] = temp
                        self.xvide = self.xvide + 1

        def depE(self):
                if self.estPossible() :
                        temp = self.taq[(self.xvide * 3) + self.yvide]
                        self.taq[(self.xvide * 3) + self.yvide] = self.taq[((self.xvide) * 3) + self.yvide + 1]
                        self.taq[((self.xvide) * 3) + self.yvide + 1] = temp
                        self.yvide = self.yvide + 1

        def depO(self):
                if self.ouestPossible() :
                        temp = self.taq[(self.xvide * 3) + self.yvide]
                        self.taq[(self.xvide * 3) + self.yvide] = self.taq[((self.xvide) * 3) + self.yvide - 1]
                        self.taq[((self.xvide) * 3) + self.yvide - 1] = temp
                        self.yvide = self.yvide - 1

        """Cette methode permet de melanger n fois le Taquin"""
        def melanger(self, n):
                
                while n > 0:
                        self.melangerUnefois()
                        n = n - 1


        def melangerUnefois(self):
                """ Cette methode permet de melanger 1 fois le Taquin aleatoirement """
                aleatoire = randint(0, 3)
                if aleatoire == 0 :
                        self.depN()
                elif aleatoire == 1 :
                        self.depS()
                elif aleatoire == 2 :
                        self.depE()
                elif aleatoire == 3 :
                        self.depO()


        def afficherEtat(self):
                """ Affiche l'etat du taquin dans la console """
                str = "Etat du taquin\n{}|{}|{}\n{}|{}|{}\n{}|{}|{}".format(repr(self.taq[0]), repr(self.taq[1]), repr(self.taq[2]), repr(self.taq[3]), repr(self.taq[4]), repr(self.taq[5]), repr(self.taq[6]), repr(self.taq[7]), repr(self.taq[8]))
                print(str)


class Noeud:
        """
        La classe Noeud est defini par :
      - L'etat courant du Taquin
      - Le pere du Taquin courant
      - Les fils du Taquin courant
      - L'heuristique utilisee pour arriver au Taquin courant
      - Le nombre de mouvements pour obtenir Le Taquin courant ici defini par le parametre nbMouv
      - La fonction d'evaluation du Taquin courant ici defifinie par feval
      - La direction precedente
      - On defini la classe Noeud et ses parametres de facon suivante :
        """

        def __init__(self, noeudPrecedent, paramTaquin, paramDirectPrec, paramG, distElem):
                self.noeudPapa = noeudPrecedent
                self.directPrec = paramDirectPrec
                self.taquin = paramTaquin
                self.heuristique = self.taquin.heuristique(distElem)
                self.fils = []
                self.g=paramG
                self.f=self.g+self.heuristique
                        

class Arbre:
        """
        La classe Arbre est definie par :
        - Son sommet (l'Etat Initial du Taquin)
        - Son Noeud courant
        - La liste de Noeuds a la Frontiere
        - La liste de Noeuds deja explores
        - Les methodes de creation des Fils
        - La methode de comparaison de deux Taquins
        - La methode de choix d'heuristique
        """

        """ On prends en parametre le Taquin initial """
        def __init__(self, paramTaquin, distElem):
                self.sommet = Noeud(None, paramTaquin, None, 0, distElem)
                self.noeudCourant = self.sommet
                self.frontiere = []
                self.explore = []
                self.explore.append(self.sommet)
                self.creerFils(None, distElem)


        """ Methode de creation des fils et ajout a la frontiere si non explores """
        def creerFils(self, directPrec, distElem):
                listeTmp = []
                tmpTq = copy.deepcopy(self.noeudCourant)

                """ Verification de la possibilite de deplacement et creation des fils """
                if tmpTq.taquin.nordPossible():
                        tmpTq.taquin.depN()
                        self.noeudCourant.fils.append(Noeud(self.noeudCourant, tmpTq.taquin, 0, self.noeudCourant.g+1, distElem))
                        tmpTq.g +=1
                        tmpTq.heuristique = tmpTq.taquin.heuristique(distElem)
                        tmpTq.f = tmpTq.g + tmpTq.heuristique
                        tmpTq.directPrec = 0
                        tmpTq.noeudPapa = copy.deepcopy(self.noeudCourant)
                        listeTmp.append(tmpTq)
                        tmpTq = copy.deepcopy(self.noeudCourant)
                if tmpTq.taquin.estPossible():
                        tmpTq.taquin.depE()
                        self.noeudCourant.fils.append(Noeud(self.noeudCourant, tmpTq.taquin, 1, self.noeudCourant.g+1, distElem))
                        tmpTq.g +=1
                        tmpTq.heuristique = tmpTq.taquin.heuristique(distElem)
                        tmpTq.f = tmpTq.g + tmpTq.heuristique
                        tmpTq.directPrec = 1
                        tmpTq.noeudPapa = copy.deepcopy(self.noeudCourant)
                        listeTmp.append(tmpTq)
                        tmpTq = copy.deepcopy(self.noeudCourant)
                if tmpTq.taquin.sudPossible():
                        tmpTq.taquin.depS()
                        self.noeudCourant.fils.append(Noeud(self.noeudCourant, tmpTq.taquin, 2, self.noeudCourant.g+1, distElem))
                        tmpTq.g +=1
                        tmpTq.heuristique = tmpTq.taquin.heuristique(distElem)
                        tmpTq.f = tmpTq.g + tmpTq.heuristique
                        tmpTq.directPrec = 2
                        tmpTq.noeudPapa = copy.deepcopy(self.noeudCourant)
                        listeTmp.append(tmpTq)
                        tmpTq = copy.deepcopy(self.noeudCourant)
                if tmpTq.taquin.ouestPossible():
                        tmpTq.taquin.depO()
                        self.noeudCourant.fils.append(Noeud(self.noeudCourant, tmpTq.taquin, 3, self.noeudCourant.g+1, distElem))
                        tmpTq.g +=1
                        tmpTq.heuristique = tmpTq.taquin.heuristique(distElem)
                        tmpTq.f = tmpTq.g + tmpTq.heuristique
                        tmpTq.directPrec = 3
                        tmpTq.noeudPapa = copy.deepcopy(self.noeudCourant)
                        listeTmp.append(tmpTq)
                        tmpTq = copy.deepcopy(self.noeudCourant)

                """ Verification de l'existance des fils dans la frontiere et dans la liste des Etats Explores """
                for i in listeTmp:
                        insertion = True
                        for j in self.frontiere:
                                if self.comparerTaquin(i.taquin.taq, j.taquin.taq):
                                   insertion = False
                                   break
                        for j in self.explore:
                                if self.comparerTaquin(i.taquin.taq, j.taquin.taq):
                                   insertion = False
                                   break
                        if insertion:
                                self.frontiere.append(i)

        """ Comparaison de 2 Taquin : s'ils sont pareils de type boolean """
        def comparerTaquin(self, tq1, tq2):
                pareil = True
                i = 0
                while i<9:
                        if tq1[i]!=tq2[i]:
                                pareil = False
                                break
                        i+=1
                return pareil
                        
                                       

        """
        On choisi comme Noeud courant, le Noeud qui a la Fonction d'Evaluation la plus basse dans la Frontiere
        On reprends l'indice du tableau Frontiere du meilleur Noeud
        """
        def choisirH(self):
                minimal = 5000
                i=0
                IndiceMeilleurNoeud=0
                while i < len(self.frontiere):
                        if minimal > self.frontiere[i].f:
                                minimal = self.frontiere[i].f
                                IndiceMeilleurNoeud=i
                        i = i+1
                return IndiceMeilleurNoeud


if __name__ == "__main__" :
        tq = Taquin()
        tq.afficherEtat()
        

        tq.melanger(30)
        tqInit = copy.deepcopy(tq)
        print("Melange du taquin")
        tq.afficherEtat()


        """On cree une fenetre"""
        fenetre = Tk()
        champ_label = Label(fenetre, text="Taquin Intelligence Artificielle")
        champ_label.pack()
        interface = Interface(fenetre, tq)
        
        
        """Creation des evenements clavier, ceux-ci ont ete tires d'internet"""
        fenetre.bind("<Up>", interface.monter) 
        fenetre.bind("<Down>", interface.descendre) 
        fenetre.bind("<Left>", interface.gauche) 
        fenetre.bind("<Right>", interface.droite) 

        """On boucle sur l'interface graphique"""
        interface.mainloop()
        interface.destroy()