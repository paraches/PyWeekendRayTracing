import math

import Ray
from Hittable import Hittable, HitRecord
from Vec3 import Point3


class Sphere(Hittable):
    def __init__(self, center: Point3, radius: float, material):
        self.center = center
        self.radius = radius
        self.material = material

    def hit(self, r: Ray.Ray, t_min: float = 0, t_max: float = float('inf')) -> (bool, HitRecord):
        oc = r.origin.sub(self.center)
        a = r.direction.mag_sq()
        half_b = oc.dot(r.direction)
        c = oc.mag_sq() - self.radius*self.radius

        discriminant = half_b*half_b - a*c
        if discriminant < 0:
            return False, None
        sqrtd = math.sqrt(discriminant)

        # Find the nearest root that lies in the acceptable range.
        root = (-half_b - sqrtd) / a
        if root < t_min or t_max < root:
            root = (-half_b + sqrtd) / a
            if root < t_min or t_max < root:
                return False, None

        p = r.at(root)
        normal = p.sub(self.center).div(self.radius)
        rec = HitRecord(p, normal, self.material, root)
        rec.set_face_normal(r, normal)
        return True, rec
