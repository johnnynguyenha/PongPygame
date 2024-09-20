from settings import *
from random import choice, uniform
import time

class Paddle(pygame.sprite.Sprite): # notice that players and opponents are both paddles
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.Surface(SIZE['paddle'], pygame.SRCALPHA)
        pygame.draw.rect(self.image, COLORS['paddle'], pygame.FRect((0, 0), SIZE['paddle']), 0, 4) #rounded corners for rectangle
        self.rect = self.image.get_frect(center = POS['player'])
        self.old_rect = self.rect.copy()
        self.direction = 0
        self.shadow_surf = self.image.copy()
        pygame.draw.rect(self.shadow_surf, COLORS['paddle shadow'], pygame.FRect((0, 0), SIZE['paddle']), 0, 4) #rounded corners for rectangle

    def move(self, dt):
        if (self.rect.left < 0):
            self.rect.left = 0
        if (self.rect.right > WINDOW_WIDTH):
            self.rect.right = WINDOW_WIDTH
        if (self.rect.bottom > WINDOW_HEIGHT):
            self.rect.bottom = WINDOW_HEIGHT
        if (self.rect.top < 0):
            self.rect.top = 0
        self.rect.y += self.direction * self.velocity * dt

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)

class Player(Paddle): #inherits from paddle
    def __init__(self, groups):
        super().__init__(groups)
        self.velocity = SPEED['player']
        

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

class Opponent(Paddle): # opponent inherits from paddle
    def __init__(self, groups, ball):
        super().__init__(groups)
        self.velocity = SPEED['opponent']
        self.rect.center = POS['opponent']
        self.ball = ball

    def input(self):
        if (self.rect.centery < self.ball.rect.centery): # if the opponent is under the ball, go up
            self.direction = 1
        if (self.rect.centery > self.ball.rect.centery):
            self.direction = -1

class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, paddle_sprites, update_score):
        super().__init__(groups)
        self.update_score = update_score
        self.image = pygame.Surface(SIZE['ball'], pygame.SRCALPHA)
        pygame.draw.circle(self.image, COLORS['ball'], (SIZE['ball'][0]/2, SIZE['ball'][1]/2), SIZE['ball'][0]/2) # the image is still technically a rect, we are just drawing a circle on top of an invisible box
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.direction = pygame.Vector2(choice((-1,1)), uniform(0.7, 0.8) * choice((-1, 1)))
        self.velocity = SPEED['ball']
        self.paddle_sprites = paddle_sprites
        self.old_rect = self.rect.copy()
        self.clock = pygame.time.get_ticks()
        self.is_resetting = False
        self.reset_time = 0

        #shadow surface
        self.shadow_surf = self.image.copy()
        pygame.draw.circle(self.shadow_surf, COLORS['ball shadow'], (SIZE['ball'][0]/2, SIZE['ball'][1]/2), SIZE['ball'][0]/2) # the image is still technically a rect, we are just drawing a circle on top of an invisible box


    def move(self, dt):
        self.rect.x += self.direction.x * self.velocity * dt  
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.velocity * dt
        self.collision('vertical')

    def collision(self, direction): #code to check for moving object collision
        for sprite in self.paddle_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal': # if the ball hit the left side of the paddle and in the frame before the collision, was the ball's right side less than the paddle's left side (meaning the ball hit the paddle from left to right)
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect   .right = sprite.rect.left
                        self.direction.x *= -1
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.direction.x *= -1
                else:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top: #checks if the bottom of the ball hits the top of the paddle and if the ball was on top of the paddle in the previous frame
                        self.rect.bottom = sprite.rect.top
                        self.direction.y *= -1
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom: #checks if the top of the ball hits the bottom of the paddle and if the ball was on bottom of the paddle in the previous frame
                        self.rect.top = sprite.rect.bottom
                        self.direction.y *= -1

    def wall_collision(self):
        if (self.rect.left < 0):
            self.update_score('player')
            self.reset()
        if (self.rect.right > WINDOW_WIDTH):
            self.update_score('opponent')
            self.reset()
        if (self.rect.bottom > WINDOW_HEIGHT):
            self.direction.y = self.direction.y * -1
            self.rect.bottom = WINDOW_HEIGHT
        if (self.rect.top < 0):
            self.rect.top = 0
            self.direction.y = self.direction.y * -1
    def reset(self):
        self.rect.center = (WINDOW_WIDTH /2, WINDOW_HEIGHT/2)
        self.direction = pygame.Vector2(0,0)
        self.is_resetting = True
        self.reset_time = pygame.time.get_ticks()

    def resume(self):
        if self.is_resetting:
            if pygame.time.get_ticks() - self.reset_time > 1000:  # Check if 2 seconds passed
                self.is_resetting = False  # Reset is over
        if not self.is_resetting:
            self.direction = pygame.Vector2(choice((-1,1)), uniform(0.7, 0.8) * choice((-1, 1)))
    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.move(dt)
        self.wall_collision()
        if self.is_resetting:
            self.resume()

