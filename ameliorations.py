import graphe
import argparse
import os
from copy import deepcopy

def charger_donnees_rep(graphe, fichier):
    fichier = fichier.replace('.txt', '')
    mon_fichier = open(fichier + ".txt", "r")
    nom_ligne = fichier.replace('données/', '')
    lignes = (mon_fichier.read()).split('\n')
    i = 1
    if (lignes[0] != "# stations"):
        print("Erreur, le fichier doit commencer par # stations\n")
    while (lignes[i] != "# connexions"):
        ligne = lignes[i].split(':')
        graphe.ajouter_sommet(int(ligne[0]), ligne[1])
        i += 1

    for k in range (i + 1, len(lignes) - 1):
        ligne = lignes[k].split('/')
        graphe.ajouter_arete(int(ligne[0]), int(ligne[1]), nom_ligne, int(ligne[2]))
        k += 1
    mon_fichier.close()

def charger_donnees(graphe, fichier):
    charger_donnees_rep(graphe, "données/" + fichier)


def remplissage_dic(reseau, elem):
    res = dict()
    for sommet in reseau.sommets():
        res[sommet] = elem
    return res

def Numerotations(reseau):
    debut = remplissage_dic(reseau, 0)
    parent = remplissage_dic(reseau, None)
    ancetre = remplissage_dic(reseau, float("inf"))
    instant = 0
    def aux(s):
        nonlocal instant 
        instant = instant + 1
        debut[s] = ancetre[s] = instant
        for voisin in reseau.voisins(s):
            if debut[voisin]:
                if parent[s] != voisin:
                    ancetre[s] = min(ancetre[s], debut[voisin])
            else:
                parent[voisin] = s
                aux(voisin)
                ancetre[s] = min(ancetre[s], ancetre[voisin])
    for sommet in reseau.sommets():
        if debut[sommet] == 0:
            aux(sommet)
    return debut, parent, ancetre

def racine(reseau, parent):
    res = []
    for element in reseau.sommets():
        if parent[element] == None:
            res.append(element)
    return res

def points_articulation(reseau):

    def maj_degre(reseau, depart, degre_dep, parent):
        for voisin in reseau.voisins(depart):
            if parent[voisin] != depart:
                degre_dep = degre_dep - 1
        return degre_dep

    def aux(reseau, debut, parent, ancetre):
        articulations = []
        racines = racine(reseau, parent)

        for depart in racines:
            degre_dep = maj_degre(reseau, depart, reseau.degre(depart), parent)
            if degre_dep >= 2:
                articulations.append(depart)

        racines.append(None)
        for v in reseau.sommets():
            if (parent[v] not in racines) and (ancetre[v] >= debut[parent[v]]):
                if (parent[v] not in articulations):
                    articulations.append(parent[v])
        return articulations 

    debut, parent, ancetre = Numerotations(reseau)
    return aux(reseau, debut, parent, ancetre)


def ponts(reseau):
    debut, parent, ancetre = Numerotations(reseau)
    res = []
    for sommet in reseau.sommets():
        for voisin in reseau.voisins(sommet):
            if ancetre[sommet] > debut[voisin]:
                res.append(sorted([sommet, voisin]))
    return res
    
def trouve_csp(sommet, ponts, reseau):
    def aux(sommet, ponts, reseau):
        nonlocal deja_visite
        deja_visite.append(sommet)
        for voisin in reseau.voisins(sommet):
            if (sorted([sommet, voisin]) not in ponts) and (voisin not in deja_visite):
                aux(voisin, ponts, reseau)

    deja_visite = []
    aux(sommet, ponts, reseau)
    return sorted(deja_visite)

def rech_lst(element, lst):
    for ss_lst in lst:
        if element in ss_lst:
            return True
    return False

def const_csp(reseau, res_ponts):
    res = []
    for couple in res_ponts:
        for sommet in couple:
            if rech_lst(sommet, res) != True:
                res.append(trouve_csp(sommet, res_ponts, reseau))
    return res

