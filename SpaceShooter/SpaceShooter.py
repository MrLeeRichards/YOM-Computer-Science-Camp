from pygame import *
import random

class Ship(sprite.Sprite):
    def __init__(self, game_rect):
        sprite.Sprite.__init__(self)

        self.image = image.load("Ship.png")
        self.image.convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.bottom = game_rect.centerx, game_rect.bottom

class Shot(sprite.Sprite):
    def __init__(self, ship_rect):
        sprite.Sprite.__init__(self)
        
        shot_image = image.load("Shot.png").convert_alpha()
        self.images = [shot_image, transform.rotate(shot_image, 90), transform.rotate(shot_image, 180), transform.rotate(shot_image, 270)]

        self.rect = shot_image.get_rect()
        self.rect.centerx, self.rect.centery = ship_rect.centerx, ship_rect.top

    def getImage(self):
        return random.choice(self.images)

class Bug(sprite.Sprite):
    def __init__(self, game_rect):
        sprite.Sprite.__init__(self)
        
        self.image = image.load("bug.png").convert_alpha()

        self.rect = self.image.get_rect()

        self.abs_x = random.randint(game_rect.left + self.rect.centerx, game_rect.right - self.rect.centerx)
        self.abs_y = -random.randint(game_rect.top + self.rect.centery, game_rect.bottom - self.rect.centery)

        self.rect.centerx = int(self.abs_x)
        self.rect.centery = int(self.abs_y)

        self.bug_type = random.randint(1,3)
        if self.bug_type == 1:
            self.image.fill(Color(random.randint(0,126), random.randint(0,126), 255), None, BLEND_MULT)
            self.speed = .5
            self.points = 5
            self.strafe = random.choice([1,-1])
        elif self.bug_type == 2:
            self.image.fill(Color(random.randint(0,126), 255, random.randint(0,126)), None, BLEND_MULT)
            self.speed = 1
            self.points = 10
            self.strafe = random.choice([.5,-.5])
        elif self.bug_type == 3:
            self.image.fill(Color(255, random.randint(0,126), random.randint(0,126)), None, BLEND_MULT)
            self.speed = 2
            self.points = 20
            self.strafe = 0

    def get_rect(self):
        return self.rect

    def update_bug(self, game_rect, score):
        #Bounce on the edges
        if self.rect.right >= game_rect.right:
            self.strafe = -abs(self.strafe)
        if self.rect.left <= game_rect.left:
            self.strafe = abs(self.strafe)
      
        self.abs_x += self.strafe
        self.abs_y += .0035 * self.speed * score + self.speed

        self.rect.centerx = int(self.abs_x)
        self.rect.centery = int(self.abs_y)

class GreenSplodes:
    def __init__(self):
        self.splode_centers = []
        self.image = image.load("GreenSplode.png").convert_alpha()
        self.rect = self.image.get_rect()

    def add_splode(self, center):
        self.splode_centers.append(center)

    def get_splode_rect(self, center):
        self.rect.center = center
        return self.rect

mixer.init(44100, allowedchanges=AUDIO_ALLOW_ANY_CHANGE)
init()

screen_surface = display.set_mode((640,480))
game_surface = Surface((640,480), SRCALPHA).convert_alpha()
game_rect = game_surface.get_rect()

game_clock = time.Clock()

#Set up game state data
ship = Ship(game_rect)
life_icon = transform.scale(ship.image.copy(), (int(ship.rect.width * .5), int(ship.rect.height * .5)))
shots = []

bugs = [Bug(game_rect) for i in range(20)]

ongoing = True
back_color = Color(0,0,0,100)
damage_color = Color(50, 0, 0)
green_splodes = GreenSplodes()

score = 0
score_font = font.SysFont("Consolas", 16)

lives = 4

start = font.SysFont("Consolas", 64).render("START", False, Color(255,0,0))
start_rect = start.get_rect()
start_rect.center = game_rect.center

game_surface.blit(start, start_rect)
screen_surface.blit(game_surface, (0,0))
display.flip()

ready = False
while not ready:
    for next_event in event.get():
        if next_event.type == MOUSEBUTTONDOWN:
            ready = True
        elif next_event.type == QUIT:
            ongoing = False

    game_clock.tick(60)

music = mixer.Sound("MountainKing.ogg")
music.play()

