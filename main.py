import os
import sys
from Vec3 import Color, Point3, Vec3
from Ray import Ray


def ray_color(r: Ray):
    unit_direction = r.direction.normalize()
    t = 0.5 * (unit_direction.y + 1.0)
    return Color(1.0, 1.0, 1.0).mult(1.0 - t).add(Color(0.5, 0.7, 1.0).mult(t))


if __name__ == '__main__':
    filename = 's4_1.ppm'

    # Image
    aspect_ratio = 16.0 / 9.0
    image_width: int = 400
    image_height: int = int(image_width / aspect_ratio)

    # Camera

    viewport_height = 2.0
    viewport_width = aspect_ratio * viewport_height
    focal_length = 1.0

    origin = Point3(0, 0, 0)
    horizontal = Vec3(viewport_width, 0, 0)
    vertical = Vec3(0, viewport_height, 0)
    lower_left_corner = origin.sub(horizontal.div(2)).sub(vertical.div(2)).sub(Vec3(0, 0, focal_length))

    # Render
    with open(filename, 'w') as f:
        f.write(f'P3\n{image_width} {image_height}\n255\n')

        for j in reversed(range(image_height)):
            print(f'Scanlines remaining: {j}', file=sys.stderr)
            for i in range(image_width):
                u = float(i) / (image_width - 1)
                v = float(j) / (image_height - 1)
                r = Ray(origin, lower_left_corner.add(horizontal.mult(u)).add(vertical.mult(v)).sub(origin))
                pixel_color = ray_color(r)
                pixel_color.write_color(f)
        print('\nDone.\n', file=sys.stderr)

    os.system(f'open -a preview {filename}')
