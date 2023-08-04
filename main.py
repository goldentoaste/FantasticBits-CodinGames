import sys, math


#### Consts ####

LEFT = 0  # need to score right
RIGHT = 1  # own goal is on right side, need to score left
SIDE = LEFT  # to be init later in main
#### End Consts ####


class V2:
    # Vector 2 class

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f"V2({self.x}, {self.y})"

    def __add__(self, target: "V2"):
        return V2(self.x + target.x, self.y + target.y)

    def __mul__(self, target: int):
        return V2(self.x * target, self.y * target)

    def __sub__(self, target: "V2") -> "V2":
        return self + (-1 * target)

    def __div__(self, target: int) -> "V2":
        return self * (1 / target)

    def dot(self, target: "V2"):
        """Dot product of this vector and another"""
        return self.x * target.x + self.y + target.y

    def mag(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalized(self) -> "V2":
        return self / self.mag()

    def angleTo(self, target: "V2") -> float:
        """Calc for the smaller vector between the 2 vectors, in radians"""
        return math.acos(self.normalized().dot(target.normalized()))


class Entity:
    def __init__(self, eid: str, pos: V2, vel: V2):
        self.id = eid
        self.pos = pos
        self.vel = vel
        
    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y

    @property
    def vx(self):
        return self.vel.x

    @property
    def vy(self):
        return self.vel.y


    def __str__(self):
        return f"Entity({self.id}), pos:{self.pos}, vel: {self.vel}"
    
    def currentHeading(self)->V2:
        '''
        returns the position this object will end up at assuming no velocity changes
        '''
        
        return self.pos + self.vel
    
    def calcInterceptCourse(self, target: 'Entity', maxThrust : int):

        '''
        target: other entity this one will try to intercept.
        maxThrust: the *max* magnitude this obj can accelerate by in 1 turn.
        
        returns the expected point of interception and max thrust needed to intercept.
        Use max thrust if interception not possible in 1 frame, 
        but, if possible, calc the exact needed velocity change
        '''
        
        
        
        
        return target.currentHeading(), maxThrust
        
        
        
        
        
    
if __name__ == "__main__":
    SIDE = int(input())  # should be either left or right
    pass
