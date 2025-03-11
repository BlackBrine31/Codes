import turtle as t
t.setpos(10,200)
def draw_hexagon(size):
    for j in range(6):
        t.forward(size)
        t.right(60)
t.speed(0)  
t.bgcolor("black")
t.pencolor("cyan")  
size = 100
increment = -2

for i in range(100): 
    draw_hexagon(size)
    size += increment 

t.right(90)
size = 100
for i in range(100): 
    draw_hexagon(size)
    size += increment 
t.hideturtle()
t.done()
