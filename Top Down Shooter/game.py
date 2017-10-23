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

        
# class for the actual game        
class Game(object):
    def __init__(self, map, player, width, height):
        # List to store all the enemies and game data during the current wave
        self.enemies = []
        self.projectiles = []

        # width and height of the display window
        self.width = width
        self.height = height

        # The pygame window
        self.window = pygame.display.set_mode((self.width, self.height))

        # Store the map to play with and the player to use
        self.map = map
        self.player = player

        # Hold the portion of the map to show on the display based off the players position
        self.map_view = pygame.Surface((self.width, self.height))
        
        # List to keep track of what keyboard button have been pressed
        # W, A, S, D
        self.input_map = [False, False, False, False]

        # Create a pygame clock object
        self.clock = pygame.time.Clock()

        #set crashed state variable to false
        self.crashed = False

    # Function to setup the game
    def setup(self):
        pass

    # Function to actually play the game
    def play(self):
        while not self.crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True

                # Detect when keys are pressed
                if event.type == pygame.KEYDOWN:    
                    if event.key == pygame.K_w:
                        self.input_map[0] = True
                    if event.key == pygame.K_a:
                        self.input_map[1] = True
                    if event.key == pygame.K_s:
                        self.input_map[2] = True
                    if event.key == pygame.K_d:
                        self.input_map[3] = True
                        
                # Detect when keys are released       
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.input_map[0] = False
                    if event.key == pygame.K_a:
                        self.input_map[1] = False
                    if event.key == pygame.K_s:
                        self.input_map[2] = False
                    if event.key == pygame.K_d:
                        self.input_map[3] = False


            # create a surface of only a portion of the map based on player position
            self.map_view = pygame.Surface((self.width, self.height))
            self.map_view.blit(self.map, (0,0), (self.player.x, self.player.y,\
                                                 self.width, self.height))

            self.player.move_keyboard(self.input_map, 3200, 2400)

            # print the background then the player in the center on top of the background
            self.window.blit(self.map_view, (0,0))
            self.window.blit(soup.image, (self.width/2 - self.player.width/2, \
                                          self.height/2 - self.player.height/2))
                
            pygame.display.update()

            # limit the game to 60 fps
            self.clock.tick(60)

        pygame.quit()
        quit()


#############################################################################
# Play the Game
#############################################################################

WIDTH = 800
HEIGHT = 600

# map object
play_map = pygame.image.load("images/background.png")

# Create a player object of some soup
soup =  Player("images/soup.png")

# Create the game object
game = Game(play_map, soup, WIDTH, HEIGHT)

# Setup the game
game.setup()

# run the game
game.play()


##try:
##    while(True):
##
##        #RUN CODE HERE
##
##
##
##except KeyboardInterrupt:
##    # reset the GPIO pins
##    GPIO.cleanup()




















