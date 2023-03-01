import turtle
import math
import os
import time
import random
import winsound

#Ścieżka
#os.chdir("I:\Python\Projekt")

#Ustawienie ekranu
wn = turtle.Screen()
wn.cv._rootwindow.resizable(False, False)
wn.title("Żabbor")
wn.setup(600, 800)
wn.bgcolor("black")
wn.bgpic("background2.gif")
wn.tracer(0)

#Definiowanie kształtu
shapes = ["frog_one_up.gif", "frog_one_down.gif", "frog_one_left.gif", "frog_one_right.gif", "car_left.gif", "car_right.gif", "log.gif", 
    "turtle_left.gif", "turtle_right.gif", "turtle_right_half.gif", "turtle_left_half.gif", 
    "turtle_submerged.gif", "home.gif", "frog_home.gif", "frog_small.gif",
    "pickup_left.gif", "pickup_right.gif", "tir_left.gif", "tir_right.gif",
    "tractor_left.gif", "tractor_right.gif", "snake.gif", "snake_right.gif"]
for shape in shapes:
    wn.register_shape(shape)

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()
pen.penup()

#Klasy
class Sprite():
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y 
        self.width = width
        self.height = height 
        self.image = image

    def render(self, pen):
        pen.goto(self.x, self.y)
        pen.shape(self.image)
        pen.stamp()

    def update(self):
        pass

    #Detekcja kolizji
    def is_collision(self, other):
        x_collision = (math.fabs(self.x - other.x) * 2) < (self.width + other.width)
        y_collision = (math.fabs(self.y - other.y) * 2) < (self.height + other.height)
        return (x_collision and y_collision)

class Player(Sprite):
    def __init__(self, x, y, width, height, image):
        Sprite.__init__(self, x, y, width, height, image)
        self.dx = 0
        self.collision = False
        self.frogs_home = 0
        self.max_time = 60
        self.time_remaining = 60
        self.start_time = time.time()
        self.lives = 5
        self.level = 1

    def up(self):
        self.y += 50
        self.sound_hop()
        self.image = "frog_one_up.gif"
    
    def down(self):
        if self.y <= -300:
            self.y -= 0
            self.image = "frog_one_down.gif"
        else:
            self.y -= 50
            player.sound_hop()
            self.image = "frog_one_down.gif"

    def right(self):
        self.x += 50
        player.sound_hop()
        self.image = "frog_one_right.gif"

    def left(self):
        self.x -= 50
        player.sound_hop()
        self.image = "frog_one_left.gif"

    def update(self):
        self.x += self.dx

    #Ściana - kolizja
        if self.x < -300 or self.x > 300:
            player.x = 0
            player.y = -300

        self.time_remaining = self.max_time - round(time.time() - self.start_time)

        #Koniec czasu
        if self.time_remaining <= 0:
            player.lives -= 1
            self.go_home()

    def go_home(self):
        self.dx = 0
        self.x = 0
        self.y = -300
        self.max_time = 60
        self.time_remaining = 60
        self.start_time = time.time()

    def next_level(self):
        self.level += 1

    def sound_hop(self):
        winsound.PlaySound("sound_hop.wav", winsound.SND_ASYNC)

    def sound_plunk(self):
        winsound.PlaySound("sound_plunk.wav", winsound.SND_ASYNC)

    def sound_squash(self):
        winsound.PlaySound("sound_squash.wav", winsound.SND_ASYNC)

    def sound_time(self):
        winsound.PlaySound("sound_time.wav", winsound.SND_ASYNC)

class Car(Sprite):
    def __init__(self, x, y, width, height, image, dx):
        Sprite.__init__(self, x, y, width, height, image)
        self.dx = dx

    def update(self):
        self.x += self.dx

        #Ściana - kolizja
        if self.x < -400:
            self.x = 400

        if self.x > 400:
            self.x = -400

class Log(Sprite):
    def __init__(self, x, y, width, height, image, dx):
        Sprite.__init__(self, x, y, width, height, image)
        self.dx = dx

    def update(self):
        self.x += self.dx

        #Ściana - kolizja
        if self.x < -400:
            self.x = 400

        if self.x > 400:
            self.x = -400

