import turtle
import skyforce
    

def init():
    rohan = turtle.Pen()
def goto(x,y):
    rohan.penup()
    rohan.goto(x,y)
    rohan.pendown()
def square(s):
    for i in range(4):
        rohan.forward(s)
        rohan.right(90)
def rectangle(l,w):
    for i in range(2):
        rohan.forward(l)
        rohan.right(90)
        rohan.forward(w)
        rohan.right(90)
def circle(r):
    rohan.circle(r)
def write(w):
    rohan.write(w)
def shape(sides,size):
    for i in range(sides):
        rohan.forward(size)
        rohan.right(360/sides)
def part_circle(r,d):
    rohan.circle(r,d)
def left(degree):
    rohan.left(degree)
def right(degree):
    rohan.right(degree)
def diag(d):
    rohan.setheading(d)
def up(l):
    rohan.forward(l)
def r():
    left(90)
    up(10)
    part_circle(10,180)
    diag(45)
def f():
    up(10)
    right(90)
    up(5)
    goto(0,0)
    up(5)
    right(90)
    up(5)
    goto(7,7)
    
    
rohan = turtle.Pen()
