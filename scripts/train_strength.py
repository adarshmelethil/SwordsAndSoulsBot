from time import time as now

from PIL import Image
import mss
import mss.tools

from pymouse import PyMouseEvent
from pykeyboard import PyKeyboard

gamePosition = {
	"up": [(),()], # up
	"right": [(),()], # right
	"down": [(),()], # down
	"left": [(),()], # left
}
POSITION = ["up", "right", "down", "left"]
positionSet = [0, 0]

class Mouse(PyMouseEvent):
	def __init__(self):
		PyMouseEvent.__init__(self)

	def click(self, x, y, button, pressed):
		global gamePosition, positionSet
		if pressed:
			if positionSet[0] >= len(POSITION):
				positionSet = [0, 0]
				return
			gamePosition[POSITION[positionSet[0]]][positionSet[1]] = (x, y)
			positionSet[1] += 1
			if positionSet[1] >= 2:
				positionSet[0] += 1
				positionSet[1] = 0
				if positionSet[0] < len(POSITION):
					print("Next: {}".format(POSITION[positionSet[0]]))

ar, ag, ab, = (140,60,60)
def findApple(im):
	x, y = im.size
	for i in range(x):
		for j in range(y):
			r, g, b = im.getpixel((i, j))
			# Red
			if r > ar and g < ag and b < ab:
				return True
	return False

sr, sg, = (180,180,)
def findStar(im):
	return False
	x, y = im.size
	for i in range(x):
		for j in range(y):
			r, g, _ = im.getpixel((i, j))
			# Red
			if r > sr and g > sg:
				return True
	return False

last_attack = {
	"up": now(),
	"right": now(),
	"down": now(),
	"left": now(),
}
time_out = 0.1
def takeAction(k, sct, position, direction):
	global last_attack
	x1, y1 = position[0]
	x2, y2 = position[1]
	monitor = {"top": y1, "left": x1, "width": x2-x1, "height": y2-y1}

	sct_img = sct.grab(monitor)
	im = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

	if direction == "left":
		if findStar(im) and (now()-last_attack[direction]) > time_out:
			k.tap_key(direction)
			last_attack[direction] = now()
	else:
		if findApple(im) and (now()-last_attack[direction]) > time_out:
			k.tap_key(direction)
			last_attack[direction] = now()


import random
def main(k):
	with mss.mss() as sct:
		while True:
			if positionSet[0] == len(gamePosition):
				for direction, position in gamePosition.items():
					takeAction(k, sct, position, direction)


if __name__ == "__main__":
	m = Mouse()
	k = PyKeyboard()
	try:
		m.start()
		main(k)
	except KeyboardInterrupt:
		exit(0)
