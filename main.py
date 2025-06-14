import pygame
import sys
import random
import tkinter as tk
from tkinter import simpledialog
from database import enregistrer_score  # Ton fichier database.py doit exister

from ia import minmax
from logique import mouvements_possibles, pion_adverse
pygame.init()
                            #reste le Koul
ia_active = False
niveau_ia = 1  # 1 = facile, 2 = moyen, 3 = difficile
menu_actif = True

# Constantes
TAILLE_CASE = 60
LARGEUR = TAILLE_CASE * 10
HAUTEUR_TITRE = 30
HAUTEUR = TAILLE_CASE * 10 + HAUTEUR_TITRE
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Dames Marocaines")

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
BEIGE = (245, 245, 220)
MARRON = (139, 69, 19)
VERT = (0, 255, 0, 150)
ROUGE = (255, 0, 0, 150)
BLEU_CIEL = (135, 206, 250)
COULEUR_TITRE = (50, 50, 50)
FOND_TITRE = (240, 240, 240)

# Police
font_titre = pygame.font.Font(None, 24)
font_fin = pygame.font.Font(None, 48)
font_menu = pygame.font.Font(None, 36)

# Variables globales
plateau = [[None for _ in range(10)] for _ in range(10)]
joueur_actuel = 'noir'
pion_selectionne = None
deplacements_valides = []
partie_terminee = False
gagnant = None

def initialiser_plateau():
    global partie_terminee, gagnant
    partie_terminee = False
    gagnant = None
    for ligne in range(10):
        for colonne in range(10):
            if (ligne + colonne) % 2 == 1:
                if ligne < 4:
                    plateau[ligne][colonne] = 'noir'
                elif ligne >= 6:
                    plateau[ligne][colonne] = 'blanc'
                else:
                    plateau[ligne][colonne] = None
            else:
                plateau[ligne][colonne] = None

def compter_pieces():
    """Compte les pièces de chaque joueur"""
    pieces_noir = 0
    pieces_blanc = 0
    
    for ligne in range(10):
        for colonne in range(10):
            pion = plateau[ligne][colonne]
            if pion is not None:
                if 'noir' in pion:
                    pieces_noir += 1
                elif 'blanc' in pion:
                    pieces_blanc += 1
    
    return pieces_noir, pieces_blanc

def joueur_peut_jouer(couleur):
    """Vérifie si le joueur a des mouvements possibles"""
    for ligne in range(10):
        for colonne in range(10):
            pion = plateau[ligne][colonne]
            if pion is not None and couleur in pion:
                if mouvements_possibles(plateau, ligne, colonne):
                    return True
    return False

def verifier_fin_partie():
    """Vérifie si la partie est terminée"""
    global partie_terminee, gagnant
    
    pieces_noir, pieces_blanc = compter_pieces()
    
    # Vérifier si un joueur n'a plus de pièces
    if pieces_noir == 0:
        partie_terminee = True
        gagnant = 'blanc'
        return True
    elif pieces_blanc == 0:
        partie_terminee = True
        gagnant = 'noir'
        return True
    
    # Vérifier si le joueur actuel ne peut pas jouer
    if not joueur_peut_jouer(joueur_actuel):
        partie_terminee = True
        gagnant = 'blanc' if joueur_actuel == 'noir' else 'noir'
        return True
    
    return False

def est_prise(depart, arrivee):
    l1, c1 = depart
    l2, c2 = arrivee
    return abs(l2 - l1) >= 2 and abs(c2 - c1) >= 2

def case_est_noire(ligne, colonne):
    return (ligne + colonne) % 2 == 1

def pion_adverse(pion, autre_pion):
    if pion is None or autre_pion is None:
        return False
    couleur = pion.replace('_dame', '')
    autre_couleur = autre_pion.replace('_dame', '')
    return couleur != autre_couleur

def prises_possibles_pour_joueur(couleur):
    prises = []
    for l in range(10):
        for c in range(10):
            pion = plateau[l][c]
            if pion is not None and couleur in pion:
                for deplacement in mouvements_possibles(plateau, l, c):
                    if est_prise((l, c), deplacement):
                        prises.append((l, c))
    return prises

