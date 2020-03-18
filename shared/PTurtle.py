#PROJECT PTURTLE -- ROHAN FERNANDES -- TURTLE FUNCTIONS ONLY
#Copyright 2020 - Present ROHAN FERNANDES
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files(the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#@NOTE: ONLY USE IF HAVE CONSENT FROM ROHAN FERNANDES 
#V 0.0.1 BETA PTURTLE -- MODIFY VERSION FOR PROJECT ATLAS: FAST, FUEL EFFICIENT, THE OFFICAL SPACE ROCKET OF THE FIREBOLT SPACE AGENCY (FSA)
from turtle import * #getting all functions from Turtle
import skyforce #import skyforce that is in shared folder

class VRTurtle:
    def __init__(self,hi):
        self.hi = hi
    def goto(self,x,y):
        hi.penup()
        hi.goto(x,y)
        hi.pendown()
    def goto_line(self,x,y):
        hi.goto(x,y)
    def square(self,s):
        for i in range(4):
            hi.forward(s)
            hi.right(90)
    def rectangle(self,l,w):
        for i in range(2):
            hi.forward(l)
            hi.right(90)
            hi.forward(w)
            hi.right(90)
    def circle(self,r):
        hi.circle(r)
    def write(self,w):
        hi.write(w)
    def shape(self,sides,size):
        for i in range(sides):
            hi.forward(size)
            hi.right(360/sides)
    def part_circle(self,r,d):
        hi.circle(r,d)
    def left(self,degree):
        hi.left(degree)
    def right(self,degree):
        hi.right(degree)
    def diag(self,d):
        hi.setheading(d)
    def up(self,l):
        hi.forward(l)
hi = Pen()
turtle = VRTurtle(hi)
turtle.rectangle()

del hi 