class Turtle(Sprite):
    def __init__(self, x, y, width, height, image, dx):
        Sprite.__init__(self, x, y, width, height, image)
        self.dx = dx
        self.state = "full" #half, submerged
        self.full_time = random.randint(5, 8)
        self.half_up_time = random.randint(3, 5)
        self.half_down_time = random.randint(3, 5)
        self.submerged_time = random.randint(2, 3)
        self.start_time = time.time()

    def update(self):
        self.x += self.dx

        #Ściana - kolizja
        if self.x < -400:
            self.x = 400

        if self.x > 400:
            self.x = -400

        #Aktualizacja żółwia
        if self.state == "full":
            if self.dx > 0:
                self.image = "turtle_right.gif"
            else:
                self.image = "turtle_left.gif"
        elif self.state == "half_up" or self.state == "half_down":
            if self.dx > 0:
                self.image = "turtle_right_half.gif"
            else:
                self.image = "turtle_left_half.gif"
        elif self.state == "submerged":
            self.image = "turtle_submerged.gif"

        #Czasomierz
        if self.state == "full" and time.time() - self.start_time > self.full_time:
            self.state = "half_down"
            self.start_time = time.time()
        elif self.state == "half_down" and time.time() - self.start_time > self.half_down_time:
            self.state = "submerged"
            self.start_time = time.time()
        elif self.state == "submerged" and time.time() - self.start_time > self.submerged_time:
            self.state = "half_up"
            self.start_time = time.time()
        elif self.state == "half_up" and time.time() - self.start_time > self.half_up_time:
            self.state = "full"
            self.start_time = time.time()
        
class Home(Sprite):
    def __init__(self, x, y, width, height, image):
        Sprite.__init__(self, x, y, width, height, image)
        self.dx = 0

class Timer():
    def __init__(self, max_time):
        self.x = 250
        self.y = -370
        self.max_time = max_time
        self.width = 200

    def render(self, time, pen):
        pen.color("green")
        pen.pensize(5)
        pen.penup()
        pen.goto(self.x, self.y)
        pen.pendown()
        percent = time/self.max_time
        dx = percent * self.width
        pen.goto(self.x-dx, self.y)
        pen.penup()

class Snake(Sprite):
    def __init__(self, x, y, width, height, image, dx):
        Sprite.__init__(self, x, y, width, height, image)
        self.dx = dx

    def update(self):
        self.x += self.dx

    #Ściana - kolizja
        if self.x < -400:
            self.x = 400

        if self.x > 400:
            self.x = -400

#Obiekty w grze
player = Player(0, -300, 40, 40, "frog_one_up.gif")
timer = Timer(60)
snake = Snake(0, 0, 91, 40, "snake.gif", 0)

level_1 = [
    Car(0, -250, 45, 40, "tractor_left.gif", -0.29),
    Car(270, -250, 39, 40, "car_left.gif", -0.29),

    Car(100, -200, 106, 40, "tir_right.gif", 0.33),
    Car(-200, -200, 52, 40, "pickup_right.gif", 0.33),

    Car(50, -150, 52, 40, "pickup_left.gif", -0.3),
    Car(350, -150, 39, 40, "car_left.gif", -0.3),

    Car(150, -100, 53, 40, "car_right.gif", 0.35),
    Car(-150, -100, 45, 40, "tractor_right.gif", 0.35),

    Car(350, -50, 106, 40, "tir_left.gif", -0.45),
    Car(20, -50, 59, 40, "car_left.gif", -0.45),

    Log(0, 50, 168, 40, "log.gif", 0.26),
    Log(400, 50, 168, 40, "log.gif", 0.26),

    Turtle(200, 100, 155, 40, "turtle_left.gif", -0.25),
    Turtle(-200, 100, 155, 40, "turtle_left.gif", -0.25),

    Log(100, 150, 168, 40, "log.gif", 0.3),
    Log(500, 150, 168, 40, "log.gif", 0.3),

    Turtle(0, 200, 142, 40, "turtle_right.gif", 0.24),
    Turtle(-500, 200, 142, 40, "turtle_right.gif", 0.24),

    Log(-500, 250, 168, 40, "log.gif", -0.23),
    Log(0, 250, 168, 40, "log.gif", -0.23)
    ] 

