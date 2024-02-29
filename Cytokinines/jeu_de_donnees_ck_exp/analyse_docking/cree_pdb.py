#!/usr/env/bin python3

import sys

nom_ligand = sys.argv[1]
nom_fichier_ligand = sys.argv[2]
nom_fichier_recepteur = sys.argv[3]
sortie = sys.argv[4]

#on charge le fichier pdbqt du récepteur et celui pdb du ligand

cmd.load(nom_fichier_ligand)
cmd.load(nom_fichier_recepteur)
#add hydrogens
cmd.h_add

#save all
cmd.save(sortie + "/prot_lig_" + nom_ligand + ".pdb")

