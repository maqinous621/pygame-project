import pygame
import sys
from spielfigur import Spielfigur, Gegner

# Bildschirmgröße 
breite = 1920
hoehe = 1080

# Farben
schwarz = (0, 0, 0)
weiss = (255, 255, 255)
rot = (200, 50, 50)
gruen = (50, 200, 50)
grau = (100, 100, 100)

# Boden-Y-Position (wo die Figuren stehen)
boden_y = 780

# --- Plattform-Klasse ---
class Plattform:
    # Eine Plattform auf der die Figur stehen kann

    def __init__(self, x, y, breite, hoehe, farbe=(80, 50, 20)):
        self.rect = pygame.Rect(x, y, breite, hoehe)
        self.farbe = farbe

    def zeichnen(self, screen):
        pygame.draw.rect(screen, self.farbe, self.rect)
        pygame.draw.rect(screen, schwarz, self.rect, 2)  # dünner Rahmen

