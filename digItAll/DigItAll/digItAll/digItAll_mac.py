# dig it all version 2.0

# ************************************ TO DO **********************************************
# 1) enemy and player collision - add noise and inability to detect
# 2) weight limit: need to empty junk, trash icon
# 3) pouch: see all finds and info blurb about them by clicking on each
# 4) 2-3 other beep signals depending on what is found

import random
import time
import math
import pygame
from pygame import mixer
import time

# hide for mac, unhide for windows - need to find sound for mac
# import winsound
# player_beep = mixer.Sound('C:/Users/nahol/Dropbox/Code/beep.wav')
# high_tone = mixer.Sound('C:/Users/nahol/Dropbox/Code/high_tone_beep.wav')
# low_tone = mixer.Sound ('C:/Users/nahol/Dropbox/Code/low_tone_beep.wav')


# from threading import Timer
# import multitimer
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()



WIDTH = 900
HEIGHT = 800
item_image_size = (200, 200)
finds_pouch = []

# set frame
frame = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dig It All!')
clock = pygame.time.Clock()

scoreFile = open('highscores.txt', 'a')

# register shapes
background_image = pygame.image.load('grass-bg.gif')

# character images
playerImg = pygame.image.load('player_right.gif')
player_left = pygame.image.load('player_left.gif')
player_down = pygame.image.load('player_up.gif')
player_up = pygame.image.load('player_down.gif')

enemy_down = pygame.image.load('enemy_down.gif')
enemy_up = pygame.image.load('enemy_up.gif')
enemy_left = pygame.image.load('enemy_left.gif')
enemy_right = pygame.image.load('enemy_right.gif')

plug = pygame.image.load('plug.gif')

# item images
barber = pygame.image.load('barber-quarter.gif')
buckle = pygame.image.load('colonial-shoe-buckle.gif')
crotal_bell = pygame.image.load('crotal-bell.gif')
dandy = pygame.image.load('dandy-button.gif')
gw = pygame.image.load('gw-button.gif')
harmonica_reed = pygame.image.load('harmonica-reed.gif')
jaw_harp = pygame.image.load('jaw-harp.gif')
skellie = pygame.image.load('key.gif')
musket_ball = pygame.image.load('musket-ball.gif')
ox_knob = pygame.image.load('ox-knob.gif')
pull_tab = pygame.image.load('pull-tab.gif')
nail = pygame.image.load('rusty-nail.gif')
thimble = pygame.image.load('thimble.gif')
tombac = pygame.image.load('tombac-button.gif')
two_tine_fork = pygame.image.load('two-tine-fork.gif')
walking_half = pygame.image.load('walking-half.gif')


rareItems = ['GW button', 'oak tree shilling', 'gold ring', 'Fugio']
commonItems = ['tombac button', 'ox knob', 'harmonica reed', 'musket ball']*5
semiRareItems = ['colonial shoe buckle', 'walking half dollar', 'real', 'skeleton key', 'two-tine fork', 'crotal bell', 'jaw harp', 'barber quarter', 'thimble', 'dandy button', 'walking half dollar']*2
junk = ['beer can', 'rusty nail', 'rifle shell', 'pull tab']*5
allItems = rareItems + commonItems + semiRareItems + junk

# complete list
# image_pairs = {'ox knob': ox_knob, 'skeleton key': skellie, 'rusty nail': nail, 'two-tine fork': two_tine_fork,
#             'gw button': gw, 'soda can': soda_can, 'beer can': beer_cap,
#             'pull tab': pull_tab, 'musket ball': musket_ball, 'barber quarter': barber, 'thimble': thimble,
#              'dandy button': dandy, 'walking half dollar': walking_half, 'jaw harp': jaw_harp,
#             'tombac button': tombac, 'harmonica reed': harmonica_reed, 'crotal bell': crotal_bell,
#              'colonial shoe buckle': buckle}

