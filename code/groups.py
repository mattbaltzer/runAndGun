from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw (self, target_pos):
            # Sets up the camera to put the player in the middle of the screen and follow the player if they move left, right, up or down. [0] references the x position and [1] references the y position
            self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
            self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)

            for sprite in self:
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)