import os
import random
import sys
import math
from Vec3 import Color, Point3, Vec3
from Ray import Ray
from Hittable import HittableList, HitRecord
from Sphere import Sphere
from Camera import Camera
from GeometryUtil import constrain


def hit_sphere(center: Point3, radius: float, r: Ray) -> float:
    oc = r.origin.sub(center)
    a = r.direction.mag_sq()
    half_b = oc.dot(r.direction)
    c = oc.mag_sq() - radius*radius
    discriminant = half_b*half_b - a*c
    if discriminant < 0:
        return -1.0
    else:
        return (-half_b - math.sqrt(discriminant)) / a


def ray_color(r: Ray, world: HittableList):
    hit_or_not, rec = world.hit(r, 0, float('inf'))
    if hit_or_not:
        return rec.normal.add(Color(1, 1, 1)).mult(0.5)
    unit_direction = r.direction.normalize()
    t = 0.5 * (unit_direction.y + 1.0)
    return Color(1.0, 1.0, 1.0).mult(1.0 - t).add(Color(0.5, 0.7, 1.0).mult(t))


def write_color(out, pixel_color: Color, samples_per_pixel: int):
    r = pixel_color.x
    g = pixel_color.y
    b = pixel_color.z

    scale = 1.0 / samples_per_pixel
    r *= scale
    g *= scale
    b *= scale

    out.write(f'{int(256 * constrain(r, 0, 0.999))} {int(256 * constrain(g, 0, 0.999))} {int(256 * constrain(b, 0, 0.999))}\n')


if __name__ == '__main__':
    filename = 's7_1.ppm'

    # Image
    aspect_ratio = 16.0 / 9.0
    image_width: int = 400
    image_height: int = int(image_width / aspect_ratio)
    samples_per_pixel = 100

    # World
    world = HittableList([])
    world.add(Sphere(Point3(0, 0, -1), 0.5))
    world.add(Sphere(Point3(0, -100.5, -1), 100))

    # Camera
    cam = Camera()

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
                    pixel_color = pixel_color.add(ray_color(r, world))
                write_color(f, pixel_color, samples_per_pixel)
        print('\nDone.\n', file=sys.stderr)

    os.system(f'open -a preview {filename}')
