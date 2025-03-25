import turtle as t
import random as r

# make the screen
wn = t.Screen()
wn.title("Turtle")
wn.bgcolor("lightblue")
wn.setup(width=600,height=600)

# player
player = t.Turtle()
player.shape("turtle")
player.color("#192011")
player.speed(0)





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
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
