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
Copyright 2020 - Present Aaron Ma.
All Rights Reserved.

Licensed under the MIT License

Helper file for testing if hardware has no radiation.
"""
import time
from . import spec_ram

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
    test_add_3_7x          = test_add_3_7() == 10
    test_divide_360_6x     = test_divide_360_6() == 60
    test_multiply_6_90x    = test_multiply_6_90() == 540
    test_subtract_252_464x = test_subtract_252_464() == -210
    test_wrong_valuex      = test_wrong_value() == 80
    tests = (test_add_3_7x, test_divide_360_6x, test_multiply_6_90x, test_subtract_252_464x, test_wrong_valuex)
    correct = (True, True, True, True, False)
    if correct == tests:
        print("Yay! Your hardware currently has no radiation.")
        ctime = time.ctime()
        print("Last checked: {}".format(ctime))
        spec_ram.append(ctime)
        lc = input("Would you like to see all the last checked time? (Y/n)")
        
        if lc != 'Y' or 'y':
            # @TODO(aaronhma or rohan): UPDATE
            print()
        
        else:
            pass
        
    else:
        raise Exception("Your hardware has radiation!")
    
test()