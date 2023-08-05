import sys, math
from typing import List, Dict, Iterable

#### Consts ####

LEFT = 0  # need to score right
RIGHT = 1  # own goal is on right side, need to score left
SIDE = LEFT  # to be init later in main

NAVMODE_THRESHOLD = 1000
# field/coords can be at most 16000 x 7500
W = 16000
H = 7500


#### End Consts ####

### --- ###

#### Game Vars ####


allies: Dict[int, "Wizard"] = {}
opponents: Dict[int, "Wizard"] = {}
sniffles: Dict[int, "Sniffle"] = {}

gameTime = 0  # up to 200, in turns

allieScore = 0
allieMagic = 0
opponentScore = 0
opponentMagic = 0

allieGoal = (0, 0)  # 2 point representing allie goal
opponentGoal = (0, 0)  # point for opponent goal

#### End Game Vars####


def firstNot(target, iterable: Iterable):
    for item in iterable:
        if item != target:
            return item
    return None


class V2:
    # Vector 2 class
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @classmethod
    def ZERO(cls):
        return V2(0,0)

    def __str__(self):
        return f"V2({self.x}, {self.y})"

    def __add__(self, target: "V2"):
        return V2(self.x + target.x, self.y + target.y)

    def __mul__(self, target: int):
        return V2(self.x * target, self.y * target)

    def __rmul__(self, target: int):
        return self.__mul__(target)

    def __sub__(self, target: "V2") -> "V2":
        return self + (-1 * target)

    def __truediv__(self, target: int) -> "V2":
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

    def distTo(self, target: "V2"):
        return (target - self).mag()

    @classmethod
    def avg(cls, vectors: List["V2"]) -> "V2":
        return sum(vectors, start=V2.ZERO()) / len(vectors)



#### init ####
SIDE = int(input())  # which side are we playing on

allieGoal = (V2(0, 1750), V2(0, 5750))  # assume we are left side
opponentGoal = (V2(16000, 1750), V2(16000, 5750))

# swap if right side
if SIDE:
    allieGoal, opponentGoal = opponentGoal, allieGoal

#### end init ####


class Entity:
    def __init__(self, eid: str, pos: V2, vel: V2):
        self.id = eid
        self.pos = pos
        self.vel = vel
        self.type = "undefined"

    def update(self, pos: V2, vel: V2):
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

    def distTo(self, target:'Entity'):
        return self.pos.distTo(target.pos)

    def currentHeading(self) -> V2:
        """
        returns the position this object will end up at assuming no velocity changes
        """

        return self.pos + self.vel

    def calcChaseCourse(self, target: "Entity", maxThrust: int):
        """
        target: other entity this one will try to intercept.
        maxThrust: the *max* magnitude this obj can accelerate by in 1 turn.

        Note this only accounts for 1 time step, should be used to gain marginal advantage in close range only

        returns the expected point of interception and max thrust needed to intercept.
        Use max thrust if interception not possible in 1 frame,
        but, if possible, calc the exact needed velocity change
        """

        # err
        targetPos = target.currentHeading()

        # error is much we need to correct by
        error = targetPos - self.pos - self.vel

        # solve for thrust needed in the direction of targetPos
        # thrust cannot exceed 'maxThrust'
        thrust = min(maxThrust, error.mag())

        return target.currentHeading(), thrust

    def calcInterceptCourse(self, target: "Entity", maxThrust: int):
        """
        target: other entity this one will try to intercept.
        maxThrust: the *max* magnitude this obj can accelerate by in 1 turn.


        Note: this is meant to calc intercept for longer distance.
        The algo is simple and has errors, but should diminish as we approach target. 

        returns the expected point of interception and max thrust needed to intercept.
        Use max thrust if interception not possible in 1 frame,
        but, if possible, calc the exact needed velocity change
        """

    

        ### stack overflow /better version?
        # https://gamedev.stackexchange.com/a/28312

        # time it must for self to travel the straight line distance
        distTime = target.pos.distTo(self.pos) / maxThrust

        # where the target will be at after ^ time passed
        targetHeading = target.pos + target.vel * distTime

        # head to where target will be
        return targetHeading, maxThrust
        



