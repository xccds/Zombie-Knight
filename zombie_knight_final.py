import pygame, random
from pygame.math  import Vector2


#Set display surface (tile size is 32x32 so 1280/32 = 40 tiles wide, 736/32 = 23 tiles high)
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 736
#Set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (25, 200, 25)
FPS = 30


class Resources:

    def __init__(self):

        self.background_image = pygame.transform.scale(pygame.image.load("images/background.png"), (1280, 736))

        self.image_tile = {}
        for i in range(1,6):
            self.image_tile[f"tile_{i}"] = pygame.transform.scale(pygame.image.load(f"images/tiles/Tile ({i}).png"), (32,32))
        
        self.image_ruby = []
        for i in range(7):
            self.image_ruby.append(pygame.transform.scale(pygame.image.load(f"images/ruby/tile00{i}.png"), (64,64)))
        
        self.image_portal = {}
        self.image_portal["green"] = []
        self.image_portal["purple"] = []
        for i in range(22):
            self.image_portal["green"].append(pygame.transform.scale(pygame.image.load("images/portals/green/tile{:03d}.png".format(i)), (72,72)))
            self.image_portal["purple"].append(pygame.transform.scale(pygame.image.load("images/portals/purple/tile{:03d}.png".format(i)), (72,72)))

        self.image_player = {}
        self.image_player['Move_right'] = []
        self.image_player['Idling_right'] = []
        self.image_player['Jumping_right'] = []
        for i in range(1,11):
            self.image_player['Move_right'].append(pygame.transform.scale(pygame.image.load(f"images/player/run/Run ({i}).png"), (64,64)))
            self.image_player['Idling_right'].append(pygame.transform.scale(pygame.image.load(f"images/player/idle/Idle ({i}).png"), (64,64)))
            self.image_player['Jumping_right'].append(pygame.transform.scale(pygame.image.load(f"images/player/jump/Jump ({i}).png"), (64,64)))

        self.image_zombie_boy = {}
        self.image_zombie_giri = {}

        self.image_zombie_boy['Walking_right'] = []
        self.image_zombie_boy['Dying_right'] = []
        self.image_zombie_giri['Walking_right'] = []
        self.image_zombie_giri['Dying_right'] = []
        for i in range(1,11):
            self.image_zombie_boy['Walking_right'].append(pygame.transform.scale(pygame.image.load(f"images/zombie/boy/walk/Walk ({i}).png"), (64,64)))
            self.image_zombie_boy['Dying_right'].append(pygame.transform.scale(pygame.image.load(f"images/zombie/boy/dead/Dead ({i}).png"), (64,64)))
            self.image_zombie_giri['Walking_right'].append(pygame.transform.scale(pygame.image.load(f"images/zombie/girl/walk/Walk ({i}).png"), (64,64)))
            self.image_zombie_giri['Dying_right'].append(pygame.transform.scale(pygame.image.load(f"images/zombie/girl/dead/Dead ({i}).png"), (64,64)))
            

        self.lost_ruby_sound = pygame.mixer.Sound("sounds/lost_ruby.wav")
        self.ruby_pickup_sound = pygame.mixer.Sound("sounds/ruby_pickup.wav")
        self.jump_sound = pygame.mixer.Sound("sounds/jump_sound.wav")
        self.slash_sound = pygame.mixer.Sound("sounds/slash_sound.wav")
        self.portal_sound = pygame.mixer.Sound("sounds/portal_sound.wav")
        self.hit_sound = pygame.mixer.Sound("sounds/player_hit.wav")
        self.zombie_hit_sound = pygame.mixer.Sound("sounds/zombie_hit.wav")
        self.zombie_kick_sound = pygame.mixer.Sound("sounds/zombie_kick.wav")

        self.title_font = pygame.font.Font("fonts/Poultrygeist.ttf", 48)
        self.HUD_font = pygame.font.Font("fonts/Pixel.ttf", 24)

        pygame.mixer.music.load("sounds/level_music.wav")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1, 0.0)

        # Create the tile map
        #0 -> no tile, 1 -> dirt, 2-5 -> platforms, 6 -> ruby maker, 7-8 -> portals, 9 -> player
        #23 rows and 40 columns
        self.tile_map = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

