import math

from Vec3 import Point3, Vec3
from Ray import Ray
from RandomVector import random_in_unit_disk


class Camera:
    def __init__(self, look_from: Point3, look_at: Point3, vup: Vec3, vfov: float, aspect_ratio: float, aperture: float, focus_dist: float):
        theta = vfov * math.pi / 180
        h = math.tan(theta / 2)
        self.aspect_ratio = aspect_ratio
        viewport_height = 2.0 * h
        viewport_width = self.aspect_ratio * viewport_height

        self.w = look_from.sub(look_at).normalize()
        self.u = vup.cross(self.w).normalize()
        self.v = self.w.cross(self.u)

        self.origin = look_from
        self.horizontal = self.u.mult(viewport_width * focus_dist)
        self.vertical = self.v.mult(viewport_height * focus_dist)
        self.lower_left_corner = self.origin.sub(self.horizontal.div(2)).sub(self.vertical.div(2)).sub(self.w.mult(focus_dist))

        self.lens_radius = aperture / 2

    def get_ray(self, s: float, t: float) -> Ray:
        rd = random_in_unit_disk().mult(self.lens_radius)
        offset = self.u.mult(rd.x).add(self.v.mult(rd.y))

        return Ray(self.origin.add(offset),
                   self.lower_left_corner.add(self.horizontal.mult(s)).add(self.vertical.mult(t)).sub(self.origin).sub(offset))
