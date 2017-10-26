import pygame

# Base class with x and y pos and x and y vec for other classes to inherit from
class Asset(pygame.sprite.Sprite):
    def __init__(self, image = "no-image"):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        
        self.x = 0
        self.y = 0
        self.x_vector = 0
        self.y_vector = 0

        self.image = pygame.image.load(image)
        
        # create a collision box for the player using pygame image ractange
        self.box = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

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
        self._y = int(value) #+ (self.height/2)

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
        if self._x >= x_max and self._x_vector > 0:
            self._x_vector = 0
        
        elif self._x <= 0 and self._x_vector < 0:
            self._x = 0
            
        if self._y >= y_max and self._y_vector > 0:
            self._y_vector = 0
        
        elif self._y <= 0 and self._y_vector < 0:
            self._y = 0
            
        self._x += self._x_vector
        self._y += self._y_vector

# Top down shooter weapon and bullet class
class Bullet(Asset):
    # Inherit from asset class for x and y pos and x and y velocity\
    # get the x and y max from the map
    def __init__(self, image, x, y, x_vec, y_vec, speed):
        # Call the parent class (Asset) constructor
        Asset.__init__(self, image)

        self._x = x
        self._y = y
        self._x_vector = x_vec
        self._y_vector = y_vec
        self.speed = speed

    # update the position of the bullet on the screen
    # have the bullet delete itself if outside the bounds of the map
    def update(self):
        self._x += self._x_vector * self.speed
        self._y += self._y_vector * self.speed
        

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
        bullet = Bullet("images/ball.png", player.x, player.y, self._x_vector, self._y_vector, 8)
        return bullet







        
