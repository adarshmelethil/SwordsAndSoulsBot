import os 
from tkinter import Frame, Label, Button, LEFT, RIGHT, Canvas
from PIL import Image, ImageTk
from pynput import mouse
import mss
import threading
# import Button, Controller, Listener


dir_path = os.path.dirname(os.path.realpath(__file__))

class Window(Frame):
  def __init__(self, master=None):
    Frame.__init__(self, master)
    self.master = master
    self.pack()
    
    self.placeholder_image = Image.open(
      os.path.join(dir_path, "sword_and_soul.png")).resize((500,500))
    
    self.image_size = (500, 500)
    self.picture_canvas = Canvas(self, width=self.image_size[0], height=self.image_size[1])
    self.picture_canvas.pack()
  
    # self.picture_canvas.create_image(0, 0, image=self.place_holder, anchor="nw")
    self.setCanvasImage(self.placeholder_image)

    self.button = Button(
      self, text="QUIT", fg="red", command=self.quit)
    self.button.pack(side=LEFT)

    self.test_button = Button(self, text="Select Window", command=self.selectWindow)
    self.test_button.pack(side=RIGHT)

    self.test_button = Button(self, text="Start", command=self.startAuto)
    self.test_button.pack(side=RIGHT)

    self.test_button = Button(self, text="Test", command=self.testFunc)
    self.test_button.pack(side=RIGHT)

    self.cow_img = Image.open(os.path.join(dir_path, "cow.jpg"))
    
    self.test = False

    self.select_window = False
    self.game_window = []
    self.automation = False

    # Screenshot
    self.sct = mss.mss()

    # Mouse
    self.mouse_listener = mouse.Listener(
        on_move=self.on_move,
        on_click=self.on_click)
    self.mouse_listener.start()


  def __del__(self):
    self.sct.close()

  def auto(self):
    while self.automation:
      im = self.grabScreen()
      print(im)
      self.setCanvasImage(im)

  def startAuto(self):
    if not self.automation:
      self.automation = True
      t = threading.Thread(target=self.auto)
      t.start()
    else:
      self.automation = False

  def selectWindow(self):
    self.select_window = True
    self.game_window = []

  def on_move(self, x, y):
    # self.automation = False
    if self.test:
      print('Pointer moved to {0}'.format(
        (x, y)))

  def on_click(self, x, y, button, pressed):
    if self.select_window and pressed:
      print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))

      self.game_window.append((x,y))
      if len(self.game_window) >= 2:
        self.select_window = False
        print(self.game_window)
        self.setCanvasImage(self.grabScreen())
    return True
  
  def grabScreen(self):
    x1, y1 = self.game_window[0]
    x2, y2 = self.game_window[1]
    monitor = {"top": y1, "left": x1, "width": x2-x1, "height": y2-y1}

    sct_img = self.sct.grab(monitor)
    im = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
    return im
  # def on_scroll(self, x, y, dx, dy):
  #   print('Scrolled {0} at {1}'.format(
  #       'down' if dy < 0 else 'up',
  #       (x, y)))

  def setCanvasImage(self, image):
    self.tkimage = ImageTk.PhotoImage(image.resize(self.image_size))
    # self.picture_canvas.config(width=width, height=height)
    self.picture_canvas.create_image(0, 0, image=self.tkimage, anchor="nw")
    

  def testFunc(self):
    self.test = not self.test
    
    if self.test:
      # self.picture_label.configure(image=self.cow)
      self.setCanvasImage(self.cow_img)
    else:
      # self.picture_canvas.create_image(0, 0, image=self.place_holder, anchor="nw")
      self.setCanvasImage(self.placeholder_image)
      # self.picture_label.configure(image=self.place_holder)
    # self.picture_label.image = self.cow
