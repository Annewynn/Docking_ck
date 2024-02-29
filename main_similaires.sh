#!/usr/bin/env bash

#ce script prépare les ligands similaires à ceux expérimentaux au docking


#on a déjà téléchargé les fichiers sdf contenant les ligands similaires 
#on a déjà converti les récepteurs au format pdbqt

#conversion des ligands expérimentaux au format pdbqt, pour le docking avec AutoDockTools et Vina
#d abord transformation en pdb avec obabel
#(fonctionne avec anaconda)
cd Cytokinines/base_de_donnees
rm -r bdd_pdbqt/*/
dir="*.sdf"
for fichier in $dir; do
#on veut faire un dossier par ck expérimental duquel les ligands sont similaires
#https://openbabel.org/docs/dev/Command-line_tools/babel.html
    dossier=`echo $fichier | cut -d . -f 1 | cut -d '_' -f 3-10`
    mkdir bdd_pdbqt/$dossier
    #on veut spliter le fichier pdb produit, comportant toutes les molécules
    obabel $fichier -opdb -mhs -O bdd_pdbqt/$dossier/molecule.pdb
done

#puis transformation en pdbqt des pdb avec adt
cd bdd_pdbqt
dir="*/"
for direc in $dir; do
    cd $direc
    file="*.pdb"
    echo $direc
    for fichier in $file; do
    echo $fichier
        sortie="$fichier.pdbqt"
        /media/naelle/ASTNL_WDsmall/AutoDockTools/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_ligand4.py -l $fichier -o $sortie -A 'hydrogens' -U nphs
    done
    cd ..
done
echo "ligands expérimentaux convertis (flexibles)"
cd ..


#crée les fichiers de config dans cytokinines/base_de_donnees/configs
cd configs
rm -r */
rm -r ../docking/*/
dir="../../../modeles_choisis_HK4_p.ramosa/bdd_pdbqt/*.pdbqt"
for fichier in $dir; do
    dir_ligands="../bdd_pdbqt/*"
    fichiers_ligands="../bdd_pdbqt/*/*.pdbqt"
    for dossier in $dir_ligands; do
        dossier_creer=`echo $dossier | cut -d '/' -f 3`
        if [ ! -d "$dossier_creer" ]; then
            mkdir $dossier_creer
            mkdir ../docking/$dossier_creer
        fi
        fichiers_ligands="../bdd_pdbqt/$dossier_creer/*.pdbqt"
        for ligand in $fichiers_ligands; do
            ./cree_config.py $fichier $ligand $dossier_creer
        done
    done
    echo "congifs pour le modèle $fichier faites"
done
: '
#docking à lancer sur la machine bioinfo
#avec le script docking_vina.sh
#pour chaque fichier de config, lancer un vina et mettre le résultat dans ../docking/nom de la molécule similaire

cd Cytokinines/base_de_donnees/configs
for dossier in "*/"; do
    dir="$dossier/*.txt"
    for fichier in $dir; do
        ../../../../../offmann-b/SOFTWARES/autodock_vina_1_1_2_linux_x86/bin/vina --config $fichier
    done 
done
'