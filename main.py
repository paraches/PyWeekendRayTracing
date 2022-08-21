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


if __name__ == '__main__':
    start = time.time()

    filename = 's11_2_2.ppm'

    # Image
    aspect_ratio = 16.0 / 9.0
    image_width: int = 400
    image_height: int = int(image_width / aspect_ratio)
    samples_per_pixel = 100
    max_depth = 50

    # World
    world = HittableList([])

    material_ground = Lambertian(Color(0.8, 0.8, 0.0))
    material_center = Lambertian(Color(0.1, 0.2, 0.5))
    material_left = Dielectric(1.5)
    material_right = Metal(Color(0.8, 0.6, 0.2), 0.0)

    world.add(Sphere(Point3( 0.0, -100.5, -1.0), 100.0, material_ground))
    world.add(Sphere(Point3( 0.0,    0.0, -1.0),   0.5, material_center))
    world.add(Sphere(Point3(-1.0,    0.0, -1.0),   0.5, material_left))
    world.add(Sphere(Point3(-1.0,    0.0, -1.0), -0.45, material_left))
    world.add(Sphere(Point3( 1.0,    0.0, -1.0),   0.5, material_right))

    # Camera
    cam = Camera(Point3(-2, 2, 1), Point3(0, 0, -1), Vec3(0, 1, 0), 20, aspect_ratio)

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