# modified list
image_pairs = {'ox knob': ox_knob, 'skeleton key': skellie, 'rusty nail': nail, 'two-tine fork': two_tine_fork,
            'GW button': gw, 'pull tab': pull_tab, 'musket ball': musket_ball, 'barber quarter': barber, 'thimble': thimble,
             'dandy button': dandy, 'walking half dollar': walking_half, 'jaw harp': jaw_harp,
            'tombac button': tombac, 'harmonica reed': harmonica_reed, 'crotal bell': crotal_bell,
             'colonial shoe buckle': buckle}

weights = {'shovel': 20, 'detector': 30, 'GW button': 4, 'tree coin': 3, 'gold ring': 6, 'Fugio': 4, 'rusty nail': 4, 'tombac button': 3, 'pull tab': 1,
        'ox knob': 7, 'harmonica reed': 3, 'two-tine fork': 9, 'colonial shoe buckle': 8, 'walking half dollar': 5, 'real': 3, 'skeleton key': 5, 'crotal bell': 10, 'jaw harp':  4, 'rifle shell': 2, 'beer can': 5,
        'musket ball': 5, 'barber quarter': 4, 'thimble': 2, 'dandy button': 3, }

values = {'shovel': 0, 'detector': 0, 'GW button': 75, 'tree coin': 100, 'gold ring': 50, 'Fugio': 25, 'rusty nail': 0, 'tombac button': 5, 'pull tab': 0,
        'ox knob': 2, 'harmonica reed': 2, 'two-tine fork': 10, 'colonial shoe buckle': 25, 'walking half dollar': 25, 'real': 50, 'skeleton key': 10, 'crotal bell': 15, 'jaw harp': 8, 'rifle shell': 0, 'beer can': 0,
        'musket ball': 2, 'barber quarter': 15, 'thimble': 10, 'dandy button': 10}



# define colors
green = (0,255,0)
white = (255,255,255)
black = (0,0,0)

# define variables
menuOpen = True
treasuresOpen = False
highScoresOpen = False
inPlay = False
item_locs_found = []
dig = False
score = 0
digIt = ()
playerDigs = False
recentDig = False
recentItem = 'undefined'
recentImage = 'undefined'
highScores = []


# define game functions

def mainMenu():
    global menux, menuy, menuw, menuh, spacing, buttonSize, yspacing, button_font
    menux = WIDTH/4
    menuy = HEIGHT/4
    menuw = WIDTH/2
    menuh = HEIGHT/2
    spacing = 50
    yspacing = 30
    buttonSize = [350,40]
    menu_font = pygame.font.Font('freesansbold.ttf', 50)
    button_font = pygame.font.Font('freesansbold.ttf', 30)

    # menu window
    pygame.draw.rect(frame, white, [menux,menuy,menuw,menuh])
    menuTitle = menu_font.render("Menu", True, black)
    frame.blit(menuTitle, (menux+150,menuy+20))

    # play button
    playButton = button_font.render("Play", True, white)
    pygame.draw.rect(frame, black, [menux+spacing, menuy+yspacing*3, buttonSize[0], buttonSize[1]])
    frame.blit(playButton, (menux+spacing,menuy+yspacing*3+5))

    # pouch button
    pouchButton = button_font.render('View Treasures', True, white)
    pygame.draw.rect(frame, black, [menux+spacing, menuy+yspacing*5, buttonSize[0], buttonSize[1]])
    frame.blit(pouchButton, (menux+spacing,menuy+yspacing*5+5))

    # high score button
    highScoreButton = button_font.render("High Score", True, white)
    pygame.draw.rect(frame, black, [menux+spacing, menuy+yspacing*7, buttonSize[0], buttonSize[1]])
    frame.blit(highScoreButton, (menux+spacing,menuy+yspacing*7+5))

    # quit button
    quitButton = button_font.render("Quit", True, white)
    pygame.draw.rect(frame, black, [menux+spacing, menuy+yspacing*9, buttonSize[0], buttonSize[1]])
    frame.blit(quitButton, (menux+spacing,menuy+yspacing*9+5))



