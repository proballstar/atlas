import itertools
import threading
import time
import sys

done = False
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        else:
            pass
        sys.stdout.write('\rLOADING ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    print("Done!")

def setup():
    """
    Copyright 2020 - Present Aaron Ma.
    """
    # @TODO(aaronhma): update
    developer = True
    utf = "UTF-8"
    supported_lang = ["en"]
    lang = supported_lang[-1]
    sep = "-"
    if developer != False:
        print("""
       _______ _                _____ 
    /\|__   __| |        /\    / ____|
   /  \  | |  | |       /  \  | (___  
  / /\ \ | |  | |      / /\ \  \___ \ 
 / ____ \| |  | |____ / ____ \ ____) |
/_/    \_\_|  |______/_/    \_\_____/ 

        Copyright 2020 - Present Aaron Ma.
        Guest starring Rohan Fernandes.
        \n
        STAGE 2 CONFIGURATION WIZARD
        \n\n
        /    ----------------------------------------    \\
          Let's choose the settings that's right for you.       
        \\    ----------------------------------------    /
        """)
        t = threading.Thread(target=animate)
        t.start()
        time.sleep(2)
        print("\n\nCalibrating language...")
        print("Language: {}{}{}\n".format(utf, "-", lang))
        # @TODO(aaronhma): Calibrate
        #print("\nCalibrating ")
        #time.sleep(2)
    else:
        pass

setup()
done = True