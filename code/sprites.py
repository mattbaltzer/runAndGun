from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class AnimatedSprite(Sprite):
    def __init__(self, frames, pos, groups):
        self.frames, self.frame_index, self.animation_speed = frames, 0, 10
        super().__init__(pos, self.frames[self.frame_index], groups)

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
    
class Player(AnimatedSprite):
    def __init__(self, pos, groups, collision_sprites, frames):
        surf = pygame.Surface((40,80))
        super().__init__(frames, pos, groups)
        self.pos = pos

        # Player image
        self.rect = self.image.get_frect(center = pos)
        self.facing_right = True

        # Player movement and direction
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites
        self.gravity = 50
        self.on_ground = False

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        # self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        # self.direction = self.direction.normalize() if self.direction else self.direction
        if keys[pygame.K_SPACE] and self.on_ground:
            self.direction.y = -20
            
        # if keys[pygame.K_a]:
        #     self.direction.x -= 1
        #     self.facing_right = False

        # if keys[pygame.K_w]:
        #     self.direction.y -= 1

        # if keys[pygame.K_s]:
        #     self.direction.y += 1

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

    def update(self, dt):
        self.check_ground()
        self.move(dt)
        self.input()
        self.animate(dt)