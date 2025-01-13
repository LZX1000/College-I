import pygame
import math

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
            self.rect = self.image.get_rect(center=pos)
            self.size = size

        def update(self, display_surface, pos):
            display_surface.blit(self.image, self.rect.topleft)
            self.rect.center = pos

    class GameBackground(pygame.sprite.Sprite):
        def __init__(self, pos, size=None):
            super().__init__()
            self.source_image = pygame.image.load(f"assets/SnakeBackground1.png")

            original_size = self.source_image.get_size()
            if size is None:
                size = (
                    original_size[0] * pixelation_factor,
                    original_size[1] * pixelation_factor
                )
            self.image = pygame.transform.scale(self.source_image, size)
            self.rect = self.image.get_rect(center=pos)
            self.size = size

        def update(self, display_surface, pos):
            display_surface.blit(self.image, self.rect.topleft)
            self.rect.center = pos

    # Display
    ## Resolutions
    internal_width = 640
    internal_height = 360
    screen_size = (1920, 1080)
    pixelation_factor = 2
    ## Surfaces
    internal_surface = pygame.Surface((internal_width, internal_height)) # For rendering
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
    ## Background
    background_pos = pygame.Vector2(internal_width // 2, internal_height // 2)
    background = GameBackground(background_pos)

    # Player Settings
    movement_speed = 120
    normal_movement_speed = movement_speed
    player_pos = pygame.Vector2((internal_width // 2), (internal_height // 2))

    player = GamePlayer(player_pos)
    running = True
    max_fps = 60
    dt = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        # Misc inputs
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            movement_speed /= 2
            diagonal_speed = movement_speed / math.sqrt(2)
        else:
            movement_speed = normal_movement_speed
            diagonal_speed = movement_speed / math.sqrt(2)
        if keys[pygame.K_ESCAPE]:
            running = False
        # Diagonal movement
        if keys[pygame.K_w] and keys[pygame.K_a] or keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            player_pos.x -= diagonal_speed * dt
            player_pos.y -= diagonal_speed * dt
        elif keys[pygame.K_w] and keys[pygame.K_d] or keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            player_pos.x += diagonal_speed * dt
            player_pos.y -= diagonal_speed * dt
        elif keys[pygame.K_s] and keys[pygame.K_a] or keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            player_pos.x -= diagonal_speed * dt
            player_pos.y += diagonal_speed * dt
        elif keys[pygame.K_s] and keys[pygame.K_d] or keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            player_pos.x += diagonal_speed * dt
            player_pos.y += diagonal_speed * dt
        # Straight movement
        elif keys[pygame.K_w] or keys[pygame.K_UP]:
            player_pos.y -= movement_speed * dt
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player_pos.y += movement_speed * dt
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player_pos.x -= movement_speed * dt
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player_pos.x += movement_speed * dt

        # Player bounds
        player_pos.x = max(0, min(internal_width, player_pos.x))
        player_pos.y = max(0, min(internal_height, player_pos.y))

        # Render in 640x360
        internal_surface.fill((0, 0, 0)) # Sub-background
        background.update(internal_surface, background_pos)
        player.update(internal_surface, player_pos)

        # Upscale to 1920x1080
        scaled_surface = pygame.transform.scale(internal_surface, screen_size)
        screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()
        # Tick Speed
        dt = clock.tick(max_fps) / 1000
    
if __name__ == "__main__":
    main()