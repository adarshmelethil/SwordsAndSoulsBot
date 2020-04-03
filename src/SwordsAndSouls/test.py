import mss
from PIL import Image

game_window = [(951.6015625, 271.10546875), (1432.71484375, 678.953125)]

with mss.mss() as sct:
  x1, y1 = game_window[0]
  x2, y2 = game_window[1]
  monitor = {"top": y1, "left": x1, "width": x2-x1, "height": y2-y1}

  sct_img = sct.grab(monitor)
  im = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

  im.save("test.jpg")

  filename = sct.shot()
  print(filename)

