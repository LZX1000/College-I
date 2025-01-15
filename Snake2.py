import pygame
import math
import ctypes

def main():
    # Initialize
    pygame.init()
    clock = pygame.time.Clock()

    pygame.display.set_caption("Snake")

    class GamePlayer(pygame.sprite.Sprite):
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
            self.collision_point = pygame.Vector2(self.rect.centerx, self.rect.top)

        def update_collision_point(self):
            offset_x = 0
            offset_y = -self.rect.height / 2
            radians = math.radians(-self.angle)
            rotated_x = offset_x * math.cos(radians) - offset_y * math.sin(radians)
            rotated_y = offset_x * math.sin(radians) + offset_y * math.cos(radians)
            self.collision_point.x = self.rect.centerx + rotated_x
            self.collision_point.y = self.rect.centery + rotated_y

        def update(self, display_surface, pos):
            # # Update positions
            self.rect.center = pos
            self.update_collision_point()
            rotated_image = pygame.transform.rotate(self.image, self.angle)
            rotated_rect = rotated_image.get_rect(center=self.rect.center)
            # # Render player
            display_surface.blit(rotated_image, rotated_rect.topleft)
            '''debug code'''
            pygame.draw.circle(internal_surface, (255, 0, 0), (int(player.collision_point.x), int(player.collision_point.y)), 3)

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

        class Grass(pygame.sprite.Sprite):
            def __init__(self, pos, size=None):
                super().__init__()
                self.source_image = pygame.image.load(f"assets/SnakeBackgroundGrass1.png")

                original_size = self.source_image.get_size()
                if size is None:
                    size = (
                        original_size[0] * pixelation_factor,
                        original_size[1] * pixelation_factor
                    )
                self.image = pygame.transform.scale(self.source_image, size)

                self.rect = self.image.get_rect(center=pos)
                self.movement_points = []

            def update(self, display_surface, pos):
                display_surface.blit(self.image, self.rect.topleft)
                self.rect.center = pos

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
    
    # Display
    # # Resolutions
    internal_width = 640
    internal_height = 360
    ctypes.windll.user32.SetProcessDPIAware()
    screen_size = (1920, 1080)
    pixelation_factor = 2
    # # Surfaces
    internal_surface = pygame.Surface((internal_width, internal_height)) # For rendering
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
    # # Background
    background_pos = pygame.Vector2(internal_width // 2, internal_height // 2)
    background = Backgrounds(background_pos)

    # Player Settings
    movement_speed = 120
    normal_movement_speed = movement_speed
    player_pos = pygame.Vector2((internal_width // 2), (internal_height // 2))

    player = GamePlayer(player_pos)
    player_movement = (0, 0)
    running = True
    gamestate = "game"
    max_fps = 60
    dt = 0

    while running:
        alive = True

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
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                movement_speed /= 2
                # diagonal_speed = movement_speed / math.sqrt(2)
            else:
                movement_speed = normal_movement_speed
                # diagonal_speed = movement_speed / math.sqrt(2)
            if keys[pygame.K_r]:
                player_pos = pygame.Vector2((internal_width // 2), (internal_height // 2))
            # # Diagonal movement
            # if keys[pygame.K_w] and keys[pygame.K_a] or keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            #     player_pos.x -= diagonal_speed * dt
            #     player_pos.y -= diagonal_speed * dt
            # elif keys[pygame.K_w] and keys[pygame.K_d] or keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            #     player_pos.x += diagonal_speed * dt
            #     player_pos.y -= diagonal_speed * dt
            # elif keys[pygame.K_s] and keys[pygame.K_a] or keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            #     player_pos.x -= diagonal_speed * dt
            #     player_pos.y += diagonal_speed * dt
            # elif keys[pygame.K_s] and keys[pygame.K_d] or keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            #     player_pos.x += diagonal_speed * dt
            #     player_pos.y += diagonal_speed * dt
            # Straight movement
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player.angle = 0
                player_movement = (0, -1)
                # player_pos.y -= movement_speed * dt
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player.angle = 180
                player_movement = (0, 1)
                # player_pos.y += movement_speed * dt
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player.angle = 90
                player_movement = (-1, 0)
                # player_pos.x -= movement_speed * dt
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player.angle = 270
                player_movement = (1, 0)
                # player_pos.x += movement_speed * dt

            # Player movement
            player_pos.x += player_movement[0] * movement_speed * dt
            player_pos.y += player_movement[1] * movement_speed * dt

            # Player bounds
            if not background.grass.rect.collidepoint(player.collision_point):
                gamestate = "menu"

            # Render in 640x360
            internal_surface.fill((36, 201, 29)) # Sub-background
            background.game_update(internal_surface, background_pos)
            player.update(internal_surface, player_pos)

            # Upscale to 1920x1080
            scaled_surface = pygame.transform.scale(internal_surface, screen_size)
            screen.blit(scaled_surface, (0, 0))

            pygame.display.flip()
            # Tick Speed
            dt = clock.tick(max_fps) / 1000
    
if __name__ == "__main__":
    main()