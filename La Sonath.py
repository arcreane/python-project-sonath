import pygame
import sys
import GreenButton
import Sliperry
import aMaZengineers

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)

# Classe de progression (peut être utilisée pour suivre l'avancée dans les jeux)
class Progression:
    def __init__(self):
        self.niveau = 0

    def avancer(self):
        self.niveau += 1

# Menu principal
class MenuPrincipal:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.progression = Progression()
        self.font = pygame.font.Font(None, 48)
        self.button_font = pygame.font.Font(None, 32)
        self.button_width = 250
        self.button_height = 60
        self.button_x = (screen.get_width() - self.button_width) // 2
        self.button_spacing = 80
        self.buttons = {
            "GreenButton": (self.button_x, 150, self.lancer_jeu1),
            "Sliperry": (self.button_x, 150 + self.button_spacing, self.lancer_jeu2),
            "aMaZengineers": (self.button_x, 150 + 2 * self.button_spacing, self.lancer_jeu3),
            "Quitter": (self.button_x, 150 + 3 * self.button_spacing, self.quitter)
        }

    def lancer_jeu1(self):
        GreenButton.jouer_jeu1(self.screen, self.clock, self.progression, self.afficher_menu)

    def lancer_jeu2(self):
        Sliperry.jouer_jeu2(self.screen, self.clock, self.progression, self.afficher_menu)

    def lancer_jeu3(self):
        aMaZengineers.jouer_jeu3(self.screen, self.clock, self.progression, self.afficher_menu)

    def quitter(self):
        pygame.quit()
        sys.exit()

    def afficher_menu(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitter()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for text, (x, y, action) in self.buttons.items():
                        if x <= mouse_pos[0] <= x + self.button_width and y <= mouse_pos[1] <= y + self.button_height:
                            action()

            self.screen.fill(GRAY)

            # Affichage du titre
            title_text = self.font.render("Menu des Jeux", True, BLACK)
            title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 60))
            self.screen.blit(title_text, title_rect)

            # Affichage des boutons
            for text, (x, y, _) in self.buttons.items():
                pygame.draw.rect(self.screen, BLACK, (x, y, self.button_width, self.button_height), 2)
                button_text = self.button_font.render(text, True, BLACK)
                button_rect = button_text.get_rect(center=(x + self.button_width // 2, y + self.button_height // 2))
                self.screen.blit(button_text, button_rect)

            pygame.display.flip()
            self.clock.tick(60)

# Point d'entrée du programme
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Menu Principal")
    clock = pygame.time.Clock()

    menu = MenuPrincipal(screen, clock)
    menu.afficher_menu()
