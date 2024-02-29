#!/usr/bin/env bash

#pour chaque fichier de config, lancer un vina et mettre le résultat dans ../docking
cd Cytokinines/jeu_de_donnees_ck_exp/configs
dir="*.txt"
for fichier in $dir; do
    ../../../../../offmann-b/SOFTWARES/autodock_vina_1_1_2_linux_x86/bin/vina --config $fichier
    echo "$fichier fait"
done 