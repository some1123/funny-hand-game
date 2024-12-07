28.11 - started doing the project, 
due to python bugs it is separated into the class coding
file Project 2.py and the main-part.py file in google collab with the mediapipe part, 
if I try doing it in python it gets me an error:
ImportError: DLL load failed while importing _framework_bindings

2.12 - finally fixed my mediapipe
Made both files in one, the wall for some reason won't get filled, gray wall collider bugged out and logs don't clear

4.12 - fixed gray wall collider, added coins & death
Made difficulties that make walls spawn more or less often and gaps be larger or smaller

7.12 - finished the first version of the game
Bugs fixed:
 - difficulty affects gap size now, it bugged out
 - coins wont spawn out of your screen
 - everything now works for any camera with 640x480 and more (did not try for less)
 - the cheat strat when you take your hand out of cam view (it triggers the stop-updating-anything failsafe which I use for pausing the game) and put it back in behind a wall is fixed with a scary anticheat wall which eternally updates and instakills u
 - difficulties now use screen sections instead of pixels
