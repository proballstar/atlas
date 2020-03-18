#Gui
import turtle
import random

rohan = turtle.Pen()
num = random.randint(1,100)
colorlist = ["red","orange","yellow","green","blue","purple"]

def forward(num):
    forward(num,colorlist)
    rohan.forward(num)
    rohan.pencolor(random.choice(colorlist))
                   
def right(num,colorlist):
    rohan.right(num)
    rohan.pencolor(random.choice(colorlist))
    
def left(num,colorlist):
    rohan.left(num)
    rohan.pencolor(random.choice(colorlist))
    
def backward(num,colorlist):
    rohan.backward(num)
    rohan.pencolor(random.choice(colorlist))

#create a screen
screen = turtle.Screen()
#tell screen to listen to the keystrokes/clicks
screen.listen()
#tie the keys to functions
screen.onkey(forward,'Up')
screen.onkey(nackward,'Down')
screen.onkey(right,'Right')
screen.onkey(left,'Left')

del rohan, num, colorlist, screen