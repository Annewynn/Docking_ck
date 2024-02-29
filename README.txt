
Lancement de la recherche-téléchargement de ligands similaires : 

	- télécharger les fichiers sdf 3D des ligands de référence dans Cytokinines/jeu_de_donnees_ck_exp, à la place de 			ceux déjà présents (https://pubchemdocs.ncbi.nlm.nih.gov/downloads)
	- installer pubchempy (https://pubchempy.readthedocs.io/en/latest/)
	- éventuellement adapter Cytokinines/recherche.py si les ligands contiennent des id smiles à la place des id pubchem
	- lancer le script en ligne de commande avec ./Cytokinines/recherche.py x
		x étant le nombre maximum de ligands similaires voulus par ligand
	
	- les sorties se trouvent dans Cytokinines/base_de_donnees





Lancement du pipeline de préparation au docking (main.sh ou main_similaires.sh) : 

	- installer openbabel et AutoDockTools
	- changer dans le script à lancer le chemin vers prepare_receptor4.py et prepare_ligand4.py
	- les fichiers pdb des récepteurs choisis doivent être dans modeles_choisis_HK4_p.ramosa/
	- les fichiers sdf des ligands doivent être dans Cytokinines/jeu_de_donnees_ck_exp/
	
	- en fonction de si ce sont les expérimentaux ou les similaires :
	
	- expérimentaux : lancer en ligne de commande ./main.sh
	- similaires : lancer en ligne de commande ./main_similaires.sh (nécessite que main.sh ait déjà été lancé sur les 			expérimentaux car il ne s'occupe pas des récepteurs)
	
	attention à régler le nombre de cpu et les paramètres de docking dans configs/cree_config.py
	
	- sortie : Cytokinines/jeu_de_donnees_ck_exp/configs/ ou Cytokinines/base_de_donnees/configs/
	
	
	
	
	
Lancement du docking : 
	- installer Autodock Vina ou y avoir accès
	- adapter le chemin de vina dans docking_vina.sh ou docking_vina_similaires.sh
	- lancer vina en ligne de commande avec 
		nohup ./docking_vina.sh &> dock.log &
	



Lancement du pipeline d'analyse du docking : 
	- installer Pymol, plip, et les librairies python pandas et beautifulsoup
		Plip peut nécessiter de passer par Anaconda pour fonctionner
		
	- en fonction des ligands, lancer : 
	- expérimentaux : Cytokinines/jeu_de_donnees_ck_exp/analyse_docking/analyse_docking.sh
	- similaires : Cytokinines/base_de_donnees/analyse_docking/analyse_docking.sh
	
	- sortie : matrice.csv remplie et prête à analyser
	
	
	
