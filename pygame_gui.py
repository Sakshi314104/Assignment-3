import pygame
import random
import sys

# Basic tip
# space = Jump,'
# f=fire

# pygame
pygame.init()


# Game paramaeters
# game dimenstions
GAME_SCREEN_WIDTH = 800
GAME_SCREEN_HEIGHT = 400

# fps of game
FPS = 60
# falling of player
GRAVITY = 0.75
# thresh scrolling
SCROLL_THRESH = 200
# max_levels
MAX_LEVELS = 3

# Colors coding
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19) 

# Create screen
screen = pygame.display.set_mode((GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

def create_surface(color, width, height):
    # create Pygame surface
    surface_ = pygame.Surface((width, height))
    surface_.fill(color)
    return surface_

class Player(pygame.sprite.Sprite):
    # player create
    def __init__(self, x, y):
        super().__init__()
        # my player shape
        self.image = create_surface(BROWN, 30, 50) 
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
        # jumping velocity  
        self.velocity_y = 0 
        # prevents multiple jumps
        self.jumping = False
        # direction -1 left & 1 for right
        self.direction = 1 
        self.speed = 6
        self.health = 100
        self.max_health = 100
        self.lives = 3
        self.score = 0
        self.flip = False 
        self.shoot_cooldown = 0 

    # update player's state, like movments etc  
    def update(self): 
        dx = 0
        dy = 0
        # shoot cooldown Decrease 
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        key = pygame.key.get_pressed()
        # horzontal movement control
        if key[pygame.K_LEFT]:
            # speed
            dx = -self.speed
            # direction
            self.direction = -1
            # flip when moving left
            self.flip = True 
        if key[pygame.K_RIGHT]:
            dx = self.speed
            self.direction = 1
            # no flip when moving right
            self.flip = False 
        
        # jumping
        if key[pygame.K_SPACE] and not self.jumping:
            # upward velocity 
            self.velocity_y = -15 
            self.jumping = True
        
        # gravity 
        self.velocity_y += GRAVITY
        if self.velocity_y > 10: 
            self.velocity_y = 10
        dy += self.velocity_y

        #player's position update 
        self.rect.x += dx
        self.rect.y += dy
        
        # reset jumping stats
        if self.rect.bottom > GAME_SCREEN_HEIGHT - 50:
            self.rect.bottom = GAME_SCREEN_HEIGHT - 50
            self.jumping = False 
            # no vertical movement
            self.velocity_y = 0 

    
       #for firing 
    def shoot(self):

        if self.shoot_cooldown == 0:
            # For faster firing cooldown to 5 frames
            self.shoot_cooldown = 7 
            # shoot right direction
            if self.direction == 1:
                myfire_bullet = movement_handling(self.rect.right, self.rect.centery, self.direction)
            else:
                # shoot right direction right
                myfire_bullet = movement_handling(self.rect.left, self.rect.centery, self.direction)
            return myfire_bullet
        return None
    
    # health
    def draw_health(self, world_shift): 
    #    this is the ration of current health 
    # and max_health
        ratio_of_health = self.health / self.max_health
        # health bar 
        pygame.draw.rect(screen, RED, (self.rect.x + world_shift, self.rect.y - 11, 30, 5)) # Background (red for lost health)
        pygame.draw.rect(screen, GREEN, (self.rect.x + world_shift, self.rect.y - 11, 30 * ratio_of_health, 5)) # Foreground (green for current health)

# handle moving of player and enemies.Firings of player
class movement_handling(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        # bullet color
        self.image = create_surface(BLUE, 10, 5) 
        self.rect = self.image.get_rect()
        # xcoordinate
        self.rect.x = x 
        # ycoordinate
        self.rect.y = y 
        # direction to go
        self.direction = direction 
        # bullet speed
        self.speed = 12 
        # damage to enemies
        self.damage = 25 
        
    def update(self, world_shift): 
        # Move movement_handling in world coordinates
        self.rect.x += (self.direction * self.speed) 
        # check the off-screen
        if (self.rect.right + world_shift) < 0 or (self.rect.left + world_shift) > GAME_SCREEN_WIDTH:
            self.kill()

# create enemy , and boss.handle movements, health
class Game_Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y, enemy_type):
        super().__init__()
        self.enemy_type = enemy_type
        # this is for normal enemy
        if enemy_type == "normal":
            self.image = create_surface(RED, 30, 50) 
            self.health = 50
            self.speed = 2
            # score I get
            self.score = 100 
            # this is for boss
        elif enemy_type == "boss":
            self.image = create_surface((255, 165, 0), 60, 80) 
            self.health = 200
            self.speed = 1
            # score I get
            self.score = 500 
        
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 
        self.move_direction = 1 
        self.move_counter = 0 
        self.max_health = self.health 
    # update emrmy position    
    def update(self, world_shift):
        self.rect.x += (self.move_direction * self.speed) 
        self.move_counter += 1
        # after some frames change the direction
        if self.move_counter > 50:
            self.move_direction *= -1
            self.move_counter = 0
          # 
    def draw_health(self, world_shift):
        ratio_health = self.health / self.max_health
        bar_width_heath = self.rect.width if self.enemy_type == "normal" else 60 # Boss has a fixed bar width
        # bar
        pygame.draw.rect(screen, RED, (self.rect.x + world_shift, self.rect.y - 10, bar_width_heath, 5)) # Background (red)
        pygame.draw.rect(screen, GREEN, (self.rect.x + world_shift, self.rect.y - 10, bar_width_heath * ratio_health, 5)) # Foreground (green)

# collecting thins like health boost or extra life
class Extra_health_bonus(pygame.sprite.Sprite):
    def __init__(self, x, y, Extra_health__type):
        super().__init__()
        self.image = create_surface(GREEN, 20, 20) 
        self.Extra_health__type = Extra_health__type
        if Extra_health__type == "health":
            # health_score_amount
            self.value = 25 
        elif Extra_health__type == "life":
            self.image = create_surface((255, 192, 203), 20, 20) 
            # life gain
            self.value = 1 
        
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 

# interaction_between game of players and enemies 
class World():
    def __init__(self, level):
        self.level = level
        self.world_shift = 0 
        
        self.level_length = 1200 + (level * 200) 
        # sky blue background
        self.bg_color = (135, 206, 235) 
        self.ground_height = 50 
        # level complete flag
        self.completed = False 
        self.boss_spawned = False
        # boss defeat flag
        self.boss_defeated = False 
        # end reach falg
        self.end_reached = False 

        # create game objects
        self.player = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()
        self.bullets_fire = pygame.sprite.Group()
        self.health_plus_bonus = pygame.sprite.Group()
        
        # Add the player to the world
        self.player.add(Player(100, GAME_SCREEN_HEIGHT - 150)) # Player starts at world X 100
        # Generate the level elements
        self.create_level_game()
    # 
    def create_level_game(self):
        """
        Generates enemies and health_plus_bonus for the current level.
        """
        # Clear any existing enemies and health_plus_bonus from previous levels
        self.enemies.empty()
        self.health_plus_bonus.empty()
        # new level boss spawn laf
        self.boss_spawned = False 
        # boss defeat flag reset
        self.boss_defeated = False 
        # end level flag reset
        self.end_reached = False 
        # level complete flag
        self.completed = False 
        # new level work shift flag reset
        self.world_shift = 0 
        # enemies added on a regualr level
        for i in range(5 + self.level * 2):
            x_values = random.randint(300, self.level_length - 100)
            y_values = GAME_SCREEN_HEIGHT - 100
            self.enemies.add(Game_Enemy(x_values, y_values, "normal"))
        
        # Add health_plus_bonus based on level
        for i in range(3 + self.level):
            x = random.randint(200, self.level_length - 100)
            y = random.randint(100, GAME_SCREEN_HEIGHT - 150) # Collectibles can be higher up (world Y)
            type_ = random.choice(["health", "life"])
            self.health_plus_bonus.add(Extra_health_bonus(x, y, type_))
    
    def spawn_boss(self):

        if not self.boss_spawned:
            # add boss at the end of the level
            self.enemies.add(Game_Enemy(self.level_length - 200, GAME_SCREEN_HEIGHT - 130, "boss"))
            self.boss_spawned = True
            # display output
            print("BOSS SPAWNED") 
            
    # update game elements
    def update(self):
        player = self.player.sprite
        player.update() 
        
        # play screen position update
        player_screen_x_position = player.rect.x + self.world_shift
        
        # player moves to left so based on some threshold the display change
        if player_screen_x_position > GAME_SCREEN_WIDTH - SCROLL_THRESH:
            self.world_shift -= (player_screen_x_position - (GAME_SCREEN_WIDTH - SCROLL_THRESH))
            
        # If player moves left and hits threshold, shift world right
        if player_screen_x_position < SCROLL_THRESH:
            self.world_shift += (SCROLL_THRESH - player_screen_x_position)

        # Cannot scroll past the end of the level 
        if self.world_shift > 0: 
            self.world_shift = 0
        # Cannot scroll past the end of the level (world_shift cannot be less than max_shift)
        max_world_shift = -(self.level_length - GAME_SCREEN_WIDTH)
        if self.world_shift < max_world_shift:
            self.world_shift = max_world_shift
            
        # boss comes when player near the end
        if not self.boss_spawned and player.rect.x > self.level_length - 400:
            self.spawn_boss()
        
     #  level completion condition
        if self.world_shift <= -(self.level_length - GAME_SCREEN_WIDTH):
            self.end_reached = True
            print("Great END REACHED ") 
        
        # Update all other sprites (their rect.x/y are world coordinates)
        self.enemies.update(self.world_shift)
        self.bullets_fire.update(self.world_shift)
        self.health_plus_bonus.update(self.world_shift) 
        
        # Check if boss is defeated (still useful for score/feedback)
        if self.boss_spawned and len(self.enemies) == 0:
            self.boss_defeated = True
            print("BOSS DEFEATED") # Debug message
        
        # NEW LEVEL COMPLETE CONDITION: Player just needs to reach the end
        if self.end_reached:
            self.completed = True
            print("LEVEL COMPLETE") # Debug message
            return "level_complete"
        
        # Check for collisions between player, bullets_fire, enemies, and health_plus_bonus
        collision_result = self.check_players_collisions()
        if collision_result == "game_over":
            return "game_over" # Return game_over if player runs out of lives
        
        return "playing" # Default state if no special conditions met
    
        # check all collisions.
    def check_players_collisions(self):
        player = self.player.sprite
        
        # Create a screen-relative rect 
        player_screen_rect = pygame.Rect(player.rect.x + self.world_shift, player.rect.y, player.rect.width, player.rect.height)
        
        # Player with enemies collision
        for enemy in self.enemies:
            # Create a screen-relative rect for the enemy
            enemy_screen_rect = pygame.Rect(enemy.rect.x + self.world_shift, enemy.rect.y, enemy.rect.width, enemy.rect.height)
            if player_screen_rect.colliderect(enemy_screen_rect): # Use colliderect for temporary rects
                # loss health
                player.health -= 1
                if player.health <= 0:
                    # loss life
                    player.lives -= 1 
                    player.health = player.max_health 
                    # game over no life
                    if player.lives <= 0:
                        return "game_over, Try again" 
                    
        
        
        for movement_handling in self.bullets_fire:
            # Create a screen-relative rect for the movement_handling
            projectile_screen_rect = pygame.Rect(movement_handling.rect.x + self.world_shift, movement_handling.rect.y, movement_handling.rect.width, movement_handling.rect.height)
            
            # Find enemies hit by this movement_handling, using screen-relative rects
            # We iterate through enemies and check collision manually
            enemies_hit_by_projectile = []
            for enemy in self.enemies:
                enemy_screen_rect = pygame.Rect(enemy.rect.x + self.world_shift, enemy.rect.y, enemy.rect.width, enemy.rect.height)
                if projectile_screen_rect.colliderect(enemy_screen_rect):
                    enemies_hit_by_projectile.append(enemy)

            for enemy in enemies_hit_by_projectile:
                enemy.health -= movement_handling.damage # Game_Enemy takes damage
                movement_handling.kill() # movement_handling is destroyed on hit
                if enemy.health <= 0:
                    player.score += enemy.score # Add score for defeating enemy
                    enemy.kill() # Remove enemy from game
        
        # Player with health_plus_bonus collision
        for collectible in self.health_plus_bonus:
            # Create a screen-relative 
            collectible_screen_rect = pygame.Rect(collectible.rect.x + self.world_shift, collectible.rect.y, collectible.rect.width, collectible.rect.height)
            if player_screen_rect.colliderect(collectible_screen_rect): 
                if collectible.Extra_health__type == "health":
                    # Restore health
                    player.health = min(player.health + collectible.value, player.max_health) 
                elif collectible.Extra_health__type == "life":
                    player.lives += collectible.value # Gain a life
                collectible.kill() # Remove collectible
                player.score += 50 # Add score for collecting
        
        return "playing"
        
    # draw game elements
    def draw(self):
        # sky color background 
        screen.fill(self.bg_color) 
        # Draw ground green rectangle
        pygame.draw.rect(screen, (34, 139, 34), (self.world_shift, GAME_SCREEN_HEIGHT - self.ground_height, 
                                                 self.level_length, self.ground_height))
        
        #  health bars , draw enemies and their
        for enemy in self.enemies:
            screen.blit(enemy.image, (enemy.rect.x + self.world_shift, enemy.rect.y))
            enemy.draw_health(self.world_shift) 
        
        # Draw health_plus_bonus
        for collectible in self.health_plus_bonus:
            screen.blit(collectible.image, (collectible.rect.x + self.world_shift, collectible.rect.y))
        
        # Draw bullets_fire, adjusted by world_shift
        for movement_handling in self.bullets_fire:
            screen.blit(movement_handling.image, (movement_handling.rect.x + self.world_shift, movement_handling.rect.y))
        
        # Draw player and their health bar, adjusted by world_shift
        player = self.player.sprite
        screen.blit(pygame.transform.flip(player.image, player.flip, False), (player.rect.x + self.world_shift, player.rect.y))
        player.draw_health(self.world_shift) # Pass world_shift to player.draw_health()
        
        # Display score, lives, and current level
        font = pygame.font.SysFont('Arial', 20)
        score_text = font.render(f'Score: {player.score}', True, BLACK)
        lives_text = font.render(f'Lives: {player.lives}', True, BLACK)
        level_text = font.render(f'Level: {self.level}', True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 40))
        screen.blit(level_text, (10, 70))

# main clas to manage overall game 
class Game:

    def __init__(self):
        # start with level 
        self.level = 1 

        self.world = World(self.level) # Initialize the first world/level
        # flag status for game over
        self.game_over = False 
        # flag status for all stages clear.
        self.game_complete = False 
        # prevent input during level transition new flag
        self.level_transitioning = False 
    
    def run(self):

    
        # Event handling
        for event in pygame.event.get():
            # close button
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r and (self.game_over or self.game_complete):
                    self.__init__() 
               
                if event.key == pygame.K_f and not self.game_over and not self.game_complete and not self.level_transitioning:
                    bullet = self.world.player.sprite.shoot()
                    if bullet:
                        self.world.bullets_fire.add(bullet)
        
        # Game logic
        if not self.game_over and not self.game_complete:
            result = self.world.update() 
            
            if result == "game_over":
                self.game_over = True 
            elif result == "level_complete":
                self.level_transitioning = True 

                # Show level complete message
                screen.fill(WHITE)
                font = pygame.font.SysFont('Arial', 40)
                level_text = font.render(f'Level {self.level} Complete!', True, BLACK)
                next_text = font.render('Loading next level...', True, BLACK)
                screen.blit(level_text, (GAME_SCREEN_WIDTH//2 - level_text.get_width()//2, GAME_SCREEN_HEIGHT//2 - 30))
                screen.blit(next_text, (GAME_SCREEN_WIDTH//2 - next_text.get_width()//2, GAME_SCREEN_HEIGHT//2 + 30))
                pygame.display.update()
                # 3 second delay before loading next level
                pygame.time.delay(3000) 
                
                if self.level < MAX_LEVELS:
                    # Move to next level then max 3 levels
                    self.level += 1
                    # Preserve player stats 
                    player_stats = {
                        'score': self.world.player.sprite.score,
                        'lives': self.world.player.sprite.lives,
                        'health': self.world.player.sprite.health
                    }
                    self.world = World(self.level) # Create a new world for the next level
                 
                    self.world.player.sprite.score = player_stats['score']
                    self.world.player.sprite.lives = player_stats['lives']
                    self.world.player.sprite.health = player_stats['health']
                else:
                    #completed all levels
                    self.game_complete = True 
                    #Reset flag after transition
                self.level_transitioning = False 
            # make a new world
            self.world.draw() 
        else:
            # Display when the game complete or over.
            screen.fill(WHITE)
            font = pygame.font.SysFont('Arial', 40)
            
            if self.game_over:
                text = font.render('GAME OVER sorry buddy - Press R to restart', True, BLACK)
            else:
                text = font.render('YOU WIN!, Great Buddy - Press R to restart', True, BLACK)
            
            score_text = font.render(f'Final Score: {self.world.player.sprite.score}', True, BLACK)
            screen.blit(text, (GAME_SCREEN_WIDTH//2 - text.get_width()//2, GAME_SCREEN_HEIGHT//2 - 50))
            screen.blit(score_text, (GAME_SCREEN_WIDTH//2 - score_text.get_width()//2, GAME_SCREEN_HEIGHT//2 + 10))
        
        pygame.display.update() 
        clock.tick(FPS) 




if __name__ == "__main__":
    game = Game()
    while True:
        game.run()

