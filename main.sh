#!/usr/bin/env bash

#ce script lance la préparation au docking des ligands expérimentaux
#et de leurs récepteurs

#téléchargement des ligands possibles (fait à part)
#cd Cytokinines
#./recherche.py

#cd ..
#conversion des recepteurs modélisés au format pdbqt, pour le docking avec AutoDockTools et Vina
cd modeles_choisis_HK4_p.ramosa   #changer de dossier
dir="*.pdb"   #sélectionner tous les fichiers au format pdb dans le dossier courant
#source initMGLtools.sh
for fichier in $dir; do   #pour chaque fichier pdb dans le dossier courant
    sortie="bdd_pdbqt/$fichier.pdbqt"
    /media/naelle/ASTNL_WDsmall/AutoDockTools/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_receptor4.py -r $fichier -o $sortie -A checkhydrogens -U nphs
    #lancer le script prepare_receptor4.py qui prend en entrée un fichier $fichier pdb et génère un fichier sortie $sortie au format pdbqt
done  #le convertir au format pdbqt
echo "modèles convertis"

#conversion des ligands expérimentaux au format pdbqt, pour le docking avec AutoDockTools et Vina
#d'abord transformation en pdb avec obabel
cd ../Cytokinines/jeu_de_donnees_ck_exp
dir="*.sdf"
for fichier in $dir; do
    sortie="bdd_pdbqt/$fichier.pdb"
    obabel $fichier -O $sortie -hs
done

#puis transformation en pdbqt des pdb avec adt
cd bdd_pdbqt
dir="*.pdb"
#source initMGLtools.sh
for fichier in $dir; do
    sortie="$fichier.pdbqt"
    /media/naelle/ASTNL_WDsmall/AutoDockTools/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_ligand4.py -l $fichier -o $sortie -A 'hydrogens' -U nphs
done
echo "ligands expérimentaux convertis (flexibles)"
cd ..

#crée les fichiers de config dans cytokinines/jeu_de_donnees_ck_exp/configs
cd configs
dir="../../../modeles_choisis_HK4_p.ramosa/bdd_pdbqt/*.pdbqt"
for fichier in $dir; do
    dir_ligands="../bdd_pdbqt/*.pdbqt"
    for ligand in $dir_ligands; do
        ./cree_config.py $fichier $ligand
    done
    echo "congifs pour le modèle $fichier faites"
done

#docking à lancer sur la machine bioinfo
#avec le script docking_vina.sh
#pour chaque fichier de config, lancer un vina et mettre le résultat dans ../docking

#cd Cytokinines/jeu_de_donnees_ck_exp/configs
#dir="*.txt"
#for fichier in $dir; do
#    ../../../../../offmann-b/SOFTWARES/autodock_vina_1_1_2_linux_x86/bin/vina --config $fichier
#done 