class Item():
    def __init__(self, pos, id):
        self.posx = pos[0]
        self.posy = pos[1]
        self.pos  = (pos[0], pos[1])
        self.id = id
        self.wt = 0
        self.value = 0
        self.type = ''
        self.image = barber

    def get_image(self):
        for key in image_pairs:
            if key == self.id:
                self.image = image_pairs[key]


    def get_wt(self):
        for key in weights:
            if key == self.id:
                self.wt = weights[key]

    def get_value(self):
        for key in values:
            if key == self.id:
                self.value = values[key]

    def get_type(self):
        pass

    def get_center(self):
        w = (self.posx + item_image_size[0]) / 2
        h = (self.posy + item_image_size[1]) / 2
        self.pos = (w, h)
        return (self.pos)

    def draw(self):
        pygame.draw.circle(frame, white, (self.pos), 5)


def createItems():
    global item_list, items, item_locs
    item_list = []
    items = []
    item_locs = []
    while len(items) < 25:
        choice = random.choice(allItems)
        posx = random.randrange(0, WIDTH)
        posy = random.randrange(0, HEIGHT)
        new = Item((posx, posy), choice)
        new.get_image()
        items.append(new)
        item_locs.append((posx, posy))

createItems()
for i in items:
    # i.get_image()
    i.get_wt()
    i.get_value()
    i.get_type()


def treasuresPouch():
    global menuOpen, finds_pouch
    menuOpen = False
    menuh = HEIGHT/2
    menuw = WIDTH/2
    x = 100
    y = 150

    font = pygame.font.Font('freesansbold.ttf', 20)
    font2 = pygame.font.Font('freesansbold.ttf', 30)
    pouch = [100, 100, WIDTH-200, HEIGHT-200]
    button = [110, 110, 130, 40]
    pygame.draw.rect(frame, white, pouch)
    pygame.draw.rect(frame, black, button)
    goBack = font.render('<< Go Back', True, white)
    treasures = font2.render('Treasures Pouch', True, black)
    frame.blit(goBack, (120, 120))
    frame.blit(treasures, (350, 120))

    for find in finds_pouch:
        img = find.image
        img = pygame.transform.scale(img,(100,100))
        frame.blit(img, (x,y))
        x += 100
        if x > 700:
            x = 100
            y += 100


def highScore():
    pouch = [100, 100, WIDTH-200, HEIGHT-200]
    pygame.draw.rect(frame, white, pouch)
    button = [110, 110, 130, 40]
    pygame.draw.rect(frame, black, button)
    title_font = pygame.font.Font('freesansbold.ttf', 30)
    highScore = title_font.render("High Scores", True, black)
    frame.blit(highScore, (350, 120))
    font = pygame.font.Font('freesansbold.ttf', 20)
    goBack = font.render('<< Go Back', True, white)
    frame.blit(goBack, (120, 120))
    x = 400
    y = 200
    for score in highScores:
        hScore = font.render(str(score), True, black)
        frame.blit(hScore, (x, y))
        y += 30


# draw game background and menus
def draw():
    global treasuresOpen, menuOpen
    frame.blit(background_image, (0,0))
    if menuOpen == True:
        treasuresOpen = False
        mainMenu()
    if treasuresOpen == True:
        menuOpen = False
        treasuresPouch()
    if highScoresOpen == True:
        menuOpen = False
        highScore()


def tooHeavy():
    font = pygame.font.Font('freesansbold.ttf', 20)
    tooHeavy = font.render('You are carrying too much - must empty pouch before you can dig any more', True, black)
    frame.blit(tooHeavy, (10, 400))


# show player score
def showScore():
    font = pygame.font.Font('freesansbold.ttf', 20)
    score = font.render('Score: ' + str(player1.score), True, black)
    frame.blit(score, (750, 10))

