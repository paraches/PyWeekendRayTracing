import math
import random
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

    def asterisk(self, other):  # '*'
        return PVector(self.x * other.x, self.y * other.y, self.z * other.z)

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

    def near_zero(self) -> bool:
        s = 1e-8
        return (abs(self.x) < s) and (abs(self.y) < s) and (abs(self.z) < s)

    def reflect(self, other):
        return self.sub(other.mult(self.dot(other)*2))

    def refract(self, other, etai_over_etat):
        cos_theta = min(self.reverse().dot(other), 1.0)
        r_out_perp = self.add(other.mult(cos_theta)).mult(etai_over_etat)
        r_out_parallel = other.mult(-math.sqrt(abs(1.0 - r_out_perp.mag_sq())))
        return r_out_perp.add(r_out_parallel)

    def write_color(self, out=sys.stdout):
        out.write(f'{int(255.999 * self.x)} {int(255.999 * self.y)} {int(255.999 * self.z)}\n')

    @staticmethod
    def random():
        # 0..<1
        return PVector(random.random(), random.random(), random.random())

    @staticmethod
    def random_ranged(min: float, max: float):
        # uniform -> min + (max-min) * random()
        return PVector(random.uniform(min, max), random.uniform(min, max), random.uniform(min, max))
