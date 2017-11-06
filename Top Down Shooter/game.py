import pygame
from classes import *
from random import randint

#initialize pygame
pygame.init()

#initialize the pygame sound mixer
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

myFont = pygame.font.SysFont("monospace", 15)
        
# class for the actual game        
class Game(object):
    def __init__(self, map, width, height):
        # Groups to store all the enemies and game data during the current wave
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

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
        
        # Create the different weapon objects
        self.machine_gun = Weapon("images/fire-bolt.png")
        self.shotgun = Weapon_Shotgun("images/fire-bolt.png")
        
        # Create a player object of some soup and use the machine gun as
        # the default weapon
        self.player =  Player("images/soup.png", self, self.machine_gun)

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

        # Game variables
        self.wave_number = 1
        self.inventory = None
        self.active_powerup = None
        self.powerup_timer = 0

        # Sound objects
        self.ding = pygame.mixer.Sound("sounds/ding.wav")
        self.hitmarker = pygame.mixer.Sound("sounds/hitmarker.wav")
        self.pew = pygame.mixer.Sound("sounds/pew.wav")
         

        # variable to keep track of what screen to display
        self.screen = "game"

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
                if enemy.health <= 0:
                    enemy.kill()
                    self.player.score += 1
                    self.ding.play()
                    print "Enemy Killed"
                    # roll for a random power up drop
                    # have a 25% chance of a powerup drop
                    self.roll_powerup(25,enemy)
                

        # Check for enemy-player collision
        # remove the enemy upon collision
        collisions = pygame.sprite.spritecollide(self.player, self.enemies, True)

        for enemy in collisions:
            self.player.health -= 1
            self.hitmarker.play()

        # Check for player-powerup collision
        collisions = pygame.sprite.spritecollide(self.player, self.powerups, False)

        # update the dropped powerups on the screen
        for p in self.powerups:
            self.temp_map.blit(p.image, (p.rect.x, p.rect.y))
        
        # Add powerup to enventory if not carrying one
        for p in collisions:
            if self.inventory == None:
                self.inventory = p
                self.powerups.remove(p)

        # If there is an active powerup
        if not self.active_powerup == None:
            # If the power up has run out of time
            if pygame.time.get_ticks() - self.powerup_timer > self.active_powerup.time:
                # End the powerup
                print "PowerUp ended"
                self.active_powerup.end()
                self.active_powerup = None
                

                

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
                        
            
    # spawn a single enemy at a random map location
    # given the enemy a random speed and random health
    def spawn_enemy(self):
        # Choose a random enemy speed
        speed = randint(2, 4)
        # choose a random enemy health
        health = randint(1, 3)

        # choose a random starting position
        x = randint(0, self.map.get_width())
        y = randint(0, self.map.get_height())

        self.enemies.add(Enemy("images/enemy.png", x, y, health, speed, self.player))

        print "Enemy Spawned"

    # Rolls for a random chance of a powerup
    # use a whole number percentage for chance (do not put the percent sign)
    def roll_powerup(self, chance, enemy):
        rand_num = randint(0,100)

        if rand_num < chance:
            self.spawn_powerup(enemy.rect.x, enemy.rect.y)

    # Spawn a powerup at a location
    def spawn_powerup(self, x, y):
        # choose a random number
        rand_num = randint(1,3)

        # Spawn one of 3 powerups based off that random number
        if rand_num == 1:
            self.powerups.add(PowerUp_Health("images/health.png", x, y, self.player))

        elif rand_num == 2:
            self.powerups.add(PowerUp_Speed("images/speed.png", x, y, self.player))

        else:
            self.powerups.add(PowerUp_Weapon("images/nuke.png", self.shotgun, x, y, self.player))

    # Activate the powerup in the player inventory
    def activate_powerup(self):
        self.active_powerup = self.inventory
        self.inventory = None
        self.active_powerup.use()

        self.powerup_timer = pygame.time.get_ticks()
        print "PowerUp Used"
        
    # Display game hud
    # show the health, current wave, and the score
    def game_hud(self):
        health = myFont.render("Health: " + str(self.player.health), 1, (255,255,255), (0,0,0))
        wave = myFont.render("Wave: " + str(self.wave_number), 1, (255,255,255), (0,0,0))
        score = myFont.render("Score: " + str(self.player.score), 1, (255,255,255), (0,0,0))
        powerup = myFont.render("PowerUp: ", 1, (255,255,255), (0,0,0))

        self.window.blit(health, (10,10))
        self.window.blit(score, (self.width-100, 10))
        self.window.blit(wave, (self.width-100, self.height - 20))

        if self.inventory:
            self.window.blit(powerup, (self.width/2 - 20, 15))
            self.window.blit(self.inventory.image, (self.width/2 + 50, 5))

        if self.active_powerup:
            time_left = self.active_powerup.time - (pygame.time.get_ticks() - self.powerup_timer)
            timer = myFont.render("PowerUp: " + str(time_left), 1, (255,255,255), (0,0,0))
            
            self.window.blit(timer, (self.width/2, 25))
    
    # Play a wave                     
    def play_wave(self, wave_number):
        enemies_to_spawn = wave_number ** (1.5)
        spawn_delay = 1000
        last_spawn = 0

        print "Wave {} Started".format(wave_number)
        
        while(True):
            
            if (pygame.time.get_ticks() - last_spawn > spawn_delay) and enemies_to_spawn > 0:
                self.spawn_enemy()
                spawn_delay = randint(1000, 3000)
                last_spawn = pygame.time.get_ticks()
                enemies_to_spawn -= 1


            # check for inputs
            self.check_events()

            # Move the player using keyboard inputs
            self.player.move_keyboard(self.input_map, self.map.get_width(), self.map.get_height())
            
            # create a surface of only a portion of the map based on player position
            # apply the offsets to the map_view image to have it centered correctly
            self.map_view = pygame.Surface((self.width, self.height))
            
            self.update()
            
            self.map_view.blit(self.temp_map, (0,0), ((self.player.rect.x - self.x_offset), \
                                                 (self.player.rect.y - self.y_offset),\
                                                 self.width, self.height))

            if self.input_map['left_click'] == True:
                self.player.fire()
                self.pew.play()
                #self.fire_weapon()
            if self.input_map['right_click'] == True and self.inventory != None \
               and self.active_powerup == None:
                self.activate_powerup()

            # print the background then the player in the center on top of the background
            self.window.blit(self.map_view, (0,0))
            self.window.blit(self.player.image, (self.width/2 - self.player.width/2, \
                                          self.height/2 - self.player.height/2))

            # Display game hud
            self.game_hud()

            # update the pygame display    
            pygame.display.update()

            # Check for conditions to end the wave
            if enemies_to_spawn <= 0 and len(self.enemies) <= 0:
                self.wave_number += 1
                break

            elif self.player.health <= 0:
                self.screen = "lose_screen"
                break

            # limit the game to 60 fps
            self.clock.tick(60)

        print "Wave {} Completed".format(wave_number)
    
    # Main Menu screen
    def main_menu(self):
        print "add main menu code"

    # Lose screen
    def lose_screen(self):
        print "Add lose screen code"


    # level up screen
    def level_up_screen(self):
        print "add level up screen code"

    # credit screen
    def credit_screen(self):
        print "add credit screen code"

    # highscores screen
    def highscores_screen(self):
        print "add highscores screen code"

    # Function to actually play the game
    def play(self):
        test_timer = 0
        while not self.crashed:

            # Check for which game screen or menu to display
            if self.screen == "game":
                self.play_wave(self.wave_number)

            elif self.screen == "main_menu":
                self.main_menu()

            elif self.screen == "lose_screen":
                self.lose_screen()

            elif self.screen == "level_up_screen":
                self.level_up_screen()

            elif self.screen == "credit_screen":
                self.credit_screen()

            elif self.screen == "highscores_screen":
                self.highscores_screen()
                
            else:
                pass

            self.clock.tick(60)

        #pygame.quit()
        quit()


#############################################################################
# Play the Game
#############################################################################

WIDTH = 800
HEIGHT = 600

# map object
play_map = pygame.image.load("images/background.png")

# Create the game object
game = Game(play_map, WIDTH, HEIGHT)

# Setup the game
game.setup()

# run the game
game.play()




















