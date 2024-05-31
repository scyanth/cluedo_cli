import random
import time

print("-------Cluedo CLI -------")

# nombre de joueurs (de 3 à 6)
nbjoueurs = 3
print("Le nombre de joueurs est de " + str(nbjoueurs) + ".")

# prénoms des bots :
prenoms = ["Alice","Bernard","Celine","David","Emma","Fred"]
# (si doublon avec prénoms de joueurs humains : prenom 2, et ainsi de suite)

# noms des joueurs
noms_joueurs = {0:"j0",1:"j1",2:"j2",3:"j3",4:"j4",5:"j5"}

# type : humain = 0, bots par niveau de difficulté = 1 à 2
types_joueurs = {0:1,1:1,2:1,3:1,4:1,5:1}

for j in range(0,nbjoueurs):
    if (types_joueurs[j] == 0):
        print("Joueur humain : " + noms_joueurs[j])
    elif (types_joueurs[j] == 1):
        print("Bot niveau 1 : " + noms_joueurs[j])
    elif (types_joueurs[j] == 2):
        print("Bot niveau 2 : " + noms_joueurs[j])

time.sleep(1)

# tous les éléments du jeu (ces listes servent pour les 3 piles de départ + pour faciliter l'édition)
personnages = ["Colonel Moutarde","Révérend Olive","Professeur Violet","Madame Pervenche","Mademoiselle Rose","Madame Leblanc"]
armes = ["Le poignard","Le chandelier","Le revolver","La corde","La matraque","La clé anglaise"]
pieces = ["La cuisine","Le salon","La salle à manger","La véranda","La salle de bal","Le bureau","La bibliothèque","La salle de billard","Le hall"]

tous_personnages = personnages.copy()
toutes_armes = armes.copy()
toutes_pieces = pieces.copy()

# tirage aléatoire d'un élément de chaque catégorie
random.seed(time.time())
personnage_rng = int(random.randrange(0,6)) # (+1)
personnage_crime = personnages[personnage_rng]
personnages.pop(personnage_rng)
arme_rng = int(random.randrange(0,6))
arme_crime = armes[arme_rng]
armes.pop(arme_rng)
piece_rng = int(random.randrange(0,9))
piece_crime = pieces[piece_rng]
pieces.pop(piece_rng)

print("Le set gagnant sera : " + personnage_crime + " dans " + piece_crime + " avec " + arme_crime + ".")
time.sleep(1)

# constitution de la pile globale
pile = []
for pers in personnages:
    element = {}
    element["categorie"] = "personnage"
    element["nom"] = pers
    pile.append(element)
for a in armes:
    element = {}
    element["categorie"] = "arme"
    element["nom"] = a
    pile.append(element)
for piece in pieces:
    element = {}
    element["categorie"] = "piece"
    element["nom"] = piece
    pile.append(element)

# mélange
random.shuffle(pile)

# distribution
tous_sets = {0:[],1:[],2:[],3:[],4:[],5:[]}
j=0
while len(pile) > 0:
    set_j = tous_sets[j]
    set_j.append(pile[0])
    pile.pop(0)
    tous_sets[j] = set_j
    j=j+1
    if (j == nbjoueurs):
        j=0

# définition du 1er joueur : si distribution inégale cf ci-dessous, sinon aléatoire
# si 4 joueurs : 5-5-4-4 donc j2, si 5 joueurs : 4-4-4-3-3 donc j3
if (nbjoueurs == 4):
    joueur_init = 2
    print("Le premier joueur sera j" + str(joueur_init) + " car il possède moins de cartes.")
elif (nbjoueurs == 5):
    joueur_init = 3
    print("Le premier joueur sera j" + str(joueur_init) + " car il possède moins de cartes.")
else:
    random.seed(time.time())
    joueur_init = int(random.randrange(0,nbjoueurs))
    print("Le premier joueur défini au hasard sera j" + str(joueur_init) + ".")

time.sleep(1)

# ce qu'il restera après éliminations, pour chaque joueur (carnet de notes)
candidats = {0:{"personnage":tous_personnages.copy(),"arme":toutes_armes.copy(),"piece":toutes_pieces.copy()},
             1:{"personnage":tous_personnages.copy(),"arme":toutes_armes.copy(),"piece":toutes_pieces.copy()},
             2:{"personnage":tous_personnages.copy(),"arme":toutes_armes.copy(),"piece":toutes_pieces.copy()},
             3:{"personnage":tous_personnages.copy(),"arme":toutes_armes.copy(),"piece":toutes_pieces.copy()},
             4:{"personnage":tous_personnages.copy(),"arme":toutes_armes.copy(),"piece":toutes_pieces.copy()},
             5:{"personnage":tous_personnages.copy(),"arme":toutes_armes.copy(),"piece":toutes_pieces.copy()}}

