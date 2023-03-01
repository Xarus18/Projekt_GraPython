import turtle
import os

#Ścieżka
os.chdir("I:\Kacper\IV semestr\Python\Projekt")

#Ustawienie ekranu
wn = turtle.Screen()
wn.cv._rootwindow.resizable(False, False)
wn.title("Żabbor")
wn.setup(600, 800)
wn.bgcolor("black")
wn.bgpic("splash.gif")
wn.tracer(0)

def start_game():
    global game_state
    game_state = "game"

pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()

#Obsługa klawiatury
wn.listen()
wn.onkeypress(start_game, "s")

game_state = "splash"

#Główna pętla
while True:

    #Ekrany
    if game_state == "splash":
        wn.bgpic("splash.gif")
        
    elif game_state == "game":
        import zabbor

    #Update ekranu
    wn.update()