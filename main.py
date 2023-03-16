from tkinter import *
from tkinter.messagebox import *
import random

GAME_WIDTH = 500
GAME_HEIGHT = 500
SPEED = 100
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
FOREGROUND_COLOR = "#00FF00"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        for i in range (0, BODY_PARTS):
            self.coordinates.append([0,0])
        
        for x,y in self.coordinates:
            square = canva.create_rectangle(x , y , x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x,y]
        canva.create_oval(x,y,x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def turn(snake, food):
    x,y = snake.coordinates[0]
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0,(x,y))
    square = canva.create_rectangle(x,y,x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags="snake")
    snake.squares.insert(0, square)
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        subtitle.config(text="Score : {}".format(score))
        canva.delete("food")
        food = Food()
    else :
        del snake.coordinates[-1]
        canva.delete(snake.squares[-1])
        del snake.squares[-1]
    if check_collisions(snake):
        game_over()
    else:
        root.after(SPEED, turn, snake, food)

def change_direction(new_direction):
    global direction
    if new_direction == "left":
        if direction != "right":
            direction = new_direction
    if new_direction == "right":
        if direction != "left":
            direction = new_direction
    if new_direction == "up":
        if direction != "down":
            direction = new_direction
    if new_direction == "down":
        if direction != "up":
            direction = new_direction

def check_collisions(snake):
    x,y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

def game_over():
    global lose
    lose = True
    canva.delete(ALL)
    canva.create_text(canva.winfo_width()/2, canva.winfo_height()/2, font=("Consolas",40),text="Fin de la Partie", fill="red", tag="lose")

def restart_game():
    global score, direction, lose
    if lose == True:
        direction = "down"
        score = 0
        subtitle.config(text="Score : {}".format(score))
        canva.delete(ALL)
        snake = Snake()
        food = Food()
        turn(snake,food)
        lose = False
    else:
        pass

def input():
    showinfo("Snake","Déplace toi grâce aux flèches de ton clavier et recommence une partie en appuyant sur R")

def rules():
    showinfo("Snake","Tu contrôles un serpent qui avale de la nourriture pour grandir, et ce serpent meurt dès qu'il rentre en contact avec quoi que ce soit, y compris son corps. Bonne chance !")

def about():
    showinfo("Snake","Jeu développé par Gauthier GALON, Olivier NOWAK, Guilhem SIGAL, Antoine LACHAUX. EPSI SN1")


# Création de la fenêtre
root = Tk()

# Personnaliser la fenêtre
root.title("Snake")
root.iconbitmap("logo.ico")
root.resizable(False,False)

score = 0
direction = "down"

# Créer la frame
frame_title = Frame(root,background=FOREGROUND_COLOR)

# Ajouter des textes
title = Label(frame_title,text="Snake", font=("Consolas",40), background=FOREGROUND_COLOR, foreground=BACKGROUND_COLOR)
title.pack()

subtitle = Label(frame_title,text="Score : {}".format(score), font=("Consolas",20), background=FOREGROUND_COLOR, foreground=BACKGROUND_COLOR)
subtitle.pack()

frame_title.pack(expand=YES, pady=10)

canva = Canvas(root, background=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canva.pack()

# Créer une barre de menu
bar_menu = Menu(root)
help_menu = Menu(bar_menu, tearoff=0)
help_menu.add_command(label="Règles", command=rules)
help_menu.add_command(label="Touches", command=input)
help_menu.add_command(label="À Propos", command=about)
help_menu.add_command(label="Quitter", command=quit)


bar_menu.add_cascade(label="Aide", menu=help_menu)
root.config(menu=bar_menu)

# Créer la frame
frame_button = Frame(root,background=BACKGROUND_COLOR)
restart = Button(frame_button, text="Recommencer", font="Consolas", background=SNAKE_COLOR, foreground=BACKGROUND_COLOR,command=restart_game)
restart.pack()
frame_button.pack(side=BOTTOM,pady=10)


# Créer le jeu
snake = Snake()
food = Food()
lose = False
turn(snake,food)

root.bind('<Up>', lambda event: change_direction('up'))
root.bind('<Down>', lambda event: change_direction('down'))
root.bind('<Left>', lambda event: change_direction('left'))
root.bind('<Right>', lambda event: change_direction('right'))
root.bind('r', lambda event:restart_game())

# Afficher la fenêtre
root.mainloop()