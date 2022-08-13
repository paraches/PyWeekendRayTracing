import os


if __name__ == '__main__':
    filename = 's2_1.ppm'

    # Image

    image_width = 256
    image_height = 256

    # Render
    with open(filename, 'w') as f:
        f.write(f'P3\n{image_width} {image_height}\n255\n')

        for j in reversed(range(image_height)):
            for i in range(image_width):
                r = i / (image_width - 1)
                g = j / (image_height - 1)
                b = 0.25

                ir = int(255.999 * r)
                ig = int(255.999 * g)
                ib = int(255.999 * b)

                f.write(f'{ir} {ig} {ib}\n')

    os.system(f'open -a preview {filename}')
