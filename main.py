import datetime
import math
import time
import os
import random
import sys
from Vec3 import Color, Point3, Vec3
from Ray import Ray
from Hittable import HittableList, Hittable
from Sphere import Sphere
from Camera import Camera
from GeometryUtil import constrain
from Material import Lambertian, Metal, Dielectric


def ray_color(r: Ray, world: Hittable, depth: int):
    if depth <= 0:
        return Color()

    hit_or_not, rec = world.hit(r, 0.001, float('inf'))
    if hit_or_not:
        result, rec, attenuation, scattered = rec.material.scatter(r, rec)
        if result:
            return attenuation.asterisk(ray_color(scattered, world, depth-1))
        return Color()

    unit_direction = r.direction.normalize()
    t = 0.5 * (unit_direction.y + 1.0)
    return Color(1.0, 1.0, 1.0).mult(1.0 - t).add(Color(0.5, 0.7, 1.0).mult(t))


def write_color(out, pixel_color: Color, samples_per_pixel: int):
    r = pixel_color.x
    g = pixel_color.y
    b = pixel_color.z

    scale = 1.0 / samples_per_pixel
    r = math.sqrt(scale * r)
    g = math.sqrt(scale * g)
    b = math.sqrt(scale * b)

    out.write(f'{int(256 * constrain(r, 0, 0.999))} {int(256 * constrain(g, 0, 0.999))} {int(256 * constrain(b, 0, 0.999))}\n')


def random_scene() -> HittableList:
    world = HittableList([])

    ground_material = Lambertian(Color(0.5, 0.5, 0.5))
    world.add(Sphere(Point3(0, -1000, 0), 1000, ground_material))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random.random()
            center = Point3(a + 0.9 * random.random(), 0.2, b + 0.9 * random.random())

            if center.sub(Point3(4, 0.2, 0)).mag() > 0.9:
                if choose_mat < 0.8:
                    albedo = Color.random().asterisk(Color.random())
                    sphere_material = Lambertian(albedo)
                    world.add(Sphere(center, 0.2, sphere_material))
                elif choose_mat < 0.95:
                    albedo = Color.random_ranged(0.5, 1)
                    fuzz = random.uniform(0, 0.5)
                    sphere_material = Metal(albedo, fuzz)
                    world.add(Sphere(center, 0.2, sphere_material))
                else:
                    sphere_material = Dielectric(1.5)
                    world.add(Sphere(center, 0.2, sphere_material))

    material1 = Dielectric(1.5)
    world.add(Sphere(Point3(0, 1, 0), 1.0, material1))

    material2 = Lambertian(Color(0.4, 0.2, 0.1))
    world.add(Sphere(Point3(-4, 1, 0), 1.0, material2))

    material3 = Metal(Color(0.7, 0.6, 0.5), 0.0)
    world.add(Sphere(Point3(4, 1, 0), 1.0, material3))

    return world


if __name__ == '__main__':
    start = time.time()

    filename = 's13_1.ppm'

    # Image
    aspect_ratio = 3.0 / 2.0
    image_width: int = 600     # 1200
    image_height: int = int(image_width / aspect_ratio)
    samples_per_pixel = 100     # 500
    max_depth = 50

    # World
    world = random_scene()

    # Camera
    look_from = Point3(13, 2, 3)
    look_at = Point3(0, 0, 0)
    vup = Vec3(0, 1, 0)
    dist_to_focus = 10.0
    aperture = 0.1

    cam = Camera(look_from, look_at, vup, 20, aspect_ratio, aperture, dist_to_focus)

    # Render
    with open(filename, 'w') as f:
        f.write(f'P3\n{image_width} {image_height}\n255\n')

        for j in reversed(range(image_height)):
            print(f'Scanlines remaining: {j}', file=sys.stderr)
            for i in range(image_width):
                pixel_color = Color()
                for s in range(samples_per_pixel):
                    u = (float(i) + random.random()) / (image_width - 1)
                    v = (float(j) + random.random()) / (image_height - 1)
                    r = cam.get_ray(u, v)
                    pixel_color = pixel_color.add(ray_color(r, world, max_depth))
                write_color(f, pixel_color, samples_per_pixel)
        print('\nDone.\n', file=sys.stderr)

    os.system(f'open -a preview {filename}')

    elapsed_time = time.time() - start
    time_delta = datetime.timedelta(seconds=elapsed_time)
    print(time_delta)
