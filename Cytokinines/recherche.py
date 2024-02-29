#!/usr/bin/env python3

import pubchempy as pcp
# doc sur https://pubchempy.readthedocs.io/en/latest/
#https://readthedocs.org/projects/pubchempy/downloads/pdf/latest/
import os, time, sys

#pour chaque composant dont on a téléchargé le fichier sdf
# on trouve leur id, on cherche les molécules similaires
#à un seuil de 90% et on récuppère l'id des structures semblables dans une liste

#pour chaque liste ainsi créée, on la parcours et on met chaque id dans une nouvelle liste
#si on en retrouve un identique dans deux listes on ne met pas la nouvelle 
#on enlève également les 16 id
#on retient combien de composants sont ignorés dans chaque liste / total trouvés

#on télécharge la structure 3d au format sdf de chaque nouvelle liste, et on lui donne comme nom
#pubchem_similaire_nom du ligand.sdf

#input : nombre maximum de ligands similaires à une même molécule à télécharger
#1000 est un maximum
#output : 
#par ligand : 
#nombre de molécules similaires trouvées
#nombre de molécules gardées après filtration
#nombre de molécules dont on a pu avoir la structure 3d

#input 1
nombre_similaires_max = sys.argv[1]

#on accède au répertoire du jeu de données ...
fichiers = []
for (dirpath, dirnames, filenames) in os.walk("jeu_de_donnees_ck_exp/"):
    for file in filenames:
        if file.endswith(".sdf"):
            fichiers.append(os.path.join(dirpath, file))
#...et on en extrait les id 
#dhrog n'en a pas, on récuppère quand même sa première ligne qui est son code smiles
ids = {}
for fichier in fichiers:
    f = open(fichier, 'r')
    id = f.readline().strip()
    ids[os.path.basename(fichier)[:-4]] = id
#pour chaque id, on fait une recherche de similarité 2d à un seuil de 90%. 
#v1 : on limite le nombre max de sorties à 1000
#v2 : on limite le nombre de sorties à 15 pour avoir un panel de 150 molécules max (plus réaliste par rapport au temps demandé par le docking)
#lent
#calcul du temps mis : 
start = time.time()
liste_ligands_potentiels = {}
for nom in ids:
    print(nom + " : cid " + ids[nom])
    id = ids[nom]
    if not id == "C([C@@H](C(C(N(C1=C2C(=NC(=N1)[H])[N](C(=N2)[H])[C@H]3[C@@H]([C@@H]([C@H](O3)C(O[H])([H])[H])O[H])O[H])[H])([H])[H])([H])[H])C(O[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)C(O[H])([H])[H])O[H])O[H])O[H])([H])[H])([H])([H])[H]" :
        #on fait une recherche par similarité, sur le cid, maximum 15 composants
        liste_ligands_potentiels[id] = pcp.get_compounds(int(id), 'cid', searchtype="similarity", MaxRecords = nombre_similaires_max)
    else : 
        liste_ligands_potentiels[id] = pcp.get_compounds(id, 'smiles', searchtype="similarity", MaxRecords = nombre_similaires_max)
    print(str(len(liste_ligands_potentiels[id])) + " similaires")
end = time.time()
print("temps mis pour obtenir les molécules similaires : " + str((end-start)/60) + " min")
#pour chaque ligand potentiel, son id est .to_dict()["cid"]
#on met chaque ligand potentiel dans une nouvelle liste, si on retombe plusieurs fois sur l'id on ne l'inclus qu'une fois
#on enlève également les id de ids
liste_ligands_uniques = {}
#clé = nom du composant expériemental (clé de liste_ligands_potentiels)
#valeur = ligands[id] = composant
i = 0
somme = 0
nom_ckexp = [y for y in ids]
for ckexp in liste_ligands_potentiels:
    ligands = {}
    for ligand in liste_ligands_potentiels[ckexp]:
        id_a_check = ligand.record['id']['id']['cid']
        unique = True
        #si l'id n'est pas dans la liste ids on peut le rajouter
        for x in ids.values():
            if not x == "C([C@@H](C(C(N(C1=C2C(=NC(=N1)[H])[N](C(=N2)[H])[C@H]3[C@@H]([C@@H]([C@H](O3)C(O[H])([H])[H])O[H])O[H])[H])([H])[H])([H])[H])C(O[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)C(O[H])([H])[H])O[H])O[H])O[H])([H])[H])([H])([H])[H]" :
                if id_a_check == int(x) : unique = False
        #si c'est le premier ligand on met tous ses similaires dans la liste
        if i == 0 and unique == True: ligands[id_a_check] = ligand
        elif unique == True:
            for noms in liste_ligands_uniques:
                for id in liste_ligands_uniques[noms]:
                    if id == id_a_check: 
                        unique = False
                        break
                if unique == False: break
        if unique == True : ligands[id_a_check] = ligand
    liste_ligands_uniques[ckexp] = ligands
    print(nom_ckexp[i] + " : " + str(len(liste_ligands_uniques[ckexp])) + " gardés sur " + str(len(liste_ligands_potentiels[ckexp])))
    i = i+1
    somme = somme + len(liste_ligands_uniques[ckexp])
print(str(somme+15) + " ligands ont été gardés au total")
#on télécharge les fichiers sdf des ligands retenus
i = 0
for ckexp in liste_ligands_uniques:
    liste = [x for x in liste_ligands_uniques[ckexp]]
    #si on a pas 0 molécules dans la liste on peut créer un fichier les  regroupant
    if not len(liste) == 0:
        if not x == "C([C@@H](C(C(N(C1=C2C(=NC(=N1)[H])[N](C(=N2)[H])[C@H]3[C@@H]([C@@H]([C@H](O3)C(O[H])([H])[H])O[H])O[H])[H])([H])[H])([H])[H])C(O[C@H]4[C@@H]([C@H]([C@@H]([C@H](O4)C(O[H])([H])[H])O[H])O[H])O[H])([H])[H])([H])([H])[H]" :
            pcp.download('SDF', 'base_de_donnees/pubchem_similaire_' + nom_ckexp[i] + '.sdf', liste, "cid", overwrite=True, record_type='3d')
        else :
            pcp.download('SDF', 'base_de_donnees/pubchem_similaire_' + nom_ckexp[i] + '.sdf', liste, "smiles", overwrite=True, record_type='3d')   
    i = i+1
print("fichiers téléchargés dans le dossier base de donnees")