# draw plug after digging
def drawPlug(pos, plug):
    frame.blit(plug, pos)




class Player():
    global playerImg, currentPos, item_locs_found, score
    def __init__(self, pos, image):
        self.posx = pos[0]
        self.posy = pos[1]
        self.pos = (self.posx, self.posy)
        self.image = playerImg
        self.vel = 2
        self.rect = self.image.get_rect()
        self.orientation = 'right'
        self.score = 0
        self.wt = 0

    def draw(self, pos):
        if self.orientation == 'right':
            self.image = playerImg
            frame.blit(self.image, self.pos)
        elif self.orientation == 'left':
            self.image = player_left
            frame.blit(self.image, self.pos)
        elif self.orientation == 'up':
            self.image = player_down
            frame.blit(self.image,  self.pos)
        elif self.orientation == 'down':
            self.image = player_up
            frame.blit(self.image,  self.pos)

    def update(self, pos):
        self.pos = pos

    # check if player is walking over hidden item
    def isCollision(self, other):
        # offset to account for player image size (pos uses top left corner of image)
        #dist = math.sqrt((x1 - x)**2 + ((y1 - y)**2))
        dist = math.sqrt((self.pos[0]+50 - other.pos[0])**2 + ((self.pos[1]+50 - other.pos[1])**2))
        if other.pos not in item_locs_found:
            if dist < 10:
                return True
            else:
                return False

    # dig item and add to pouch
    def dig(self, item):
        if item.pos not in item_locs_found:
            finds_pouch.append(item)
            item_locs_found.append(item.pos)
            self.score += item.value
            self.wt += item.wt
        # rot = [0, 90, 180, 270]
        # randomRot = random.choice(rot)
        # rotPlug = pygame.transform.rotate(plug, randomRot)
        # return rotPlug


    # show dug item decription and image when dug
    def showDug(self, itemName, image):
        font = pygame.font.Font('freesansbold.ttf', 20)
        display = font.render("You dug a " + str(itemName), True, black)
        frame.blit(display, (100, 50))
        frame.blit(image, (300, 50))


class Enemy(Player):
    def __init__(self, pos, image):
        self.pos = pos
        self.image = image
        self.vel = 2
        self.orientation = 'right'
        self.score = 0
        self.wt = 0

    def draw(self, pos):
        if self.orientation == 'right':
            self.image = enemy_right
            frame.blit(self.image, self.pos)
        elif self.orientation == 'left':
            self.image = enemy_left
            frame.blit(self.image, self.pos)
        elif self.orientation == 'up':
            self.image = enemy_up
            frame.blit(self.image,  self.pos)
        elif self.orientation == 'down':
            self.image = enemy_down
            frame.blit(self.image,  self.pos)

    def isCollision(self, other):
        # offset to account for player image size (pos uses top left corner of image)
        #dist = math.sqrt((x1 - x)**2 + ((y1 - y)**2))
        dist = math.sqrt((self.pos[0]+50 - other.pos[0])**2 + ((self.pos[1]+50 - other.pos[1])**2))
        if other.pos not in item_locs_found:
            if dist < 10:
                return True
            else:
                return False

    # dig item and add to pouch
    def dig(self, item):
        if item.pos not in item_locs_found:
            item_locs_found.append(item.pos)
            self.score += item.value
            self.wt += item.wt




# create player
player_start_pos = (0,500)
player1 = Player(player_start_pos, playerImg)

# create items
items_id = []
for i in items:
    new_id = i.id
    items_id.append(new_id)

# create enemy
enemy_start_pos = (50,50)
enemy1 = Enemy(enemy_start_pos, enemy_down)





