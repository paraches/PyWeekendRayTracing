import os
import sys
from Vec3 import Color


if __name__ == '__main__':
    filename = 's3_1.ppm'

    # Image

    image_width = 256
    image_height = 256

    # Render
    with open(filename, 'w') as f:
        f.write(f'P3\n{image_width} {image_height}\n255\n')

        for j in reversed(range(image_height)):
            print(f'Scanlines remaining: {j}', file=sys.stderr)
            for i in range(image_width):
                pixel_color = Color(i / (image_width - 1), j / (image_height - 1), 0.25)
                pixel_color.write_color(f)
        print('\nDone.\n', file=sys.stderr)

    os.system(f'open -a preview {filename}')