def ia_jouer():
    from ia import minmax

    meilleur_coup = minmax(plateau, niveau_ia, True)[1]
    if meilleur_coup:
        dep, arr = meilleur_coup
        effectuer_deplacement(dep, arr, prises_possibles_pour_joueur("blanc"))
    else:
        print("IA ne trouve aucun coup.")

def effectuer_deplacement(depart, arrivee, prises_avant):
    global joueur_actuel, pion_selectionne, deplacements_valides

    l1, c1 = depart
    l2, c2 = arrivee
    pion = plateau[l1][c1]
    est_dame = '_dame' in pion

    # Si déplacement est une prise, enlever la ou les pièces capturées
    if est_prise(depart, arrivee):
        if est_dame:
            # Pour les sultans, capturer tous les pions adverses sur le chemin
            dl = 1 if l2 > l1 else -1
            dc = 1 if c2 > c1 else -1
            
            # Parcourir tout le chemin de départ à arrivée
            l_actuelle = l1 + dl
            c_actuelle = c1 + dc
            
            while l_actuelle != l2 or c_actuelle != c2:
                if plateau[l_actuelle][c_actuelle] is not None and pion_adverse(pion, plateau[l_actuelle][c_actuelle]):
                    plateau[l_actuelle][c_actuelle] = None  # Capturer le pion adverse
                l_actuelle += dl
                c_actuelle += dc
            
            # Capturer aussi le pion sur la case d'arrivée s'il y en a un
            if plateau[l2][c2] is not None and pion_adverse(pion, plateau[l2][c2]):
                plateau[l2][c2] = None
        else:
            # Pour les pions normaux, capturer seulement le pion sauté
            l_capt = (l1 + l2) // 2
            c_capt = (c1 + c2) // 2
            plateau[l_capt][c_capt] = None

    plateau[l2][c2] = pion
    plateau[l1][c1] = None

    # Promotion en sultan (dame)
    if pion == 'noir' and l2 == 9:
        plateau[l2][c2] = 'noir_dame'
    elif pion == 'blanc' and l2 == 0:
        plateau[l2][c2] = 'blanc_dame'

    # Règle du Pion Neffakh
    if prises_avant and not est_prise(depart, arrivee):
        for l, c in prises_avant:
            if plateau[l][c] is not None and joueur_actuel in plateau[l][c]:
                plateau[l][c] = None
                break

    # Changement de joueur
    joueur_actuel = 'blanc' if joueur_actuel == 'noir' else 'noir'
    pion_selectionne = None
    deplacements_valides.clear()
    
    # Vérifier si la partie est terminée
    verifier_fin_partie()
    # Juste après le déplacement du joueur
    if ia_active and joueur_actuel == "blanc" and not partie_terminee:
        ia_jouer()


