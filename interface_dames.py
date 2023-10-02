# Auteurs: À compléter

from tkinter import Tk, Label, Frame, Button, N, S,ttk,DISABLED,NORMAL
from canvas_damier import CanvasDamier
from partie import Partie
from position import Position
from piece import Piece
import numpy as np


class FenetrePartie(Tk):
    """Interface graphique de la partie de dames.

    Attributes:
        partie (Partie): Le gestionnaire de la partie de dame
        canvas_damier (CanvasDamier): Le «widget» gérant l'affichage du damier à l'écran
        messages (Label): Un «widget» affichant des messages textes à l'utilisateur du programme

        TODO: AJOUTER VOS PROPRES ATTRIBUTS ICI!
    """

    def __init__(self):
        """Constructeur de la classe FenetrePartie. On initialise une partie en utilisant la classe Partie du TP3 et
        on dispose les «widgets» dans la fenêtre.
        """

        # Appel du constructeur de la classe de base (Tk)
        super().__init__()
        #Le tour
        self.liste_position = []
        self.coup_precedent = []
        self.coup_precedent_status = ''

        # La partie
        self.partie = Partie()


        # Ajout d'une étiquette de configuration
        self.widget_configuration = Frame(self)
        self.widget_configuration.grid(row=0, column=1, sticky=N)

        # bouton nouvelle partie
        self.bouton_nouvelle_partie = Button(self.widget_configuration, text="Nouvelle Partie",
                                             command=self.creer_nouvelle_partie)
        self.bouton_nouvelle_partie.grid(row=6, column=1)
        # Label et Liste pour les thèmes
        optionTheme = ["rouge", 'bleu', 'orange', 'vert']
        self.labelTheme = Label(self.widget_configuration, text="Thème")
        self.labelTheme.grid(row=4, column=0)

        # Combobox pour le  changement de thème
        self.comboTheme = ttk.Combobox(self.widget_configuration)
        self.comboTheme.grid(row=4, column=1)
        self.comboTheme.bind('<<ComboboxSelected>>', self.changer_couleur)
        self.comboTheme['values'] = optionTheme

        # Bouton pour annuler le coup précédent
        self.coupPrecedent = Button(self.widget_configuration, text='Annuler Coup', command=self.annuler_coup)
        self.coupPrecedent.grid(row=5, column=0)
        # tour courant
        self.tour_courant = Label(self.widget_configuration, text='Couleur joueur courant :\n' + str(self.partie.couleur_joueur_courant))
        self.tour_courant.grid(row=1, column=0)

        # Ajout etiquette peut faire prise
        self.faire_prise = Label(self.widget_configuration)
        self.faire_prise.grid(row=2, column=0)

        #Liste position source valide
        self.position_source_valide = Label(self.widget_configuration, text='Position source valide :\n' + str(self.partie.liste_position_source_valide))
        self.position_source_valide.grid(row=3, column=0)

        # bouton sauvegarde
        self.bouton_sauvegarde = Button(self.widget_configuration, text="Sauvegarde", command=self.sauvegarder_partie)
        self.bouton_sauvegarde.grid(row=5, column=1)

        # bouton charger
        self.bouton_charger = Button(self.widget_configuration, text="Charger", command=self.charger_partie)
        self.bouton_charger.grid(row=6, column=0)

        # bouton quitter
        self.bouton_quitter = Button(self.widget_configuration, text="Quitter", command=self.quit)
        self.bouton_quitter.grid(row=7, column=0, sticky=S)

        # Création du canvas damier.
        self.canvas_damier = CanvasDamier(self, self.partie.damier, 60)
        self.canvas_damier.grid(column=0, row=0)
        self.canvas_damier.bind('<Button-1>', self.selectionner)

        # Ajout d'une étiquette d'information.
        self.messages = Label(self)
        self.messages.grid()


        # Nom de la fenêtre («title» est une méthode de la classe de base «Tk»)
        self.title("Jeu de dames")

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)




    def selectionner(self, event):
        """Méthode qui gère le clic de souris sur le damier.

        Args:
            event (tkinter.Event): Objet décrivant l'évènement qui a causé l'appel de la méthode.

        """

        # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
        ligne = event.y // self.canvas_damier.n_pixels_par_case
        colonne = event.x // self.canvas_damier.n_pixels_par_case
        position = Position(ligne, colonne)

        self.liste_position.append(position)

        # On récupère l'information sur la pièce à l'endroit choisi.
        piece = self.partie.damier.recuperer_piece_a_position(self.liste_position[0])



        if piece is None:
            self.messages['foreground'] = 'red'
            self.messages['text'] = 'Erreur: Aucune pièce à cet endroit.'
        elif piece is not None and len(self.liste_position) == 1:
            self.messages['foreground'] = 'black'
            self.messages['text'] = 'Pièce sélectionnée à la position {}.'.format(position)
        else:
            self.messages['foreground'] = 'black'
            self.messages['text'] = 'Déplacement effectué'





        if len(self.liste_position) == 2:
            self.tour()
            self.canvas_damier.actualiser()
            self.liste_position = []


    def tour(self):
        """Méthode qui gère les tours du jeu de dame et met à jour les informations de la partie.

                """
    # Détermine si le joueur courant a la possibilité de prendre une pièce adverse.

        # Verification des positions
        try:
            # Effectuer le déplacement (à l'aide de la méthode du damier appropriée)
            position_source, position_cible = self.partie.verification_positions_deplacement(self.liste_position[0], self.liste_position[1])
            resultat_deplacement = self.canvas_damier.damier.deplacer(position_source, position_cible)
            self.coupPrecedent['state'] = NORMAL

            self.coup_precedent = self.liste_position

            if resultat_deplacement == 'prise':
                self.coupPrecedent['state'] = DISABLED

            if resultat_deplacement == "erreur":
                self.messages['foreground'] = 'red'
                self.messages['text'] = "Une erreur s'est produite lors du déplacement."
                self.liste_position = []
                return

            if resultat_deplacement == "prise" and self.canvas_damier.damier.piece_peut_faire_une_prise(
                    position_cible):
                self.partie.doit_prendre = True
                self.partie.position_source_forcee = position_cible

            elif self.partie.couleur_joueur_courant == "blanc":
                self.partie.couleur_joueur_courant = "noir"
                self.partie.position_source_forcee = None
            else:
                self.partie.couleur_joueur_courant = "blanc"
                self.partie.position_source_forcee = None

            damier = []

            for position in self.partie.damier.cases:
                damier.append(position)


            if self.partie.damier.piece_de_couleur_peut_faire_une_prise(self.partie.couleur_joueur_courant):
                for une_position in range(len(damier)):
                    if self.partie.damier.piece_peut_faire_une_prise(damier[une_position]):
                        pos_source = damier[une_position]
                        position_valide = []

                        position_valide = np.asarray(self.position_saut(pos_source))
                        for saut in range(len(position_valide)):

                            if self.partie.damier.piece_peut_sauter_vers(pos_source, position_valide[saut]):
                                self.partie.damier.deplacer(pos_source, position_valide[saut])
                                self.canvas_damier.actualiser()
                                self.messages['foreground'] = 'black'
                                self.messages['text'] = 'Coup Automatique'
                                if self.partie.couleur_joueur_courant == 'blanc':
                                    self.partie.couleur_joueur_courant = 'noir'
                                elif self.partie.couleur_joueur_courant == 'noir':
                                    self.partie.couleur_joueur_courant = 'blanc'

                            self.coupPrecedent['state'] = DISABLED





        except TypeError:
            self.messages['foreground'] = 'red'
            self.messages['text'] = "Deplacement impossible"
        except AttributeError:
            self.messages['foreground'] = 'red'
            self.messages['text'] = "Deplacement impossible"


        # Mettre à jour les attributs de la classe et les affichages

        self.partie.doit_prendre = False
        if self.canvas_damier.damier.piece_de_couleur_peut_faire_une_prise(self.partie.couleur_joueur_courant):
            self.partie.doit_prendre = True

         # faire une prise
        if self.partie.doit_prendre == True and self.partie.position_source_forcee is not None:
            self.faire_prise['text'] = " Doit prendre avec la pièce en position {}.".format(self.partie.position_source_forcee)
        elif self.partie.doit_prendre == True:
            self.faire_prise['text'] = "Vous devez faire une prise"
        else:
            self.faire_prise['text'] = ''



        self.messages['foreground'] = 'black'
        self.tour_courant['text'] = 'Couleur joueur courant :\n' + str(self.partie.couleur_joueur_courant)

        self.liste_position = []
        self.actualiser_position_source_valide()


    def creer_nouvelle_partie(self):
        """Méthode qui effectue la fermeture du jeu.

                """
        self.destroy()
        self.__init__()


    def actualiser_position_source_valide(self):
        """Méthode qui actualise l'affichage de ou des positions sources valides pour le tour.

                        """
        self.partie.liste_position_source_valide = []

        if self.partie.position_source_forcee is not None:
            self.partie.liste_position_source_valide.append(self.partie.position_source_forcee)

        elif self.partie.doit_prendre == True:
            for position in self.partie.damier.cases:
                if self.partie.damier.cases[position].couleur == self.partie.couleur_joueur_courant and self.partie.damier.piece_peut_faire_une_prise(position):
                    self.partie.liste_position_source_valide.append(position)

        else:
            for position in self.partie.damier.cases:
                if self.partie.damier.cases[position].couleur == self.partie.couleur_joueur_courant and self.partie.damier.piece_peut_se_deplacer(position):
                    self.partie.liste_position_source_valide.append(position)

        self.position_source_valide['foreground'] = 'black'
        self.position_source_valide['text'] = 'Position source valide :\n' + str(self.partie.liste_position_source_valide)


    def sauvegarder_partie(self):
        """Méthode qui sauvegarde la partie dans un fichier .txt.

                        """

        # Ouverture en ecriture
        f_1 = open('sauvegarde.txt', 'w')
        f_1.write(str(self.partie.doit_prendre)+'\n')
        f_1.write(str(self.partie.position_source_forcee)+'\n')
        f_1.write(self.partie.couleur_joueur_courant+'\n')
        f_1.write(str(self.partie.liste_position_source_valide)+'\n')
        for position in self.partie.damier.cases:
            f_1.write(str(position.ligne)+'\n')
            f_1.write(str(position.colonne)+'\n')
            f_1.write(self.partie.damier.cases[position].couleur+'\n')
            f_1.write(self.partie.damier.cases[position].type_de_piece+'\n')

        # Fermeture
        f_1.close()

    def charger_partie(self):
        """Méthode qui charge la partie à partir du fichier .txt sauvegarder et ensuite actualise les affichages.

                                """

        #Ouverture en lecture
        f_1 = open('sauvegarde.txt', 'r')

        #chargement des information relative a la partie sauvegarde
        doit_prendre = f_1.readlines(1)[0].rstrip('\n')
        if doit_prendre == 'False':
            doit_prendre = False
        else:
            doit_prendre = True
        self.partie.doit_prendre = doit_prendre

        position_source_forcee = f_1.readlines(1)[0].rstrip('\n')
        if position_source_forcee == 'None':
            position_source_forcee = None
        else:
            position_source_forcee = Position(int(position_source_forcee[1:2]), int(position_source_forcee[4:5]))
        self.partie.position_source_forcee = position_source_forcee

        self.partie.couleur_joueur_courant = f_1.readlines(1)[0].rstrip('\n')

        liste_position_source_valide_texte = f_1.readlines(1)[0].rstrip("\n").strip('][')
        liste_nombre = []
        for element in liste_position_source_valide_texte:
            try:
                liste_nombre.append(int(element))
            except:
                pass
        nombre_position = len(liste_nombre)/2
        i = 0
        liste_position_source_valide = []
        while (i<nombre_position):
            liste_position_source_valide.append(Position(liste_nombre[i*2], liste_nombre[i*2+1]))
            i += 1
        self.partie.liste_position_source_valide = liste_position_source_valide

        #chargement du damier sauvegarder
        damier_temporaire = {}
        liste_damier = f_1.readlines()
        nombre_de_piece = len(liste_damier)/4
        i = 0
        while(i < nombre_de_piece):
            ligne = liste_damier[i*4]
            ligne = ligne.rstrip('\n')
            colonne = liste_damier[i*4+1]
            colonne = colonne.rstrip('\n')
            couleur = liste_damier[i*4+2]
            couleur = couleur.rstrip('\n')
            type_de_piece = liste_damier[i*4+3]
            type_de_piece = type_de_piece.rstrip('\n')
            position = Position(int(ligne), int(colonne))
            piece = Piece(str(couleur), str(type_de_piece))
            damier_temporaire[position] = piece
            i+=1

        #actualisation affichage
        self.partie.damier.cases = damier_temporaire
        self.canvas_damier.actualiser()

        self.position_source_valide['foreground'] = 'black'
        self.position_source_valide['text'] = self.partie.liste_position_source_valide

        self.messages['foreground'] = 'black'
        self.tour_courant['text'] = self.partie.couleur_joueur_courant

        #Fermeture
        f_1.close()

    def changer_couleur(self,event):
        '''
        Permet de faire changer la couleur à l'aide d'un combobox
        paramètre: event:

        '''
        couleur = self.comboTheme.get()
        if couleur == 'rouge':
            couleur = 'red'
        elif couleur == 'vert':
            couleur = 'green'
        elif couleur == 'bleu':
            couleur = 'blue'
        self.canvas_damier.dessiner_cases(couleur)
        self.canvas_damier.couleur = couleur
        self.canvas_damier.dessiner_pieces()
    def annuler_coup(self):
        '''
        Permet d'annuler le coup précédent quand le bouton est cliqué

        '''


        piece = self.partie.damier.recuperer_piece_a_position(self.coup_precedent[1])


        self.partie.damier.cases[self.coup_precedent[0]] = piece
        del self.partie.damier.cases[self.coup_precedent[1]]
        self.canvas_damier.actualiser()
        self.coupPrecedent['state'] = DISABLED

        if self.partie.couleur_joueur_courant == 'blanc':
            self.partie.couleur_joueur_courant = 'noir'
            self.tour_courant['text'] = 'noir'
        elif self.partie.couleur_joueur_courant == 'noir':
            self.partie.couleur_joueur_courant = 'blanc'
            self.tour_courant['text'] = 'blanc'
        self.coup_precedent.clear()
    def position_saut(self,position):
        '''
        Permet de me donner les sauts possibles à l'aide d'une position donnée
        :param position:
        :return: liste: position_valide
        '''
        position_valide = []
        for saut in range(len(position.quatre_positions_sauts())):
            if  self.partie.damier.position_est_dans_damier(position.quatre_positions_sauts()[saut]):
                position_valide.append(position.quatre_positions_sauts()[saut])

        return position_valide





if __name__ == '__main__':
    # Point d'entrée principal du TP4.
    fenetre = FenetrePartie()
    fenetre.mainloop()