# Game Loop
def gameLoop():
    global menuOpen, treasuresOpen, highScoresOpen, inPlay, digIt, playerDigs, recentDig, recentItem, recentImage

    quitGame = False
    playerx = player1.pos[0]
    playery = player1.pos[1]
    movex = 0
    movey = 0


    while not quitGame:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        keypress = pygame.key.get_pressed()

        # quits and closes game when user hits window X
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # ********* MENU ***********
            if menuOpen == True:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # close menu, play game
                    if mouse[0] > menux+spacing and mouse[0] < menux+spacing+buttonSize[0]:
                        if mouse[1] > menuy+yspacing*3 and mouse[1] < menuy+yspacing*3+buttonSize[1]:
                            if click[0] == 0:
                                menuOpen = False
                                inPlay = True

                    # open treasures pouch
                    if mouse[0] > menux+spacing and mouse[0] < menux+spacing+buttonSize[0]:
                        if mouse[1] > menuy+yspacing*5 and mouse[1] < menuy+yspacing*5+buttonSize[1]:
                            if click[0] == 0:
                                menuOpen = False
                                treasuresOpen = True

                    # open high score
                    if mouse[0] > menux+spacing and mouse[0] < menux+spacing+buttonSize[0]:
                        if mouse[1] > menuy+yspacing*7 and mouse[1] < menuy+yspacing*7+buttonSize[1]:
                            if click[0] == 0:
                                highScoresOpen = True

                    # quit game
                    if mouse[0] > menux+spacing and mouse[0] < menux+spacing+buttonSize[0]:
                        if mouse[1] > menuy+yspacing*9 and mouse[1] < menuy+yspacing*9+buttonSize[1]:
                            if click[0] == 0:
                                pygame.quit()
                                quit()

                    if len(highScores) < 10:
                        for i in highScores:
                            if score > i:
                                scoreFile.write(str(score))
                                highScores.append(score)
                                scoreFile.close()

            if treasuresOpen == True or highScoresOpen == True:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # from treasures pouch, return to main menu
                    if mouse[0] > 110 and mouse[0] < 240:
                        if mouse[1] > 110 and mouse[1] < 150:
                            treasuresOpen = False
                            highScoresOpen = False
                            menuOpen = True

            # reopen menu
            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key == 'm':
                    menuOpen = True
                    inPlay = False

        # ****** END OF MENU *******


        # ***** MAIN GAME LOOP *****
            if inPlay == True:

                if event.type == pygame.KEYDOWN:
                    recentDig = False
                    key = pygame.key.name(event.key)
                    x = player1.pos[0]
                    y = player1.pos[1]
                    if key == 'left':
                        player1.orientation = 'left'
                        movex = -player1.vel
                    elif key == 'right':
                        movex = player1.vel
                        player1.orientation = 'right'
                    elif key == 'up':
                        player1.orientation = 'up'
                        movey -= player1.vel
                    elif key == 'down':
                        player1.orientation = 'down'
                        movey += player1.vel
                    elif key == 'space':
                        playerDigs = True

                if event.type == pygame.KEYUP:
                    movex = 0
                    movey = 0
                    playerDigs = False


        frame.fill(white)
        draw()
        showScore()

        playerx += movex
        playery += movey
        player1.draw(player_start_pos)
        player1.update((playerx,playery))

        enemy1.draw(enemy_start_pos)


        # check for collisions
        for i in items:
            i.draw()

            if player1.isCollision(i):
                if i.pos not in item_locs_found:
                    # player_beep.play() fix for mac
                    dig = True
                    if dig == True:
                        if playerDigs == True:
                            player1.dig(i)
                            newPlug = player1.dig(i)
                            print (newPlug)
                            recentDig = True
                            recentItem = i.id
                            recentImage = i.image

            else:
                dig = False

            if i.pos in item_locs_found:
                # drawPlug(i.pos, newPlug)
                drawPlug(i.pos, plug)


        if recentDig == True:
            player1.showDug(recentItem, recentImage)

        # check wt - not sure if want to include this in game
        if player1.wt > 10:
            # playerDigs = False
            # tooHeavy()
            pass











        pygame.display.update()
        clock.tick(60)
    # end of gameLoop


gameLoop()
pygame.quit()
quit()
