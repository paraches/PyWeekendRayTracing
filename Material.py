from abc import ABC, abstractmethod
from Ray import Ray
from Hittable import HitRecord
from Vec3 import Color
from RandomVector import random_unit_vector, random_in_unit_sphere


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
    def __init__(self, albedo: Color, f: float):
        self.albedo = albedo
        self.fuzz = f if f < 1 else 1

    def scatter(self, r_in: Ray, rec: HitRecord) -> (bool, HitRecord, Color, Ray):
        reflected = r_in.direction.normalize().reflect(rec.normal)
        scattered = Ray(rec.p, reflected.add(random_in_unit_sphere().mult(self.fuzz)))
        attenuation = self.albedo
        return scattered.direction.dot(rec.normal) > 0, rec, attenuation, scattered


class Dielectric(Material):
    def __init__(self, index_of_refraction):
        self.ir = index_of_refraction

    def scatter(self, r_in: Ray, rec: HitRecord) -> (bool, HitRecord, Color, Ray):
        attenuation = Color(1.0, 1.0, 1.0)
        refraction_ratio = 1.0 / self.ir if rec.front_face else self.ir
        unit_direction = r_in.direction.normalize()
        refracted = unit_direction.refract(rec.normal, refraction_ratio)

        scattered = Ray(rec.p, refracted)
        return True, rec, attenuation, scattered
