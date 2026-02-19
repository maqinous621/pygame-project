import pygame

class Gegner:
    def __init__(self, screen, gegnerArt, x, y, xMin, xMax, breite, hoehe, richtung, geschwindigkeit, leben, laufAnimation = [], standAnimation = [], sprungAnimation = [], totAnimation = [], trefferAnimation = []):
        self.screen = screen
        self.gegnerArt = gegnerArt
        self.x = x
        self.y = y 
        self.xMin = xMin
        self.xMax = xMax
        self.breite = breite
        self.hoehe = hoehe
        self.richtung = richtung
        self.geschwindigkeit = geschwindigkeit
        self.leben = leben
        self.laufAnimation = laufAnimation
        self.standAnimation = standAnimation
        self.sprungAnimation = sprungAnimation
        self.totAnimation = totAnimation
        self.trefferAnimation = trefferAnimation
        self.laufIndex = 0
        self.standIndex = 0 
        self.sprungIndex = 0
        self.totIndex = 0
        self.trefferIndex = 0
        self.herzen = [pygame.image.load("PNG/leben/voll.png"), pygame.image.load("PNG/leben/halb.png"), pygame.image.load("PNG/leben/leer.png")]
        self.hitbox = pygame.Rect(self.x, self.y, self.breite, self.hoehe)
        self.sprung = False
        self.dead = False
        self.go = True
        self.last = [1,0] #Letzte Richtung

    def bewegen(self):
        if self.gegnerArt == "Nahkampf":
            if self.richtung == [1,0,0,0]: # Links
                self.x -= self.geschwindigkeit
                self.last = [1,0]
                self.laufIndex += 1
            elif self.richtung == [0,1,0,0]: # Rechts
                self.x += self.geschwindigkeit
                self.last = [0,1]
                self.laufIndex += 1
        elif self.gegnerArt == "Fernkampf":
            pass
        elif self.gegnerArt == "Fliegend":
            pass
        elif self.gegnerArt == "Boss":
            pass

    def Bewegungsregler(self):
        if self.x <= self.xMin:
            self.richtung = [0,1,0,0]
            self.laufIndex = 0
        elif self.x >= self.xMax:
            self.richtung = [1,0,0,0]
            self.laufIndex = 0

    def gegnerImage(self):
        if self.gegnerArt == "Nahkampf":
            if self.laufIndex >= len(self.laufAnimation) ** 2 - 1: 
                self.laufIndex = 0
            if self.richtung == [1,0,0,0]: # Links
                self.screen.blit(pygame.transform.flip(pygame.transform.scale(self.laufAnimation[self.laufIndex//len(self.laufAnimation)], (self.breite, self.hoehe)), True, False), (self.x, self.y))
            elif self.richtung == [0,1,0,0]: # Rechts
                self.screen.blit(pygame.transform.scale(self.laufAnimation[self.laufIndex//len(self.laufAnimation)], (self.breite, self.hoehe)), (self.x, self.y))
        elif self.gegnerArt == "Fernkampf":
            pass
        elif self.gegnerArt == "Fliegend":
            pass
        elif self.gegnerArt == "Boss":
            pass

        # Herzenanzeige
        #VOLL
        if self.leben >= 2:
            self.screen.blit(self.herzen[0], (self.x - 25,self.y-70))
        if self.leben >= 4:
            self.screen.blit(self.herzen[0], (self.x + 37,self.y-70))
        if self.leben == 6:
            self.screen.blit(self.herzen[0], (self.x + 99,self.y-70))
        #HALB
        if self.leben == 1:
            self.screen.blit(self.herzen[1], (self.x - 25,self.y-70))
        elif self.leben == 3:
            self.screen.blit(self.herzen[1], (self.x + 37,self.y-70))
        if self.leben == 5:
            self.screen.blit(self.herzen[1], (self.x + 99,self.y-70))
        #LEER
        if self.leben <= 0:
            self.screen.blit(self.herzen[2], (self.x - 25,self.y-70))
        if self.leben <= 2:
            self.screen.blit(self.herzen[2], (self.x + 37,self.y-70))
        if self.leben <= 4:
            self.screen.blit(self.herzen[2], (self.x + 99,self.y-70))
        


        