import pygame
import random
import time
import ctypes
from typing import List, Tuple

def main():
    class Ball:
        def __init__(self) -> None:
            rarity = random.randint(1, 100)
            if rarity <= 75:
                self.rarity = "Common"
                self.color = (0, 0, 0)
                self.money_value = 1
            elif rarity <= 95:
                self.rarity = "Rare"
                self.color = (0, 0, 255)
                self.money_value = 5
            elif rarity <= 99:
                self.rarity = "Epic"
                self.color = (255, 0, 255)
                self.money_value = 25
            else:
                self.rarity = "Legendary"
                self.color = (255, 0, 0)
                self.money_value = 100
            
            self.time = time.monotonic()
        
        def check_for_payount(self) -> int:
            if time.monotonic() - self.time >= 5:
                self.time = time.monotonic()
                return self.money_value
            return 0

    class CombinedBall:
        def __init__(self, rarity, money_value) -> None:
            self.money_value = money_value
            self.rarity = rarity
            self.count = 2
            self.time = time.monotonic()
        
        def check_for_payount(self) -> int:
            if time.monotonic() - self.time >= 5:
                self.time = time.monotonic()
                return self.money_value * self.count
            return 0
        
    class Button(pygame.sprite.Sprite):
        '''
        Creates a button object, contains a text surface and a rect object.
        '''
        def __init__(
            self,
            surface: pygame.Surface,
            text: str |
                  List[str] |
                  List[Tuple[str, Tuple[int, int, int]]] |
                  None = None,
                  /,
            offset: List[Tuple[int, int]] |
                    Tuple[int, int] |
                    None = [(0, 0)],
            text_color: Tuple[int, int, int] | None = (0, 0, 0),
            spacing: int | None = 20,
            type: str = "Upgrade",
            debug_color: Tuple[int, int, int] | None = (255, 0, 0)
        ) -> None:
            super().__init__()
            # Prepare text
            texts = []
            text_surfaces = []
            self.spacing = spacing
            if isinstance(text, str):
                texts = [(text, text_color)]
            elif isinstance(text, list):
                for t in text:
                    if isinstance(t, tuple):
                        texts.append(t)
                    else:
                        texts.append((t, text_color))
            else:
                texts = [("", text_color)]
            
            for (text, color) in texts:
                text_surface = font.render(text, False, color)
                text_surfaces.append(text_surface)
            # Prepare offsets
            if isinstance(offset[0], tuple):
                offsets = offset
            elif isinstance(offset[0], int) or isinstance(offset[0], float):
                offsets = [offset]

            total_offset_x = sum(offset[0] for offset in offsets)
            total_offset_y = sum(offset[1] for offset in offsets)

            self.text_surfaces = text_surfaces
            self.debug_color = debug_color

            self.rect = pygame.Rect(
                total_offset_x,
                total_offset_y,
                surface.get_width() / 2 if type.lower() == "menu" else surface.get_width(),
                30
            )
        
        def update(
            self,
            surface: pygame.Surface,
            pos: Tuple[int, int] | None = None
        ) -> None:
            '''
            Updates the given surface by blitting text surfaces at the specified position.
            '''
            if pos is None:
                pos = self.rect.topleft
            for i, text_surface in enumerate(self.text_surfaces):
                surface.blit(text_surface, (pos[0], pos[1] + (i * self.spacing)))

        def debug(self, surface: pygame.Surface) -> None:
            '''
            Draws a debug rectangle on the given surface.
            '''
            pygame.draw.rect(surface, self.debug_color, self.rect, 1)

    class Upgrade:
        def __init__(
            self,
            surface: pygame.Surface,
            name: str | None = "",
            type: str | None = "money",
            cost: int | None = 0,
            max_level: int | None = 999,
            description: str | None = "",
            level: int | None = 0
        ) -> None:
            self.name = name
            self.type = type
            self.cost = cost
            self.level = level
            self.max_level = max_level
            self.description = description
            self.button = Button(
                surface,
                [self.name, self.description],
                offset=[(menu_surface.get_width() / 2, 0), ((internal_width / 3) * 2, 0)],
                debug_color=(255, 0, 0)
            )

    # Initialize
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 20)
    pygame.display.set_caption("CollegeI")
    clock = pygame.time.Clock()

    # Display
    # # Resolutions
    internal_width = 640
    internal_height = 360
    ctypes.windll.user32.SetProcessDPIAware()
    screen_size = (1920, 1080)
    # pixelation_factor = 2
    # # Surfaces
    internal_surface = pygame.Surface((internal_width, internal_height)) # For rendering
    menu_surface = pygame.Surface((internal_width / 3, internal_height)) # For rendering
    screen = pygame.display.set_mode(screen_size) # pygame.FULLSCREEN

    # Menu Buttons
    balls_menu_button = Button(
        menu_surface,
        "Balls",
        type="Menu",
        offset=((internal_width / 3) * 2, 0),
        debug_color=[0, 0, 255]
    )
    upgrades_menu_button = Button(
        menu_surface,
        "Upgrades",
        type="Menu",
        offset=[(menu_surface.get_width() / 2, 0), ((internal_width / 3) * 2, 0)],
        debug_color=[0, 255, 0]
    )

    running = True
    new = True # Change when adding saving
    debug_mode = False
    menu_type = "Balls"
    max_fps = 60
    dt = 0

    all_upgrades = []
    '''********************Add this to a startup file later********************'''
    raw_upgrades = [
        ("Money Per Click", "money", 10, 10, "Increase money per click by 1"),
        ("Ball Value", "money", 10, 10, "Increase ball value by 1")
    ]
    '''************************************************************************'''

    for upgrade in raw_upgrades:
        all_upgrades.append(Upgrade(menu_surface, upgrade[0], upgrade[1], upgrade[2], upgrade[3], upgrade[4]))

    while running:
        # Reset
        if new:
            player_money = 100
            player_money_per_click = 1
            new_ball_cost = 10
            balls = []
            unresolved_balls = []
            combined_balls = []
            available_upgrades = all_upgrades
            legendary_ball_count = 0
            epic_ball_count = 0
            rare_ball_count = 0
            common_ball_count = 0
            new = False

        scaled_mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (
            scaled_mouse_pos[0] * internal_width / screen_size[0],
            scaled_mouse_pos[1] * internal_height / screen_size[1]
            )
        keys = pygame.key.get_pressed()

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if balls_menu_button.rect.collidepoint(mouse_pos):
                        menu_type = "Balls"
                    elif upgrades_menu_button.rect.collidepoint(mouse_pos):
                        menu_type = "Upgrades"
                    else:
                        player_money += player_money_per_click
                elif event.button == 3:
                    if menu_type == "Upgrades":
                        menu_type = "Balls"
                    elif menu_type == "Balls":
                        menu_type = "Upgrades"
        # Handle keypresses
        if keys[pygame.K_ESCAPE]:
            running = False
    
        if keys[pygame.K_RETURN]:
            if not enter_pressed:
                enter_pressed = True
                enter_timer = time.monotonic()
                if player_money >= new_ball_cost:
                    player_money -= new_ball_cost
                    new_ball_cost = int(round(len(balls) ** 2) / 2 + 11)
                    unresolved_balls.append(0)
                    enter_interval_timer = time.monotonic()
            elif not enter_press_override:
                if player_money >= new_ball_cost and time.monotonic() - enter_interval_timer >= 0.1:
                    player_money -= new_ball_cost
                    new_ball_cost = int(round(len(balls) ** 2) / 2 + 11)
                    unresolved_balls.append(0)
                    enter_interval_timer = time.monotonic()
            else:
                if time.monotonic() - enter_timer >= 0.5:
                    enter_pressed = False
                    enter_press_override = True
        else:
            enter_pressed = False
            enter_press_override = False
        
        if keys[pygame.K_LCTRL] and keys[pygame.K_q]:
            player_money += 100000

        if keys[pygame.K_LCTRL] and keys[pygame.K_SPACE]:
            if not space_pressed:
                space_pressed = True
                if debug_mode:
                    debug_mode = False
                else:
                    debug_mode = True
        else:
            space_pressed = False
        
        if len(unresolved_balls) > 0:
            while unresolved_balls:
                new_ball = Ball()
                resolved = False
                recent_ball_rarity = new_ball.rarity
                recent_ball_color = new_ball.color
                if new_ball.rarity == "Common":
                    common_ball_count += 1
                elif new_ball.rarity == "Rare":
                    rare_ball_count += 1
                elif new_ball.rarity == "Epic":
                    epic_ball_count += 1
                else:
                    legendary_ball_count += 1
                while not resolved:
                    for ball in combined_balls:
                        if ball.rarity == new_ball.rarity and ball.time % 5 == new_ball.time % 5:
                            ball.count += 1
                            resolved = True
                            combined_balls.append(new_ball)
                            break
                    for ball in balls:
                        if ball.rarity == new_ball.rarity and ball.time % 5 == new_ball.time % 5:
                            new_ball = CombinedBall(new_ball.rarity, new_ball.money_value)
                            resolved = True
                            balls.remove(ball)
                            combined_balls.append(new_ball)
                            break
                    balls.append(new_ball)
                unresolved_balls.pop(0)

        for ball in balls:
            player_money += ball.check_for_payount()
        for ball in combined_balls:
            player_money += ball.check_for_payount()

        # Render in 640x360
        internal_surface.fill((180, 180, 180)) # Sub-background
        # background.game_update(internal_surface)
        money_text_surface = font.render(f"Money :  {player_money}", False, (0, 0, 0))
        ball_cost_text_surface = font.render(f"Ball Cost : {new_ball_cost}", False, (0, 0, 0))
        owned_balls_text_surface = font.render(f"Owned Balls : {len(balls)}", False, (0, 0, 0))
        # Balls Menu
        if menu_type == "Balls":
            common_ball_count_text_surface = font.render(f"Common Balls : {common_ball_count}", False, (0, 0, 0))
            rare_ball_count_text_surface = font.render(f"Rare Balls : {rare_ball_count}", False, (0, 0, 0))
            epic_ball_count_text_surface = font.render(f"Epic Balls : {epic_ball_count}", False, (0, 0, 0))
            legendary_ball_count_text_surface = font.render(f"Legendary Balls : {legendary_ball_count}", False, (0, 0, 0))
            if len(balls) > 0:
                most_recent_ball_text_surface1 = font.render(f"Most Recent Ball :", False, (0, 0, 0))
                most_recent_ball_text_surface2 = font.render(f"        {recent_ball_rarity} Ball", False, (recent_ball_color))
            # # Blit to Balls Menu
            menu_surface.fill((255, 255, 255)) # Sub-background
            menu_surface.blit(common_ball_count_text_surface, (0, 40))
            menu_surface.blit(rare_ball_count_text_surface, (0, 60))
            menu_surface.blit(epic_ball_count_text_surface, (0, 80))
            menu_surface.blit(legendary_ball_count_text_surface, (0, 100))
            if len(balls) > 0:
                menu_surface.blit(most_recent_ball_text_surface1, (0, 140))
                menu_surface.blit(most_recent_ball_text_surface2, (0, 160))
        elif menu_type == "Upgrades":
            available_upgrade_text_surfaces = []
            available_upgrade_buttons = []
            for upgrade in available_upgrades:
                available_upgrade_name_text_surface = font.render(f"{upgrade.name} :", False, (0, 0, 0))
                available_upgrade_price_text_surface = font.render(f"   {upgrade.cost} {upgrade.type}", False, (0, 0, 0))
                available_upgrade_text_surfaces.append((available_upgrade_name_text_surface, available_upgrade_price_text_surface))
            # # Blit to Upgrades Menu
            menu_surface.fill((255, 255, 255)) # Sub-background
            for i, upgrade_text_surface in enumerate(available_upgrade_text_surfaces):
                menu_surface.blit(upgrade_text_surface[0], (0, i * 40 + 40))
                menu_surface.blit(upgrade_text_surface[1], (0, i * 40 + 60))
        balls_menu_button.update(menu_surface, (0, 0))
        upgrades_menu_button.update(menu_surface, (menu_surface.get_width() / 2, 0))
        # Blit to internal_surface
        internal_surface.blit(menu_surface, ((internal_width / 3) * 2, 0))
        # # Text
        internal_surface.blit(money_text_surface, (0, 0))
        internal_surface.blit(ball_cost_text_surface, (0, 20))
        internal_surface.blit(owned_balls_text_surface, (0, 40))
        # Debug
        if debug_mode:
            # Menu buttons
            balls_menu_button.debug(internal_surface)
            upgrades_menu_button.debug(internal_surface)
            # Mouse
            pygame.draw.circle(internal_surface, (0, 0, 0), mouse_pos, 2)

        # Upscale to 1920x1080
        scaled_surface = pygame.transform.scale(internal_surface, screen_size)
        screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()
        # Tick Speed
        dt = clock.tick(max_fps) / 1000

    # Save

if __name__ == "__main__":
    main()
