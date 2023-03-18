import pygame as pg
from random import randint
pg.init()
window=pg.display.set_mode((1920, 1080))
pg.display.set_caption("Shoter")
miss_enemy=0
score=0
gameover="rock-576668.png"
levl=1
count_animation=0
class GameSprite():
    def __init__(self, img, x, y, width, height, speed):
        self.image=pg.transform.scale(pg.image.load(img),(width, height))
        self.width=width
        self.height=height
        self.rect=self.image.get_rect()
        self.rect.x=x        
        self.rect.y=y
        self.speed = speed
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def control(self):
        keys=pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.rect.x>0:
            self.rect.x-=self.speed
        if keys[pg.K_RIGHT] and self.rect.x<1820:
            self.rect.x+=self.speed

class Enemy(GameSprite):
    def respawn(self):
        self.rect.y=0
        self.rect.x=randint(0, 1820)
    def control(self):
        global miss_enemy
        if self.rect.y<1080:
            self.rect.y+=self.speed
        else:
            miss_enemy+=1
            self.respawn()
    def kill(self):
        global bullet , score
        for i in bullet:
            if pg.sprite.collide_rect(self, i):
                score+=1
                self.respawn()
                bullet.remove(i)
class Boss(GameSprite):
    def __init__(self, img, x, y, width, height, speed,health, direction):
        super().__init__(img, x, y, width, height, speed)
        self.health=health
        self.direction=direction
    def move(self):
        global count_animation
        if self.direction==1:
            self.rect.x+=self.speed
        if self.direction==2:
            self.rect.x+=self.speed
        if self.rect.x>1500:
            self.direction=2
        if self.rect.x<0:
            self.direction=1 
        self.image=pg.transform.scale(pg.image.load(f"boss/{count_animation}.gif"),(self.width, self.height))
        count_animation+=1
        if count_animation>59:
            count_animation=0
class Bullet(GameSprite):
    def control(self):
        self.rect.y-=self.speed
bg = GameSprite("clouds-7613361_1920.png", 0, 0, 1920, 1080, 0)
player = Player("rocket-147466.png", 1000,980, 100, 100, 15)
boss=Boss("boss/0.gif", 250, 0, 300, 200, 3, 200, 1)
enemeies=[]
bullet=[]
for i in range(10):
    enemeies.append(Enemy("rock-576668.png",randint (0,980),0, 100,100, 4))
game = True
music = pg.mixer.Sound("The Ice Giants.mp3")
music.set_volume(0.35)
music.play(-1)
while game:
    pg.time.Clock().tick(120)
    for i in pg.event.get():
        if i.type==pg.QUIT:
            exit()
        if i.type==pg.MOUSEBUTTONDOWN:
            bullet.append(Bullet("nuclear-36817.png", player.rect.x+40, player.rect.y, 20, 40, 10 ))
    if score >200:
        levl+=1
        score=0
        enemeies.append(Enemy("rock-576668.png",randint (0,980),0, 100,100, 4))
        game=False
    bg.reset()
    if levl>3:
        boss.move()
        boss.reset()
    player.reset()
    player.control()
    for i in enemeies:
        i.reset()
        i.control()
        i.kill()
        if pg.sprite.collide_rect(i, player) or miss_enemy>5:
            gameover="lose.png"
            game=False
    for i in bullet:
        i.control()
        i.reset()
    lable=pg.font.SysFont("Arial", 25).render(f"Score: {score}", True, "red")
    window.blit(lable, (20, 20))
    lable2=pg.font.SysFont("Arial", 25).render(f"miss: {miss_enemy}", True, "red")
    window.blit(lable2, (20, 50))
    lable2=pg.font.SysFont("Arial", 25).render(f"levl: {levl}", True, "red")
    window.blit(lable2, (20, 80))
    pg.display.flip()
bg = GameSprite(gameover, 0, 0, 1920, 1080, 0)
while True:
    pg.time.Clock().tick(60)
    for i in pg.event.get():
        if i.type==pg.QUIT:
            exit()
    bg.reset()
    pg.display.flip()