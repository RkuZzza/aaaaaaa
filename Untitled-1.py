from pygame import *

# Создаем экран и загружаем фон
win_height = 700
win_width = 900
win = display.set_mode((win_width,win_height))
display.set_caption("Лабиринт")
background = image.load("fon.jpg")
background = transform.scale(background,(win_width,win_height))
# Создаем игровой таймер и частоту обновления
clock = time.Clock()
FPS = 40

mixer.init()
mixer.music.load("jungles.ogg")
mixer.music.play()
money = mixer.Sound("money.ogg")
kick = mixer.Sound("kick.ogg")

# Класс персонажей
class GameSprite(sprite.Sprite):
    # конструктор класса
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (100, 100))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
	
    # Метод перерисовки персонажа
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_UP] and self.rect.y > 10:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y < win_height - 100:
            self.rect.y += self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < win_width - 100:
            self.rect.x += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 10:
            self.rect.x -= self.speed        

class Enemy(GameSprite):
    direction = "left"
    def update(self):
        if self.rect.x >= win_width - 100:
            self.direction = "left"
        if self.rect.x <= 580:
            self.direction = "right"

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color1, color2, color3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width,self.height))
        self.image.fill((color1, color2, color3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

hero = Player("pngwing.png", 40, 600, 10)
monster = Enemy("cyborg.png",win_width - 100, 380, 2)
final = GameSprite("treasure.png", win_width - 120, win_height - 100, 0)

wall_1 = Wall(150, 200, 100, 200, 150, 10, 490) 
wall_2 = Wall(150, 200, 100, 200, 150, 180, 10) 
wall_3 = Wall(150, 200, 100, 530, 30, 10, 250) 
wall_4 = Wall(150, 200, 100, 430, 320, 100, 10)
wall_5 = Wall(150, 200, 100, 430, 520, 200, 10)
wall_6 = Wall(150, 200, 100, 650, 470, 10, 150)
#wall_7 = Wall(150, 200, 100, 430, 520, 200, 10)

font.init()
font = font.Font(None, 200)
won = font.render("YOU WIN!", True, (0,0,255))
lose = font.render("YOU LOSE!", True, (255,0,0))

# Игровой цикл
game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        win.blit(background, (0,0))
        hero.update()
        monster.update()

        hero.reset()
        monster.reset()
        final.reset()
        wall_1.draw_wall()
        wall_2.draw_wall()
        wall_3.draw_wall()
        wall_4.draw_wall()
        wall_5.draw_wall()
        wall_6.draw_wall()
        #wall_7.draw_wall()

    if sprite.collide_rect(hero, final):
        finish = True
        money.play()
        win.blit(won, (100, 300))

    if sprite.collide_rect(hero, monster) or sprite.collide_rect(hero, wall_1) or sprite.collide_rect(hero, wall_2) or sprite.collide_rect(hero, wall_3):
        #finish = True
        #kick.play()
        #win.blit(lose, (100, 300))
        hero.rect.x = 40
        hero.rect.y = 600        

    display.update()
    clock.tick(FPS)


