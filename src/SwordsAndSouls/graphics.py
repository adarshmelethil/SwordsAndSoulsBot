import os 
from tkinter import Frame, Label, Button, LEFT, RIGHT, Canvas
from PIL import Image, ImageTk
from pynput import mouse
from pynput import keyboard
import mss
import threading
import cv2
from numpy import asarray

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
    self.themouse = mouse.Controller()
    self.thekeyboard = keyboard.Controller()


  def __del__(self):
    self.sct.close()

  def auto(self):
    count = 0
    prev_data = None
    while self.automation:
      count += 1
      print(count)
      image = self.grabScreen()
      
      data = asarray(image)
      if prev_data is None:
        prev_data = data
      else:
        prev_data_tmp = data
        data = data - prev_data
        prev_data = prev_data_tmp


      # create Pillow image
      
      # data = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
      image2 = Image.fromarray(data)
      # print(im)
      self.setCanvasImage(image2)

      if count > 50:
        break
    print(f"Ran {count} loops")

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
    self.automation = False
    # if self.test:
    #   print('Pointer moved to {0}'.format(
    #     (x, y)))
    pass

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
    

  def click(self):
    self.themouse.press(mouse.Button.left)
    self.themouse.release(mouse.Button.left)

  def tap(self, key):
    self.thekeyboard.press(key)
    self.thekeyboard.release(key)

  def centerMouse(self):
    width = self.game_window[1][0] - self.game_window[0][0]
    height = self.game_window[1][1] - self.game_window[0][1]
    x_move = (self.game_window[0][0] + width/2) - self.themouse.position[0]
    y_move = (self.game_window[0][1] + height/2) - self.themouse.position[1]

    self.themouse.move(x_move, y_move)

  def testFunc(self):
    self.test = not self.test
    
    # Move pointer relative to current position
    if len(self.game_window) > 1:
      self.centerMouse()
      self.click()
      self.click()
      self.tap(keyboard.Key.up)

    # Press and release
    


