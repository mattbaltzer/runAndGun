from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Player(Sprite):
    def __init__(self, pos, groups, collision_sprites):
        surf = pygame.Surface((40,80))
        super().__init__(pos, surf, groups)
        self.pos = pos

        # Player image
        self.rect = self.image.get_frect(center = pos)
        self.facing_right = True

        # Player movement and direction
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        # if keys[pygame.K_d]:
        #     self.direction.x += 1
        #     self.facing_right = True

        # if keys[pygame.K_a]:
        #     self.direction.x -= 1
        #     self.facing_right = False

        # if keys[pygame.K_w]:
        #     self.direction.y -= 1

        # if keys[pygame.K_s]:
        #     self.direction.y += 1

    def move(self, dt):
        self.rect.centery += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.centerx += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.direction = self.direction.normalize() if self.direction else self.direction

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
                

    def update(self, dt):
        self.move(dt)
        self.input()