class Tile(pygame.sprite.Sprite):

    def __init__(self, x, y, resources, image_int, main_group, sub_group):
        super().__init__()
        #Load in the correct image and add it to the correct sub group
        self.image = resources.image_tile[f'tile_{image_int}']
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        #Create a mask for better player collisions
        self.mask = pygame.mask.from_surface(self.image)
        sub_group.add(self)
        main_group.add(self)

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, resources, platform_group, portal_group):
        super().__init__()

        #Set constant variables
        self.HORIZONTAL_ACCELERATION = 1.5
        self.HORIZONTAL_FRICTION = 0.15
        self.VERTICAL_ACCELERATION = 1.5 #Gravity
        self.VERTICAL_JUMP_SPEED = 22 #Determines how high the player can jump
        self.STARTING_HEALTH = 100

        self.resources = resources  

        #Animation frames
        self.move_right_sprites = resources.image_player['Move_right']
        self.move_left_sprites = [pygame.transform.flip(s, True, False) for s in self.move_right_sprites]
        self.idle_right_sprites = resources.image_player['Idling_right']
        self.idle_left_sprites = [pygame.transform.flip(s, True, False) for s in self.idle_right_sprites]
        self.jump_right_sprites = resources.image_player['Jumping_right']
        self.jump_left_sprites = [pygame.transform.flip(s, True, False) for s in self.jump_right_sprites]

        #Load image and get rect
        self.index = 0
        self.image = self.idle_right_sprites[self.index]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        #Attach sprite groups
        self.platform_group = platform_group
        self.portal_group = portal_group

        #Animation booleans
        self.animate_jump = False
        #self.animate_fire = False

        #Kinematics vectors
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, self.VERTICAL_ACCELERATION)

        #Set intial player values
        self.health = self.STARTING_HEALTH
        self.starting_x = x
        self.starting_y = y


    def update(self):
        self.move()
        self.check_collisions()
        self.check_animations()

        #Update the players mask
        self.mask = pygame.mask.from_surface(self.image)


    def move(self):
        #Set the acceleration vector
        self.acceleration = Vector2(0, self.VERTICAL_ACCELERATION)

        #If the user is pressing a key, set the x-component of the acceleration to be non-zero
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -1*self.HORIZONTAL_ACCELERATION
            self.animate(self.move_left_sprites, .5)
        elif keys[pygame.K_RIGHT]:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION
            self.animate(self.move_right_sprites, .5)
        else:
            if self.velocity.x > 0:
                self.animate(self.idle_right_sprites, .5)
            else:
                self.animate(self.idle_left_sprites, .5)

        self.acceleration.x -= self.velocity.x*self.HORIZONTAL_FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5*self.acceleration

        #Update rect based on kinematic calculations and add wrap around movement
        if self.position.x < 0:
            self.position.x = WINDOW_WIDTH
        elif self.position.x > WINDOW_WIDTH:
            self.position.x = 0
        
        self.rect.bottomleft = self.position


    def check_collisions(self):
        #Collision check between player and platforms when falling
        if self.velocity.y > 0:
            collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False, pygame.sprite.collide_mask)
            if collided_platforms:
                self.position.y = collided_platforms[0].rect.top + 5
                self.velocity.y = 0

        #Collision check between player and platform if jumping up
        if self.velocity.y < 0:
            collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False, pygame.sprite.collide_mask)
            if collided_platforms:
                self.velocity.y = 0
                while pygame.sprite.spritecollide(self, self.platform_group, False):
                    self.position.y += 1
                    self.rect.bottomleft = self.position

        #Collision check for portals
        if pygame.sprite.spritecollide(self, self.portal_group, False):
            self.resources.portal_sound.play()
            #Determine which portal you are moving to
            #Left and right
            if self.position.x > WINDOW_WIDTH//2:
                self.position.x = 86
            else:
                self.position.x = WINDOW_WIDTH - 150
            #Top and bottom
            if self.position.y > WINDOW_HEIGHT//2:
                self.position.y = 64
            else:
                self.position.y = WINDOW_HEIGHT - 132

            self.rect.bottomleft = self.position


    def check_animations(self):
        #Animate the player jump
        if self.animate_jump:
            if self.velocity.x > 0:
                self.animate(self.jump_right_sprites, .1)
            else:
                self.animate(self.jump_left_sprites, .1)


    def jump(self):
        #Only jump if on a platform
        if pygame.sprite.spritecollide(self, self.platform_group, False):
            self.resources.jump_sound.play()
            self.velocity.y = -1*self.VERTICAL_JUMP_SPEED
            self.animate_jump = True


    def reset(self):
        self.velocity = Vector2(0,0)
        self.position = Vector2(self.starting_x, self.starting_y)
        self.rect.bottomleft = self.position


    def animate(self, sprite_list, speed):
        if self.index < len(sprite_list) -1:
            self.index += speed
        else:
            self.index = 0
            if self.animate_jump:
                self.animate_jump = False

        self.image = sprite_list[int(self.index)]

