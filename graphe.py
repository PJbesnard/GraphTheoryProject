#!/usr/bin/env python3
# -*- coding: utf-8 -*-



class Graphe(object):

    def __init__(self):
        """Initialise un graphe sans arêtes"""
        self.graphe = dict()
        self.noms = dict()
        self.durees = dict()
        self.lignes = dict()

    
    def noms_stations_str(self):
        res = []
        for sommet in self.noms:
            res.append(self.noms[sommet] + " (" + str(sommet) + ')')
        return '\n'.join(sorted(res))


    def ajouter_sommet(self, id_sommet, nom_sommet):
        """Ajoute un sommet (de n'importe quel type hashable) au graphe."""
        if id_sommet not in self.graphe:
            self.graphe[id_sommet] = set()
        self.noms[id_sommet] = nom_sommet

    def ajouter_sommets(self, iterable):
        """Ajoute tous les sommets de l'itérable donné au graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des éléments hashables."""
        for (id_sommet, nom_sommet) in iterable:
            self.ajouter_sommet(id_sommet, nom_sommet)

    def ajouter_arete(self, id_s1, id_s2, nom_metro, duree = -1):
        """Ajoute une arête entre les sommmets u et v, en créant les sommets
        manquants le cas échéant."""
        # vérification de l'existence de u et v, et création(s) sinon
        if id_s1 not in self.graphe:
            self.graphe[id_s1] = set()
        if id_s2 not in self.graphe:
            self.graphe[id_s2] = set()
        # ajout de u (resp. v) parmi les voisins de v (resp. u)
        self.graphe[id_s1].add(id_s2)
        self.graphe[id_s2].add(id_s1)
        self.lignes[(id_s1, id_s2)] = nom_metro
        self.durees[id_s1, id_s2] = duree

    def ajouter_aretes(self, iterable):
        for (id_s1, id_s2, nom_ligne) in iterable:
            self.ajouter_arete(id_s1, id_s2, nom_ligne)


    def sommets(self):
        return sorted(list(self.graphe.keys()))

    def nom_sommet(self, id_sommet):
        return self.noms[id_sommet]

    def aretes(self):
        res = []
        for sommet in self.graphe:
            for arete in self.graphe[sommet]:
                if sommet < arete:
                    res.append((sommet, arete, self.lignes[(sommet, arete)]))
        return res

    def voisins(self, id_s):
        return sorted(list(self.graphe[id_s]))

    def degre(self, id_s):
        return len(self.graphe[id_s])
