from abc import ABC, abstractmethod
from Vec3 import Point3, Vec3
from Ray import Ray


class HitRecord:
    def __init__(self, p: Point3, normal: Vec3, material, t: float, front_face: bool = False):
        self.p = p
        self.normal = normal
        self.material = material
        self.t = t
        self.front_face = front_face

    def set_face_normal(self, r: Ray, outward_normal: Vec3):
        self.front_face = r.direction.dot(outward_normal) < 0
        self.normal = outward_normal if self.front_face else outward_normal.reverse()


class Hittable(ABC):
    @abstractmethod
    def hit(self, r, t_min: float = 0, t_max: float = float('inf')) -> (bool, HitRecord):
        pass


class HittableList(Hittable):
    def __init__(self, hittable_list: [Hittable]):
        self.objects: [Hittable] = hittable_list

    def clear(self):
        self.objects = []

    def add(self, hittable_object: Hittable):
        self.objects.append(hittable_object)

    def hit(self, r, t_min: float = 0, t_max: float = float('inf')) -> (bool, HitRecord):
        hit_record = None
        hit_anything = False
        closest_so_far = t_max

        for hittable_object in self.objects:
            hit_or_not, temp_rec = hittable_object.hit(r, t_min, closest_so_far)
            if hit_or_not:
                hit_anything = True
                closest_so_far = temp_rec.t
                hit_record = temp_rec

        return hit_anything, hit_record
