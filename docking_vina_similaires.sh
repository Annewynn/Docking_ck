#!/usr/bin/env bash

#pour chaque fichier de config, lancer un vina et mettre le résultat dans ../docking
#nohup ./docking_vina_similaires.sh &> dock.log &
cd Cytokinines/base_de_donnees/configs
for dossier in "*/"; do
    dir="$dossier/*.txt"
    for fichier in $dir; do
        ../../../../../offmann-b/SOFTWARES/autodock_vina_1_1_2_linux_x86/bin/vina --config $fichier
    done 
done