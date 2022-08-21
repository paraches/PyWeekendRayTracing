import math

from Vec3 import Point3, Vec3
from Ray import Ray


class Camera:
    def __init__(self, vfov: float, aspect_ratio):
        self.theta = vfov * math.pi / 180
        h = math.tan(self.theta / 2)
        self.aspect_ratio = aspect_ratio
        viewport_height = 2.0 * h
        viewport_width = self.aspect_ratio * viewport_height

        self.focal_length = 1.0

        self.origin = Point3(0, 0, 0)
        self.horizontal = Vec3(viewport_width, 0, 0)
        self.vertical = Vec3(0, viewport_height, 0)
        self.lower_left_corner = self.origin.sub(self.horizontal.div(2)).sub(self.vertical.div(2)).sub(Vec3(0, 0, self.focal_length))

    def get_ray(self, u: float, v: float) -> Ray:
        return Ray(self.origin, self.lower_left_corner.add(self.horizontal.mult(u)).add(self.vertical.mult(v)).sub(self.origin))