class Zombie(pygame.sprite.Sprite):

    def __init__(self, resources, platform_group, portal_group, min_speed, max_speed):
        super().__init__()

        #Set constant variables
        self.VERTICAL_ACCELERATION = 3 #Gravity
        gender = random.randint(0,1)
        if gender == 0:
            zombie_images = resources.image_zombie_boy
        else:
            zombie_images = resources.image_zombie_giri

        #Walking
        self.walk_right_sprites = zombie_images['Walking_right']
        self.walk_left_sprites = [pygame.transform.flip(s, True, False) for s in self.walk_right_sprites]

        #Dying
        self.die_right_sprites = zombie_images['Dying_right']
        self.die_left_sprites = [pygame.transform.flip(s, True, False) for s in self.die_right_sprites]


        #Load an image and get rect
        self.direction = random.choice([-1, 1])

        self.index = 0
        if self.direction == -1:
            self.image = self.walk_left_sprites[self.index]
        else:
            self.image = self.walk_right_sprites[self.index]
        
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (random.randint(100, WINDOW_WIDTH - 100), -100)

        #Attach sprite groups
        self.platform_group = platform_group
        self.portal_group = portal_group

        self.resources = resources

        #Kinematics vectors
        self.position = Vector2(self.rect.x, self.rect.y)
        self.velocity = Vector2(self.direction*random.randint(min_speed, max_speed), 0)
        self.acceleration = Vector2(0, self.VERTICAL_ACCELERATION)

        #Intial zombie values
        self.is_dead = False
        self.round_time = 0
        self.frame_count = 0


    def update(self):
        """Update the zombie"""
        self.move()
        self.check_collisions()
        self.check_animations()


    def move(self):
        if not self.is_dead:
            if self.direction == -1:
                self.animate(self.walk_left_sprites, .5)
            else:
                self.animate(self.walk_right_sprites, .5)
            #Calculate new kinematics values: (4, 1) + (2, 8) = (6, 9)
            self.velocity += self.acceleration
            self.position += self.velocity + 0.5*self.acceleration

            #Update rect based on kinematic calculations and add wrap around movement
            if self.position.x < 0:
                self.position.x = WINDOW_WIDTH
            elif self.position.x > WINDOW_WIDTH:
                self.position.x = 0
            
            self.rect.bottomleft = self.position


    def check_collisions(self):
        """Check for collisions with platforms and portals"""
        #Collision check between zombie and platforms when falling
        collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False)
        if collided_platforms:
            self.position.y = collided_platforms[0].rect.top + 1
            self.velocity.y = 0

        #Collision check for portals
        if pygame.sprite.spritecollide(self, self.portal_group, False):
            self.resources.portal_sound.play()
            #Determine which portal you are moving to
            #Left and right
            if self.position.x > WINDOW_WIDTH//2:
                self.position.x = 86
            else:
                self.position.x = WINDOW_WIDTH - 150
            #Top and bottom
            if self.position.y > WINDOW_HEIGHT//2:
                self.position.y = 64
            else:
                self.position.y = WINDOW_HEIGHT - 132

            self.rect.bottomleft = self.position


    def check_animations(self):
        #Animate the zombie death
        if self.is_dead:
            if self.direction == 1:
                self.animate(self.die_right_sprites, .095)
            else:
                self.animate(self.die_left_sprites, .095)


    def animate(self, sprite_list, speed):
        """Animate the zombie's actions"""
        if self.index < len(sprite_list) -1:
            self.index += speed
        else:
            self.index = 0
            #End the death animation
            if self.is_dead:
                self.kill()

        self.image = sprite_list[int(self.index)]

