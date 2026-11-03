"""
SPACE SHOOTER
BCA Project - Rungta International Skills University
Single-file Pygame project.

Run:
    python -m pip install pygame
    python one.py

Create test screenshots and a PDF:
    python one.py --capture-tests

Controls:
    LEFT / RIGHT : Move the ship
    SPACE        : Fire
    P            : Pause / resume
    R            : Restart after Game Over
    ESC          : Quit
"""

import argparse
import random
import sys
from pathlib import Path

import pygame

# ----------------------------- Configuration -----------------------------

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
FPS = 60

SHIP_WIDTH = 50
SHIP_HEIGHT = 50
SHIP_SPEED = 8

BULLET_WIDTH = 5
BULLET_HEIGHT = 10
BULLET_SPEED = 10
MAX_BULLETS = 5

ENEMY_SIZE = 40
ENEMY_BASE_SPEED = 2
ENEMY_SPAWN_FRAMES = 60

STARTING_LIVES = 3
SCORE_PER_ENEMY = 10

BLACK = (7, 10, 25)
WHITE = (245, 248, 255)
BLUE = (60, 155, 255)
CYAN = (80, 225, 255)
RED = (255, 75, 85)
YELLOW = (255, 220, 90)
MUTED = (160, 180, 210)
PANEL = (16, 25, 48)

pygame.init()
pygame.display.set_caption("Space Shooter | BCA Project")


def clamp(value, low, high):
    """Return value restricted to the inclusive range [low, high]."""
    return max(low, min(value, high))


class Star:
    """Small background star used to make the space scene feel alive."""

    def __init__(self):
        self.x = random.randrange(SCREEN_WIDTH)
        self.y = random.randrange(SCREEN_HEIGHT)
        self.speed = random.choice((1, 1, 2))
        self.radius = random.choice((1, 1, 2))

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randrange(SCREEN_WIDTH)

    def draw(self, surface):
        pygame.draw.circle(surface, (115, 145, 190),
                           (self.x, self.y), self.radius)


class Ship:
    """Player spaceship. x is always kept inside the screen."""

    def __init__(self):
        self.width = SHIP_WIDTH
        self.height = SHIP_HEIGHT
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = SCREEN_HEIGHT - self.height - 30
        self.speed = SHIP_SPEED

    def move(self, direction):
        """Move left for -1, right for +1; zero means no movement."""
        self.x += direction * self.speed
        self.x = clamp(self.x, 0, SCREEN_WIDTH - self.width)

    def draw(self, surface):
        # A simple spaceship made from Pygame shapes; no external assets needed.
        cx = self.x + self.width // 2
        pygame.draw.polygon(
            surface, CYAN,
            [(cx, self.y), (self.x + self.width, self.y + self.height),
             (cx, self.y + self.height - 12), (self.x, self.y + self.height)]
        )
        pygame.draw.polygon(
            surface, BLUE,
            [(cx, self.y + 12), (self.x + self.width - 8, self.y + self.height - 4),
             (self.x + 8, self.y + self.height - 4)]
        )
        pygame.draw.circle(surface, WHITE, (cx, self.y + 27), 5)
        pygame.draw.polygon(
            surface, YELLOW,
            [(self.x + 12, self.y + self.height - 2),
             (self.x + 18, self.y + self.height + 7),
             (self.x + 22, self.y + self.height - 2)]
        )
        pygame.draw.polygon(
            surface, YELLOW,
            [(self.x + self.width - 22, self.y + self.height - 2),
             (self.x + self.width - 18, self.y + self.height + 7),
             (self.x + self.width - 12, self.y + self.height - 2)]
        )