# éléments prioritaires (pour les bots niveau 2)
personnages_prioritaires = {0:"",1:"",2:"",3:"",4:"",5:""}
armes_prioritaires = {0:"",1:"",2:"",3:"",4:"",5:""}
pieces_prioritaires = {0:"",1:"",2:"",3:"",4:"",5:""}

# avant la partie proprement dite, les joueurs éliminent les éléments de leur propre set
for j in range(0,nbjoueurs):
    set_j = tous_sets[j]
    for s in set_j:
        if (s["categorie"] == "personnage"):
            s_id = candidats[j]["personnage"].index(s["nom"])
            candidats[j]["personnage"].pop(s_id)
        if (s["categorie"] == "arme"):
            s_id = candidats[j]["arme"].index(s["nom"])
            candidats[j]["arme"].pop(s_id)
        if (s["categorie"] == "piece"):
            s_id = candidats[j]["piece"].index(s["nom"])
            candidats[j]["piece"].pop(s_id)

print("Les joueurs ont éliminé leurs propres cartes.")

# boucle de partie
print("La partie commence...")
print("---------------")
time.sleep(4)
joueurs_elimines = []
j = joueur_init
partie_terminee = False
while partie_terminee is False:
    # ignore les joueurs éliminés
    if (not(j in joueurs_elimines)):
        print ("Au tour de j" + str(j) + " :")
        # hypothèse
        # priorisation si possible (niveau 2 uniquement), sinon aléatoire
        if (personnages_prioritaires[j] != ""):
            personnage_h = personnages_prioritaires[j]
            personnage_id = candidats[j]["personnage"].index(personnage_h)
        else:
            random.seed(time.time())
            personnage_id = random.randrange(0,len(candidats[j]["personnage"]))
            personnage_h = candidats[j]["personnage"][personnage_id]
        if (armes_prioritaires[j] != ""):
            arme_h = armes_prioritaires[j]
            arme_id = candidats[j]["arme"].index(arme_h)
        else:
            random.seed(time.time())
            arme_id = random.randrange(0,len(candidats[j]["arme"]))
            arme_h = candidats[j]["arme"][arme_id]
        if (pieces_prioritaires[j] != ""):
            piece_h = pieces_prioritaires[j]
            piece_id = candidats[j]["piece"].index(piece_h)
        else:
            random.seed(time.time())
            piece_id = random.randrange(0,len(candidats[j]["piece"]))
            piece_h = candidats[j]["piece"][piece_id] 
        print ("j" + str(j) + " propose : " + personnage_h + " dans " + piece_h + " avec " + arme_h + "...")
        print("Les autres joueurs vérifient leurs cartes...")
        time.sleep(2)
        # verif par les autres joueurs
        compteur_ja = 0
        for ja in range(0,nbjoueurs):
            if (ja != j):
                elements_matches = []
                if ({"categorie":"personnage","nom":personnage_h} in tous_sets[ja]):
                    elements_matches.append(["personnage",personnage_h])
                    print("j" + str(ja) + " possède ce personnage.")
                if ({"categorie":"arme","nom":arme_h} in tous_sets[ja]):
                    elements_matches.append(["arme",arme_h])
                    print("j" + str(ja) + " possède cette arme.")
                if ({"categorie":"piece","nom":piece_h} in tous_sets[ja]):
                    elements_matches.append(["piece",piece_h])
                    print("j" + str(ja) + " possède cette pièce.")
                # élément à montrer, élimination
                if (len(elements_matches) == 1):
                    compteur_ja = compteur_ja + 1
                    print("j" + str(ja) + " montre sa carte à j" + str(j) + ".")
                    if (elements_matches[0][0] == "personnage"):
                        candidats[j]["personnage"].pop(personnage_id)
                        personnages_prioritaires[j] = ""
                    elif (elements_matches[0][0] == "arme"):
                        candidats[j]["arme"].pop(arme_id)
                        armes_prioritaires[j] = ""
                    elif (elements_matches[0][0] == "piece"):
                        candidats[j]["piece"].pop(piece_id)
                        pieces_prioritaires[j] = ""
                elif (len(elements_matches) > 1):
                    compteur_ja = compteur_ja + 1
                    random.seed(time.time())
                    element_rng = int(random.randrange(0,len(elements_matches)))
                    element = elements_matches[element_rng]
                    if (element[0] == "personnage"):
                        print("j" + str(ja) + " montre le personnage à j" + str(j) + ".")
                        candidats[j]["personnage"].pop(personnage_id)
                        personnages_prioritaires[j] = ""
                    elif (element[0] == "arme"):
                        print("j" + str(ja) + " montre l'arme à j" + str(j) + ".")
                        candidats[j]["arme"].pop(arme_id)
                        armes_prioritaires[j] = ""
                    elif (element[0] == "piece"):
                        print("j" + str(ja) + " montre la pièce à j" + str(j) + ".")
                        candidats[j]["piece"].pop(piece_id)
                        pieces_prioritaires[j] = ""
                time.sleep(2)
        # si aucun joueur n'a d'élément => accusation
        if (compteur_ja == 0):
            print("Aucun joueur ne possède de carte correspondante.")
            print ("j" + str(j) + " accuse : " + personnage_h + " dans " + piece_h + " avec " + arme_h + "...")
            time.sleep(2)
            if ((personnage_h == personnage_crime) & (arme_h == arme_crime) & (piece_h == piece_crime)):
                # le joueur gagne
                print ("correct : j" + str(j) + " a gagné !")
                partie_terminee = True
            else:
                # le joueur est éliminé
                print ("faux... j" + str(j) + " est éliminé.")
                joueurs_elimines.append(j)
        # cas particulier de trio
        elif (compteur_ja == 3):
            print("3 joueurs ayant des cartes correspondantes, les 3 de l'hypothèse sont logiquement fausses. L'ensemble des joueurs éliminent alors ces cartes (si pas déjà fait).")
            time.sleep(2)
            for ja in range(0,nbjoueurs):
                if (personnage_h in candidats[ja]["personnage"]):
                    pe_id = candidats[ja]["personnage"].index(personnage_h)
                    candidats[ja]["personnage"].pop(pe_id)
                if (personnage_h == personnages_prioritaires[ja]):
                    personnages_prioritaires[ja] = ""
                if (arme_h in candidats[ja]["arme"]):
                    a_id = candidats[ja]["arme"].index(arme_h)
                    candidats[ja]["arme"].pop(a_id)
                if (arme_h == armes_prioritaires[ja]):
                    armes_prioritaires[ja] = ""
                if (piece_h in candidats[ja]["piece"]):
                    pi_id = candidats[ja]["piece"].index(piece_h)
                    candidats[ja]["piece"].pop(pi_id)
                if (piece_h == pieces_prioritaires[ja]):
                    pieces_prioritaires[ja] = ""
                # (pour n'importe quel joueur sauf si éliminé) si reste 1 seul élément de chaque catégorie => accusation
                if (not(ja in joueurs_elimines)):
                    if ((len(candidats[ja]["personnage"]) == 1) & (len(candidats[ja]["arme"]) == 1) & (len(candidats[ja]["piece"]) == 1)):
                        print ("j" + str(ja) + " accuse : " + candidats[ja]["personnage"][0] + " dans " + candidats[ja]["piece"][0] + " avec " + candidats[ja]["arme"][0] + "...")
                        time.sleep(2)
                        if ((candidats[ja]["personnage"][0] == personnage_crime) & (candidats[ja]["arme"][0] == arme_crime) & (candidats[ja]["piece"][0] == piece_crime)):
                            # le joueur gagne
                            print ("correct : j" + str(ja) + " a gagné !")
                            partie_terminee = True
                        else:
                            # le joueur est éliminé
                            print ("faux... j" + str(ja) + " est éliminé.")
                            joueurs_elimines.append(ja)
        # (pour le joueur actif) si reste 1 seul élément de chaque catégorie => accusation
        if ((len(candidats[j]["personnage"]) == 1) & (len(candidats[j]["arme"]) == 1) & (len(candidats[j]["piece"]) == 1)):
            print ("j" + str(j) + " accuse : " + candidats[j]["personnage"][0] + " dans " + candidats[j]["piece"][0] + " avec " + candidats[j]["arme"][0] + "...")
            time.sleep(2)
            if ((candidats[j]["personnage"][0] == personnage_crime) & (candidats[j]["arme"][0] == arme_crime) & (candidats[j]["piece"][0] == piece_crime)):
                # le joueur gagne
                print ("correct : j" + str(j) + " a gagné !")
                partie_terminee = True
            else:
                # le joueur est éliminé
                print ("faux... j" + str(j) + " est éliminé.")
                joueurs_elimines.append(j)
        # pour les bots de niveau 2, priorisation des éléments joués mais non éliminés
        if (types_joueurs[j] == 2):
            if (personnage_h in candidats[j]["personnage"]):
                personnages_prioritaires[j] = personnage_h
            if (arme_h in candidats[j]["arme"]):
                armes_prioritaires[j] = arme_h
            if (piece_h in candidats[j]["piece"]):
                pieces_prioritaires[j] = piece_h
        # s'il ne reste qu'un seul joueur : il gagne
        if (len(joueurs_elimines) == nbjoueurs-1):
            for jj in range(0,nbjoueurs):
                if (not(jj in joueurs_elimines)):
                    print ("j" + str(jj) + " gagne par élimination !")
                    partie_terminee = True
                    break
        j=j+1
        print("---------------")
        time.sleep(4)
        if (j == nbjoueurs):
            j=0