class Sniffle(Entity):
    def __init__(self, eid: str, pos: V2, vel: V2, grabbed=False):
        super().__init__(eid, pos, vel)
        self.type = "sniffle"
        self.grabbed = grabbed
        self.targetted = None

    def update(self, pos: V2, vel: V2, grabbed=False):
        super().update(pos, vel)
        self.grabbed = bool(grabbed)


class Wizard(Entity):
    def __init__(self, eid: int, pos: V2, vel: V2, grabbed=False):
        super().__init__(eid, pos, vel)
        self.type = "wizard"
        self.grabbed = grabbed

    def update(self, pos: V2, vel: V2, grabbed: bool = False):
        super().update(pos, vel)
        self.grabbed = bool(grabbed)

    def play(
        self,
        allie: "Wizard",
        sniffles: Dict[int, Sniffle],
        opponents: Dict[int, "Wizard"],
    ):
        # logic for shooting
        if self.grabbed:
            goal = V2.avg(opponentGoal)
            print(f"THROW {int(goal.x)} {int(goal.y)} 500")
            return

        minSniffle = sniffles[list(sniffles.keys())[0]]
        d = 999999
        
        
        for s in sniffles.values():

            if s.targetted == self.id:
                s.targetted = None
            # TODO dont give up balls later
            if s.grabbed or s.targetted and s.targetted != self.id:
                continue

            dist = self.currentHeading().distTo(s.currentHeading())
            if dist < d:
                d = dist
                minSniffle = s
                
            
                    
        print([s.targetted for s in sniffles.values()], file=sys.stderr)
        
        if minSniffle:
            minSniffle.targetted = self.id
            print(f"minsniffle: {minSniffle.id} has been targetted by wizard #{self.id}",file=sys.stderr)
            direction, thrust = self.calcInterceptCourse(minSniffle, 150)
            print(f"MOVE {int(direction.x)} {int(direction.y)} {int(thrust)}")
            return


        # default behaviour

        

def move(dest:V2, thrust):
    print(f"MOVE {int(dest.x)} {int(dest.y)} {thrust}")


def moveTowards(source: Entity, target: Entity):
    dist = source.distTo(target)
    
    if dist < NAVMODE_THRESHOLD:
        # better for close range encouters
        dest,thrust = source.calcChaseCourse(target, 150)
    else:
        # this is more suitable for distant target
        dest, thrust = source.calcInterceptCourse(target, 150)
    
    move(dest, thrust)




def updateCycle():
    global allieScore, allieMagic, opponentScore, opponentMagic, sniffles

    # just following thier template
    allieScore, allieMagic = [int(i) for i in input().split()]
    opponentScore, opponentMagic = [int(i) for i in input().split()]

    entityCount = int(input())  # number of ents

    eids = set()
    for i in range(entityCount):
        # 1 entity per line
        vals = input().split()

        eid = int(vals[0])
        etype = vals[1]
        pos = V2(int(vals[2]), int(vals[3]))
        vel = V2(int(vals[4]), int(vals[5]))
        grabbed = bool(int(vals[6]))

        eids.add(eid)
        
        if etype == "WIZARD":
            try:
                allies[eid].update(pos, vel, grabbed)
            except KeyError:
                obj = Wizard(eid, pos, vel, grabbed)
                allies[eid] = obj

        elif etype == "OPPONENT_WIZARD":
            try:
                opponents[eid].update(pos, vel, grabbed)
            except KeyError:
                obj = Wizard(eid, pos, vel, grabbed)
                opponents[eid] = obj

        elif etype == "SNAFFLE":
            try:
                sniffles[eid].update(pos, vel, grabbed)
            except KeyError:
                obj = Sniffle(eid, pos, vel, grabbed)
                sniffles[eid] = obj
                
                
    sniffles = {k:v for k,v in sniffles.items() if k in eids}


if __name__ == "__main__":
    while True:
        updateCycle()
        for w in allies.values():
            w.play(allies[firstNot(w.id, allies)], sniffles, opponents)