class Bullet:
    """Bullet fired by the player."""

    def __init__(self, x, y):
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.x = x
        self.y = y
        self.speed = BULLET_SPEED

    def update(self):
        self.y -= self.speed

    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, YELLOW, rect, border_radius=2)
        pygame.draw.line(surface, WHITE, (self.x + 2, self.y),
                         (self.x + 2, self.y + 4), 1)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Enemy:
    """Enemy spaceship that moves down the screen."""

    def __init__(self, speed=ENEMY_BASE_SPEED, x=None, y=-ENEMY_SIZE):
        self.width = ENEMY_SIZE
        self.height = ENEMY_SIZE
        self.x = (random.randint(0, SCREEN_WIDTH - self.width)
                  if x is None else x)
        self.y = y
        self.speed = speed

    def update(self):
        self.y += self.speed

    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.polygon(
            surface, RED,
            [(self.x + 20, self.y + 40), (self.x, self.y + 10),
             (self.x + 10, self.y + 14), (self.x + 20, self.y),
             (self.x + 30, self.y + 14), (self.x + 40, self.y + 10)]
        )
        pygame.draw.rect(surface, (180, 35, 65),
                         (self.x + 7, self.y + 17, 26, 15), border_radius=4)
        pygame.draw.circle(surface, YELLOW, (self.x + 13, self.y + 23), 3)
        pygame.draw.circle(surface, YELLOW, (self.x + 27, self.y + 23), 3)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Explosion:
    """Short-lived visual effect when an enemy is destroyed."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frames_left = 14

    def update(self):
        self.frames_left -= 1

    def draw(self, surface):
        radius = max(2, 16 - self.frames_left)
        pygame.draw.circle(surface, YELLOW, (self.x, self.y), radius, 2)
        pygame.draw.circle(surface, RED, (self.x, self.y), max(1, radius // 2), 2)


class SpaceShooter:
    """Owns game state, updates objects, handles collisions and draws the UI."""

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.SysFont("arial", 38, bold=True)
        self.font = pygame.font.SysFont("arial", 22, bold=True)
        self.small_font = pygame.font.SysFont("arial", 16)
        self.stars = [Star() for _ in range(75)]
        self.reset()

    def reset(self):
        self.player = Ship()
        self.bullets = []
        self.enemies = []
        self.explosions = []
        self.score = 0
        self.lives = STARTING_LIVES
        self.enemy_spawn_timer = 0
        self.paused = False
        self.game_over = False
        self.frame_count = 0

    def fire_bullet(self):
        """Fire only when fewer than five bullets are active.

        The x coordinate is the ship's centre (x=300 at the initial position),
        matching the university's first test case.
        """
        if len(self.bullets) < MAX_BULLETS:
            bullet_x = self.player.x + self.player.width // 2
            self.bullets.append(Bullet(bullet_x, self.player.y))
            return True
        return False

    def current_enemy_speed(self):
        """Increase difficulty gradually, with a reasonable speed limit."""
        return min(ENEMY_BASE_SPEED + self.score // 100, 7)

    def spawn_enemy(self):
        self.enemies.append(Enemy(speed=self.current_enemy_speed()))
        self.enemy_spawn_timer = 0

    def update(self, movement=0):
        if self.game_over or self.paused:
            return

        self.frame_count += 1
        self.player.move(movement)

        for star in self.stars:
            star.update()

        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= ENEMY_SPAWN_FRAMES:
            self.spawn_enemy()

        # Move bullets and remove bullets that leave the top of the window.
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y + bullet.height < 0:
                self.bullets.remove(bullet)

        # Move enemies, check bottom boundary, then check bullet collisions.
        for enemy in self.enemies[:]:
            enemy.update()

            if enemy.y >= SCREEN_HEIGHT:
                self.enemies.remove(enemy)
                self.lives -= 1
                if self.lives <= 0:
                    self.lives = 0
                    self.game_over = True
                continue

            enemy_rect = enemy.get_rect()
            for bullet in self.bullets[:]:
                if enemy_rect.colliderect(bullet.get_rect()):
                    self.score += SCORE_PER_ENEMY
                    self.explosions.append(
                        Explosion(enemy.x + enemy.width // 2,
                                  enemy.y + enemy.height // 2)
                    )
                    self.enemies.remove(enemy)
                    self.bullets.remove(bullet)
                    break

        for explosion in self.explosions[:]:
            explosion.update()
            if explosion.frames_left <= 0:
                self.explosions.remove(explosion)

    def draw_background(self):
        self.screen.fill(BLACK)
        for star in self.stars:
            star.draw(self.screen)
        # Subtle horizon lines
        pygame.draw.line(self.screen, (22, 42, 75),
                         (0, SCREEN_HEIGHT - 18),
                         (SCREEN_WIDTH, SCREEN_HEIGHT - 18), 1)

    def draw_hud(self):
        pygame.draw.rect(self.screen, PANEL, (0, 0, SCREEN_WIDTH, 48))
        score_surface = self.font.render(f"SCORE: {self.score}", True, WHITE)
        lives_surface = self.font.render(f"LIVES: {self.lives}", True, WHITE)
        level = 1 + self.score // 100
        level_surface = self.small_font.render(f"LEVEL {level}", True, CYAN)
        self.screen.blit(score_surface, (14, 10))
        self.screen.blit(lives_surface, (SCREEN_WIDTH - 115, 10))
        self.screen.blit(level_surface, (SCREEN_WIDTH // 2 - 30, 16))

    def draw(self):
        self.draw_background()
        self.player.draw(self.screen)

        for bullet in self.bullets:
            bullet.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for explosion in self.explosions:
            explosion.draw(self.screen)

        self.draw_hud()

        controls = self.small_font.render(
            "MOVE: LEFT / RIGHT     FIRE: SPACE     PAUSE: P",
            True, MUTED
        )
        self.screen.blit(controls, (75, SCREEN_HEIGHT - 22))

        if self.paused and not self.game_over:
            self.draw_overlay("PAUSED", "Press P to continue")
        if self.game_over:
            self.draw_overlay("GAME OVER", f"Final Score: {self.score}   |   Press R to restart")

        pygame.display.flip()

    def draw_overlay(self, heading, message):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 175))
        self.screen.blit(overlay, (0, 0))
        title = self.title_font.render(heading, True, RED if heading == "GAME OVER" else CYAN)
        detail = self.font.render(message, True, WHITE)
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 270)))
        self.screen.blit(detail, detail.get_rect(center=(SCREEN_WIDTH // 2, 325)))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            movement = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE and not self.game_over and not self.paused:
                        self.fire_bullet()
                    elif event.key == pygame.K_p and not self.game_over:
                        self.paused = not self.paused
                    elif event.key == pygame.K_r and self.game_over:
                        self.reset()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                movement -= 1
            if keys[pygame.K_RIGHT]:
                movement += 1

            self.update(movement)
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()


def capture_test_screenshots():
    """Render the four university test cases as PNG evidence.

    This uses the same game classes and drawing methods as the playable game.
    It creates six images because Test Case 2 and Test Case 4 each have two
    separate scenarios. Run this on a computer with Pygame installed.
    """
    output_dir = Path("screenshots")
    output_dir.mkdir(exist_ok=True)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game = SpaceShooter(screen)

    def save(name):
        game.draw()
        pygame.image.save(screen, output_dir / name)

    # Test 1: initial ship x=275, then fire at (300, 520).
    game.reset()
    game.fire_bullet()
    assert len(game.bullets) == 1
    assert (game.bullets[0].x, game.bullets[0].y) == (300, 520)
    save("test_case_1_normal_input.png")

    # Test 2(a): ship is clamped at the left boundary.
    game.reset()
    game.player.x = 0
    game.player.move(-1)
    assert game.player.x == 0
    save("test_case_2a_left_boundary.png")

    # Test 2(b): ship is clamped at the right boundary.
    game.reset()
    game.player.x = SCREEN_WIDTH - SHIP_WIDTH
    game.player.move(1)
    assert game.player.x == 550
    save("test_case_2b_right_boundary.png")

    # Test 3: five bullets already active; a sixth shot is rejected.
    game.reset()
    game.bullets = [Bullet(280 + i * 5, 420 + i * 15) for i in range(5)]
    fired = game.fire_bullet()
    assert fired is False and len(game.bullets) == 5
    save("test_case_3_maximum_bullets.png")

    # Test 4(a): bullet collides with an enemy; score increases by 10.
    game.reset()
    game.player.y = 520
    game.enemies = [Enemy(x=280, y=500, speed=0)]
    game.bullets = [Bullet(300, 510)]
    game.update(0)
    assert game.score == 10 and game.lives == 3 and len(game.enemies) == 0
    save("test_case_4a_enemy_destroyed.png")

    # Test 4(b): enemy reaches the bottom; one life is lost.
    game.reset()
    game.enemies = [Enemy(x=100, y=598, speed=2)]
    game.update(0)
    assert game.lives == 2
    save("test_case_4b_enemy_reaches_bottom.png")

    # Create a PDF from the generated PNGs if ReportLab is available.
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.utils import ImageReader
        from reportlab.pdfgen import canvas

        pdf_path = output_dir / "Screenshot_Evidence.pdf"
        pdf = canvas.Canvas(str(pdf_path), pagesize=A4)
        page_w, page_h = A4
        captions = [
            "Test Case 1 - Normal Input: bullet fired at (300, 520)",
            "Test Case 2(a) - Boundary: ship remains at x = 0",
            "Test Case 2(b) - Boundary: ship remains at x = 550",
            "Test Case 3 - Invalid Input: fifth bullet limit is enforced",
            "Test Case 4(a) - Valid Scenario: enemy destroyed, score = 10",
            "Test Case 4(b) - Valid Scenario: enemy reaches bottom, lives = 2",
        ]
        filenames = [
            "test_case_1_normal_input.png",
            "test_case_2a_left_boundary.png",
            "test_case_2b_right_boundary.png",
            "test_case_3_maximum_bullets.png",
            "test_case_4a_enemy_destroyed.png",
            "test_case_4b_enemy_reaches_bottom.png",
        ]
        for filename, caption in zip(filenames, captions):
            pdf.setFont("Helvetica-Bold", 13)
            pdf.drawString(40, page_h - 45, caption)
            image = ImageReader(str(output_dir / filename))
            max_w, max_h = page_w - 80, page_h - 110
            img_w, img_h = image.getSize()
            scale = min(max_w / img_w, max_h / img_h)
            draw_w, draw_h = img_w * scale, img_h * scale
            pdf.drawImage(image, (page_w - draw_w) / 2,
                          (page_h - draw_h) / 2 - 15,
                          width=draw_w, height=draw_h)
            pdf.showPage()
        pdf.save()
        print(f"Created {pdf_path}")
    except ImportError:
        print("PNG screenshots created. Install reportlab to create the PDF:")
        print("python -m pip install reportlab")

    print("All six screenshot scenarios passed their assertions.")
    pygame.quit()


def main():
    parser = argparse.ArgumentParser(description="BCA Space Shooter project")
    parser.add_argument(
        "--capture-tests", action="store_true",
        help="capture the university test cases as PNG images and a PDF"
    )
    args = parser.parse_args()

    if args.capture_tests:
        capture_test_screenshots()
    else:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        SpaceShooter(screen).run()


if __name__ == "__main__":
    main()
