import pygame
pygame.init()
pygame.display.set_mode((1,1))

sheet = pygame.image.load("Spiel/Gegner/PNG/Flying Demon 2D Pixel Art/Sprites/without_outline/HURT.png").convert_alpha()
frameAnzahl = 4
frameBreite = sheet.get_width() // frameAnzahl
hoehe = sheet.get_height()

for i in range(frameAnzahl):
    frame = sheet.subsurface(pygame.Rect(i * frameBreite, 0, frameBreite, hoehe))
    pygame.image.save(frame, f"Spiel/Gegner/PNG/Flying Demon 2D Pixel Art/Sprites/without_outline/Hurt{i+1}.png")

print("Fertig!")