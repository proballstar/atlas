"""
Project Skyforce -- Aaron Ma & Rohan Fernandes
Copyright 2020 - Present Aaron Ma & Rohan Fernandes

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import random as rand          # Random library
import datetime import datetime    # Datetime library
import time as current_time    # Time library
import math                    # Math library

# Functions
def user(msg):
    """
    Get the user's name.
    - input:
        - message to display
    """
    user = input("What is your name? ")
    print("Hello {}! {}".format(user, msg))

def timer(time):
    """
    A timer function.
    - input:
        - time of counting down
    """
    timer = int(timer)         # convert timer to an integer
    for i in range(timer):     # for loop
        print(timer)           # print
        current_time.sleep(1)  # wait
        timer -= 1             # countdown

def random(min_num, max_num):
    """
    Use a random number generator 
        - give a & b
    prints a random number
    """
    min_num = int(input("What is the minumum? "))  # min number
    max_num = int(input("What is the maximum? "))  # maximum number
    # select a random number between min - max
    num = rand.randint(min_num, max_num)
    print(num)  # print the random #

def floor(num):
    """
    Give a decimal and it will return the number floored
    """
    new_num = math.floor(num)
    print("rf", new_num)
    return new_num

def round(flt):
    """
    Rounds number up or down, depending ONLY on LAST digit
    """
    strflt = str(flt)
    newstrflt = strflt[-1:]
    intstrflt = int(newstrflt)
    if (intstrflt >= 5):
        newflt = floor(flt)
        newflt = newflt + 1
    else:
        newflt = floor(flt)
    print(newflt)

def calculator(a, operator, b):
    """
    A calculator function for basic  2 number calculations
    """
    if (operator == "*" or "multiply"):
        num = a*b
        print(num)
    elif (operator == "/" or "divide"):
        num = a/b
        print(num)
    elif (operator == "-" or "subract"):
        num = a - b
        print(num)
    elif (operator == "+" or "add"):
        num = a + b
        print(num)
    else:
        print("invalid")

# Progress Bar
def progress_bar(t):
    """Prints a progress bar that take t seconds to complete loading."""
    from time import sleep
    for i in range(1, 101):
        print("\r{:>6}% |{:<30}|".format(
            i, u"\u2588" * round(i // 3.333)), end='', flush=True)
        sleep(t/100)
    sleep(0.1)
    print("\n")

def err_raise(error, notes):
    if err_raise == "ValueError":
        raise ValueError(notes)
    elif err_raise == "TypeError":
        raise TypeError(notes)
    elif err_raise == "NotImplemented":
        raise NotImplementedError(Notes)

class Human():
    def __init__(self, f_name, l_name, age, status):
        self.f_name = f_name
        self.l_name = l_name
        self.status = status
        self.age = age

    def intro(self):
        print("Found person: {} {} who is {} years old and works as {} onboard.".format(
            f_name, l_name, age, status))

    def find_birth_year(self):
        year = datetime.now().year
        print(year - (self.age))

    def talk(self, expression):
        pass

    def status_check(self):
        if self.status == "administrator":
            pass
        elif self.status == "mission control":
            pass
        elif self.status == "commander":
            pass
        elif self.status == "astronaut":
            pass
        else:
            print("[ALERT] I've never seen anything like that before!")

    def change_access(self, new_status):
        old_status = self.status
        self.status = new_status
        print("Successfully changed permissions from {} to {}".format(
            old_status, self.status))
aaron = Human("Aaron", "Ma", 11, "administrator")
rohan = Human("Rohan", "Fernandes", 11, "administrator")
aaron.intro()
rohan.intro()