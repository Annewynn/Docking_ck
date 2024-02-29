#!/usr/bin/env python3

import sys, re

#prend en arguments :
# 1 : le chemin du fichier pdbqt du récepteur
# 2 : le chemin du fichier pdbqt du ligand

# crée dans le répertoire courant un fichier config_nom_récepteur_nom_ligand.txt contenant les informations pour le docking

#receptor = arg 1
#ligand = arg 2
#center_x = 9.236
#center_y = 1.295
#center_z = 4.592
#size_x = 21.75
#size_y = 18.75
#size_z = 18.75
#out = nom_récepteur_nom_ligand.pdbqt
#energy_range = 4
#num_modes = 100
#exhaustiveness = 100
#log = nom_récepteur_nom_ligand.log
#cpu = 4
receptor = str(sys.argv[1])
ligand = str(sys.argv[2])

nom_recepteur = re.search("/([\w-]*)[^/]*$", receptor)
nom_ligand = re.search("/([\w-]*)[^/]*$", ligand)

#créer un fichier config...txt
# https://stackoverflow.com/questions/35807605/create-a-file-if-it-doesnt-exist
nom_fichier = "config_" + nom_recepteur[1] + "_" + nom_ligand[1] + ".txt"
f = open(nom_fichier, 'w+')  
end = "\n"
f.write("receptor = " + receptor + end) 
f.write("ligand = " + ligand + end)  
f.write("center_x = 9.236" + end)
f.write("center_y = 1.295" + end)
f.write("center_z = 4.592" + end)
f.write("size_x = 21.75" + end)
f.write("size_y = 18.75" + end)
f.write("size_z = 18.75" + end)
# à enregistrer dans le dossier ../docking
f.write("out = ../docking/" + nom_recepteur[1] + "_" + nom_ligand[1] + ".pdbqt" + end)
f.write("energy_range = 4" + end)
f.write("num_modes = 100" + end)
#exhaustiveness à 100 pour une meilleure recherche dans la boite
f.write("exhaustiveness = 100" + end)
# à enregistrer dans le dossier ../docking
f.write("log = ../docking/" + nom_recepteur[1] + "_" + nom_ligand[1] + ".log" + end)
f.write("cpu = 12" + end)
f.close()
