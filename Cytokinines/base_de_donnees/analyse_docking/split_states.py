#!/usr/bin/env python3

import sys

nom_ligand = sys.argv[1]
nom_fichier = sys.argv[2]
sortie = sys.argv[3]

#charger le fichier pdbqt des ligands, le spliter et conserver uniquement la première conformation
cmd.load(nom_fichier)
cmd.split_states(nom_ligand)
cmd.save(sortie + "/state1_" + nom_ligand + ".pdb", nom_ligand + "_0001")