level_2 = [
    Car(0, -250, 106, 40, "tir_left.gif", -0.35),
    Car(270, -250, 59, 40, "car_left.gif", -0.35),
    Car(-270, -250, 52, 40, "pickup_left.gif", -0.35),

    Car(100, -200, 45, 40, "tractor_right.gif", 0.4),
    Car(-200, -200, 53, 40, "car_right.gif", 0.4),
    Car(-500, -200, 106, 40, "tir_right.gif", 0.4),

    Car(50, -150, 45, 40, "tractor_left.gif", -0.35),
    Car(350, -150, 59, 40, "car_left.gif", -0.35),
    Car(-200, -150, 52, 40, "pickup_left.gif", -0.35),

    Car(150, -100, 106, 40, "tir_right.gif", 0.35),
    Car(-150, -100, 106, 40, "tir_right.gif", 0.35),

    Car(350, -50, 59, 40, "car_left.gif", -0.45),
    Car(20, -50, 59, 40, "car_left.gif", -0.45),

    Turtle(0, 50, 142, 40, "turtle_right.gif", 0.35),
    Log(400, 50, 168, 40, "log.gif", 0.35),

    Turtle(200, 100, 155, 40, "turtle_left.gif", -0.25),
    Turtle(-200, 100, 155, 40, "turtle_left.gif", -0.25),

    Turtle(100, 150, 142, 40, "turtle_right.gif", 0.3),
    Log(-700, 150, 168, 40, "log.gif", 0.3),

    Turtle(0, 200, 142, 40, "turtle_right.gif", 0.24),
    Turtle(-500, 200, 142, 40, "turtle_right.gif", 0.24),

    Log(-500, 250, 168, 40, "log.gif", -0.23),
    Log(0, 250, 168, 40, "log.gif", -0.23)
    ] 

level_3 = [
    Car(0, -250, 45, 40, "tractor_left.gif", -0.58),
    Car(270, -250, 45, 40, "tractor_left.gif", -0.58),

    Car(100, -200, 106, 40, "tir_right.gif", 0.66),
    Car(-200, -200, 53, 40, "car_right.gif", 0.66),

    Car(50, -150, 59, 40, "car_left.gif", -0.6),
    Car(350, -150, 59, 40, "car_left.gif", -0.6),

    Car(150, -100, 52, 40, "pickup_right.gif", 0.7),
    Car(-150, -100, 53, 40, "car_right.gif", 0.7),

    Car(350, -50, 59, 40, "car_left.gif", -0.9),
    Car(20, -50, 106, 40, "tir_left.gif", -0.9),

    Log(0, 50, 168, 40, "log.gif", 0.52),
    Log(400, 50, 168, 40, "log.gif", 0.52),

    Turtle(200, 100, 155, 40, "turtle_left.gif", -0.5),
    Turtle(-200, 100, 155, 40, "turtle_left.gif", -0.5),

    Log(100, 150, 168, 40, "log.gif", 0.6),
    Log(500, 150, 168, 40, "log.gif", 0.6),

    Turtle(0, 200, 142, 40, "turtle_right.gif", 0.48),
    Turtle(-500, 200, 142, 40, "turtle_right.gif", 0.48),

    Log(-500, 250, 168, 40, "log.gif", -0.46),
    Log(0, 250, 168, 40, "log.gif", -0.46)
    ] 

level_4 = [
    Car(0, -250, 59, 40, "car_left.gif", -0.5),
    Car(270, -250, 59, 40, "car_left.gif", -0.5),
    Car(-270, -250, 59, 40, "car_left.gif", -0.5),

    Car(100, -200, 53, 40, "car_right.gif", 0.55),
    Car(-200, -200, 53, 40, "car_right.gif", 0.55),
    Car(-500, -200, 53, 40, "car_right.gif", 0.55),

    Car(50, -150, 59, 40, "car_left.gif", -0.6),
    Car(350, -150, 59, 40, "car_left.gif", -0.6),
    Car(-200, -150, 59, 40, "car_left.gif", -0.6),

    Car(150, -100, 53, 40, "car_right.gif", 0.6),
    Car(-150, -100, 53, 40, "car_right.gif", 0.6),

    Car(350, -50, 59, 40, "car_left.gif", -0.75),
    Car(20, -50, 59, 40, "car_left.gif", -0.75),

    Turtle(0, 50, 142, 40, "turtle_right.gif", 0.65),
    Log(400, 50, 168, 40, "log.gif", 0.65),

    Turtle(200, 100, 155, 40, "turtle_left.gif", -0.55),
    Turtle(-200, 100, 155, 40, "turtle_left.gif", -0.55),

    Turtle(100, 150, 155, 40, "turtle_right.gif", 0.6),
    Log(-700, 150, 168, 40, "log.gif", 0.6),

    Turtle(0, 200, 142, 40, "turtle_right.gif", 0.54),
    Turtle(-500, 200, 142, 40, "turtle_right.gif", 0.54),

    Log(-500, 250, 168, 40, "log.gif", -0.53),
    Log(0, 250, 168, 40, "log.gif", -0.53)
    ] 

