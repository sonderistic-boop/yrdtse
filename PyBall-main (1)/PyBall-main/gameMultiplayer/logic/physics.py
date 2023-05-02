import pygame as pg
import gameMultiplayer.logic.collisions as collisions
#static value, if true then object will move, if false then object will not move

#given two objects, objects, with mass, velocity and restitution, 
#simulate a physics collision between them, and 
#return the new velocities of the objects after the collision
def objectCollision(obj1,obj2,normalVector = None):

    
    if normalVector is None:
        normalVector = ((obj2.position + pg.math.Vector2(obj2.w//2,obj2.h//2)) - (obj1.position + pg.math.Vector2(obj1.w//2,obj1.h//2))).normalize()
    

    
    relativeVelocity = obj2.velocity - obj1.velocity

    normalVelocity = relativeVelocity.dot(normalVector)


    
    if(normalVelocity > 0) and ((obj1.staticValue == True) and (obj2.staticValue == True)):
        return
    
    e = min(obj1.restitution,obj2.restitution)

    j = -(1+e) * normalVelocity / (obj1.inverseMass + obj2.inverseMass)

    impulse = normalVector * j

    if obj1.staticValue:
        obj1.velocity -= impulse * (obj1.inverseMass)
    if obj2.staticValue:
        obj2.velocity += impulse * (obj2.inverseMass)
    #floating_error(obj1,obj2,normalVector)




#obj1 gets kicked by obj2
def thrust(obj1,obj2):
    e = min(obj1.restitution,obj2.restitution)
    normalVector = ((obj2.position + pg.math.Vector2(obj2.w//2,obj2.h//2)) - (obj1.position + pg.math.Vector2(obj1.w//2,obj1.h//2))).normalize()
    obj1.velocity = normalVector * 6 *-(1+e)








def floating_error(obj1,obj2,normalVector):

    magnitude = normalVector.magnitude()
    if hasattr(obj2,"radius"):
        penetrationDepth = -(magnitude - obj1.radius - obj2.radius)
    else:
        penetrationDepth = -(magnitude - obj1.radius - obj2.w//2)
    slack = 0.2

    allowance = 0.01
  
    correction = max(penetrationDepth - slack, 0 ) / (obj1.inverseMass + obj2.inverseMass) * allowance * normalVector
    obj1.position -= obj1.inverseMass * correction
    obj2.position += obj2.inverseMass * correction





#given an object, and a wall, simulate a physics collision between them, and
#return the new velocity of the object after the collision






#simulate a physics collision between a ball and a rectangle, given the ball and the rectangle
#def circleRectanglePositionalCorrection(ball,rectangle):

