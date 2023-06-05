from itertools import permutations
from random import randint
from string import ascii_lowercase, digits

from captcha.image import ImageCaptcha

all = ascii_lowercase + digits

image = ImageCaptcha(width=100, height=100)
perms4 = list(permutations(all, 4))
perms3 = list(permutations(all, 3))

for i in range(3000):
    image.write(f"HCB", f"./trainset/hcb/hcb-{i}.png")
    image.write(f"CLAY", f"./trainset/claymore/clay-{i}.png")
    image.write(f"LAND", f"./trainset/landmine/land-{i}.png")

exit()

for i in range(333):
    r1 = randint(0, len(perms4) - 1)
    r2 = randint(0, len(perms3) - 1)
    p1 = "".join(e for e in perms4[r1])
    p2 = "".join(e for e in perms3[r2])
    image.write(f"{p1}:HCB:{p2}", f"./trainset/hcb/hcb-{i}.png")
    image.write(f"{p1}:CLAY:{p2}", f"./trainset/claymore/clay-{i}.png")
    image.write(f"{p1}:LAND:{p2}", f"./trainset/landmine/land-{i}.png")

for i in range(333, 666):
    r1 = randint(0, len(perms4) - 1)
    r2 = randint(0, len(perms3) - 1)
    p1 = "".join(e for e in perms4[r1])
    p2 = "".join(e for e in perms3[r2])
    image.write(f"HCB:{p1}:{p2}", f"./trainset/hcb/hcb-{i}.png")
    image.write(f"CLAY:{p1}:{p2}", f"./trainset/claymore/clay-{i}.png")
    image.write(f"LAND:{p1}:{p2}", f"./trainset/landmine/land-{i}.png")

for i in range(666, 1000):
    r1 = randint(0, len(perms4) - 1)
    r2 = randint(0, len(perms3) - 1)
    p1 = "".join(e for e in perms4[r1])
    p2 = "".join(e for e in perms3[r2])
    image.write(f"{p1}:{p2}:HCB", f"./trainset/hcb/hcb-{i}.png")
    image.write(f"{p1}:{p2}:CLAY", f"./trainset/claymore/clay-{i}.png")
    image.write(f"{p1}:{p2}:LAND", f"./trainset/landmine/land-{i}.png")
