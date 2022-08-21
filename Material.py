import math
import random
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
        cos_theta = min(unit_direction.reverse().dot(rec.normal), 1.0)
        sin_theta = math.sqrt(1.0 - cos_theta*cos_theta)

        cannot_refract = refraction_ratio * sin_theta > 1.0
        if cannot_refract or Dielectric.reflectance(cos_theta, refraction_ratio) > random.random():
            direction = unit_direction.reflect(rec.normal)
        else:
            direction = unit_direction.refract(rec.normal, refraction_ratio)

        scattered = Ray(rec.p, direction)
        return True, rec, attenuation, scattered

    @staticmethod
    def reflectance(cosine: float, ref_idx: float) -> float:
        r0 = (1-ref_idx) / (1+ref_idx)
        r0 = r0*r0
        return r0 + (1-r0) * pow(1 - cosine, 5)
