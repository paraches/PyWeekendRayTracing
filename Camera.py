import math

from Vec3 import Point3, Vec3
from Ray import Ray


class Camera:
    def __init__(self, look_from: Point3, look_at: Point3, vup: Vec3, vfov: float, aspect_ratio: float):
        theta = vfov * math.pi / 180
        h = math.tan(theta / 2)
        self.aspect_ratio = aspect_ratio
        viewport_height = 2.0 * h
        viewport_width = self.aspect_ratio * viewport_height

        w = look_from.sub(look_at).normalize()
        u = vup.cross(w).normalize()
        v = w.cross(u)

        self.origin = look_from
        self.horizontal = u.mult(viewport_width)
        self.vertical = v.mult(viewport_height)
        self.lower_left_corner = self.origin.sub(self.horizontal.div(2)).sub(self.vertical.div(2)).sub(w)

    def get_ray(self, s: float, t: float) -> Ray:
        return Ray(self.origin, self.lower_left_corner.add(self.horizontal.mult(s)).add(self.vertical.mult(t)).sub(self.origin))
