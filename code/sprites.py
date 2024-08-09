from settings import *
from times import Timer
from math import sin
from random import randint

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Bullet(Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(pos, surf, groups)

        # Bullet facing adjustment
        self.image = pygame.transform.flip(self.image, direction == -1, False)

        # Movement for the bullet
        self.direction = direction
        self.speed = 850

    def update(self, dt):
        self.rect.x += self.direction * self.speed * dt

class Fire(Sprite):
    def __init__(self, surf, pos, groups, player):
        super().__init__(pos, surf, groups)
        self.player = player
        self.flip = player.flip
        self.timer = Timer(100, autostart=True, func=self.kill)
        self.y_offset = pygame.Vector2(0, 8)

        if self.player.flip:
            self.rect.midright = self.player.rect.midleft + self.y_offset
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset

    def update(self, _):
        self.timer.update()

        if self.player.flip:
            self.rect.midright = self.player.rect.midleft + self.y_offset
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset

        if self.flip != self.player.flip:
            self.kill()

class AnimatedSprite(Sprite):
    def __init__(self, frames, pos, groups):
        self.frames, self.frame_index, self.animation_speed = frames, 0, 10
        super().__init__(pos, self.frames[self.frame_index], groups)

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
    
class Enemy(AnimatedSprite):
    def __init__(self, frames, pos, groups):
        super().__init__(frames, pos, groups)
        self.death_timer = Timer(200, func=self.kill)

    def destroy(self):
        self.death_timer.activate()
        self.animation_speed = 0
        self.image = pygame.mask.from_surface(self.image).to_surface()
        self.image.set_colorkey('black')

    def update(self, dt):
        self.death_timer.update()
        if not self.death_timer:
            self.animate(dt)
            self.move(dt)
        self.constraint()
    
class Player(AnimatedSprite):
    def __init__(self, pos, groups, collision_sprites, frames, create_bullet):
        super().__init__(frames, pos, groups)
        self.create_bullet = create_bullet

        # Player image
        self.rect = self.image.get_frect(center = pos)
        self.facing_right = True
        self.flip = False

        # Player movement and direction
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites
        self.gravity = 50
        self.on_ground = False

        # Player timers
        self.shoot_timer = Timer(500)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        if keys[pygame.K_SPACE] and self.on_ground:
            self.direction.y = -20  

        if pygame.mouse.get_pressed()[0] and not self.shoot_timer:
            self.create_bullet(self.rect.center, -1 if self.flip else 1)
            self.shoot_timer.activate()

    def move(self, dt):
        # Horizontal movement
        self.rect.centerx += self.direction.x * self.speed * dt
        self.collision('horizontal')

        # Vertical movement
        # This increases the direction value on each frame by the gravity variable multiplied by dt
        self.direction.y += self.gravity * dt
        self.rect.centery += self.direction.y
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

    def check_ground(self):
        # This creates a rectangle on the player that can be used to check if they are on the floor by putting the rectangle on the bottom of the player
        bottom_rect = pygame.FRect((0,0), (self.rect.width, 2)).move_to(midtop = self.rect.midbottom)
        # Looks at the collision between the bottom rectangle and the level rectangle and returns the index of them. -1 means no collision
        self.on_ground = True if bottom_rect.collidelist([sprite.rect for sprite in self.collision_sprites]) >= 0 else False

    def animate(self, dt):
        if self.direction.x:
            self.frame_index += self.animation_speed * dt
            self.flip = self.direction.x < 0
        else:
            self.frame_index = 0

        self.frame_index = 1 if not self.on_ground else self.frame_index
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        self.image = pygame.transform.flip(self.image, self.flip, False)

    def update(self, dt):
        self.shoot_timer.update()
        self.check_ground()
        self.move(dt)
        self.input()
        self.animate(dt)

class Worm(Enemy):
    def __init__(self, frames, rect, groups):
        super().__init__(frames, rect.topleft, groups)
        self.rect.bottomleft = rect.bottomleft
        self.main_rect = rect
        self.speed = randint(200, 350)
        self.direction = 1

    def move(self, dt):
        self.rect.x += self.direction * self.speed * dt

    def constraint(self):
        # If the rectangle is not entirely contained by the main rectangle then flip the frames
        if not self.main_rect.contains(self.rect):
            self.direction *= -1
            self.frames = [pygame.transform.flip(surf, True, False) for surf in self.frames]

class Bee(Enemy):
    def __init__(self, frames, pos, groups, speed):
        super().__init__(frames, pos, groups)
        self.speed = speed
        self.amplitude = randint(400, 600)
        self.frequency = randint(300, 550)

    def move(self, dt):
        self.rect.x -= self.speed * dt
        self.rect.y += sin(pygame.time.get_ticks() / self.frequency) * self.amplitude * dt

    def constraint(self):
        if self.rect.right <= 0:
            self.kill()