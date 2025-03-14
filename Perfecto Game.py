import turtle
import random

score = 0

# make the screen
win = turtle.Screen()
win.title("Find the Coin")
win.bgcolor("lightblue")
win.setup(width=600, height=600)
#score turtle
text_turtle = turtle.Turtle()
text_turtle.hideturtle()  # Hide the turtle cursor
text_turtle.penup()

# Player turtle
player = turtle.Turtle()
player.shape("turtle")
player.color("green")
player.penup()
player.speed(0)



# Food object
food = turtle.Turtle()
def change_turtle_size(stretch_wid, stretch_len):
    food.turtlesize(stretch_wid, stretch_len)
def change_player(stretch_wid, stretch_len):
    player.turtlesize(stretch_wid, stretch_len)
# Set different sizes
change_turtle_size(0.5, 0.5)
change_player(0.8, 0.8)

food.shape("circle")
food.color("red")
food.penup()
food.speed(0)
food.goto(random.randint(-250, 250), random.randint(-250, 250))

def show_variable(value):
    text_turtle.clear()  # Clear previous text
    text_turtle.goto(-100, 200)  # Set position
    text_turtle.write(f"Score: {value}", font=("Arial", 16, "bold"))

# Show the initial score
show_variable(score)

# Example: Update score after 2 seconds
def update_score():
    global score
    show_variable(score)
    win.ontimer(update_score, 500)  # Update every 0.5 seconds

# Start updating the score
win.ontimer(update_score, 500)
# Player Movement
def go_up():
    y = player.ycor()
    if y < 280:
        player.sety(y + 20)
    player.setheading(90)

def go_down():
    y = player.ycor()
    if y > -280:
        player.sety(y - 20)
    player.setheading(270)

def go_left():
    x = player.xcor()
    if x > -280:
        player.setx(x - 20)
    player.setheading(180)
def go_right():
    x = player.xcor()
    if x < 280:
        player.setx(x + 20)
    player.setheading(0)
# Keyboard movement
win.listen()
win.onkey(go_up, "w")
win.onkey(go_down, "s")
win.onkey(go_left, "a")
win.onkey(go_right, "d")

# Game Loop
while True:
    # Updating the window
    win.update()
    
    # If player touches food
    if player.distance(food) < 15:
        food.goto(random.randint(-250, 250), random.randint(-250, 250))
        score+=1
        while player.distance(food) < 50:
            food.goto(random.randint(-250, 250), random.randint(-250, 250))
