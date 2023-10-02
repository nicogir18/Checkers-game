# Auteurs: Jean-Francis et Pascal Germain

from damier import Damier
from position import Position


class Partie:
    """Gestionnaire de partie de dames.

    Attributes:
        damier (Damier): Le damier de la partie, contenant notamment les pièces.
        couleur_joueur_courant (str): Le joueur à qui c'est le tour de jouer.
        doit_prendre (bool): Un booléen représentant si le joueur actif doit absolument effectuer une prise
            de pièce. Sera utile pour valider les mouvements et pour gérer les prises multiples.
        position_source_selectionnee (Position): La position source qui a été sélectionnée. Utile pour sauvegarder
            cette information avant de poursuivre. Contient None si aucune pièce n'est sélectionnée.
        position_source_forcee (Position): Une position avec laquelle le joueur actif doit absolument jouer. Le
            seul moment où cette position est utilisée est après une prise: si le joueur peut encore prendre
            d'autres pièces adverses, il doit absolument le faire. Ce membre contient None si aucune position n'est
            forcée.
        liste_position_source_valide (list): Contient les positions source valide lors du tour à jouer.

    """
    def __init__(self):
        """Constructeur de la classe Partie. Initialise les attributs à leur valeur par défaut. Le damier est construit
        avec les pièces à leur valeur initiales, le joueur actif est le joueur blanc, et celui-ci n'est pas forcé
        de prendre une pièce adverse. Aucune position source n'est sélectionnée, et aucune position source n'est forcée.

        """
        self.damier = Damier()
        self.doit_prendre = False
        self.position_source_selectionnee = None
        self.position_source_forcee = None
        self.couleur_joueur_courant = 'blanc'
        self.liste_position_source_valide = [Position(5, 0), Position(5, 2), Position(5, 4), Position(5, 6)]


    def position_source_valide(self, position_source):
        """Vérifie la validité de la position source, notamment:
            - Est-ce que la position contient une pièce?
            - Est-ce que cette pièce est de la couleur du joueur actif?
            - Si le joueur doit absolument continuer son mouvement avec une prise supplémentaire, a-t-il choisi la
              bonne pièce?

        Cette méthode retourne deux valeurs. La première valeur est Booléenne (True ou False), et la seconde valeur est
        un message d'erreur indiquant la raison pourquoi la position n'est pas valide (ou une chaîne vide s'il n'y a pas
        d'erreur).

        ATTENTION: Utilisez les attributs de la classe pour connaître les informations sur le jeu! (le damier, le joueur
            actif, si une position source est forcée, etc.

        ATTENTION: Vous avez accès ici à un attribut de type Damier. vous avez accès à plusieurs méthodes pratiques
            dans le damier qui vous simplifieront la tâche ici :)

        Args:
            position_source (Position): La position source à valider.

        Returns:
            bool, str: Un couple où le premier élément représente la validité de la position (True ou False), et le
                 deuxième élément est un message d'erreur (ou une chaîne vide s'il n'y a pas d'erreur).

        """
        piece_source = self.damier.recuperer_piece_a_position(position_source)
        if piece_source is None:
            return False, "Position source invalide: aucune pièce à cet endroit"

        if not piece_source.couleur == self.couleur_joueur_courant:
            return False, "Position source invalide: pièce de mauvaise couleur"

        if self.position_source_forcee is not None:
            if not (self.position_source_forcee == position_source):
                return False, "Position source invalide: vous devez faire jouer avec la pièce " + \
                    "en ({},{})".format(self.position_source_forcee.ligne, self.position_source_forcee.colonne)

        return True, ""

    def position_cible_valide(self, position_cible):
        """Vérifie si la position cible est valide (en fonction de la position source sélectionnée). Doit non seulement
        vérifier si le déplacement serait valide (utilisez les méthodes que vous avez programmées dans le Damier!), mais
        également si le joueur a respecté la contrainte de prise obligatoire.

        Returns:
            bool, str: Deux valeurs, la première étant Booléenne et indiquant si la position cible est valide, et la
                seconde valeur est une chaîne de caractères indiquant un message d'erreur (ou une chaîne vide s'il n'y
                a pas d'erreur).

        """
        if self.damier.piece_peut_se_deplacer_vers(self.position_source_selectionnee, position_cible):
            if not self.doit_prendre:
                return True, ""
            else:
                return False, "Le déplacement demandé n'est pas une prise alors qu'une prise est possible"

        elif self.damier.piece_peut_sauter_vers(self.position_source_selectionnee, position_cible):
            return True, ""

        return False, "Position cible invalide"

    def verification_positions_deplacement(self, position_source_clic, position_cible_clic):
        """ Valide les positions source et cible cliqué. Cette méthode doit demander
        les positions à l'utilisateur tant que celles-ci sont invalides.

        Cette méthode ne doit jamais planter, peu importe ce que l'utilisateur entre.

        Args:
            position_source_clic: La position source cliqué (objet de type Position)
            position_cible_clic: La position cible cliqué (objet de type Position)

        Returns:
            Position, Position: Un couple de deux positions (source et cible).

        """
        position_source = position_source_clic
        position_valide, message = self.position_source_valide(position_source)
        if not position_valide:
            print("Erreur: {}.\n".format(message))
        else:
            self.position_source_selectionnee = position_source



        position_cible = position_cible_clic
        position_valide, message = self.position_cible_valide(position_cible)
        if not position_valide:
            print(message + "\n")
            self.position_source_selectionnee = None
        else:
            position_valide = True
            return position_source, position_cible


if __name__ == "__main__":

    pass