def trouve_feuille(csp, ponts):
    res = []
    x = 0
    for lst in csp:
        for element in lst:
            for lst2 in ponts:
                if element in lst2:
                    x += 1
        if x < 2:
            res.append(lst)
        x = 0
    return res

def defini_arete(feuilles, lst_ponts, indice):
    for a in feuilles[0]:
        for b in feuilles[indice]:
            if ([a, b] not in lst_ponts) and ([b, a] not in lst_ponts):
                return (a, b)
            

def relie_feuilles(feuilles, reseau, lst_ponts):
    res = []
    for i in range(1, len(feuilles)):
        res.append(defini_arete(feuilles, lst_ponts, i))
    return res

def amelioration_ponts(reseau):
    lst_ponts = sorted(ponts(reseau))
    csp = sorted(const_csp(reseau, lst_ponts))
    feuilles = trouve_feuille(csp, lst_ponts)
    return relie_feuilles(feuilles, reseau, lst_ponts)

def selectionnne_voisin(point, parents, ancetre, depart, reseau):
    for voisin in reseau.voisins(point):
        if (point == parents[voisin]) and (ancetre[voisin] >= depart[point]):
            return voisin

def selectionne_voisin_racine(racine, reseau, parents):
    a, b = 0, 0
    for voisin in reseau.voisins(racine):
        if (racine == parents[voisin]) and (a == 0):
            a = voisin
        if (racine == parents[voisin]) and (voisin != a) and (b == 0):
            return a, voisin

def amelioration_points_articulation(reseau):
    res = []
    reseau_bis = deepcopy(reseau)
    depart, parent, ancetre = Numerotations(reseau)
    racines = racine(reseau, parent)
    lst_pt_art = (points_articulation(reseau))[::-1]
    while(len(lst_pt_art) != 0):
        if (lst_pt_art[0] in racines):
            a, b = selectionne_voisin_racine(lst_pt_art[0], reseau_bis, parent)
        else:
            a, b = racines[0], selectionnne_voisin(lst_pt_art[0], parent, ancetre, depart, reseau)
        reseau_bis.ajouter_arete(a, b, None)
        res.append((a, b))
        lst_pt_art = (points_articulation(reseau_bis))[::-1]
        depart, parent, ancetre = Numerotations(reseau_bis)
    return res

def print_erreur_arg(lst):
    print("Erreur, aucun metro/rer ne correspond(ent) au(x) element(s) suivant(s):", end='')
    for elem in lst:
        print(' ' + elem, end='')
    print(' ')

def defaut_chargement(reseau):
    for elem in os.listdir('.'):
        if (elem.endswith('.txt')):
            charger_donnees_rep(reseau, elem)

def def_transport(transport):
    if (transport == "METRO_"):
        return "metro"
    if (transport == "RER_"):
        return "rer"

def print_ligne(arg, flag):
    if (flag == 1):
        return(' ' + arg)
    if (flag == 0):
        return(arg)

def chargement_defaut(reseau, transport):
    flag = 0
    print("Chargement des lignes [", end='')
    for elem in os.listdir("données/"):
        if (elem.endswith('.txt')) and (transport in elem):
            str_elem = elem.replace('.txt','')
            print(print_ligne(str_elem.replace(transport,''), flag), end='')
            flag = 1
            charger_donnees(reseau, elem)
    print("] de " + def_transport(transport) + "... terminé.")

def chargement_lignes(reseau, transport, lst):
    if (lst == []):
        chargement_defaut(reseau, transport)
        return
    res, flag, flag2 = [], 0, 0
    print("Chargement des lignes [", end='')
    for arg in lst:
        for elem in os.listdir("données/"):
            if (elem == (transport + arg + ".txt")):
                charger_donnees(reseau, transport + arg + ".txt")
                print(print_ligne(arg, flag2), end='')
                flag,flag2 = 1, 1
        if (flag == 0):
            res.append(arg)
        flag = 0
    print("] de " + def_transport(transport) + "... terminé.")
    if (len(res) > 0):
        print_erreur_arg(res)

