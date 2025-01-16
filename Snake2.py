import pygame
import math
import random
import ctypes

def main():
    # Initialize
    pygame.init()
    clock = pygame.time.Clock()

    pygame.display.set_caption("Snake")

    class GamePlayer(pygame.sprite.Sprite):
        class Nose(pygame.sprite.Sprite):
            def __init__(self, player):
                super().__init__()
                self.pos = pygame.Vector2(player.rect.centerx, player.rect.top)
                self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], 1, 1)

            def update(self, pos):
                offset_x = 0
                offset_y = -player.rect.height / 2
                radians = math.radians(-player.angle)
                rotated_x = offset_x * math.cos(radians) - offset_y * math.sin(radians)
                rotated_y = offset_x * math.sin(radians) + offset_y * math.cos(radians)
                self.pos.x = player.rect.centerx + rotated_x
                self.pos.y = player.rect.centery + rotated_y
                self.rect.center = pos

            def debug(self, internal_surface):
                pygame.draw.circle(internal_surface, (255, 0, 0),
                                   (int(player.nose.pos.x),
                                   int(player.nose.pos.y)), 3)

        class MovementPoint(pygame.sprite.Sprite):
            def __init__(self, player):
                super().__init__()
                self.pos = pygame.Vector2(player.rect.centerx, player.rect.centery - player.rect.height / 4)
                self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], 1, 1)

            def update(self, pos):
                offset_x = 0
                offset_y = -player.rect.height / 4
                radians = math.radians(-player.angle)
                rotated_x = offset_x * math.cos(radians) - offset_y * math.sin(radians)
                rotated_y = offset_x * math.sin(radians) + offset_y * math.cos(radians)
                self.pos.x = self.rect.centerx + rotated_x
                self.pos.y = self.rect.centery + rotated_y
                self.rect.center = pos

            def debug(self, internal_surface):
                pygame.draw.circle(internal_surface, (0, 255, 0),
                                   (int(player.movement_point.pos.x),
                                   int(player.movement_point.pos.y)), 3)

        def __init__(self, pos, size=None):
            super().__init__()
            self.source_image = pygame.image.load(f"assets/GameCharacter.png")

            original_size = self.source_image.get_size()
            if size is None:
                size = (
                    original_size[0] * pixelation_factor,
                    original_size[1] * pixelation_factor
                )
            self.image = pygame.transform.scale(self.source_image, size)
            self.angle = 0

            self.rect = self.image.get_rect(center=pos)
            
            self.nose = self.Nose(self)
            self.movement_point = self.MovementPoint(self)

        def update(self, display_surface, pos):
            # # Update positions
            self.rect.center = pos
            rotated_image = pygame.transform.rotate(self.image, self.angle)
            rotated_rect = rotated_image.get_rect(center=self.rect.center)
            self.nose.update(pos)
            self.movement_point.update(pos)
            # # Render player
            display_surface.blit(rotated_image, rotated_rect.topleft)
        
        def debug(self, internal_surface):
            self.nose.debug(internal_surface)
            self.movement_point.debug(internal_surface)

    class GameFood(pygame.sprite.Sprite):
        def __init__(self, pos, size=None):
            super().__init__()
            self.source_image = pygame.image.load(f"assets/Point.png")

            original_size = self.source_image.get_size()
            if size is None:
                size = (
                    original_size[0] * pixelation_factor,
                    original_size[1] * pixelation_factor
                )
            self.image = pygame.transform.scale(self.source_image, size)

            self.rect = self.image.get_rect(center=pos)

        def update(self, display_surface, pos):
            display_surface.blit(self.image, self.rect.topleft)
            self.rect.center = pos

        def debug(self, internal_surface):
            pygame.draw.rect(internal_surface, (255, 0, 0), self.rect, 1)

    class Backgrounds():
        class Menu(pygame.sprite.Sprite):
            def __init__(self, pos, size=None):
                super().__init__()
                self.source_image = pygame.image.load(f"assets/SnakeBackgroundMenu1.png")

                original_size = self.source_image.get_size()
                if size is None:
                    size = (
                        original_size[0] * pixelation_factor,
                        original_size[1] * pixelation_factor
                    )
                self.image = pygame.transform.scale(self.source_image, size)
                self.rect = self.image.get_rect(center=pos)

            def update(self, display_surface, pos):
                display_surface.blit(self.image, self.rect.topleft)
                self.rect.center = pos

        class GameBlock(pygame.sprite.Sprite):
            def __init__(self, pos, block_width):
                super().__init__()
                self.pos = pos
                self.collision_point = pygame.Vector2(self.pos)
                self.rect = pygame.rect.Rect(pos[0] - block_width / 2, pos[1] - block_width / 2,
                                             block_width, block_width)

        class Grass(pygame.sprite.Sprite):
            def __init__(self, pos, size=None, width=11):
                super().__init__()
                self.source_image = pygame.image.load(f"assets/SnakeBackgroundGrass1.png")

                original_size = self.source_image.get_size()
                if size is None:
                    size = (
                        original_size[0] * pixelation_factor,
                        original_size[1] * pixelation_factor
                    )
                self.image = pygame.transform.scale(self.source_image, size)

                self.rect = self.image.get_rect(center=pos) # Whole grass collision
                self.block_width = self.image.get_width() / width
                self.blocks_list = []
                for i in range(width):
                    block_height_pos = self.rect.topleft[1] + i * self.block_width + self.block_width / 2
                    for i in range(width):
                        block_pos = ((self.rect.topleft[0] + i * self.block_width + self.block_width / 2),
                                     block_height_pos)
                        block = Backgrounds.GameBlock(block_pos, self.block_width)
                        self.blocks_list.append(block)
                self.blocks_group = pygame.sprite.Group(self.blocks_list)
        
            def update(self, display_surface, pos):
                display_surface.blit(self.image, self.rect.topleft)
            
            def debug(self, internal_surface):
                for block in self.blocks_list:
                    pygame.draw.circle(internal_surface, (0, 0, 255), block.collision_point, 2)
                    pygame.draw.rect(internal_surface, (0, 255, 255), block.rect, 1)

        class Edge(pygame.sprite.Sprite):
            def __init__(self, pos, size=None):
                super().__init__()
                self.source_image = pygame.image.load(f"assets/SnakeBackgroundEdge1.png")

                original_size = self.source_image.get_size()
                if size is None:
                    size = (
                        original_size[0] * pixelation_factor,
                        original_size[1] * pixelation_factor
                    )
                self.image = pygame.transform.scale(self.source_image, size)
                self.rect = self.image.get_rect(center=pos)

            def update(self, display_surface, pos):
                display_surface.blit(self.image, self.rect.topleft)
                self.rect.center = pos

        def __init__(self, pos, size=None):
            self.grass = self.Grass(pos, size)
            self.edge = self.Edge(pos, size)
            self.menu = self.Menu(pos, size)

            self.grass_group = pygame.sprite.Group(self.grass)

        def game_update(self, display_surface, pos):
            self.grass.update(display_surface, pos)
            self.edge.update(display_surface, pos)
        
        def menu_update(self, display_surface, pos):
            self.menu.update(display_surface, pos)

    def spawn_food(max_food, food_list):
        while len(food_list) < max_food:
            food = GameFood(background.grass.blocks_list[random.randint(0, len(background.grass.blocks_list) - 1)].pos)
            food_list.append(food)
        return food_list
    
    def render_food(food_list, debug=False):
        for food in food_list:
            food.update(internal_surface, food.rect.center)
            if debug:
                food.debug(internal_surface)
    
    # Display
    # # Resolutions
    internal_width = 640
    internal_height = 360
    ctypes.windll.user32.SetProcessDPIAware()
    screen_size = (1920, 1080)
    pixelation_factor = 2
    # # Surfaces
    internal_surface = pygame.Surface((internal_width, internal_height)) # For rendering
    screen = pygame.display.set_mode(screen_size) # pygame.FULLSCREEN
    # # Background
    background_pos = pygame.Vector2(internal_width // 2, internal_height // 2)
    background = Backgrounds(background_pos)
    # Player Settings
    movement_speed = 120
    player_pos = pygame.Vector2((internal_width // 2), (internal_height // 2))
    # # Food Settings
    max_food = 3
    food_list = []

    player = GamePlayer(player_pos)
    player_movement = (0, 0)
    running = True
    free = True
    requested_movement = False
    gamestate = "game"
    max_fps = 60
    dt = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if gamestate == "menu":
            # Misc inputs
            if keys[pygame.K_ESCAPE]:
                running = False
            elif keys[pygame.K_RETURN]:
                gamestate = "game"

            # Render in 640x360
            internal_surface.fill((0, 0, 0)) # Sub-background
            background.menu_update(internal_surface, background_pos)
            player.update(internal_surface, player_pos)

            # Upscale to 1920x1080
            scaled_surface = pygame.transform.scale(internal_surface, screen_size)
            screen.blit(scaled_surface, (0, 0))
        
        elif gamestate == "game":
            # Misc inputs
            if keys[pygame.K_ESCAPE]:
                gamestate = "menu"
            if keys[pygame.K_r]:
                player_pos = pygame.Vector2((internal_width // 2), (internal_height // 2))
            # Movement detection
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                if player_movement != (0, 1):
                    player.angle = 0
                    requested_direction = (0, -1)
                    requested_movement = True
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                if player_movement != (0, -1):
                    player.angle = 180
                    requested_direction = (0, 1)
                    requested_movement = True
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                if player_movement != (1, 0):
                    player.angle = 90
                    requested_direction = (-1, 0)
                    requested_movement = True
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                if player_movement != (-1, 0):
                    player.angle = 270
                    requested_direction = (1, 0)
                    requested_movement = True

            # Player movement
            if background.grass.rect.collidepoint(player.nose.pos):
                # Food collision
                for food in food_list:
                    if player.nose.rect.colliderect(food.rect):
                        food_list.remove(food)
                # Movement restriction
                if requested_movement and requested_direction != player_movement and free:
                    movement_box = pygame.sprite.spritecollide(player.movement_point, background.grass.blocks_group, False)
                    # Keep player centered on blocks
                    if movement_box:
                        old_movement_box = movement_box
                        requested_movement = False
                        free = False
                        player_movement = requested_direction
                        player_pos.x = movement_box[0].pos[0]
                        player_pos.y = movement_box[0].pos[1]
                        movement_box = None
                # Remove movement restriction
                elif not free:
                    if not pygame.sprite.spritecollide(player.movement_point, old_movement_box, False):
                        free = True
                # Move player
                player_pos.x += player_movement[0] * movement_speed * dt
                player_pos.y += player_movement[1] * movement_speed * dt
            else:
                requested_movement = False
                gamestate = "menu"

            # Player bounds
            if not background.grass.rect.collidepoint(player.nose.pos):
                gamestate = "menu"

            # Render in 640x360
            internal_surface.fill((36, 201, 29)) # Sub-background
            background.game_update(internal_surface, background_pos)
            background.grass.debug(internal_surface)
            # Food
            food_list = spawn_food(max_food, food_list)
            render_food(food_list, debug=True)
            # Render Player
            player.update(internal_surface, player_pos)
            player.debug(internal_surface)

            # Upscale to 1920x1080
            scaled_surface = pygame.transform.scale(internal_surface, screen_size)
            screen.blit(scaled_surface, (0, 0))

            pygame.display.flip()
            # Tick Speed
            dt = clock.tick(max_fps) / 1000

if __name__ == "__main__":
    main()