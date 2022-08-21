import random

from Vec3 import Vec3


def random_in_unit_disk() -> Vec3:
    while True:
        p = Vec3(random.uniform(-1, 1), random.uniform(-1, 1), 0)
        if p.mag_sq() >= 1:
            continue
        return p


def random_in_unit_sphere(min_range: float = -1, max_range: float = 1) -> Vec3:
    while True:
        p: Vec3 = Vec3.random_ranged(min_range, max_range)
        if p.mag_sq() >= 1:
            continue
        return p


def random_unit_vector() -> Vec3:
    return random_in_unit_sphere().normalize()


def random_in_hemisphere(normal: Vec3) -> Vec3:
    in_unit_sphere = random_in_unit_sphere()
    if in_unit_sphere.dot(normal) > 0.0:
        return in_unit_sphere
    else:
        return in_unit_sphere.reverse()
