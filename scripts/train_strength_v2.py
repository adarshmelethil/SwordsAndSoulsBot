from time import time as now

from PIL import Image
import mss
import mss.tools

from pymouse import PyMouseEvent
from pykeyboard import PyKeyboard


gameScreen = [(), ()]
positionSet = 0

apple_colors = ["#8e302e", "#9b322f"]

actions = ["up", "right", "down"]
last_attack = {
	"up": now(),
	"right": now(),
	"down": now(),
	"left": now(),
}
time_out = 0.1
X = 440
Y = {
	"up": 543,
	"right": 719,
	"down": 870,
}

def rgbToHex(rgb):
	return '#%02x%02x%02x' % rgb

class Mouse(PyMouseEvent):
	def __init__(self):
		PyMouseEvent.__init__(self)

	def click(self, x, y, button, pressed):
		global positionSet
		if pressed:
			if positionSet >= 2:
				positionSet = 0
				return
			
			gameScreen[positionSet] = (x, y)
			positionSet += 1


def takeAction(k, sct, position):
	global last_attack
	x1, y1 = position[0]
	x2, y2 = position[1]
	monitor = {"top": y1, "left": x1, "width": x2-x1, "height": y2-y1}

	sct_img = sct.grab(monitor)
	im = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
	
	# if direction == "left":
	# 	if findStar(im) and (now()-last_attack[direction]) > time_out:
	# 		k.tap_key(direction)
	# 		last_attack[direction] = now()
	# else:
	for action in actions:
		if (now()-last_attack[action]) > time_out:

			if rgbToHex(im.getpixel((X, Y[action]))) in apple_colors:
				k.tap_key(action)
				print("{}: tap".format(action))
				last_attack[action] = now()
	
def main(k):
	with mss.mss() as sct:
		while True:
			if positionSet == 2:
				takeAction(k, sct, gameScreen)


if __name__ == "__main__":
	m = Mouse()
	k = PyKeyboard()
	try:
		m.start()
		main(k)
	except KeyboardInterrupt:
		exit(0)
