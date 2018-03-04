import pygame
from pygame import *
import random, os, time

from types import *

pygame.init()

# Initialize variables
display_width = 600
display_height = 600
HH = int(display_height/2)
HW = int(display_width/2)
FPS = 120

# Initialize colors
black = (0,0,0)
white = (255,255,255)
ltGreen = (153,255,153)
ltRed = (255, 204, 204)

homedir = os.path.dirname(__file__)
imagedir = os.path.join(homedir, "images")

gameTitle = "Olive Oil Mike"

gameDisplay = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()

pygame.display.set_caption(gameTitle)

persistentCount = 0
muPos = 0
muPosPrev = 0
musicList=os.listdir("music")
random.shuffle(musicList)


# Import background
bkIMG = pygame.image.load(os.path.join(imagedir,"background.png"))
bkIMG = bkIMG.convert()

# Import intro logo
IntroLogo = pygame.image.load(os.path.join(imagedir,"IntroLogo.png"))
IntroLogo = IntroLogo
Logorect = IntroLogo.get_rect()
hw_logo = int(Logorect.width/2)

# Import Player icon
plW = 390
plH = 490
scale = 7

PlayerSpriteRightMike = pygame.image.load(os.path.join(imagedir,"PlayerSpriteRightMike.png"))
PlayerSpriteRightMike = pygame.transform.scale(PlayerSpriteRightMike,(int(plW/scale),int(plH/scale)))
PlayerSpriteLeftMike = pygame.image.load(os.path.join(imagedir,"PlayerSpriteLeftMike.png"))
PlayerSpriteLeftMike = pygame.transform.scale(PlayerSpriteLeftMike,(int(plW/scale),int(plH/scale)))

PlayerSpriteRightGrant = pygame.image.load(os.path.join(imagedir,"PlayerSpriteRightGrant.png"))
PlayerSpriteRightGrant = pygame.transform.scale(PlayerSpriteRightGrant,(int(plW/scale),int(plH/scale)))
PlayerSpriteLeftGrant = pygame.image.load(os.path.join(imagedir,"PlayerSpriteLeftGrant.png"))
PlayerSpriteLeftGrant = pygame.transform.scale(PlayerSpriteLeftGrant,(int(plW/scale),int(plH/scale)))

PlayerSpriteRightVinny = pygame.image.load(os.path.join(imagedir,"PlayerSpriteRightVinny.png"))
PlayerSpriteRightVinny = pygame.transform.scale(PlayerSpriteRightVinny,(int(plW/scale),int(plH/scale)))
PlayerSpriteLeftVinny = pygame.image.load(os.path.join(imagedir,"PlayerSpriteLeftVinny.png"))
PlayerSpriteLeftVinny = pygame.transform.scale(PlayerSpriteLeftVinny,(int(plW/scale),int(plH/scale)))

PlayerR_mask = pygame.mask.from_surface(PlayerSpriteRightMike)
PLayerL_mask = pygame.mask.from_surface(PlayerSpriteLeftMike)

# import olive oil collectible
OilW = 548
OilH = 720
oilImg = pygame.image.load(os.path.join(imagedir,"OliveOilCollect.png"))
oilImg = pygame.transform.scale(oilImg,(int(OilW/8), int(OilH/8)))

# import rock
RockW = 640
RockH = 480
rockImg = pygame.image.load(os.path.join(imagedir,"Rock.png"))
rockImg = pygame.transform.scale(rockImg,(150,150))


# DEFINE CLASSES

class item(pygame.sprite.Sprite):

    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange( 0-self.rect.width, display_width + self.rect.width)
        self.rect.y = random.randrange(-100, -50)
        self.speedy = random.randrange(3, 10)
        self.speedx = random.randrange(-1,1)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > display_height+10 or self.rect.left+self.rect.width <0 or self.rect.right-self.rect.width>display_width:
            self.rect.x = random.randrange( 0-self.rect.width, display_width - self.rect.width)
            self.rect.y = random.randrange(-100, -50)
            self.speedy = random.randrange(3, 10)
            self.speedx = random.randrange(-1, 1)

        self.mask = pygame.mask.from_surface(self.image)


class player(pygame.sprite.Sprite):
    # sprite for the player

    PlayerSpriteLeft = PlayerSpriteLeftMike
    PlayerSpriteRight = PlayerSpriteRightMike    

    def __init__(self, velocity):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.PlayerSpriteLeft.convert_alpha()
        self.rect = self.image.get_rect()
        self.velocity = velocity
        self.rect.centerx = HW
        self.rect.centery = display_height - self.rect.height/2

    def update(self):
        k = pygame.key.get_pressed()

        if k[K_LEFT]:
            self.rect.x -= self.velocity
            self.image = self.PlayerSpriteLeft.convert_alpha()
        elif k[K_RIGHT]:
            self.rect.x += self.velocity
            self.image = self.PlayerSpriteRight.convert_alpha()

        if k[K_UP]:
            self.rect.y -= self.velocity
        elif k[K_DOWN]:
            self.rect.y += self.velocity

        if self.rect.right > display_width:
            self.rect.right = display_width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= display_height:
            self.rect.bottom = display_height

    def setMike(self):
        self.PlayerSpriteLeft = PlayerSpriteLeftMike
        self.PlayerSpriteRight = PlayerSpriteRightMike
        self.image = self.PlayerSpriteLeft.convert_alpha()

    def setGrant(self):
        self.PlayerSpriteLeft = PlayerSpriteLeftGrant
        self.PlayerSpriteRight = PlayerSpriteRightGrant
        self.image = self.PlayerSpriteLeft.convert_alpha()

    def setVinny(self):
        self.PlayerSpriteLeft = PlayerSpriteLeftVinny
        self.PlayerSpriteRight = PlayerSpriteRightVinny
        self.image = self.PlayerSpriteLeft.convert_alpha()

       # self.mask = pygame.mask.from_surface(self.image)

