import pygame

#initialize pygame
pygame.init()

# Player Sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self,image = "no-image"):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image)
        
        # create a collision box for the player using pygame image ractange
        self.box = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        self.x = 0
        self.y = 0
        self.x_vector = 0
        self.y_vector = 0
    
    # getters and setters for x and y positions
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        # Ensures the x-value is a int
        self._x = int(value)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        # Ensures the y-value is a int
        self._y = int(value) + (self.height/2)

    # getters and setters for x and y vectors
    @property
    def x_vector(self):
        return self._x_vector
    
    @x_vector.setter
    def x_vector(self, value):
        self._x_vector = value

    @property
    def y_vector(self):
        return self._y_vector

    @y_vector.setter
    def y_vector(self, value):
        self._y_vector = value

    def move_keyboard(self, key_input, x_max, y_max):
        if key_input[0] == True:
            self._y_vector = -7
        
        elif key_input[2] == True:
            self._y_vector = 7
        else:
            self._y_vector = 0

        if key_input[1] == True:
            self._x_vector = -7
        
        elif key_input[3] == True:
            self._x_vector = 7
        else:
            self._x_vector = 0
            

        self._x += self._x_vector #+ (self.width*0.5)
        self._y += self._y_vector #+ (self.height*0.5)

        
        

#############################################################################
# Setup the game
#############################################################################

WIDTH = 800
HEIGHT = 600

# create a pygame display object
# set the width and height of the display
game_display = pygame.display.set_mode((WIDTH, HEIGHT))

#need to make some sort of class for this background and play area
play_map = pygame.image.load("images/background.png")

#create a pygame clock object
clock = pygame.time.Clock()

#set crashed state variable to false
crashed = False

# Create a player object of some soup
soup =  Player("images/soup.png")

#############################################################################
# Play the Game
# need to put all this in a class of its own also
#############################################################################

#set background on display to all white
game_display.fill((255,255,255))

# array to store status of keyboard inputs
# W, A, S, D
input_map = [False, False, False, False]

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_w:
                input_map[0] = True
            if event.key == pygame.K_a:
                input_map[1] = True
            if event.key == pygame.K_s:
                input_map[2] = True
            if event.key == pygame.K_d:
                input_map[3] = True
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                input_map[0] = False
            if event.key == pygame.K_a:
                input_map[1] = False
            if event.key == pygame.K_s:
                input_map[2] = False
            if event.key == pygame.K_d:
                input_map[3] = False


    # create a surface of only a portion of the map based on player position
    map_display = pygame.Surface((WIDTH, HEIGHT))
    map_display.blit(play_map, (0,0), (soup.x, soup.y, WIDTH, HEIGHT))

    soup.move_keyboard(input_map, 3200, 2400)

    # print the background then the player in the center on top of the background
    game_display.blit(map_display, (0,0))
    game_display.blit(soup.image, (WIDTH/2 - soup.width/2, HEIGHT/2 - soup.height/2))
        
    pygame.display.update()

    # limit the game to 60 fps
    clock.tick(60)

pygame.quit()
quit()

























