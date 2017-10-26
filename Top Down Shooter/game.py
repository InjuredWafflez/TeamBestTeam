import pygame
from classes import *

#initialize pygame
pygame.init()
        
# class for the actual game        
class Game(object):
    def __init__(self, map, player, width, height):
        # List to store all the enemies and game data during the current wave
        self.enemies = []
        self.projectiles = []

        # width and height of the display window
        self.width = width
        self.height = height

        # Map offsets since (0,0) on the display is top left and not center
        # these offset the map based off the size of the display
        self.x_offset = width/2
        self.y_offset = height/2

        # The pygame window
        self.window = pygame.display.set_mode((self.width, self.height))

        # Store the map to play with and the player to use
        self.map = map
        self.player = player

        # Hold the portion of the map to show on the display based off the players position
        self.map_view = pygame.Surface((self.width, self.height))
        
        # Dictionary to keep track of what keyboard button have been pressed
        # W, A, S, D
        self.input_map = {'w':False, 'a':False, 's':False, 'd':False,\
                          'left_click':False, 'right_click':False}

        # store the position of the mouse for weapon use
        # stored as '(x,y)' value
        self.mouse_pos = pygame.mouse.get_pos()

        # Create a pygame clock object
        self.clock = pygame.time.Clock()

        #set crashed state variable to false
        self.crashed = False

    # Function to setup the game
    def setup(self):
        pass

    def update(self):
        # iterate through the enemies and projectiles lists and call their
        # respective update functions
        pass

    # check for pygame events
    # update the input status variables
    def check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True

                # Update the mouse pos
                if event.type == pygame.MOUSEMOTION:
                    self.mouse_pos = pygame.mouse.get_pos()

                # Detect when keys are pressed
                if event.type == pygame.KEYDOWN:    
                    if event.key == pygame.K_w:
                        self.input_map['w'] = True
                    elif event.key == pygame.K_a:
                        self.input_map['a'] = True
                    elif event.key == pygame.K_s:
                        self.input_map['s'] = True
                    elif event.key == pygame.K_d:
                        self.input_map['d'] = True
                        
                # Detect when keys are released       
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.input_map['w'] = False
                    elif event.key == pygame.K_a:
                        self.input_map['a'] = False
                    elif event.key == pygame.K_s:
                        self.input_map['s'] = False
                    elif event.key == pygame.K_d:
                        self.input_map['d'] = False

                # Detect if the mouse has been clicked
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.input_map['left_click'] = True
                    elif event.button == 3:
                        self.input_map['right_click'] = True
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.input_map['left_click'] = False
                    elif event.button == 3:
                        self.input_map['right_click'] = False
                    

    # Function to actually play the game
    def play(self):
        while not self.crashed:

            # check for inputs
            self.check_events()

            # create a surface of only a portion of the map based on player position
            # apply the offsets to the map_view image to have it centered correctly
            self.map_view = pygame.Surface((self.width, self.height))
            self.map_view.blit(self.map, (0,0), ((self.player.x - self.x_offset), \
                                                 (self.player.y - self.y_offset),\
                                                 self.width, self.height))

            self.player.move_keyboard(self.input_map, self.map.get_width(), self.map.get_height())

            # print the background then the player in the center on top of the background
            self.window.blit(self.map_view, (0,0))
            self.window.blit(soup.image, (self.width/2 - self.player.width/2, \
                                          self.height/2 - self.player.height/2))

            # update the pygame display    
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




