def dessiner_plateau():
    pygame.draw.rect(screen, FOND_TITRE, (0, 0, LARGEUR, HAUTEUR_TITRE))
    
    if partie_terminee:
            texte = font_titre.render(f"PARTIE TERMINÉE - {gagnant.upper()} GAGNE!", True, COULEUR_TITRE)
            x_centre = (LARGEUR - texte.get_width()) // 2
            screen.blit(texte, (x_centre, 5))
    else:
        pieces_noir, pieces_blanc = compter_pieces()
        texte_tour = font_titre.render(f"Tour: {joueur_actuel.upper()} | Noir: {pieces_noir} | Blanc: {pieces_blanc}", True, COULEUR_TITRE)
        x_centre_tour = (LARGEUR - texte_tour.get_width()) // 2
        screen.blit(texte_tour, (x_centre_tour, 2))

        couleur_adverse = 'blanc' if joueur_actuel == 'noir' else 'noir'
        prises_adverses = prises_possibles_pour_joueur(couleur_adverse)

        if prises_adverses:
            texte_koul = font_titre.render("Appuie sur 'K' pour forcer une prise (Koul)", True, (80, 80, 80))
            x_centre_koul = (LARGEUR - texte_koul.get_width()) // 2
            screen.blit(texte_koul, (x_centre_koul, 16))


    s_vert = pygame.Surface((TAILLE_CASE, TAILLE_CASE), pygame.SRCALPHA)
    s_vert.fill(VERT)
    s_rouge = pygame.Surface((TAILLE_CASE, TAILLE_CASE), pygame.SRCALPHA)
    s_rouge.fill(ROUGE)

    for ligne in range(10):
        for colonne in range(10):
            x = colonne * TAILLE_CASE
            y = HAUTEUR_TITRE + ligne * TAILLE_CASE

            couleur_case = MARRON if case_est_noire(ligne, colonne) else BEIGE
            pygame.draw.rect(screen, couleur_case, (x, y, TAILLE_CASE, TAILLE_CASE))

            if not partie_terminee and pion_selectionne is not None and (ligne, colonne) in deplacements_valides:
                if est_prise(pion_selectionne, (ligne, colonne)):
                    screen.blit(s_rouge, (x, y))
                else:
                    screen.blit(s_vert, (x, y))

            pion = plateau[ligne][colonne]
            if pion is not None:
                couleur_pion = NOIR if 'noir' in pion else BLANC
                centre_x = x + TAILLE_CASE // 2
                centre_y = y + TAILLE_CASE // 2
                pygame.draw.circle(screen, couleur_pion, (centre_x, centre_y), TAILLE_CASE // 3)
                if '_dame' in pion:
                    # Couronne pour les sultans
                    pygame.draw.rect(screen, (255, 215, 0), (centre_x - 8, centre_y + 5, 16, 4))
                    pygame.draw.polygon(screen, (255, 215, 0), [(centre_x, centre_y - 6), (centre_x - 3, centre_y + 5), (centre_x + 3, centre_y + 5)])
                    pygame.draw.polygon(screen, (255, 215, 0), [(centre_x - 6, centre_y - 3), (centre_x - 9, centre_y + 5), (centre_x - 3, centre_y + 5)])
                    pygame.draw.polygon(screen, (255, 215, 0), [(centre_x + 6, centre_y - 3), (centre_x + 3, centre_y + 5), (centre_x + 9, centre_y + 5)])

    if not partie_terminee and pion_selectionne is not None:
        l, c = pion_selectionne
        x = c * TAILLE_CASE
        y = HAUTEUR_TITRE + l * TAILLE_CASE
        pygame.draw.rect(screen, BLEU_CIEL, (x, y, TAILLE_CASE, TAILLE_CASE), 3)

def dessiner_ecran_fin():
    """Dessine l'écran de fin de partie avec menu"""
    # Fond semi-transparent
    overlay = pygame.Surface((LARGEUR, HAUTEUR))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    # Message de victoire
    texte_victoire = font_fin.render(f"{gagnant.upper()} GAGNE!", True, BLANC)
    rect_victoire = texte_victoire.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 100))
    screen.blit(texte_victoire, rect_victoire)
    
    pieces_noir, pieces_blanc = compter_pieces()
    texte_score = font_menu.render(f"Score final - Noir: {pieces_noir} | Blanc: {pieces_blanc}", True, BLANC)
    rect_score = texte_score.get_rect(center=(LARGEUR//2, HAUTEUR//2 - 50))
    screen.blit(texte_score, rect_score)

    
    # Boutons
    bouton_rejouer = pygame.Rect(LARGEUR//2 - 100, HAUTEUR//2 + 20, 200, 50)
    bouton_quitter = pygame.Rect(LARGEUR//2 - 100, HAUTEUR//2 + 90, 200, 50)
    
    # Dessiner boutons
    pygame.draw.rect(screen, VERT, bouton_rejouer)
    pygame.draw.rect(screen, ROUGE, bouton_quitter)
    pygame.draw.rect(screen, BLANC, bouton_rejouer, 2)
    pygame.draw.rect(screen, BLANC, bouton_quitter, 2)
    
    # Texte des boutons
    texte_rejouer = font_menu.render("REJOUER", True, BLANC)
    rect_rejouer = texte_rejouer.get_rect(center=bouton_rejouer.center)
    screen.blit(texte_rejouer, rect_rejouer)
    
    texte_quitter = font_menu.render("QUITTER", True, BLANC)
    rect_quitter = texte_quitter.get_rect(center=bouton_quitter.center)
    screen.blit(texte_quitter, rect_quitter)
    
    return bouton_rejouer, bouton_quitter

def dessiner_menu():
    screen.fill((230, 230, 230))  # fond gris foncé

    titre = font_fin.render("Choisissez le niveau de l'IA", True, (0, 0, 0))
    screen.blit(titre, ((LARGEUR - titre.get_width()) // 2, 60))

    boutons = []
    niveaux = [("Facile", 1), ("Moyen", 2), ("Difficile", 3)]

    for i, (texte, niveau) in enumerate(niveaux):
        rect = pygame.Rect(220, 150 + i * 100, 150, 60)
        pygame.draw.rect(screen, MARRON, rect, border_radius=15)

        font_menu = pygame.font.SysFont('Trebuchet MS', 25, bold=True)
        label = font_menu.render(texte, True, (230, 230, 230))
        screen.blit(label, (rect.x + 38, rect.y + 16))
        boutons.append((rect, niveau))

    pygame.display.flip()
    return boutons


def main():
    bouton_rejouer, bouton_quitter = None, None
    global pion_selectionne, deplacements_valides, joueur_actuel, menu_actif, ia_active, niveau_ia
    initialiser_plateau()

    while True:
        if menu_actif:
            boutons_menu = dessiner_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    for rect, niveau in boutons_menu:
                        if rect.collidepoint(x, y):
                            niveau_ia = niveau
                            ia_active = True
                            menu_actif = False
                            initialiser_plateau()
            continue  # ne pas exécuter le reste tant que le menu est affiché

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if partie_terminee:
                    x, y = pygame.mouse.get_pos()
                    bouton_rejouer, bouton_quitter = dessiner_ecran_fin()
                    if bouton_rejouer.collidepoint(x, y):
                        joueur_actuel = 'noir'
                        pion_selectionne = None
                        deplacements_valides = []
                        initialiser_plateau()
                    elif bouton_quitter.collidepoint(x, y):
                        pygame.quit()
                        sys.exit()
                else:
                    x, y = pygame.mouse.get_pos()
                    if y < HAUTEUR_TITRE:
                        continue
                    ligne = (y - HAUTEUR_TITRE) // TAILLE_CASE
                    colonne = x // TAILLE_CASE

                    if (ligne + colonne) % 2 == 0:
                        pion_selectionne = None
                        deplacements_valides = []
                        continue

                    if pion_selectionne is not None and (ligne, colonne) in deplacements_valides:
                        prises_avant = prises_possibles_pour_joueur(joueur_actuel)
                        effectuer_deplacement(pion_selectionne, (ligne, colonne), prises_avant)
                    elif plateau[ligne][colonne] is not None and joueur_actuel in plateau[ligne][colonne]:
                        pion_selectionne = (ligne, colonne)
                        deplacements_valides = mouvements_possibles(plateau, ligne, colonne)
                    else:
                        pion_selectionne = None
                        deplacements_valides = []

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k and not partie_terminee:
                    couleur_adverse = 'blanc' if joueur_actuel == 'noir' else 'noir'
                    prises_possibles = prises_possibles_pour_joueur(couleur_adverse)
                    if prises_possibles:
                        l, c = prises_possibles[0]
                        deplacements = mouvements_possibles(plateau, l, c)
                        for dest in deplacements:
                            if est_prise((l, c), dest):
                                effectuer_deplacement((l, c), dest, prises_possibles)
                                break
                    else:
                        print("Aucune prise possible pour l'adversaire.")

        # 👇 Si IA active et c’est à elle de jouer
        if ia_active and joueur_actuel == "blanc" and not partie_terminee:
            ia_jouer()

        screen.fill(BLANC)
        dessiner_plateau()

        if partie_terminee:
            dessiner_ecran_fin()

            if not hasattr(main, "score_enregistre"):
                try:
                    pieces_noir, pieces_blanc = compter_pieces()
                    root = tk.Tk()
                    root.withdraw()
                    nom = simpledialog.askstring("Nom", "Entrez votre nom :")
                    if nom:
                        enregistrer_score(nom, pieces_noir, pieces_blanc, gagnant, niveau_ia)
                    root.destroy()
                except Exception as e:
                    print("Erreur lors de l'enregistrement :", e)
                main.score_enregistre = True



        pygame.display.flip()


if __name__ == "__main__":
    main()