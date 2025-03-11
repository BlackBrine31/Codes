import turtle as t 
from random import randint

wn= t.Screen()
wn.title("Turtle Race")
wn.bgcolor("green")
t.penup()
t.setpos(-100,200)
t.pendown()
t.color("white")
t.write("TURTLE RACE",font=("Arial",24,"bold"))
t.penup()

t.setpos(200,110)
t.color("black")
t.pendown()
t.right(90)
t.forward(150)
t.penup()
t.setpos(-500,-200)

t.pendown()
t.left(90)
t.color("brown")
t.begin_fill()
for i in range(2):
    t.forward(1000)
    t.right(90)
    t.forward(1000)
    t.right(90)
t.penup()
t.end_fill()

t1=t.Turtle()
t1.speed(0)
t1.color("orange")
t1.shape("turtle")
t1.penup()
t1.goto(-200,100)
t1.pendown()

t2=t.Turtle()
t2.speed(0)
t2.color("red")
t2.shape("turtle")
t2.penup()
t2.goto(-200,70)
t2.pendown()

t3=t.Turtle()
t3.speed(0)
t3.color("blue")
t3.shape("turtle")
t3.penup()
t3.goto(-200,40)
t3.pendown()

t4=t.Turtle()
t4.speed(0)
t4.color("black")
t4.shape("turtle")
t4.penup()
t4.goto(-200,10)
t4.pendown()
a=[t1.pos()[0],t2.pos()[0],t3.pos()[0],t4.pos()[0]]
b=True
while b:
    for i in a:
        if i<200:
            continue
        else:
            break
    t1.forward(randint(1, 6))
    t2.forward(randint(1, 6))
    t3.forward(randint(1, 6))
    t4.forward(randint(1, 6))
    a=[t1.pos()[0],t2.pos()[0],t3.pos()[0],t4.pos()[0]]
if (t1.pos())[0]>200:
    t.setpos(0,0)
    t.write("T1 WINS",font=("Arial",50,"bold"))
elif (t2.pos())[0]>200:
    t.setpos(20,0)
    t.write("T2 WINS",font=("Arial",50,"bold"))
elif (t3.pos())[0]>200:
    t.setpos(40,0)
    t.write("T3 WINS",font=("Arial",50,"bold"))
elif (t4.pos())[0]>200:
    t.setpos(60,0)
    t.write("T4 WINS",font=("Arial",50,"bold"))
t.done()
