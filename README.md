# Space Shooter Game

**Project:** Space Shooter  
**Course:** Bachelor of Computer Application (BCA)  
**University:** Rungta International Skills University  
**School:** School of Information Technology  
**Project No.:** 58  
**Language:** Python 3  
**Library:** Pygame

## 1. Project overview

Space Shooter is a 2D arcade game developed in Python using Pygame. The player controls a spaceship near the bottom of the game window, moves left or right, and fires bullets at enemies that enter from the top. The player earns points by destroying enemies and loses lives when enemies pass the bottom boundary.

## 2. Objectives

- Practise Python classes, objects, functions, loops and conditional statements.
- Use Pygame to create a graphical game window.
- Handle keyboard input and continuous movement.
- Detect collisions using `pygame.Rect.colliderect()`.
- Manage score, lives, bullets and enemy objects.
- Test the project against the four university test cases.

## 3. Features

- 600 × 600 game window running at approximately 60 FPS.
- Left and Right arrow keys move the spaceship.
- Spacebar fires bullets.
- A maximum of five bullets can be active at one time.
- Enemies spawn at the top and move downward.
- Destroying an enemy adds 10 points.
- An enemy reaching the bottom costs one life.
- The game ends when lives reach zero.
- Difficulty increases gradually as the score increases.
- Star-field background, drawn spaceship/enemy designs, explosion effect and score/lives display.
- Pause/resume with `P`, restart after Game Over with `R`, and quit with `Esc`.
- No external image or sound assets are required.

## 4. Requirements

- Python 3.9 or later recommended.
- Pygame.
- ReportLab (optional; required only to create the screenshot PDF automatically).

Install the required packages:

```bash
python -m pip install pygame
```

For automatic PDF creation as well:

```bash
python -m pip install reportlab
```

## 5. Project files

```text
SpaceShooter/
├── one.py
├── README.md
└── screenshots/
    ├── test_case_1_normal_input.png
    ├── test_case_2a_left_boundary.png
    ├── test_case_2b_right_boundary.png
    ├── test_case_3_maximum_bullets.png
    ├── test_case_4a_enemy_destroyed.png
    ├── test_case_4b_enemy_reaches_bottom.png
    └── Screenshot_Evidence.pdf
```

The `screenshots/` files are generated when the test-capture command is run.

## 6. How to execute the game

1. Install Python.
2. Open Command Prompt or the terminal in the project folder.
3. Install Pygame using `python -m pip install pygame`.
4. Run:

```bash
python one.py
```

### Controls

| Key | Action |
|---|---|
| Left Arrow | Move spaceship left |
| Right Arrow | Move spaceship right |
| Space | Fire a bullet |
| P | Pause or resume |
| R | Restart after Game Over |
| Esc | Quit the game |

## 7. Input and output details

This is a keyboard-controlled graphical game, so it does not use standard console input.

**Inputs:** Left Arrow, Right Arrow, Space, P, R and Esc.

**Outputs:** The game window displays the spaceship, enemies, bullets, score, remaining lives, level, pause state and Game Over message.

## 8. Test cases

Run the automated test-screenshot routine:

```bash
python one.py --capture-tests
```

The routine checks the following scenarios using assertions and saves six PNG images. It also creates `screenshots/Screenshot_Evidence.pdf` when ReportLab is installed.

| University test | Scenario | Expected result |
|---|---|---|
| Test Case 1 | Initial ship x = 275; press Space | One bullet at (300, 520) |
| Test Case 2(a) | Ship at x = 0; press Left | Ship remains at x = 0 |
| Test Case 2(b) | Ship at x = 550; press Right | Ship remains at x = 550 |
| Test Case 3 | Five bullets already active; press Space | No sixth bullet; five remain |
| Test Case 4(a) | Bullet hits an enemy | Enemy removed; score = 10; lives = 3 |
| Test Case 4(b) | Enemy reaches bottom | One life lost; lives = 2 |

**Important:** The automated screenshot routine validates and illustrates the listed game states. Also launch the playable game and manually test keyboard controls before submission. Keep genuine screenshots of your own game execution if your instructor specifically requires live/manual execution evidence.

## 9. Program structure

- `Ship`: stores the player's position, size and movement behaviour.
- `Bullet`: stores bullet position and upward movement.
- `Enemy`: stores enemy position and downward movement.
- `Star`: creates the moving star background.
- `Explosion`: draws a short collision effect.
- `SpaceShooter`: manages the game state, event handling, collision detection, score, lives and drawing.
- `capture_test_screenshots()`: checks the university scenarios and creates screenshot evidence.

## 10. Important logic

### Bullet limit

A bullet is added only when the current number of bullets is less than `MAX_BULLETS` (5).

### Boundary detection

The ship's x-coordinate is restricted to the range 0 through `SCREEN_WIDTH - SHIP_WIDTH` (550).

### Collision detection

The program creates Pygame rectangles for bullets and enemies and checks them with:

```python
enemy_rect.colliderect(bullet_rect)
```

When a collision occurs, the enemy and bullet are removed and the score increases by 10.

### Lives and Game Over

When an enemy reaches the bottom of the window, one life is deducted. When lives reach zero, the game displays Game Over and the final score.

## 11. Limitations and future enhancements

- Add optional background music and sound effects.
- Add different enemy types and power-ups.
- Add a high-score saving feature.
- Add a start menu and difficulty selection.
- Add more levels and visual effects.

## 12. Conclusion

The Space Shooter project demonstrates basic object-oriented programming, keyboard event handling, movement, collision detection, lists, conditional logic and graphical output using Python and Pygame. The project has been organised as a single Python file as required by the university instructions.
