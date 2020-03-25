#PROJECT PTURTLE -- ROHAN FERNANDES -- TURTLE FUNCTIONS ONLY
#Copyright 2020 - Present ROHAN FERNANDES
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files(the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from turtle import *

class Turtle:
    def __init__(self):
        self.hi = Pen()
    def goto(self,x,y):
        self.hi.penup()
        self.hi.goto(x,y)
        self.hi.pendown()
    def goto_line(self,x,y):
        self.hi.goto(x,y)
    def square(self,s):
        for i in range(4):
            self.hi.forward(s)
            self.hi.right(90)
    def rectangle(self,l,w):
        for i in range(2):
            self.hi.forward(l)
            self.hi.right(90)
            self.hi.forward(w)
            self.hi.right(90)
    def circle(self,r):
        self.hi.circle(r)
    def write(self,w):
        self.hi.write(w)
    def shape(self,sides,size):
        for i in range(sides):
            self.hi.forward(size)
            self.hi.right(360/sides)
    def semicircle(self,r,d):
        self.hi.circle(r,d)
    def left(self,degree):
        self.hi.left(degree)
    def right(self,degree):
        self.hi.right(degree)
    def diag(self,d):
        self.hi.setheading(d)
    def up(self,l):
        self.hi.forward(l)

turtle = Turtle()