def affiche_ponts(reseau):
    res = ponts(reseau)
    str_res = []
    for pont in res:
        str_res.append("   - " + reseau.nom_sommet(pont[0]) + " -- " + reseau.nom_sommet(pont[1]))
    print("Le réseau contient les " + str(len(res)) + " ponts suivants :" )
    print("\n".join(str_res))

def affiche_points_articulation(reseau):
    i = 1
    res = points_articulation(reseau)
    str_res = []
    for point in res:
        str_res.append("  " + str(i) + " : " + reseau.nom_sommet(point))
        i += 1
    print("Le réseau contient les " + str(len(res)) + " points d'articulation suivants :" )
    print("\n".join(str_res))

def affiche_stations(reseau):
    print("Le réseau contient les " + str(len(reseau.sommets())) + " stations suivantes :" )
    print(reseau.noms_stations_str())

def affiche_amelioration_ponts(reseau):
    res = amelioration_ponts(reseau)
    str_res = []
    print("On peut éliminer tous les ponts du réseau en rajoutant les " + str(len(res)) + " arêtes suivantes :")
    for arete in res:
        str_res.append("   - " + reseau.nom_sommet(arete[0]) + " -- " + reseau.nom_sommet(arete[1]))
    print("\n".join(str_res))

def affiche_amelioration_articulation(reseau):
    res = amelioration_points_articulation(reseau)
    str_res = []
    print("On peut éliminer tous les points d'articulations du réseau en rajoutant les " + str(len(res)) + " arêtes suivantes :")
    for arete in res:
        str_res.append("   - " + reseau.nom_sommet(arete[0]) + " -- " + reseau.nom_sommet(arete[1]))
    print("\n".join(str_res))

def affiche_stats(reseau, flag):
    if (flag == 1):
        print("Le réseau contient " + str(len(reseau.sommets())) + " sommets et " + str(len(reseau.aretes())) + " arêtes.\n")

def traite_argument(args):
    flag = 0
    reseau = graphe.Graphe()
    if (args.metro != 0):
        chargement_lignes(reseau, "METRO_", args.metro)
        flag = 1

    if (args.rer != 0):
        chargement_lignes(reseau, "RER_", args.rer)
        flag = 1

    if (args.metro == 0) and (args.rer == 0):
        defaut_chargement(reseau)
        flag = 1

    affiche_stats(reseau, flag)

    if (args.liste_stations) == []:
        affiche_stations(reseau)
    
    if (args.articulations == []):
        affiche_points_articulation(reseau)

    if (args.ponts == []):
        affiche_ponts(reseau)

    if (args.ameliorer_articulations == []):
        affiche_amelioration_articulation(reseau)

    if (args.ameliorer_ponts == []):
        affiche_amelioration_ponts(reseau)

def ajoute_options(parser):
    parser.add_argument("--metro", nargs='*', default=0)
    parser.add_argument("--rer", help="type de transport = rer", nargs='*', default=0)
    parser.add_argument("--liste-stations", help="affiche la liste des stations du réseau avec leur identifiant triées par ordre alphabétique", nargs='*')
    parser.add_argument("--articulations", help="affiche les points d’articulation du réseau qui a été chargé", nargs='*')
    parser.add_argument("--ponts", help="affiche les ponts du réseau qui a été chargé", nargs='*')
    parser.add_argument("--ameliorer-articulations", help="affiche les points d’articulation du réseau qui a été chargé, ainsi que les arêtes à rajouter pour que ces stations ne soient plus des points d’articulation", nargs='*')
    parser.add_argument("--ameliorer-ponts", help="affiche les ponts du réseau qui a été chargé, ainsi que les arêtes à rajouter pour que ces arêtes ne soient plus des ponts", nargs='*')
    
def main():
    """import doctest
    doctest.testmod()"""
    parser = argparse.ArgumentParser()
    ajoute_options(parser)
    args = parser.parse_args()
    traite_argument(args)

if __name__ == "__main__":
    main()