level_5 = [
    Car(0, -250, 106, 40, "tir_left.gif", -0.7),
    Car(270, -250, 106, 40, "tir_left.gif", -0.7),

    Car(100, -200, 106, 40, "tir_right.gif", 0.8),
    Car(-200, -200, 106, 40, "tir_right.gif", 0.8),

    Car(50, -150, 106, 40, "tir_left.gif", -0.9),
    Car(350, -150, 106, 40, "tir_left.gif", -0.9),

    Car(150, -100, 106, 40, "tir_right.gif", 0.7),
    Car(-150, -100, 106, 40, "tir_right.gif", 0.7),

    Car(350, -50, 106, 40, "tir_left.gif", -1.1),
    Car(20, -50, 106, 40, "tir_left.gif", -1.1),

    Turtle(0, 50, 161, 40, "turtle_right.gif", 0.7),
    Turtle(400, 50, 161, 40, "turtle_right.gif", 0.7),

    Turtle(200, 100, 155, 40, "turtle_left.gif", -0.8),
    Turtle(-200, 100, 155, 40, "turtle_left.gif", -0.8),

    Turtle(100, 150, 142, 40, "turtle_right.gif", 0.8),
    Turtle(500, 150, 142, 40, "turtle_right.gif", 0.8),

    Turtle(0, 200, 142, 40, "turtle_right.gif", 0.6),
    Turtle(-500, 200, 142, 40, "turtle_right.gif", 0.6),

    Turtle(-500, 250, 161, 40, "turtle_left.gif", -0.7),
    Turtle(0, 250, 161, 40, "turtle_left.gif", -0.7)
    ] 


homes = [
    Home(0, 300, 50, 50, "home.gif"),
    Home(-130, 300, 50, 50, "home.gif"),
    Home(-260, 300, 50, 50, "home.gif"),
    Home(130, 300, 50, 50, "home.gif"),
    Home(260, 300, 50, 50, "home.gif")
]

#Lista obiektów startowych
sprites = level_1 + homes
sprites.append(player)
sprites.append(snake)

#Klawiatura - obsługa
wn.listen()
wn.onkeypress(player.up, "Up")
wn.onkeypress(player.down, "Down")
wn.onkeypress(player.right, "Right")
wn.onkeypress(player.left, "Left")

while True:
    #Renderowanie
    for sprite in sprites:
        sprite.render(pen)
        sprite.update()
    
    #Renderowanie czasomierzu
    timer.render(player.time_remaining, pen)

    #Renderowanie żyć
    pen.goto(-290, -375)
    pen.shape("frog_small.gif")
    for life in range(player.lives):
        pen.goto(-270 + (life * 30), -365)
        pen.stamp()

    #Sprawdzanie kolizji
    player.dx = 0
    player.collision = False
    for sprite in sprites:
        if player.is_collision(sprite):
            if isinstance(sprite, Car):
                player.lives -= 1
                player.sound_squash()
                player.go_home()
                break
            elif isinstance(sprite, Log):
                player.dx = sprite.dx
                player.collision = True
                break
            elif isinstance(sprite, Turtle) and sprite.state != "submerged":
                player.dx = sprite.dx
                player.collision = True
                break
            elif isinstance(sprite, Home):
                player.go_home()
                sprite.image = "frog_home.gif"
                player.frogs_home += 1
                break
            elif isinstance(sprite, Snake):
                player.lives -= 1
                player.sound_squash()
                player.go_home()
                break

    if(player.y == 0 and player.x > snake.x):
            snake.dx = 0.2
            snake.image = "snake_right.gif"
    elif(player.y == 0 and player.x < snake.x):
            snake.dx = -0.2
            snake.image = "snake.gif"

    #Woda
    if player.y > 0 and player.collision != True:
        player.lives -= 1
        player.sound_plunk()
        player.go_home()

    #Kolejny poziom
    if player.frogs_home == 5:
        player.go_home()
        player.frogs_home = 0
        player.next_level()
        for home in homes:
            home.image = "home.gif"
        if player.level == 1:
            sprites = level_1 + homes
            sprites.append(player)
        elif player.level == 2:
            sprites = level_2 + homes
            sprites.append(player)
        elif player.level == 3:
            sprites = level_3 + homes
            sprites.append(player)
        elif player.level == 4:
            sprites = level_4 + homes
            sprites.append(player)
        elif player.level == 5:
            sprites = level_5 + homes
            sprites.append(player)
        else:
            sprites = level_1 + homes
            sprites.append(player)



    #Koniec żyć
    if player.lives == 0:
        player.go_home()
        player.frogs_home = 0
        player.level = 1
        for home in homes:
            home.image = "home.gif"
        player.lives = 5
        
    #Update ekranu
    wn.update()

    #Czyszczenie ekranu
    pen.clear()

wn.mainloop()
