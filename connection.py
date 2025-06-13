import pygame
import sys

pygame.init()

# Constantes
LARGEUR, HAUTEUR = 600, 400
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS = (200, 200, 200)
BLEU = (70, 130, 180)

DORE = (218, 165, 32)

IVOIRE = (248, 247, 240)

# Variables globales
nom = ""
actif = False

def main():
    global nom, actif
    
    ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("DAMA")
    police = pygame.font.Font(None, 36)
    #police_titre = pygame.font.Font(None, 55)
    police_titre = pygame.font.SysFont("impact", 62)

    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Zone de clic pour activer la saisie
                rect_input = pygame.Rect(150, 200, 300, 40)
                actif = rect_input.collidepoint(event.pos)
                
            if event.type == pygame.KEYDOWN and actif:
                if event.key == pygame.K_RETURN:
                    if nom.strip():
                        print(f"Bienvenue {nom} !")  # ou faire autre chose
                elif event.key == pygame.K_BACKSPACE:
                    nom = nom[:-1]
                else:
                    if len(nom) < 15:
                        nom += event.unicode
        
        # Affichage
        ecran.fill(IVOIRE)
        
        # Titre
        titre = police_titre.render("JEU DE DAMES", True, DORE)
        ecran.blit(titre, (LARGEUR//2 - titre.get_width()//2, 50))
        
        # Label
        label = police.render("Votre nom:", True, NOIR)
        ecran.blit(label, (230, 160))
        
        # Zone de saisie
        rect_input = pygame.Rect(150, 200, 300, 40)
        couleur = BLEU if actif else GRIS
        pygame.draw.rect(ecran, couleur, rect_input, 2)
        
        # Texte saisi
        if nom:
            texte_surface = police.render(nom, True, NOIR)
            ecran.blit(texte_surface, (160, 210))
        elif not actif:
            placeholder = police.render("Cliquez ici...", True, GRIS)
            ecran.blit(placeholder, (160, 210))
            
        # Curseur
        if actif and pygame.time.get_ticks() % 1000 < 500:
            cursor_x = 160 + police.size(nom)[0]
            pygame.draw.line(ecran, NOIR, (cursor_x, 205), (cursor_x, 235), 2)
        
        # Instructions
        if not nom:
            info = police.render("Appuyez sur Entrée pour valider", True, GRIS)
            ecran.blit(info, (LARGEUR//2 - info.get_width()//2, 300))
        else:
            msg = police.render(f"Bonjour {nom}! Appuyez sur Entrée", True, BLEU)
            ecran.blit(msg, (LARGEUR//2 - msg.get_width()//2, 300))
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()