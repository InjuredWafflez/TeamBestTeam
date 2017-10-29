import pygame

# Base class with x and y pos and x and y vec for other classes to inherit from
class Asset(pygame.sprite.Sprite):
    def __init__(self, image = "no-image"):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create the image and rectangular collision box
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        
        self.rect.x = 0
        self.rect.y = 0
        self.x_vector = 0
        self.y_vector = 0
        
        # create a collision box for the player using pygame image ractange
        self.box = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

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

# Player Sprite class
class Player(Asset):
    def __init__(self,image = "no-image"):
        # Call the parent class (Asset) constructor
        Asset.__init__(self, image)

        self.health = 3
        self.speed = 7
        self.score = 0
        

    def move_keyboard(self, key_input, x_max, y_max):
        if key_input['w'] == True:
            self._y_vector = -7
        
        elif key_input['s'] == True:
            self._y_vector = 7
        else:
            self._y_vector = 0

        if key_input['a'] == True:
            self._x_vector = -7
        
        elif key_input['d'] == True:
            self._x_vector = 7
        else:
            self._x_vector = 0

        # Limit the x and y to the max determined from the map image
        if self.rect.x >= x_max and self._x_vector > 0:
            self._x_vector = 0
        
        elif self.rect.x <= 0 and self._x_vector < 0:
            self._x = 0
            
        if self.rect.y >= y_max and self._y_vector > 0:
            self._y_vector = 0
        
        elif self.rect.y <= 0 and self._y_vector < 0:
            self._y = 0
            
        self.rect.x += self._x_vector
        self.rect.y += self._y_vector

    def hit(self):
        self.health -= 1
        

# Top down shooter weapon and bullet class
class Bullet(Asset):
    # Inherit from asset class for x and y pos and x and y velocity\
    # get the x and y max from the map
    def __init__(self, image, player, x_vec, y_vec, damage, speed):
        # Call the parent class (Asset) constructor
        Asset.__init__(self, image)

        self.player = player
        self.rect.x = self.player.rect.x
        self.rect.y = self.player.rect.y
        self._x_vector = x_vec
        self._y_vector = y_vec
        self.speed = speed
        self.damage = damage

    # update the position of the bullet on the screen
    # have the bullet delete itself if outside the bounds of the map
    def update(self):
        self.rect.x += (self._x_vector * self.speed) + self.player.x_vector
        self.rect.y += (self._y_vector * self.speed) + self.player.y_vector
        

class Weapon(Asset):
    def __init__(self, image):
        # Call the parent class (Asset) constructor
        Asset.__init__(self, image)

        self.display_width =  pygame.display.get_surface().get_width()
        self.display_height =  pygame.display.get_surface().get_height()
    
    # upadate the x and y aim vector of the weapon
    # using the players position and mouse
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self._x_vector =  mouse_pos[0] - (self.display_width/2)
        self._y_vector = mouse_pos[1] - (self.display_height/2)

        # Find the maginitude of the vector
        vec_mag = (self._x_vector**2 + self._y_vector**2)**(0.5)

        # Create unit vector components using the magnitude
        self._x_vector = self._x_vector / vec_mag
        self._y_vector = self._y_vector / vec_mag
    
    # create a bullet at the players postion
    def fire(self, player):
        self.update()
        # Create a bullet objeect
        bullet = Bullet("images/ball.png", player, self._x_vector, self._y_vector, 1, 9)
        return bullet

class Enemy(Asset):
    # Initialize enemy with player object so the enemy can track the player
    def __init__(self, image, x, y, health, speed, player):
        Asset.__init__(self, image)

        self.rect.x = x
        self.rect.y = y

        self.health = health
        self.speed = speed
        
        self.player = player
        

    def update(self):
        # Update the enemy vector
        self._x_vector = (self.player.rect.x - self.rect.x)
        self._y_vector = (self.player.rect.y - self.rect.y)

        # Find the maginitude of the vector
        vec_mag = (self._x_vector**2 + self._y_vector**2)**(0.5)

        # Create unit vector components using the magnitude and speed
        self._x_vector = (self._x_vector / vec_mag)
        self._y_vector = (self._y_vector / vec_mag)

        # Update the position of the enemy
        self.rect.x += self._x_vector * self.speed
        self.rect.y += self._y_vector * self.speed

    # call this when the enemy is hit with a bullet
    # this will lower the health and destroy the object if need be
    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            self.player.score += 1
            print "Enemy Killed"
        

# Class for game powerups
class PowerUp(Asset):
    def __init__(self, image):
        Asset.__init__(self, image)







        
