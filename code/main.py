from settings import * 
from sprites import *
from groups import *
from support import *
from times import Timer
from random import randint
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
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # Load the game
        self.load_assets()
        self.setup()

        # Timers for the game
        self.bee_timer = Timer(800, func= self.create_bee, autostart=True, repeat=True)

    def create_bee(self):
        Bee(
            frames=self.bee_frames, 
            pos = (self.level_width + WINDOW_WIDTH, randint(0, self.level_height)), 
            groups = (self.all_sprites, self.enemy_sprites),
            speed = randint(300, 500),
            )

    def create_bullet(self, pos, direction):
        # If the player is facing to the right, you'd place the topleft of the bullet 34 pixels,
        # otherwise if you're facing left you move the bullet by it's width and then adding 34 pixels
        x = pos[0] + direction * 34 if direction == 1 else pos[0] + direction * 34 - self.bullet_surf.get_width()
        Bullet(self.bullet_surf, (x, pos[1]), direction, (self.all_sprites, self.bullet_sprites))
        Fire(self.fire_surf, pos, self.all_sprites, self.player)
        self.audio['shoot'].play()
        self.audio['shoot'].set_volume(0.04)

    def load_assets(self):
        # Loading the graphics
        self.player_frames = import_folder('images', 'player')
        self.bullet_surf = import_image('images', 'gun', 'bullet')
        self.fire_surf = import_image('images', 'gun', 'fire')
        self.bee_frames = import_folder('images', 'enemies', 'bee')
        self.worm_frames = import_folder('images', 'enemies', 'worm')

        # Loading the sounds
        self.audio = audio_importer('audio')
        
    def setup(self):
        map = load_pygame(join('.', 'data', 'maps', 'world.tmx'))
        self.level_width = map.width * TILE_SIZE
        self.level_height = map.height * TILE_SIZE

        for x, y, image in map.get_layer_by_name('Main').tiles():
            # Creates the collision object for the player to interact with. Didn't have a surface so had to create one with pygame by using the width and height of the collision object
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites, self.collision_sprites))

        for x, y, image in map.get_layer_by_name('Decoration').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites))

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                # Putting the collision sprites at the end of Player makes it an arguement and allows the player to access the group, it isn't in the Collision Sprites group
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.player_frames, self.create_bullet)
            if obj.name == 'Worm':
                Worm(self.worm_frames, pygame.FRect(obj.x, obj.y, obj.width, obj.height), (self.all_sprites, self.enemy_sprites))

        self.audio['music'].play(loops = -1)
        self.audio['music'].set_volume(0.05)

    def collision(self):
        # Bullets - > Enemies
        for bullet in self.bullet_sprites:
            sprite_collision = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
            if sprite_collision:
                self.audio['impact'].play()
                self.audio['impact'].set_volume(0.04)
                bullet.kill()
                for sprite in sprite_collision:
                    sprite.destroy()

        # Enemies -> Player
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.running = False

    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
            
            # update
            self.bee_timer.update()
            self.all_sprites.update(dt)
            self.collision()

            # draw 
            self.display_surface.fill(BG_COLOR)
            # This is causing the display surface to follow the player around, like a camera
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run() 