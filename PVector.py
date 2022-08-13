import math
import sys


class PVector:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f'[{self.x}, {self.y}, {self.z}]'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def add(self, other):
        return PVector(self.x + other.x, self.y + other.y, self.z + other.z)

    def sub(self, other):
        return PVector(self.x - other.x, self.y - other.y, self.z - other.z)

    def mult(self, other):
        return PVector(self.x * other, self.y * other, self.z * other)

    def div(self, other):
        return self.mult(1/other)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return PVector(self.y * other.z - self.z * other.y,
                       self.z * other.x - self.x * other.z,
                       self.x * other.y - self.y * other.x)

    def mag(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def mag_sq(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    def normalize(self):
        mag = self.mag()
        return PVector(self.x / mag, self.y / mag, self.z / mag)

    def copy(self):
        return PVector(self.x, self.y, self.z)

    def reverse(self):
        return PVector(-self.x, -self.y, -self.z)

    def write_color(self, out=sys.stdout):
        out.write(f'{int(255.999 * self.x)} {int(255.999 * self.y)} {int(255.999 * self.z)}\n')
