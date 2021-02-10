
# GraphTheoryProject
This project aim to implement algorithms to measure the fragility of a network according to criteria defined below and to automatically strengthen fragile networks.

The graphs considered are undirected and constructed from simplified data from the RER / Metro network of the RATP (french train companies).

1. This program starts by executing an algorithm detecting the articulation points then the bridges in the graphs represented by the map of the different metro / RER
2. Once the weaknesses of the graph have been identified, the algorithm strengthens it in two complementary ways: 
	- by modifying it so that no edge is a bridge
	- by modifying it  so that no vertex is a point of articulation



## How to use

Show all stations on a line :
```$ python3 ameliorations.py --metro 7b --liste-stations```
```Chargement des lignes ['7b'] de metro ... terminé.```
```Le réseau contient 8 sommets et 8 arêtes.```

```Le réseau contient les 8 stations suivantes: ```

```- Bolivar (2075)```
```- Botzaris (2002)```
```- Buttes-Chaumont (2013)```
```- Danube (1635)```
```- Jaurès (1900)```
```...```

Show all bridges and articulation points in a line :
```$ python3 ameliorations.py --metro 7b --ponts --articulations```
```Chargement des lignes ['7b'] de metro ... terminé.```
```Le réseau contient 8 sommets et 8 arêtes.```

```Le réseau contient les 4 ponts suivants:```

```- Bolivar -- Buttes-Chaumont ```
```- Bolivar -- Jaurès- ```
```- Botzaris -- Buttes-Chaumont```
```- Jaurès -- Louis Blanc```

```Le réseau contient les 4 points d'articulation suivants:```

```1 : Bolivar```
```2 : Botzaris```
```3 : Buttes-Chaumont```
```4 : Jaurès```

Show edges to add to remove bridges from the network :
```$ python3 ameliorations.py --rer --ameliorer-ponts```
```Chargement de toutes les lignes de rer ... terminé.```
```Le réseau contient 92 sommets et 91 arêtes.```

```On peut éliminer tous les ponts du réseau en rajoutant les 8 arêtes suivantes:```

```- Aéroport Charles de Gaulle 2 TGV -- Cergy-Le-Haut```
```- Aéroport Charles de Gaulle 2 TGV -- Robinson```
```- Boissy-Saint-Léger -- Poissy```
```- Boissy-Saint-Léger -- Saint-Germain-en-Laye```
```- Cergy-Le-Haut -- Saint-Rémy-lès-Chevreuse```
```- Marne-la-Vallée Chessy -- Mitry-Claye```
```- Mitry-Claye -- Robinson```
```- Poissy -- Saint-Rémy-lès-Chevreuse```

## References
- S. Even,Graph Algorithms, Cambridge University Press, 2nd edition 2012
- K. P. Eswaran et R. E. Tarjan,Augmentation problems, SIAM Journal on Computing, 5 (1976),pages 653–665


*Developed by Pierre-Jean Besnard*