# ------------------------ #

def oil_count(count_oil):
    font = pygame.font.Font('freesansbold.ttf', 25)
    text = font.render("Olive Oil: "+str(count_oil),True,white)
    gameDisplay.blit(text,(0,0))

def gameQuit():
    pygame.quit()
    quit()

def text_object(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None, size=20):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",size)
    textSurf, textRect = text_object(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def message_display(text, pos):
    largeText = pygame.font.Font('freesansbold.ttf',25)
    TextSurf = largeText.render(text, True, white)
    TextRect = TextSurf.get_rect()
    TextRect.center = ((display_width/2),(display_height/2 + pos*50))
    gameDisplay.blit(TextSurf,TextRect)

    pygame.display.update()


def crash(count, count2):
    message_display("You were hit by that kid throwing rocks...", 0)
    message_display("You collected " + str(count) + " bottles...", 1)
    clock.tick(10)

    if count == count2 and count != 0:
        time.sleep(1)

    gameLoop()


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameQuit()

        gameDisplay.blit(bkIMG, (0, 0))
        gameDisplay.blit(IntroLogo,(HW-hw_logo,100))


        button("PLAY", HW-200, HH+20, 400, 50, white, ltGreen, gameLoop)
        button("CHOOSE CHARACTER", HW-200, HH+90, 400, 50, white, ltGreen, gameChar)
        button("CREDITS", HW-200, HH+160, 400, 50, white, ltGreen, gameCredits)
        button("QUIT", HW-200, HH+230, 400, 50, white, ltRed , gameQuit)

        pygame.display.update()
'''
        clock.tick(FPS)
'''

def gameLoop():

    global persistentCount
    count = 0
    gameExit = False


    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameQuit()

#MUSIC HANDLING
        global muPos
        global muPosPrev

        if len(musicList) > 0:
            if not pygame.mixer.music.get_busy():
                if muPos != muPosPrev:
                    pygame.mixer.music.play(1)
                elif muPos == muPosPrev:
                    pygame.mixer.music.load("music/" + musicList[muPos])
                    pygame.mixer.music.play(1)
                    if muPos < len(musicList) - 1:
                        muPos += 1
                    else:
                        muPos = 0
            elif muPos != muPosPrev:
                muPosPrev = muPos

        # Backgound blit
        gameDisplay.blit(bkIMG,(0,0))

        # Update
        all_sprites.update()

        # check collision
        hits = pygame.sprite.spritecollide(player, rock_sprites, False, pygame.sprite.collide_mask)
        if hits:
            crash(persistentCount, count)

        # check player collected oil
        collect = pygame.sprite.spritecollide(player, oil_sprites, True, pygame.sprite.collide_mask)
        for i in collect:
            o = item(oilImg)
            all_sprites.add(o)
            oil_sprites.add(o)
            count += 1

        persistentCount = count
        # Draw / Render
        all_sprites.draw(gameDisplay)
        oil_count(count)

        pygame.display.update()

        clock.tick(FPS)


def gameChar():
    time.sleep(.5)
    char = True

    while char:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameQuit()

        gameDisplay.blit(bkIMG, (0, 0))
        gameDisplay.blit(IntroLogo,(HW-hw_logo,100))

        button("MIKE (THE GOOD BOY)", HW-200, HH+20, 400, 50, white, ltGreen, setMike)
        button("VINNY (EYY, BROOKLYN)", HW-200, HH+90, 400, 50, white, ltRed , setVinny)
        button("GRANT (NOT THIS ONE)", HW-200, HH+160, 400, 50, white, ltRed , setGrant)

        pygame.display.update()

def gameCredits():
    time.sleep(.5)
    char = True

    while char:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameQuit()

        gameDisplay.blit(bkIMG, (0, 0))
        gameDisplay.blit(IntroLogo,(HW-hw_logo,100))

        button("Candy-Colored Sky by  Catmosphere (Creative Commons)", HW-250, HH+20, 500, 50, white, ltGreen, None, 14)
#        button("Steamshovel Harry by Brad Sucks and Allen (Creative Commons)", HW-250, HH+90, 500, 50, white, ltGreen, None, 14)
        button("BACK", HW-250, HH+170, 500, 50, white, ltRed, backToIntro)

        pygame.display.update()


def setGrant():
    player.setGrant();
    time.sleep(.5)
    game_intro()

def setVinny():
    player.setVinny();
    time.sleep(.5)
    game_intro()

def setMike():
    player.setMike()
    time.sleep(.5)
    game_intro()

def backToIntro():
    time.sleep(.5)
    game_intro()



''' EXECUTE CODE'''

# ---- Initialize player and items ---- #

all_sprites = pygame.sprite.Group()
oil_sprites = pygame.sprite.Group()
rock_sprites = pygame.sprite.Group()

player = player(10)
all_sprites.add(player)

for i in range(1):
    o = item(oilImg)
    all_sprites.add(o)
    oil_sprites.add(o)

for j in range(6):
    r = item(rockImg)
    all_sprites.add(r)
    rock_sprites.add(r)

game_intro()
