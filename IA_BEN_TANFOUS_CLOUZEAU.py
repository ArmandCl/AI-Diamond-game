##############################################################################
# votre IA : à vous de coder
# Rappel : ne pas changer les paramètres des méthodes
# vous pouvez ajouter librement méthodes, fonctions, champs, ...
##############################################################################

import random

class IA_Diamant:
    def __init__(self, match : str):
        """génère l'objet de la classe IA_Diamant
        Args:
            match (str): decriptif de la partie
        """
        self.historique_carte = [] #Liste des cartes qui tirer pendant une manche.
        self.reste = 0 #Initialisation du reste        
        self.nb_joueur = match.split("|")[1] #Recup de le nombre de joueur de la manche en str
        self.piege = {"P1" : 3, "P2" : 3, "P3" : 3, "P4" : 3, "P5" : 3} #Dictionnaire qui regroupe les pièges et leur quantité
        self.nb_relique = 0 # nombre relique mis en jeu dans la manche
        self.nb_piege = 0 # nombre de piege tirer dans la manche
        self.part = 0 # nombre de rubi que peut récup l'ia         
        self.total = 0 # Total des rubis que l'ia peut recup dans la manche(ça propre part + le reste)
        self.total_rubis = 0 # Total des rubis qui sont en jeu dans la manche 
        print("IA SAE reçoit match = '" + match + "'")
        
    def table(self, tour : str):
        """
        Recup les valeurs importante sur la table.
        Args:
            tour(str): descriptif du dernier tour de jeu
        """
        self.carte = tour.split("|")[1] # recup la valeur de la carte
        self.joueur_partant = 0 # initialise la variable joueur partant
        self.choix_joueur= tour.split("|",2) # Dans un premier temps separe en deux à partir du caractere "|" et le stock dans la variable choix_joueur
        self.choix_joueur.pop(1) # Supprime la valeur à l'indice 1 car il representait la carte du tour
        self.choix_joueur=self.choix_joueur[0].split(",") # Separe la chaine de caractere qui se trouve à l'indice 0 à chaque virgule 
        for i in self.choix_joueur: # boucle pour regarder chaque choix de joueur
            if i in ['N', 'R']: # si le joueur est rentré on ajoute un au compteur joueur_partant
                self.joueur_partant +=1
        if self.carte in self.piege: #Si la carte tirer est une carte piege            
            self.nb_piege += 1 # ajoute un au compteur du nombre de piege tirer            
            self.historique_carte.append(self.carte) #Ajoute la carte dans l'historique
        elif self.carte == "R": # Si la carte est une relique
            self.nb_relique += 1 #ajoute 1 au nombre de carte relique tirer.
            self.historique_carte.append(self.carte) #Ajoute la carte dans l'historique
        else:
            self.reste += int(self.carte) % (int(self.nb_joueur)-self.joueur_partant) # Calcule pour ajouter le reste que peux avoir l'IA avec les joueur encore en jeu
            self.part +=  int(self.carte) // (int(self.nb_joueur)-self.joueur_partant) # Calcule la part que peut avoir l'IA avec les joueurs encore en jeu
            self.total_rubis += int(self.carte) # ajoute les rubis à chaque tour pour avoir le total de rubis de la manche
            self.historique_carte.append(self.carte) #Ajoute la carte dans l'historique
            self.total += self.part + self.reste # Total que peux recevoir l'IA en comptant la part + le reste

    
        



    def action(self, tour : str) -> str:
        """Appelé à chaque décision du joueur IA
        Args:
            tour (str): descriptif du dernier tour de jeu
        Returns:
            str: 'X' ou 'R'
        """        
        self.table(tour)
        risque = 0 #initialise le risque à 0
        risque += self.nb_piege*33 #multipli le nombre de piege par 33. Si 3 cartes tirer le risque sera à 99% donc dangereux.
        risque += (self.total_rubis - 35)*3 #regarde le total de rubis en jeu pendant la manche soustrait par une moyenne de 
                                            #rubis total d'une manche et multiplier par 3.Cela permet de baisser ou non le risque.
        risque += (int(self.nb_joueur)-self.joueur_partant)//100 # Permet de rajouter du risque moins il a de joueur restant.
        #Regarde si une carte relique a été piocher et si le nombre de rubis total est inferieur ou supperieur à 7
        #Cette suite de condition permet d'ajouter du risque en fonction de plusieurs situations.
        #Plus le risque est élevé plus il a la proba de sortir 
        if self.carte == "R" and self.total_rubis < 7: 
            if risque > 66:
                risque += self.nb_relique * 25
            else:
                risque += self.nb_relique * 5  
        elif self.carte == "R":
            if risque > 50:
                risque += self.nb_relique * 35
            else:
                risque += self.nb_relique * 20  
        # Tire un nombre entre 0 et 100.
        # Si le nombre est inferieur au risque alors l'IA rentre sinon il reste
        if random.randint(0,100) < risque:
            return "R"
        else:
            return "X"                       
        print("    IA SAE reçoit tour = '" + tour + "'")

    def fin_de_manche(self, raison : str, dernier_tour : str) -> None:
        """Appelé à chaque fin de manche

        Args:
            raison (str): 'R' si tout le monde est un piège ou "P1","P2",... si un piège a été déclenché
            dernier_tour (str): descriptif du dernier tour de la manche
        """
        print("  IA SAE reçoit en fin de manche raison = '" + raison + "' et dernier_tour = '" + dernier_tour + "'" )
        # Réinitialise toutes les listes et variables que nous devons réutiliser 
        # pour le bon fonctionnement de la prochaine manche
        self.nb_relique = 0
        self.nb_piege = 0
        self.part = 0
        self.reste = 0
        self.historique_carte = []        
        self.total_rubis=0

    def game_over(self, scores : str) -> None:
        """Appelé à la fin du jeu ; sert à ce que vous voulez

        Args:
            scores (str): descriptif des scores de fin de jeu
        """
        print("IA SAE reçoit en fin de jeu scores = '" + scores +"'")
