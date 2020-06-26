import pygame
pygame.init()

frame = pygame.display.set_mode((500, 500))
white = (255,255,255)
black = (0,0,0)

player = pygame.image.load('enemy_down.gif')



class Player():
    def __init__(self, pos, image):
        self.image = image
        self.pos = pos

    def draw(self):
        frame.blit(self.image, self.pos)

    def update(self, pos):
        self.pos = pos

player1 = Player((300,300), player)

def gameLoop():

    quitGame = False
    x = player1.pos[0]
    y = player1.pos[1]
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

            if event.type == pygame.KEYDOWN:


                if event.key == pygame.K_LEFT:
                    movex = -0.1






        frame.fill(white)
        x += movex

        player1.draw()
        player1.update((x,y))




        pygame.display.update()


gameLoop()
pygame.quit()
quit()






#----------------------------------------------------------
