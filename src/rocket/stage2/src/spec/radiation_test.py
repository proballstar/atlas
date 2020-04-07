"""
       _______ _                _____ 
    /\|__   __| |        /\    / ____|
   /  \  | |  | |       /  \  | (___  
  / /\ \ | |  | |      / /\ \  \___ \ 
 / ____ \| |  | |____ / ____ \ ____) |
/_/    \_\_|  |______/_/    \_\_____/ 

This file is part of Atlas and Firebolt Space Agency.

Copyright 2017 - 2020 Firebolt, Inc,
Copyright 2017 - 2020 Firebolt Space Agency,
Copyright 2020 - Present Aaron Ma,
Copyright 2020 - Present Rohan Fernandes.
All Rights Reserved.

Licensed under the MIT License

Helper file for testing if hardware has no radiation.
"""
#
# MIT License
#
# Copyright (c) 2017 - 2020 Firebolt Space Agency,
# Copyright (c) 2017 - 2020 Firebolt, Inc,
# Copyright (C) 2020 - Present Aaron Ma,
# Copyright (c) 2020 - Present Rohan Fernandes.
# All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
try:
       import time

except ImportError:
       raise ImportError("Is Python installed correctly?")

try:
       from . import spec_ram

except ImportError:
       raise ImportError("Your version of Atlas is corrupt!")

# @TODO(aaronhma): Create generic functions for these
def add(x, y):
       """
       input:
              - x: int
              - y: int
       returns: int
       """
       return x + y

def subtract(x, y):
       return y - x

def multiply(x, y):
       return x * y

def divide(x, y):
       retrun y / x

def test_add_3_7():
    return 3 + 7

def test_divide_360_6():
    return 360 / 6

def test_multiply_6_90():
    return 6 * 90

def test_subtract_252_464():
    return 254 - 464

def test_wrong_value():
    return 34 + 45

def test():
    # Define 4 correct values
    test_add_3_7x          = test_add_3_7() == 10
    test_divide_360_6x     = test_divide_360_6() == 60
    test_multiply_6_90x    = test_multiply_6_90() == 540
    test_subtract_252_464x = test_subtract_252_464() == -210

    # Define 1 wrong value
    test_wrong_valuex      = test_wrong_value() == 80
    
    # Store the computer's output in a tuple
    tests = (test_add_3_7x, test_divide_360_6x, test_multiply_6_90x, test_subtract_252_464x, test_wrong_valuex)
       
    # Store the correct value in a tuple
    correct = (True, True, True, True, False)
    
    # All tests passed!
    if correct == tests:
        print("Yay! Your hardware currently has no radiation.")
        ctime = time.ctime()
        print("Last checked: {}".format(ctime))
        spec_ram.last_checked.append(ctime)
        lc = input("Would you like to see all the last checked time? (Y/n)")
              
        # User entered yes
        if lc != 'Y' or 'y':
            print(spec_ram.last_checked)
        
        # Anything else
        else:
            pass
    
    # Test failed
    else:
        raise Exception("Your hardware has radiation!")
    
#test()
