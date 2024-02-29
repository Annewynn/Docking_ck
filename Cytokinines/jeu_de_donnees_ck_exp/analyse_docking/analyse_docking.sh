#!/usr/bin/env bash

#ce script lance, pour chaque fichier pdbqt dans jeu_de_donnees_ck_exp/docking : 

#   - le script split_states.py qui récuppère la conformation de meilleure énergie et l'enregistre au format pdb
#   - on récuppère le fichier pdbqt du récepteur de ce ligand à partir de son nom
#   - le script cree_pdb génère un fichier pdb interprétable par plip
#   - plip -f fichier ligand + récepteur -x (NECESSITE ANACONDA ACTIF)
#   - le script analyse_result_plip.py qui récuppère les interactions et les stocke dans analyse_docking/matrice.csv

#   toutes les sorties se font dans jeu_de_donnees_ck_exp/analyse_docking/nom du récepteur + nom du ligand/

# ce script sera ensuite modifié pour analyser l'ensemble des dockings réalisés


rm -r */
#dossier courant : Cytokinines/jeu_de_donnees_ck_exp/analyse_docking
dir="../docking/*.pdbqt"   #sélectionner tous les fichiers au format pdbqt dans docking
# on renomme les fichiers pour en enlever les - et les remplacer par des _
rename 'y/-/_/' ../docking/*.pdbqt
for fichier in $dir; do   #pour chaque fichier pdbqt dans docking
    #on crée un dossier portant le nom du ligand (5 récepteurs possibles par ligand donc 3*5=15 fichiers potentiels)
    dossier=`echo $fichier | cut -d '/' -f 3 | cut -d . -f 1 | cut -d '_' -f 3-10`
    if [ ! -d "$dossier" ]; then
        mkdir $dossier
    fi
    #split_states : nom du ligand, chemin du fichier pdbqt du ligand, chemin de sortie
    nom_ligand=`echo $fichier | cut -d '/' -f 3 | cut -d . -f 1`
    #https://pymolwiki.org/index.php/Scripting_FAQs
    pymol -cq split_states.py -- $nom_ligand $fichier $dossier 2>/dev/null
done  
echo "split_states fait"
#lancement de cree_pdb.py, toujours dans le dossier courant
dir="*/*.pdb"
for fichier in $dir; do
    #on récupère le nom du fichier du récepteur puis son chemin
    recepteur=`echo $fichier | cut -d '/' -f 2 | cut -d . -f 1 | cut -d '_' -f 2-3`
    chem_recept="../../../modeles_choisis_HK4_p.ramosa/$recepteur.B99990001.pdb"
    #on recupere aussi le nom du ligand
    nom_ligand=`echo $fichier | cut -d '/' -f 2 | cut -d . -f 1`
    #nom du dossier où on est en train de regarder
    dossier=`echo $fichier | cut -d '/' -f 1`
    #renombrer le récepteur
    #pdb_reres -2 $chem_recept > $chem_recept
    pymol -cq cree_pdb.py -- $nom_ligand $fichier $chem_recept $dossier 2>/dev/null
done
echo "fichier interprétable par PLIP créé"

#puis on fait passer ce fichier dans plip (prot_lig.*.pdb)
#ANACONDA DOIT ETRE ACTIF
dir="*/prot_lig_state1_*.pdb"
for fichier in $dir; do
    nom_ligand=`echo $fichier | cut -d '/' -f 2 | cut -d . -f 1`
    dossier=`echo $fichier | cut -d '/' -f 1`
    plip -f $fichier --name $fichier -x 1>/dev/null 2>/dev/null
done
echo "plip exécuté"

#redirection des fichiers créés par plip dans le dossier courant vers sortie_plip_non_xml
mkdir sortie_plip_non_xml
mv plipfixed* sortie_plip_non_xml
mv prot_lig* sortie_plip_non_xml

#puis on lit les fichiers xml
# on renomme les fichiers pour en enlever les - et les remplacer par des _
rename 'y/-/_/' ../../base_de_donnees/*.sdf
rename 'y/-/_/' ../docking/*.log
rename 'y/-/_/' ../*.sdf
dir="*/*.xml"
for fichier in $dir; do
#./analyse_result_plip.py 
#arg 1 : $fichier
#arg 2 : fichier log de vina correspondant, soit ../docking/nom du fichier.log
#arg 3 : fichier sdf avec les similaires
    nom_ligand=`echo $fichier | cut -d '/' -f 2 | cut -d . -f 1 | cut -d '_' -f 4-10`
    log="../docking/$nom_ligand.log"
    dossier=`echo $fichier | cut -d '/' -f 1`
    sdf="../$dossier.sdf"
    ./analyse_result_plip.py $fichier $log $sdf
done
echo "sorties plip lues"

rm -r sortie_plip_non_xml