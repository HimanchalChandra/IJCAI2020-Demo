from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import cv2
import time
from sql import *
from Utils.utils import *
import os

temp_dir = 'Output/'

class UI:
	def __init__(self, vs, outputPath):

		self.vs = vs
		self.outputPath = outputPath
		self.frame = None
		self.stopEvent = None
		self.root = tki.Tk()
		self.panel = None
		btn = tki.Message(self.root, text="Message", width=200)
		btn.pack(side="bottom", fill="both", expand="yes", padx=20,
			pady=20)
		self.entry = tki.Entry(self.root, text="Message", width=50)
		self.entry.place(x=850, y=500)
		button = tki.Button(self.root, text="Deletion", command = self.deletion)
		button.pack(side="right" ,expand = "yes",  padx = 5, pady = 5)
		button = tki.Button(self.root, text="Addition",command = self.addition)
		button.pack(side="right" ,expand = "yes")
		button = tki.Button(self.root, text="Recognize")
		button.pack(side="right" ,expand = "yes")

		self.stopEvent = threading.Event()
		self.video() 
		self.root.wm_title("PyImageSearch PhotoBooth")
		self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

	
	def video(self):

		if not self.stopEvent.is_set():

			ret, self.frame = self.vs.read()
			self.frame = cv2.resize(self.frame, (600,600))
		
			image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
			image = Image.fromarray(image)
			image = ImageTk.PhotoImage(image)
		

			if self.panel is None:
				self.panel = tki.Label(image=image)
				self.panel.image = image
				self.panel.pack(side="left", padx=10, pady=10)
		

			else:
				self.panel.configure(image=image)
				self.panel.image = image
			self.panel.after(10, self.video)


	def image_capture(self):

		ts = datetime.datetime.now()
		img_name = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
		img_path = self.outputPath + img_name
		cv2.imwrite(img_path, self.frame.copy())
		print("[INFO] saved {}".format(img_name))
		return img_path


	def image_delete(self, img_path):
		os.remove(img_path)


	def recognise(self):
		pass


	def addition(self):

		if len(self.entry.get()) != 0:
			img_path = self.image_capture()
			print(img_path)
			embedding, flag = generate_embedding(img_path)
			if flag == 1:
				insertBLOB(self.entry.get(), embedding)
				self.image_delete(img_path)
			else:
				print('Image has multiple/zero faces')
		else:
			print('Enter Username')


	def deletion(self, username):

		deleteBlob(username)
		pass


	def onClose(self):

		self.vs.release()
		cv2.destroyAllWindows()
		print("[INFO] closing...")
		self.stopEvent.set()
		self.root.quit()


video = cv2.VideoCapture(2)
time.sleep(2.0)


demo_UI = UI(video, temp_dir)
demo_UI.root.mainloop()