while ongoing and lives > 0:
    #Process click and key events
    for next_event in event.get():
        if next_event.type == QUIT or (next_event.type == KEYDOWN and next_event.key == K_ESCAPE):
            ongoing = False
        elif ((next_event.type == MOUSEBUTTONDOWN and next_event.button == 1) or (next_event.type == KEYDOWN and next_event.key == K_SPACE)) and len(shots) < 2:
            shots.append(Shot(ship.rect))

    #Move ship based on mouse position
    mouse_x = mouse.get_pos()[0]
    if mouse_x > ship.rect.centerx + 5 and ship.rect.right < game_rect.right:
        ship.rect.centerx += 5
    elif mouse_x < ship.rect.centerx -5 and ship.rect.left > game_rect.left:
        ship.rect.centerx -= 5

    #Update bugs and shots
    bug_i = 0
    while bug_i < len(bugs):
        shot_i = 0
        bug_shot = False

        while shot_i < len(shots):
            if shots[shot_i].rect.bottom < game_rect.top or sprite.collide_rect(shots[shot_i], bugs[bug_i]):
                bug_shot = True
                shots.pop(shot_i)
            else:
                shot_i += 1

        ship_hit = sprite.collide_rect(ship, bugs[bug_i])
        if bug_shot or bugs[bug_i].rect.top > game_rect.bottom or ship_hit:
            if bug_shot:
                score += bugs[bug_i].points
                green_splodes.splode_centers.append(bugs[bug_i].rect.center)
            if ship_hit:
                lives -= 1
                ship.image.fill(damage_color, None, BLEND_ADD)
                green_splodes.splode_centers.append(bugs[bug_i].rect.center)
            bugs[bug_i] = Bug(game_rect)
        else:
            bugs[bug_i].update_bug(game_rect, score)

        bug_i += 1

    for i in range(len(shots)):
        shots[i].rect.y -= 10

    #Draw next frame
    game_surface.fill(back_color)
    game_surface.blit(ship.image, ship.rect)

    for shot in shots:
        game_surface.blit(shot.getImage(), shot.rect)

    for bug in bugs:
        game_surface.blit(bug.image, bug.get_rect())

    for center in green_splodes.splode_centers:
        game_surface.blit(green_splodes.image, green_splodes.get_splode_rect(center), None, BLEND_RGBA_ADD)
    green_splodes.splode_centers.clear()

    game_surface.blit(score_font.render(str(score), False, Color(255,255,255)), (5,5))
    
    for life in range(lives - 1):
        game_surface.blit(life_icon, (game_rect.width - life_icon.get_rect().width * (life + 1), 0))

    screen_surface.blit(game_surface, (0,0))
    display.flip()
    game_clock.tick(60)

game_over_hue = 0
game_over_color = Color(0,0,0,0)
game_over_font = font.SysFont("Consolas", 64)
game_over_rect = game_over_font.render("GAME OVER", False, game_over_color).get_rect()
game_over_rect.center = game_rect.center

final_score = font.SysFont("Consolas", 32).render("Final Score: " + str(score), False, Color(255,255,255))
final_rect = final_score.get_rect()
final_rect.centerx = game_over_rect.centerx
final_rect.top = game_over_rect.bottom

bounce_x = random.choice([-5, 5])
bounce_y = random.choice([-5, 5])
angle = 0

green_splodes.image = image.load("Splode.png").convert_alpha()

music.fadeout(2000)

#Game Over Screen
while ongoing:
    #Process click and key events
    for next_event in event.get():
        if next_event.type == QUIT or (next_event.type == KEYDOWN and next_event.key == K_ESCAPE):
            ongoing = False

    for bug_i in range(len(bugs)):
        if bugs[bug_i].rect.top > game_rect.bottom:
            bugs[bug_i] = Bug(game_rect)
        else:
            bugs[bug_i].update_bug(game_rect, score)

    game_surface.fill(back_color)

    for bug in bugs:
        game_surface.blit(bug.image, bug.get_rect())

        if bug.rect.collidepoint(ship.rect.center):
            bounce_x = random.choice([-5, 5])
            bounce_y = random.choice([-5, 5])
            green_splodes.splode_centers.append(ship.rect.center)

    if ship.rect.right > game_rect.right:
        bounce_x = -abs(bounce_x)
    if ship.rect.left < game_rect.left:
        bounce_x = abs(bounce_x)

    if ship.rect.bottom > game_rect.bottom:
        bounce_y = -abs(bounce_y)
    if ship.rect.top < game_rect.top:
        bounce_y = abs(bounce_y)

    ship.rect.x += bounce_x
    ship.rect.y += bounce_y
    angle = (angle + 13) % 360

    game_over_color.hsva = (game_over_hue,100,100,100)
    game_surface.blit(game_over_font.render("GAME OVER", False, game_over_color), game_over_rect)
    game_over_hue = (game_over_hue + 1) % 360
    game_surface.blit(final_score, final_rect)

    game_surface.blit(transform.rotate(ship.image, angle), ship.rect)

    for center in green_splodes.splode_centers:
        game_surface.blit(green_splodes.image, green_splodes.get_splode_rect(center), None, BLEND_RGBA_ADD)
    green_splodes.splode_centers.clear()

    screen_surface.blit(game_surface, (0,0))
    display.flip()
    game_clock.tick(60)

quit()