#!/usr/bin/env python3.8

import pandas as urs
from bs4 import BeautifulSoup as bs
import sys, os

#ce fichier récuppère la sortie xml de plip et en extrait les interactions
#elle les range dans le csv

#arg 1 : fichier xml
#dossier : nom commun (sans _)
#afx_ssbond : recepteur

#arg2 : fichier log de vina correspondant
#deltag estimé : 1re énergie

#arg3 : fichier sdf comportant les noms et id du ligand
#id pubchem : celui correspondant au nom commun
#similaire : le nom dans le titre du fichier

def interprete_plip():
	fichier = sys.argv[1]
	f = open(fichier, 'r')
	soup = bs(f, "lxml")
	#tag = soup.find("web_pins")
	#text = tag.text #Here you get your text!
	##P.S. you can also use:
	dico = {}
	if soup.find('hydrophobic_interactions').text != '': 
		aa = soup.find_all('hydrophobic_interaction')
		num = [b.resnr.text for b in aa]
		nom = [b.restype.text for b in aa]
		for i in range(len(num)):
			num[i] = num[i] + nom[i]
		if num != [] : 
			dico["Hphob"] = num

	#même chose pour les hydrogen bond
	if soup.find('hydrogen_bonds').text != '': 
		aa = soup.find_all('hydrogen_bond')
		num = [b.resnr.text for b in aa]
		nom = [b.restype.text for b in aa]
		for i in range(len(num)):
			num[i] = num[i] + nom[i]
		if num != [] : 
			dico["H"] = num

	#water bridges
	#for aa in soup.find_all('water_bridges'):
	if soup.find('water_bridges').text != '': 
		aa = soup.find_all('water_bridges')
		num = [b.resnr.text for b in aa]
		nom = [b.restype.text for b in aa]
		for i in range(len(num)):
			num[i] = num[i] + nom[i]
		if num != [] : 
			dico["WB"] = num

	#salt bridges
	if soup.find('salt_bridges').text != '': 
		aa = soup.find_all('salt_bridges')
		num = [b.resnr.text for b in aa]
		nom = [b.restype.text for b in aa]
		for i in range(len(num)):
			num[i] = num[i] + nom[i]
		if num != [] : 
			dico["SB"] = num
			
	#dataframe contenant ce qui a été trouvé dans le xml
	if dico != {}:
		donnees = urs.DataFrame({ key:urs.Series(value) for key, value in dico.items() })
		return donnees
	else : return False

def copie_csv(head, matrice):
	#nom commun : nom du dossier
	fichier_xml = sys.argv[1]
	noms = fichier_xml.split('/')
	nom_commun = noms[0]
	nom_commun = nom_commun.replace("_", " ")
	#id pubchem : dans le fichier pubchem_similaire
	fichier_similaires = open(sys.argv[3], "r")
	id = fichier_similaires.readline().strip()
	#similaire : lui même
	similaire = nom_commun
	#pourcent hausto formes : correspond au nom de la molécule dans ../../hausto_formes.csv
	pourc_hausto = ""
	fichier_hausto = urs.read_csv("../../hausto_formes.csv", sep="\t")
	index = fichier_hausto.index
	condition = fichier_hausto["nom de la molécule"] == nom_commun
	indice = index[condition].tolist()[0]
	pourc_hausto = fichier_hausto.iloc[indice, 1]
	#plage d'activité des ck : par rapport au nom de la molécule dans ../../activite_ck.csv
	activite_ck_min = ""
	activite_ck_max = ""
	fichier_activite = urs.read_csv("../../activite_ck.csv", sep="\t")
	index = fichier_activite.index
	condition = fichier_activite["nom de la molécule"] == nom_commun
	if condition.any():
		indice = index[condition].tolist()[0]
		activite_ck_min = fichier_activite.iloc[indice, 1]
		activite_ck_max = fichier_activite.iloc[indice, 3]
	#recepteur : dans le fichier xml, 4me colonne séparée par _
	recepteur = noms[1].split('_')[3]
	#delta g estimé : dans le fichier log, ligne 25 deuxième colonne
	fichier_dg = open(sys.argv[2], "r")
	contenu = fichier_dg.readlines()
	ligne = contenu[24].split(' ')
	energy = ""
	for charac in ligne:
		if charac.startswith('-'): 
			energy = charac
			break
	df = urs.DataFrame({'nom commun': [nom_commun],
                   'id pubchem': [id],
                   'similaire': [similaire], 
				   'pourcent hausto formes' : [pourc_hausto],
				   'activite min' : [activite_ck_min],
				   'activite max' : [activite_ck_max],
				   'recepteur' : [recepteur], 
				   'Delta g estimé' : [energy]})

	#si head est True, on ajoute toutes les interactions (H : ASP262 comme H ASP262)
	if head:
		for interac in tab:
			for aa in tab[interac]:
				#nan != nan
				if aa == aa:
					nom_col = interac + " " + aa
					df[nom_col] = [1]		
		df.to_csv('matrice.csv', mode='a', index=False, header=head, sep=';', index_label=False)
		#print(df)
	else :
		interactions = matrice[matrice.columns[5:]]
		for interac in tab:
			for aa in tab[interac]:
				#nan != nan
				if aa == aa:
					nom_col = interac + " " + aa
					#vérif si aa déjà dans le tableau
					trouve = False
					#print(" " + nom_col)
					df[nom_col] = [0]
					#print(df[df.columns[5:]])
					for col in interactions:
						#print(col)
						if nom_col == col: 
							trouve = True
							df[nom_col] += 1
							break
					if trouve == False:
						#on ajoute une colonne portant ce nom
						df[nom_col] += 1
		#print(df[df.columns[5:]])	
		#jointure entre les 2 dataframes
		result = urs.concat([matrice, df], sort=False)	
		result.to_csv('matrice.csv', mode = 'w', index=False, header=True, sep=';', index_label=False)

#on interprète le fichier xml de plip
tab = interprete_plip()
#on parcours ce tableau pour le ranger dans le csv
fichier = open("matrice.csv", 'a')
if os.path.getsize("matrice.csv") != 0:
	matrice = urs.read_csv("matrice.csv", sep=";")
	copie_csv(False, matrice)
else : 
	#on crée le header du fichier csv avec : 
	#nom commun, id pubchem, similaire, recepteur, pourcent hausto formes, delta g estimé, et les interactions
	#on y met les infos du ligand
	copie_csv(True, 0)
	



