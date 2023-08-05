from typing import List, Tuple
import math


class V2:
    # Vector 2 class
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @classmethod
    def ZERO(cls):
        return V2(0, 0)

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


def line2dIntersec(l1 : Tuple[V2, V2], l2: Tuple[V2, V2]):

    diff1 = l1[0] - l1[1]
    diff2 = l2[0] - l2[1]
    
    dx = V2(diff1.x, diff2.x)
    dy = V2(diff1.y, diff2.y)

    def det(a: V2, b: V2):
        return a.x * b.y - a.y * b.x
    
    div = det(dx, dy)
    
    if div==0:
        return None
    
    d = V2(det(*l1), det(*l2))
    x = det(d, dx) / div
    y = det(d, dy) / div

    return V2(x, y)



if __name__ =='__main__':

    l1 = (V2(0, 0), V2(1, 0))
    l2 = (V2(0, 0.5), V2(1, -0.5))

    print(line2dIntersec(l1, l2))