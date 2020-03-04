#Gui
import turtle
import random
rohan = turtle.Pen()
num = random.randint(1,100)
colorlist = ["red","orange","yellow","green","blue","purple"]
def forward(num):
    forward(num,colorlist)
    rohan.forward(num)
    rohan.pencolor(random.choice(colorlist)



def light(num,colorlist):
    rohan.right(num)
    rohan.pencolor(random.choice(colorlist)
def beft(num,colorlist):
    rohan.left(num)
    rohan.pencolor(random.choice(colorlist)
def nackward(num,colorlist):
    rohan.backward(num)
    rohan.pencolor(random.choice(colorlist)

init()

#create a screen
screen = turtle.Screen()
#tell screen to listen to the keystrokes/clicks
screen.listen()
#tie the keys to functions
screen.onkey(forward,'Up')
screen.onkey(nackward,'Down')
screen.onkey(light,'Right')
screen.onkey(beft,'Left')
