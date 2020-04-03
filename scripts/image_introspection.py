from time import time as now

from PIL import Image
import mss
import mss.tools

from pymouse import PyMouseEvent
from pykeyboard import PyKeyboard


gameScreen = [(), ()]
positionSet = 0

apple = ["#8e302e", "#9b322f"]

def rgbToHex(rbg):
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

sct_img, im = None, None

Y_min = 400
history = {}

def takeAction(k, sct, position):
	global last_attack
	x1, y1 = position[0]
	x2, y2 = position[1]
	monitor = {"top": y1, "left": x1, "width": x2-x1, "height": y2-y1}

	global sct_img, im
	sct_img = sct.grab(monitor)
	im = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
	
	w, h = im.size
	
	global history, changed
	for i in range(h):
		if i not in history:
			history[i] = []

		p = im.getpixel((X, i))
		col = rgbToHex(p)
		history[i] = list(set(history[i] + [col]))

		# if len(history[i]) > 2:
		# 	colors = [str(c) for c in history[i]]
		# 	print("{0}: {1}".format(i, ", ".join(colors)))

	# return changed

	# im.show()

	# if direction == "left":
	# 	if findStar(im) and (now()-last_attack[direction]) > time_out:
	# 		k.tap_key(direction)
	# 		last_attack[direction] = now()
	# else:
	# 	if findApple(im) and (now()-last_attack[direction]) > time_out:
	# 		k.tap_key(direction)
	# 		last_attack[direction] = now()

	# input()
	# exit(0)
	
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
		import json
		history_json = json.dumps(history, indent=4)
		with open("history.json", "w+") as f:
			f.write(history_json)

		exit(0)
