from PIL import ImageFont, ImageDraw, Image
import numpy as np
import random
import cv2
import glob
import string

fonts_path = r"C:\Users\sjerz\Downloads\ft"
fonts = glob.glob(fonts_path + "/*")


def generate(text, k, path):
    size = 20
    length = 3
    img = np.zeros(((size * 2) + 5, length * size, 3), np.uint8)

    r_bg = random.choice([210, 250])
    g_bg = random.choice([210, 250])
    b_bg = 210

    img[:, :, 2] += r_bg
    img[:, :, 1] += g_bg
    img[:, :, 0] += b_bg

    img_pil = Image.fromarray(img)

    font = ImageFont.truetype(random.choice(fonts), size)
    draw = ImageDraw.Draw(img_pil)
    draw.text(
        (5, 10),
        text,
        font=font,
        fill=(random.randint(0, 180), random.randint(0, 180), random.randint(0, 180)),
    )

    img = np.array(img_pil)
    thresh = random.randint(1, 5) / 150
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            rdn = random.random()
            if rdn < thresh:
                img[i][j] = random.randint(0, 123)
            elif rdn > 1 - thresh:
                img[i][j] = random.randint(123, 255)

    # cv2.imwrite(f"./trainset/{path}/{k}.png", img)
    cv2.imwrite(f"../bombs/{path}/{k}.png", img)


for i in range(150):
    generate("HCB", i, "hcb")
    generate("CLAY", i, "claymore")
    generate("LAND", i, "landmine")
