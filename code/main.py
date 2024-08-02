from settings import * 
from sprites import *
from groups import *
from support import *
# This imports a TMX map that you can use inside of the code
from pytmx.util_pygame import load_pygame

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Run and Gun')
        self.clock = pygame.time.Clock()
        self.running = True

        # Groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        # Load the game
        self.load_assets()
        self.setup()

    def load_assets(self):
        pass
        # Loading the graphics
        self.player_frames = import_folder('images', 'player')
        self.bullet_surf = import_image('images', 'gun', 'bullet')
        self.fire_surf = import_image('images', 'gun', 'fire')
        self.bee_frames = import_folder('images', 'enemies', 'bee')
        self.worm_frames = import_folder('images', 'enemies', 'worm')

    def setup(self):
        map = load_pygame(join('.', 'data', 'maps', 'world.tmx'))

        for x, y, image in map.get_layer_by_name('Main').tiles():
            # Creates the collision object for the player to interact with. Didn't have a surface so had to create one with pygame by using the width and height of the collision object
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites, self.collision_sprites))

        for x, y, image in map.get_layer_by_name('Decoration').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites))

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                # Putting the collision sprites at the end of Player makes it an arguement and allows the player to access the group, it isn't in the Collision Sprites group
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.player_frames)

    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
            
            # update
            self.all_sprites.update(dt)

            # draw 
            self.display_surface.fill(BG_COLOR)
            # This is causing the display surface to follow the player around, like a camera
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run() 