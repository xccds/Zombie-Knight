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
        
        self.image_player = {}
        self.image_player['Move_right'] = []
        self.image_player['Idling_right'] = []
        self.image_player['Jumping_right'] = []
        for i in range(1,11):
            self.image_player['Move_right'].append(pygame.transform.scale(pygame.image.load(f"images/player/run/Run ({i}).png"), (64,64)))
            self.image_player['Idling_right'].append(pygame.transform.scale(pygame.image.load(f"images/player/idle/Idle ({i}).png"), (64,64)))
            self.image_player['Jumping_right'].append(pygame.transform.scale(pygame.image.load(f"images/player/jump/Jump ({i}).png"), (64,64)))

        self.jump_sound = pygame.mixer.Sound("sounds/jump_sound.wav")

        # Create the tile map
        self.tile_map = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
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
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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

    def __init__(self, x, y, resources, platform_group):
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
        self.resources = Resources()

        self.set_sprites()
        self.set_tile()

    def set_sprites(self):
        #Create sprite groups
        self.main_tile_group = pygame.sprite.Group()
        self.platform_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()

    def set_tile(self):
        tile_map = self.resources.tile_map
        for i in range(len(tile_map)):
            #Loop through the 40 elements in a given list (cols) (j moves us across the map)
            for j in range(len(tile_map[i])):
                #Dirt tiles
                if tile_map[i][j] in [1,2,3,4,5]:
                    Tile(j*32, i*32, self.resources, tile_map[i][j], self.main_tile_group, self.platform_group)
                #Player
                elif tile_map[i][j] == 9:
                    self.player = Player(j*32 - 32, i*32 + 32, self.resources, self.platform_group)
                    self.player_group.add(self.player)

    def update(self):
        #Update the round time every second
        if pygame.time.get_ticks() - self.round_count_time > 1000:
            self.round_time -= 1
            self.round_count_time = pygame.time.get_ticks()


        self.main_tile_group.update()
        self.player_group.update()

        self.check_round_completion()
        self.check_game_over()


    def draw(self):

        background_rect = self.resources.background_image.get_rect()
        background_rect.topleft = (0, 0)

        #Draw the HUD
        self.display_surface.blit(self.resources.background_image, background_rect)
        self.main_tile_group.draw(self.display_surface)
        self.player_group.draw(self.display_surface)
        

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
        self.player.reset()
        self.pause_game("You survived the night!", "Press 'Enter' to continue...")


    def pause_game(self, main_text, sub_text):
        """Pause the game"""

        #Display the pause text
        self.display_surface.fill(BLACK)
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

        #Reset the player
        self.player.health = self.player.STARTING_HEALTH
        self.player.reset()

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