# **BottleFlip**
Trying to simulate de bottleflip chalenge using Pygame!. Created on May 15

## **How to use?**
- *Left button* to add torque on the arm in the clockwise direction
- *Right button* to add torque on the arm in the anti clockwise direction
- *Space* to drop the bottle
- *b button* to get another bottle

## **How does it work?**
This program uses *pygame* and *math* libraries. Work with 4 classes:
1. *Space*. It takes information about the size of screen in pixels, the color of the background. Methods:
    - *update*. To fill the screen with a color.
2. *Time*. Counts the time and defines the delta time used for physics
    - *update*. To add delta time to the actual time.
3. *Arm*. It is the arm xd.
    - *unhold*. To give physics propirties to the bottle before trowing it
    - *update*. To calculate the inertia (because it can be diferent if it's holding the bottle), angular aceleration, angular velocity, angle and call the draw method.
    - *draw*. To transform the position vector to other vector that represents the pixels and use this last vector to draw the arm.
4. *Bottle*. The star object, it will follow the hand of the arm and will fly when it's not holded.
    - *update_by_arm* This method is used by the arm to give physics propierties to the bottle while the arm holds it. Also calls the draw_holding function.
    - *update* To calculate physics propierties (torque, inertia, angular aceleration, angular velocity, angle, position)  and to call the draw_not_holding function.
    - *draw_not_holding*. Draw the image in the correct position and the correct angle. The pivot is it's center.
    - *draw_holding*. Draw the image in the correct position and the correct angle. It is diferent method because the pivot of the angle is the arm.
    
## **Files**
The files needed by the program are only the bottle.png and Hand.png files. There is also a svg file where I created the two png files using Ikcscape editor.


## **Math Used**
The next list can representate the math topics used in the creation of the program:
- Distant between two points 2D.
- Diferential ecuations.
- Trigonometry.
- Vector's operations.
- Lineal transformations to vectors.

## **Physic Used**
The next list can representate the physic topics used in the creation of the program:
- Uniform rectilinear motion
- Uniformly Accelerated Rectilinear Motion
- Angular motion
- Inertia
- Torque