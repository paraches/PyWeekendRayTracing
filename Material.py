from abc import ABC, abstractmethod
from Ray import Ray
from Hittable import HitRecord
from Vec3 import Color
from RandomVector import random_unit_vector


class Material(ABC):
    @abstractmethod
    def scatter(self, r_in: Ray, rec: HitRecord) -> (bool, HitRecord, Color, Ray):
        pass


class Lambertian(Material):
    def __init__(self, albedo: Color):
        self.albedo = albedo

    def scatter(self, r_in: Ray, rec: HitRecord) -> (bool, HitRecord, Color, Ray):
        scatter_direction = rec.normal.add(random_unit_vector())

        if scatter_direction.near_zero():
            scatter_direction = rec.normal

        scattered = Ray(rec.p, scatter_direction)
        attenuation = self.albedo
        return True, rec, attenuation, scattered


class Metal(Material):
    def __init__(self, albedo: Color):
        self.albedo = albedo

    def scatter(self, r_in: Ray, rec: HitRecord) -> (bool, HitRecord, Color, Ray):
        reflected = r_in.direction.normalize().reflect(rec.normal)
        scattered = Ray(rec.p, reflected)
        attenuation = self.albedo
        return scattered.direction.dot(rec.normal) > 0, rec, attenuation, scattered

