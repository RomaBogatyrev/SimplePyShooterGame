#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as timer
#from Pyinstaller
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
font.init()
font1 = font.SysFont('Arial', 36)
win = font1.render("WIN", True, (0, 255, 0))
lose = font1.render("GG", True, (255, 0, 0))
spd = 10
lost = 0
score = 0
goal = 100
max_lost = 50
life = 15
life_color = (0,255,0)
health_delay = 0


img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"
img_ast = "asteroid-icon.png"
img_heal = "healthkit.png"
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 595:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        fire_sound.play()
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class HealthKit0(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

            


win_width = 700
win_height = 500
window = display.set_mode((win_width,win_height))
display.set_caption("Shooter")
background = transform.scale(image.load(img_back), (win_width, win_height))
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), 0, 80, 50, randint(1, 3))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 60, 60, randint(1, 5))
    asteroids.add(asteroid)

healths = sprite.Group()
for i in range(1, 3):
    health = HealthKit0(img_heal, randint(30, win_width - 30), -40, 60, 60, randint(1, 5))
    healths.add(health)

bullets = sprite.Group()

finish = False
run = True
rel_time = False
num_fire = 0

while run:
    
    

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_z:
                if num_fire < 60 and rel_time == False:
                    num_fire = num_fire + 1
                    ship.fire()
                
                if num_fire >= 60 and rel_time == False:
                    last_time = timer()
                    rel_time = True
            if e.key == K_x:
                if num_fire < 60 and rel_time == False:
                    num_fire = num_fire + 1
                    ship.fire()
                
                if num_fire >= 60 and rel_time == False:
                    last_time = timer()
                    rel_time = True
            if e.key == K_c:
                if num_fire < 60 and rel_time == False:
                    num_fire = num_fire + 1
                    ship.fire()
                
                if num_fire >= 60 and rel_time == False:
                    last_time = timer()
                    rel_time = True
            if e.key == K_SPACE:
                if num_fire < 60 and rel_time == False:
                    num_fire = num_fire + 1
                    ship.fire()
                
                if num_fire >= 60 and rel_time == False:
                    last_time = timer()
                    rel_time = True
                
    if not finish:
        window.blit(background,(0, 0))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), 0, 80, 50, randint(1, 3))
            monsters.add(monster)
        collides_ast = sprite.groupcollide(asteroids, bullets, True, True)
        for c in collides_ast:
            score = score + 1
            asteroid = Enemy(img_ast, randint(80, win_width - 80), 0, 60, 60, randint(1, 3))
            asteroids.add(asteroid)

        ship.update()
        ship.reset()

        asteroids.update()
        asteroids.draw(window)

        bullets.update()
        bullets.draw(window)

        monsters.update()
        monsters.draw(window)

        healths.update()
        healths.draw(window)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font1.render("Перезарядка...", 1, (255, 255, 255))
                window.blit(reload, (32, 320 ))
            else:
                num_fire = 0
                rel_time = False

        if life > 5:
            life_color = (0, 255, 0)
        if life == 5:
            life_color = (0, 255, 0)
        if life == 4:
            life_color = (0, 150, 0)
        if life == 3:
            life_color = (255, 255, 0)
        if life == 2:
            life_color = (150, 0, 0)
        if life == 1:
            life_color = (255, 0, 0)

        health_delay = health_delay + 1

        if health_delay > 100:
            health_delay = 0

        text_speed = font1.render("Замедление " + str(spd), 1, (255, 255, 255))
        window.blit(text_speed,(32, 32))
        text_lose = font1.render("Пропущенно " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose,(32, 64))
        text_score = font1.render("Очки " + str(score), 1, (255, 255, 255))
        window.blit(text_score,(32, 96))
        text_life = font1.render("Жизни " + str(life), 1, life_color)
        window.blit(text_life,(32, 128))
        
        if sprite.spritecollide(ship, monsters, False):
            monster = Enemy(img_enemy, randint(80, win_width - 80), 0, 80, 50, randint(1, 3))
            monsters.add(monster)
        if sprite.spritecollide(ship, asteroids, False):
            asteroid = Enemy(img_ast, randint(80, win_width - 80), 0, 80, 50, randint(1, 3))
            asteroids.add(asteroid)
        if sprite.spritecollide(ship, healths, False):
            health = HealthKit0(img_heal, randint(80, win_width - 80), 0, 60, 60, randint(1, 3))
            healths.add(health)
            sprite.spritecollide(ship, healths, True)
            life = life + 1
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life - 1
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        
        

        display.update()
    time.delay(spd)