class RubyMaker(pygame.sprite.Sprite):

    def __init__(self, x, y, resources,main_group):
        super().__init__()

        #Animation frames
        self.ruby_sprites = resources.image_ruby

       #Load image and get rect
        self.index = 0
        self.image = self.ruby_sprites[self.index]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        #Add to the main group for drawing purposes
        main_group.add(self)


    def update(self):
        self.animate(self.ruby_sprites, .25)


    def animate(self, sprite_list, speed):
        if self.index < len(sprite_list) -1:
            self.index += speed
        else:
            self.index = 0

        self.image = sprite_list[int(self.index)]

class Ruby(pygame.sprite.Sprite):

    def __init__(self, resources, platform_group, portal_group):
        super().__init__()

        #Set constant variables
        self.VERTICAL_ACCELERATION = 3 #Gravity
        self.HORIZONTAL_VELOCITY = 5

        #Animation frames
        self.ruby_sprites = resources.image_ruby

        #Load image and get rect
        self.index = 0
        self.image = self.ruby_sprites[self.index]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (WINDOW_WIDTH//2, 100)

        #Attach sprite groups
        self.platform_group = platform_group
        self.portal_group = portal_group

        #Load sounds
        self.portal_sound = resources.portal_sound

        #Kinematic vectors
        self.position = Vector2(self.rect.x, self.rect.y)
        self.velocity = Vector2(random.choice([-1*self.HORIZONTAL_VELOCITY, self.HORIZONTAL_VELOCITY]), 0)
        self.acceleration = Vector2(0, self.VERTICAL_ACCELERATION)


    def update(self):
        self.animate(self.ruby_sprites, .25)
        self.move()
        self.check_collisions()


    def move(self):
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5*self.acceleration

        #Update rect based on kinematic calculations and add wrap around movement
        if self.position.x < 0:
            self.position.x = WINDOW_WIDTH
        elif self.position.x > WINDOW_WIDTH:
            self.position.x = 0
        
        self.rect.bottomleft = self.position


    def check_collisions(self):
        #Collision check between ruby and platforms when falling
        collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False)
        if collided_platforms:
            self.position.y = collided_platforms[0].rect.top + 1
            self.velocity.y = 0

        #Collision check for portals
        if pygame.sprite.spritecollide(self, self.portal_group, False):
            self.portal_sound.play()
            #Determine which portal you are moving to
            #Left and right
            if self.position.x > WINDOW_WIDTH//2:
                self.position.x = 86
            else:
                self.position.x = WINDOW_WIDTH - 150
            #Top and bottom
            if self.position.y > WINDOW_HEIGHT//2:
                self.position.y = 64
            else:
                self.position.y = WINDOW_HEIGHT - 132

            self.rect.bottomleft = self.position


    def animate(self, sprite_list, speed):
        """Animate the ruby"""
        if self.index < len(sprite_list) -1:
            self.index += speed
        else:
            self.index = 0

        self.image = sprite_list[int(self.index)]

class Portal(pygame.sprite.Sprite):
    """A class that if collided with will transport you"""

    def __init__(self, x, y, resources, color, portal_group):
        """Initialize the portal"""
        super().__init__()

        #Animation frames
        self.portal_sprites = resources.image_portal[color]

        #Load an image and get a rect
        self.index = random.randint(0, len(self.portal_sprites)-1)
        self.image = self.portal_sprites[self.index]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        #Add to the portal group
        portal_group.add(self)


    def update(self):
        """Update the portal"""
        self.animate(self.portal_sprites, .2)


    def animate(self, sprite_list, speed):
        """Animate the portal"""
        if self.index < len(sprite_list) -1:
            self.index += speed
        else:
            self.index = 0

        self.image = sprite_list[int(self.index)]

