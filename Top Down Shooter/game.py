import pygame
from classes import *
from random import randint

#initialize pygame
pygame.init()

myFont = pygame.font.SysFont("monospace", 15)
        
# class for the actual game        
class Game(object):
    def __init__(self, map, player, width, height):
        # Groups to store all the enemies and game data during the current wave
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        # width and height of the display window
        self.width = width
        self.height = height

        # The pygame window
        self.window = pygame.display.set_mode((self.width, self.height))
        # Hold the portion of the map to show on the display based off the players position
        self.map_view = pygame.Surface((self.width, self.height))

        # Store the map to play with and the player to use
        self.map = map
        self.temp_map = self.map.copy()
        self.player = player

        # Map offsets since (0,0) on the display is top left and not center
        # these offset the map based off the size of the display
        self.x_offset = width/2
        self.y_offset = height/2
        
        # Dictionary to keep track of what keyboard button have been pressed
        # W, A, S, D
        self.input_map = {'w':False, 'a':False, 's':False, 'd':False,\
                          'left_click':False, 'right_click':False}

        # Create a pygame clock object
        self.clock = pygame.time.Clock()

        #set crashed state variable to false
        self.crashed = False

        # Create a weapon object
        self.blaster = Weapon("images/fire-bolt.png")
        # weapon fire delay
        # move these to the weapon class
        self.shot_delay = 150
        self.last_shot = 0

        # Game variables
        self.wave_number = 1
        self.inventory = 0
        self.active_powerup = 0

    # Function to setup the game
    def setup(self):
        pass

    def update(self):
        # iterate through the enemies and projectiles lists and call their
        # respective update functions
        self.temp_map = self.map.copy()

        # update the bullet positions
        for b in self.bullets.sprites():
            b.update()
            if b.rect.x > self.map.get_width() or b.rect.x < 0 or \
               b.rect.y > self.map.get_height() or b.rect.y < 0:
                b.kill()
            else:
                self.temp_map.blit(b.image, (b.rect.x, b.rect.y))

        # update the positions of the enemies
        for e in self.enemies.sprites():
            e.update()
            self.temp_map.blit(e.image, (e.rect.x, e.rect.y))

        # check for bullet-enemy collisions
        # have the bullets get removed when hitting something
        collisions = pygame.sprite.groupcollide(self.enemies, self.bullets, \
                                                False, True)

        # 'hit' enemy with each collided bullet
        for enemy, b in collisions.iteritems():
            for bullet in b:
                enemy.hit(bullet.damage)

        # Check for enemy-player collision
        # remove the enemy upon collision
        collisions = pygame.sprite.spritecollide(self.player, self.enemies, True)

        for enemy in collisions:
            self.player.health -= 1

                

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
                        
    # fire the player weapon
    def fire_weapon(self):
        if pygame.time.get_ticks() - self.last_shot > self.shot_delay:
            self.bullets.add(self.blaster.fire(self.player))
            #print "Fire!"
            self.last_shot = pygame.time.get_ticks()
            
    # spawn a single enemy at a random map location
    # given the enemy a random speed and random health
    def spawn_enemy(self):
        # Choose a random enemy speed
        speed = randint(2, 5)
        # choose a random enemy health
        health = randint(1, 3)

        # choose a random starting position
        x = randint(0, self.map.get_width())
        y = randint(0, self.map.get_height())

        self.enemies.add(Enemy("images/enemy.png", x, y, health, speed, self.player))

        print "Enemy Spawned"

    # Display game hud
    # show the health, current wave, and the score
    def game_hud(self):
        health = myFont.render("Health: " + str(self.player.health), 1, (255,255,255), (0,0,0))
        wave = myFont.render("Wave: " + str(self.wave_number), 1, (255,255,255), (0,0,0))
        score = myFont.render("Score: " + str(self.player.score), 1, (255,255,255), (0,0,0))

        self.window.blit(health, (10,10))
        self.window.blit(score, (self.width-100, 10))
        self.window.blit(wave, (self.width-100, self.height - 20))

        

    # Play a wave                     
    def play_wave(self, wave_number):
        enemies_to_spawn = wave_number ** (1.5)
        spawn_delay = 1000
        last_spawn = 0

        print "Wave {} Started".format(wave_number)
        
        while(enemies_to_spawn > 0 or len(self.enemies) > 0):
            if (pygame.time.get_ticks() - last_spawn > spawn_delay) and enemies_to_spawn > 0:
                self.spawn_enemy()
                spawn_delay = randint(1000, 3000)
                last_spawn = pygame.time.get_ticks()
                enemies_to_spawn -= 1


            # check for inputs
            self.check_events()

            # create a surface of only a portion of the map based on player position
            # apply the offsets to the map_view image to have it centered correctly
            self.map_view = pygame.Surface((self.width, self.height))
            self.update()
            
            self.map_view.blit(self.temp_map, (0,0), ((self.player.rect.x - self.x_offset), \
                                                 (self.player.rect.y - self.y_offset),\
                                                 self.width, self.height))

            self.player.move_keyboard(self.input_map, self.map.get_width(), self.map.get_height())

            if self.input_map['left_click'] == True:
                self.fire_weapon()

            # print the background then the player in the center on top of the background
            self.window.blit(self.map_view, (0,0))
            self.window.blit(soup.image, (self.width/2 - self.player.width/2, \
                                          self.height/2 - self.player.height/2))

            # Display game hud
            self.game_hud()

            # update the pygame display    
            pygame.display.update()

            # limit the game to 60 fps
            self.clock.tick(60)

        print "Wave {} Completed".format(wave_number)
        
            

    # Function to actually play the game
    def play(self):
        test_timer = 0
        while not self.crashed:
            if self.player.health > 0:
                self.play_wave(self.wave_number)
                self.wave_number += 1
            else:
                print "Player Dead"
                break

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




















