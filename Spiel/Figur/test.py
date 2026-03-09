import pygame
import sys
import os
from spielfigur import Spielfigur
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Gegner.gegner import Gegner
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
    for k in gegner.kugeln:  # <- hinzufügen
        k.zeichnen()
    # pygame.draw.rect(screen, (255,0,0), zombie.hitbox, 5)
    # pygame.draw.rect(screen, (0,0,0), spieler1.hitbox, 5)
    # pygame.draw.rect(screen, (0,255,0), zombie.kopf, 5)
    # pygame.draw.rect(screen, (0,255,0), gegner.hitbox, 5)
    # pygame.draw.rect(screen, (0,0,255), gegner.kopf, 5)
    # pygame.draw.rect(screen, (255,0,0), spieler1.hitbox, 5)
    #for p in plattformen:
    #    p.pzeichnen()
    gegner.gegnerImage()
    spieler1.spielerImage()
    pygame.display.update()

linkeWand = pygame.draw.rect(screen, (0,0,0), (0,0,2,1100), 0)
rechteWand = pygame.draw.rect(screen, (0,0,0), (1914,0,2,1100), 0)
spieler1 = Spielfigur(screen, 200, 730, 320.5, 271, [0,0,1,0], 10)
# gegner =Gegner(screen, "Fernkampf", 1700, 750, 900, 900, 200, 200, [1,0,0,0], 3, 6, "Spiel/Gegner/PNG/Wraith3/PNG Sequences/Feuerball.png", angriffAnimation=[
#     pygame.image.load(f"Spiel/Gegner/PNG/Wraith3/PNG Sequences/Casting Spells/Wraith_03_Casting Spells_{i:03d}.png")
#     for i in range(0, 18)
# ], standAnimation=[
#     pygame.image.load(f"Spiel/Gegner/PNG/Wraith3/PNG Sequences/Idle/Wraith_03_Idle_{i:03d}.png") for i in range(0, 12)]
#                , trefferAnimation=[
#     pygame.image.load(f"Spiel/Gegner/PNG/Wraith3/PNG Sequences/Hurt/Wraith_03_Hurt_{i:03d}.png") for i in range(0, 12)], 
#                totAnimation=[
#     pygame.image.load(f"Spiel/Gegner/PNG/Wraith3/PNG Sequences/Dying/Wraith_03_Dying_{i:03d}.png") for i in range(0, 15)])
gegner = Gegner(screen, "Fliegend", 900, 300, 100, 1700, 200, 200, [1,0,0,0], 3, 6,"Spiel/Gegner/PNG/Demon/Sprites/projectile.png", [pygame.image.load("Spiel/Gegner/PNG/Demon/Sprites/without_outline/Attack1.png"), pygame.image.load("Spiel/Gegner/PNG/Demon/Sprites/without_outline/Attack2.png"), pygame.image.load("Spiel/Gegner/PNG/Demon/Sprites/without_outline/Attack3.png"), pygame.image.load("Spiel/Gegner/PNG/Demon/Sprites/without_outline/Attack4.png"), pygame.image.load("Spiel/Gegner/PNG/Demon/Sprites/without_outline/Attack5.png"), pygame.image.load("Spiel/Gegner/PNG/Demon/Sprites/without_outline/Attack6.png"), pygame.image.load("Spiel/Gegner/PNG/Demon/Sprites/without_outline/Attack7.png"), pygame.image.load("Spiel/Gegner/PNG/Demon/Sprites/without_outline/Attack8.png")],
    [],  # laufAnimation
    [],  # standAnimation
    [pygame.image.load("Spiel/Gegner/PNG/Demon/Sprites/without_outline/Flying1.png"),
     pygame.image.load("Spiel/Gegner/PNG/Demon/Sprites/without_outline/Flying2.png"),
     pygame.image.load("Spiel/Gegner/PNG/Demon/Sprites/without_outline/Flying3.png"),
     pygame.image.load("Spiel/Gegner/PNG/Demon/Sprites/without_outline/Flying4.png")],  # sprungAnimation (hier Flug)
    [pygame.image.load("Spiel/Gegner/PNG/Demon/Sprites/without_outline/DEATH1.png"),
     pygame.image.load("Spiel/Gegner/PNG/Demon/Sprites/without_outline/DEATH2.png"),
     pygame.image.load("Spiel/Gegner/PNG/Demon/Sprites/without_outline/DEATH3.png"),
     pygame.image.load("Spiel/Gegner/PNG/Demon/Sprites/without_outline/DEATH4.png"),
     pygame.image.load("Spiel/Gegner/PNG/Demon/Sprites/without_outline/DEATH5.png"),
     pygame.image.load("Spiel/Gegner/PNG/Demon/Sprites/without_outline/DEATH6.png"),
     pygame.image.load("Spiel/Gegner/PNG/Demon/Sprites/without_outline/DEATH7.png")],  # totAnimation
    [pygame.image.load("Spiel/Gegner/PNG/Demon/Sprites/without_outline/Hurt1.png"),
    pygame.image.load("Spiel/Gegner/PNG/Demon/Sprites/without_outline/Hurt2.png"),
    pygame.image.load("Spiel/Gegner/PNG/Demon/Sprites/without_outline/Hurt3.png"),
    pygame.image.load("Spiel/Gegner/PNG/Demon/Sprites/without_outline/Hurt4.png")])  # trefferAnimation
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
    
    if gedrueckt[pygame.K_ESCAPE]:
        sys.exit()

    if not gedrueckt[pygame.K_f]:
        spieler1.ok = True
    
    gegner.bewegen(spieler1)
    gegner.Bewegungsregler()
    spieler1.trefferCheck(gegner)
    gegner.kugelverhalten(spieler1)

    zeichnen()
    clock.tick(60)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()