class Game():

    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Zombie Knight")
        #Set constant variables
        self.STARTING_ROUND_TIME = 30
        self.STARTING_ZOMBIE_CREATION_TIME = 5
        self.clock = pygame.time.Clock()
        #Set game values
        self.score = 0
        self.round_number = 1
        self.running = False
        self.round_time = self.STARTING_ROUND_TIME
        self.round_count_time = pygame.time.get_ticks()
        self.zombie_creation_time = pygame.time.get_ticks()
        self.ruby_creation_time = pygame.time.get_ticks()
        self.resources = Resources()

        self.title_font = self.resources.title_font
        self.HUD_font = self.resources.HUD_font
        self.set_sprites()
        self.set_tile()

    def set_sprites(self):
        #Create sprite groups
        self.main_tile_group = pygame.sprite.Group()
        self.platform_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.zombie_group = pygame.sprite.Group()
        self.portal_group = pygame.sprite.Group()
        self.ruby_group = pygame.sprite.Group()

    def set_tile(self):
        tile_map = self.resources.tile_map
        for i in range(len(tile_map)):
            #Loop through the 40 elements in a given list (cols) (j moves us across the map)
            for j in range(len(tile_map[i])):
                #Dirt tiles
                if tile_map[i][j] in [1,2,3,4,5]:
                    Tile(j*32, i*32, self.resources, tile_map[i][j], self.main_tile_group, self.platform_group)
                #Ruby Maker
                elif tile_map[i][j] == 6:
                    RubyMaker(j*32, i*32, self.resources, self.main_tile_group)
                #Portals
                elif tile_map[i][j] == 7:
                    Portal(j*32, i*32, self.resources, "green", self.portal_group)
                elif tile_map[i][j] == 8:
                    Portal(j*32, i*32, self.resources, "purple", self.portal_group)
                #Player
                elif tile_map[i][j] == 9:
                    self.player = Player(j*32 - 32, i*32 + 32, self.resources, self.platform_group, self.portal_group)
                    self.player_group.add(self.player)

    def update(self):
        #Update the round time every second
        if pygame.time.get_ticks() - self.round_count_time > 1000:
            self.round_time -= 1
            self.round_count_time = pygame.time.get_ticks()


        self.main_tile_group.update()
        self.portal_group.update()
        self.player_group.update()
        self.zombie_group.update()
        self.ruby_group.update()

        self.check_collisions()
        self.add_zombie()
        self.add_ruby()
        self.check_round_completion()
        self.check_game_over()


    def draw(self):

        background_rect = self.resources.background_image.get_rect()
        background_rect.topleft = (0, 0)

        #Draw the HUD
        self.display_surface.blit(self.resources.background_image, background_rect)
        self.main_tile_group.draw(self.display_surface)
        self.portal_group.draw(self.display_surface)
        self.player_group.draw(self.display_surface)
        #self.bullet_group.draw(self.display_surface)
        self.zombie_group.draw(self.display_surface)
        self.ruby_group.draw(self.display_surface)

        #Set text
        score_text = self.HUD_font.render("Score: " + str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (10, WINDOW_HEIGHT - 50)

        health_text = self.HUD_font.render("Health: " + str(self.player.health), True, WHITE)
        health_rect = health_text.get_rect()
        health_rect.topleft = (10, WINDOW_HEIGHT - 25)

        title_text = self.title_font.render("Zombie Knight", True, GREEN)
        title_rect = title_text.get_rect()
        title_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT - 25)

        round_text = self.HUD_font.render("Night: " + str(self.round_number), True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.topright = (WINDOW_WIDTH - 10, WINDOW_HEIGHT - 50)

        time_text = self.HUD_font.render("Sunrise In: " + str(self.round_time), True, WHITE)
        time_rect = time_text.get_rect()
        time_rect.topright = (WINDOW_WIDTH - 10, WINDOW_HEIGHT - 25)

        self.display_surface.blit(score_text, score_rect)
        self.display_surface.blit(health_text, health_rect)
        self.display_surface.blit(title_text, title_rect)
        self.display_surface.blit(round_text, round_rect)
        self.display_surface.blit(time_text, time_rect)
        

    def add_zombie(self):
        #Check to add a zombie every second
        if pygame.time.get_ticks() - self.zombie_creation_time > 3000:
                zombie = Zombie(self.resources, self.platform_group, self.portal_group, self.round_number, 5 + self.round_number)
                self.zombie_group.add(zombie)
                self.zombie_creation_time = pygame.time.get_ticks()

    def add_ruby(self):
        if pygame.time.get_ticks() - self.ruby_creation_time > 6000:
            ruby = Ruby(self.resources, self.platform_group, self.portal_group)
            self.ruby_group.add(ruby)
            self.ruby_creation_time = pygame.time.get_ticks() 

    def check_collisions(self):

        collision_list = pygame.sprite.spritecollide(self.player, self.zombie_group, False)
        if collision_list:
            for zombie in collision_list:
                if not zombie.is_dead:
                    if (self.player.velocity.y > 0 and 
                        self.player.rect.centery < zombie.rect.top):
                        zombie.is_dead = True
                        self.resources.zombie_hit_sound.play()
                        self.score += 25

                    #The zombie isn't dead, so take damage
                    else:
                        self.player.health -= 20
                        self.resources.hit_sound.play()
                        #Move the player to not continually take damage
                        self.player.position.x +=  60* zombie.direction
                        self.player.position.y -= 20
                        self.player.rect.bottomleft = self.player.position

        #See if a player collided with a ruby
        if pygame.sprite.spritecollide(self.player, self.ruby_group, True):
            self.resources.ruby_pickup_sound.play()
            self.score += 100
            self.player.health += 10
            if self.player.health > self.player.STARTING_HEALTH:
                self.player.health = self.player.STARTING_HEALTH

        #See if a living zombie collided with a ruby
        for zombie in self.zombie_group:
            if zombie.is_dead == False:
                if pygame.sprite.spritecollide(zombie, self.ruby_group, True):
                    self.resources.lost_ruby_sound.play()
                    zombie = Zombie(self.resources, self.platform_group, self.portal_group, self.round_number, 5 + self.round_number)
                    self.zombie_group.add(zombie)


    def check_round_completion(self):
        """Check if the player survived a single night"""
        if self.round_time == 0:
            self.start_new_round()


    def check_game_over(self):
        """Check to see if the player lost the game"""
        if self.player.health <= 0:
            pygame.mixer.music.stop()
            self.pause_game("Game Over! Final Score: " + str(self.score), "Press 'Enter' to play again...")
            self.reset_game()


    def start_new_round(self):
        """Start a new night"""
        self.round_number += 1

        #Reset round values
        self.round_time = self.STARTING_ROUND_TIME

        self.zombie_group.empty()
        self.ruby_group.empty()
        #self.bullet_group.empty()
        self.player.reset()
        self.pause_game("You survived the night!", "Press 'Enter' to continue...")


    def pause_game(self, main_text, sub_text):
        """Pause the game"""

        pygame.mixer.music.pause()

        #Create main pause text
        main_text = self.title_font.render(main_text, True, GREEN)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        #Create sub pause text
        sub_text = self.title_font.render(sub_text, True, WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 64)

        #Display the pause text
        self.display_surface.fill(BLACK)
        self.display_surface.blit(main_text, main_rect)
        self.display_surface.blit(sub_text, sub_rect)
        pygame.display.update()

        #Pause the game until user hits enter or quits
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    #User wants to continue
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                        self.running = True
                        pygame.mixer.music.unpause()
                #User wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    self.running = False
                    pygame.mixer.music.stop()


    def reset_game(self):
        """Reset the game"""
        #Reset game values
        self.score = 0
        self.round_number = 1
        self.round_time = self.STARTING_ROUND_TIME
        self.round_count_time = pygame.time.get_ticks()
        self.zombie_creation_time = pygame.time.get_ticks()
        self.ruby_creation_time = pygame.time.get_ticks()

        #Reset the player
        self.player.health = self.player.STARTING_HEALTH
        self.player.reset()

        #Empty sprite groups
        self.zombie_group.empty()
        self.ruby_group.empty()
        #self.bullet_group.empty()

        pygame.mixer.music.play(-1, 0.0)

    def play(self):
        self.pause_game("Zombie Knight", "Press 'Enter' to Begin")
        while self.running:
            #Check to see if the user wants to quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    #Player wants to jump
                    if event.key == pygame.K_UP:
                        self.player.jump()

            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(FPS)
           
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.play()