import pygame
import sys
from spielfigur import Gegner, Spielfigur

pygame.init() # Pygame initialisieren, um Fehler zu vermeiden
info = pygame.display.Info() # Bildschirmgröße ermitteln 
screen = pygame.display.set_mode((1920, 1080), pygame.SCALED | pygame.FULLSCREEN) # Bildschirm erstellen, im Vollbildmodus und skaliert, damit es auf jedem Bildschirm funktioniert
hintergrund = pygame.image.load("Spiel/Figur/png/background.png").convert() # Hintergrundbild laden und an Bildschirmgröße anpassen
clock = pygame.time.Clock()
pygame.display.set_caption("Pygame Tutorial")

def zeichnen():
    screen.blit(hintergrund, (0,0))
    for k in spieler1.kugeln:
        k.zeichnen()
    pygame.draw.rect(screen, (255,0,0), zombie.hitbox, 5)
    pygame.draw.rect(screen, (0,0,0), spieler1.hitbox, 5)
    #for p in plattformen:
    #    p.pzeichnen()
    zombie.gegnerImage()
    spieler1.spielerImage()
    pygame.display.update()

linkeWand = pygame.draw.rect(screen, (0,0,0), (0,0,2,1100), 0)
rechteWand = pygame.draw.rect(screen, (0,0,0), (1914,0,2,1100), 0)
spieler1 = Spielfigur(screen, 200, 730, 320.5, 271, [0,0,1,0], 10)
zombie = Gegner(screen, "Nahkampf", 1800, 700, 100, 1850, 137.25, 290.25, [1,0,0,0], 3, 6, [pygame.image.load("Spiel/Figur/png/Walk1.png"), pygame.image.load("Spiel/Figur/png/Walk2.png"), pygame.image.load("Spiel/Figur/png/Walk3.png"), pygame.image.load("Spiel/Figur/png/Walk4.png"), pygame.image.load("Spiel/Figur/png/Walk5.png"), pygame.image.load("Spiel/Figur/png/Walk6.png")], [], [], ["Spiel/Figur/png/Dead1.png", "Spiel/Figur/png/Dead2.png", "Spiel/Figur/png/Dead3.png", "Spiel/Figur/png/Dead4.png", "Spiel/Figur/png/Dead5.png", "Spiel/Figur/png/Dead6.png", "Spiel/Figur/png/Dead7.png", "Spiel/Figur/png/Dead8.png"], ["Spiel/Figur/png/Hurt1.png", "Spiel/Figur/png/Hurt2.png", "Spiel/Figur/png/Hurt3.png", "Spiel/Figur/png/Hurt4.png", "Spiel/Figur/png/Hurt5.png"])
verloren = False
gewonnen = False
#plattformen = [Plattform(200, 300, plattformBild), Plattform(600, 350, plattformBild)]
go = True

while go:
    # print(clock.get_fps())
    # print(pygame.mouse.get_pos())
    # print(info.current_w, info.current_h)

    for event in pygame.event.get(): # eingaben, die über das Spielefenster kommen
        if event.type == pygame.QUIT: # braucht man, um spiel schließen zu können
            sys.exit()
 
    gedrueckt = pygame.key.get_pressed() # hier werden die Tasten funktionalisiert

    if gedrueckt[pygame.K_a] and not spieler1.hitbox.colliderect(linkeWand) and not spieler1.dead:
        spieler1.laufen([1,0])
    elif gedrueckt[pygame.K_d] and not spieler1.hitbox.colliderect(rechteWand) and not spieler1.dead:
        spieler1.laufen([0,1])
    else:
        spieler1.stehen()
    
    if gedrueckt[pygame.K_SPACE] and not spieler1.sprung and not spieler1.dead:
        spieler1.startSprung()
    spieler1.updateSprung()

    spieler1.kugelverhalten()

    if gedrueckt[pygame.K_f]:
        if len(spieler1.kugeln) <=2:
            spieler1.schiessen()
            spieler1.ok = False

    if not gedrueckt[pygame.K_f]:
        spieler1.ok = True
        
    zombie.bewegen()
    zombie.Bewegungsregler()
    spieler1.trefferCheck(zombie)

    zeichnen()
    clock.tick(60)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()