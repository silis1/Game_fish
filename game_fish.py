import pygame
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
WATER_Y = 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 32, True)

COLORS = {
    "orange": (255, 140, 40),
    "green": (90, 160, 70),
    "violet": (150, 80, 200),
}
score = 0
hook = {"x": 560, "y": 190, "state": "idle", "fish": None}


def make_fish():
    return {
        "x": random.randint(0, WIDTH),
        "y": random.randint(WATER_Y + 60, HEIGHT - 60),
        "speed": random.choice([-3, -2, 2, 3]),
        "color": random.choice(list(COLORS)),
    }


fishes = [make_fish() for _ in range(6)]



def draw_fish(fish):
    x = int(fish["x"])
    y = int(fish["y"])
    color = COLORS[fish["color"]]

    direction = 1 if fish["speed"] > 0 else -1

    # دم ماهی
    pygame.draw.polygon(screen, color, [
        (x - direction * 15, y),
        (x - direction * 30, y - 12),
        (x - direction * 30, y + 12)
    ])

    # بدن ماهی
    pygame.draw.ellipse(screen, color, (x - 20, y - 10, 40, 20))

    # چشم ماهی
    pygame.draw.circle(
        screen, (0, 0, 0),
        (x + direction * 12, y - 3), 3
    )

    # باله ماهی
    pygame.draw.polygon(screen, color, [
        (x, y - 5),
        (x - 7, y - 15),
        (x + 8, y - 5)
    ])



def cast():
    if hook["state"] == "idle":
        hook["state"] = "down"


def update():
    global score
    for fish in fishes:
        fish["x"] += fish["speed"]
        if fish["x"] < -40 or fish["x"] > WIDTH + 40:
            fish["speed"] = -fish["speed"]

    if hook["state"] == "down":
        hook["y"] += 6
        for fish in fishes:
            near_x = abs(fish["x"] - hook["x"]) < 30
            near_y = abs(fish["y"] - hook["y"]) < 20
            if near_x and near_y:
                hook["fish"] = fish
                hook["state"] = "up"
                break
        if hook["y"] > HEIGHT - 40:
            hook["state"] = "up"
    elif hook["state"] == "up":
        hook["y"] -= 8
        if hook["fish"]:
            hook["fish"]["x"] = hook["x"]
            hook["fish"]["y"] = hook["y"]
        if hook["y"] <= 190:
            if hook["fish"]:
                score += 10 
                fishes.remove(hook["fish"])
                fishes.append(make_fish())
                hook["fish"] = None
            hook["state"] = "idle"


def draw_person():
    # سر آدمک
    pygame.draw.circle(screen, (255, 220, 170), (420, 165), 12)

    # مو
    pygame.draw.arc(
        screen, (50, 30, 20),
        (408, 153, 24, 18), 0, 3.14, 4
    )

    # بدن
    pygame.draw.line(
        screen, (200, 40, 40),
        (420, 177), (420, 210), 6
    )

    # دست چپ
    pygame.draw.line(
        screen, (255, 220, 170),
        (420, 185), (405, 200), 5
    )

    # دست راست
    pygame.draw.line(
        screen, (255, 220, 170),
        (420, 185), (470, 170), 5
    )

    # پای چپ
    pygame.draw.line(
        screen, (30, 30, 30),
        (420, 210), (408, 230), 6
    )

    # پای راست
    pygame.draw.line(
        screen, (30, 30, 30),
        (420, 210), (435, 230), 6
    )

    # چوب ماهیگیری
    pygame.draw.line(
        screen, (90, 50, 20),
        (470, 170), (560, 150), 4
    )


def draw():
    screen.fill((120, 200, 255))
    water = (0, WATER_Y, WIDTH, HEIGHT - WATER_Y)
    pygame.draw.rect(screen, (30, 90, 170), water)
    pygame.draw.rect(screen, (140, 90, 40), (380, 230, 240, 20))
    draw_person()
    tip = (560, 150)
    pos = (hook["x"], hook["y"])
    pygame.draw.line(screen, (255, 255, 255), tip, pos, 2)
    pygame.draw.circle(screen, (220, 40, 40), pos, 8)
    for fish in fishes:
        draw_fish(fish)
    text = font.render(f"SCORE: {score}", True, (255, 255, 255))
    screen.blit(text, (20, 20))
    pygame.display.flip()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                cast()

    keys = pygame.key.get_pressed()
    if hook["state"] == "idle":
        move = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        hook["x"] += move * 5

    update()
    draw()
    clock.tick(60)

pygame.quit()
