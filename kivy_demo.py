from db_utils import *
from Utils.utils import *

from kivy.config import Config
Config.set('graphics', 'window_state', 'maximized')

from kivy.core.window import Window 
Window.clearcolor = (1, 1, 1, 1)

import kivy
from kivy.app import App
from kivy.uix.label import Label 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image 

from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture

from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.graphics import Color, Rectangle

import datetime
import cv2

 
kivy.require("1.11.1")

global usernames
global embeddings

class Home_Page(GridLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.cols = 2
		self.padding = [100, 100, 100, 100]
		self.add_widget(Image(source = 'Attendance.jpg'))

		buttons = GridLayout(cols = 2)

		buttons.spacing = [20, 20]

		button_1 = Button(text='TAKE \nATTENDANCE', font_size = 30, italic = True, background_color = [1, 255, 1, 1])
		button_2 = Button(text='SHOW \nATTENDANCE', font_size = 30, italic = True, background_color = [255, 1, 1, 1])
		button_3 = Button(text='ADD \nSTUDENT', font_size = 30, italic = True, background_color = [1, 1, 255, 1])
		button_4 = Button(text='REMOVE \nSTUDENT', font_size = 30, italic = True, background_color = [100, 140, 0, 1])

		button_1.bind(on_press = self.take_attendance)
		button_2.bind(on_press = self.show_attendance)
		button_3.bind(on_press = self.add_student)
		button_4.bind(on_press = self.remove_student)

		buttons.add_widget(button_1)
		buttons.add_widget(button_2)
		buttons.add_widget(button_3)
		buttons.add_widget(button_4)

		self.add_widget(buttons)


	def take_attendance(self, instance):
		global usernames, embeddings
		embeddings, usernames = readAllBlobData()
		UI_interface.screen_manager.current = "Attendance"

	def show_attendance(self, instance):
		return None

	def add_student(self, instance):
		UI_interface.screen_manager.current = "Add_Student"

	def remove_student(self, instance):
		return None


class Attendance_Page(GridLayout):
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.output_path = 'Output/'
		self.flag = 0
		self.cols = 2
		self.padding = [100, 100, 100, 100]
		self.spacing = [20, 20]
		self.begin = Button(text='BEGIN', font_size = 30, italic = True, background_color = [1, 255, 1, 1])
		self.begin.bind(on_press = self.start)
		self.add_widget(self.begin)
		self.back = Button(text='GO BACK', font_size = 30, italic = True, background_color = [255, 1, 1, 1])
		self.back.bind(on_press = self.goback)
		self.add_widget(self.back)


	def start(self, instance):
		self.flag = 1
		self.img=Image()
		self.layout = BoxLayout()
		self.layout.add_widget(self.img)
		self.remove_widget(self.begin)
		self.remove_widget(self.back)
		self.add_widget(self.layout)

		mark = Button(text='MARK ME', font_size = 30, italic = True, background_color = [255, 1, 1, 1])
		back = Button(text='GO BACK', font_size = 30, italic = True, background_color = [1, 1, 255, 1])
		self.label = Label(text='Mark Your Attendance!!', font_size = 38, color = [255, 255, 255, 1])

		mark.bind(on_press = self.recognize)
		back.bind(on_press = self.goback)

		self.button_layout = GridLayout(rows = 3, spacing = [20, 20])

		self.button_layout.add_widget(mark)
		self.button_layout.add_widget(back)
		self.button_layout.add_widget(self.label)
		
		self.add_widget(self.button_layout)

		self.capture = cv2.VideoCapture(3)
		self.event = Clock.schedule_interval(self.update, 1.0/33.0)


	def update(self, instance):

		_, self.frame = self.capture.read()
		self.frame = extract_all_faces(self.frame)
		buf1 = cv2.flip(self.frame, 0)
		buf = buf1.tostring()
		texture = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')
		texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
		self.img.texture = texture


	def recognize(self, instance):
		ts = datetime.datetime.now()
		img_name = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
		img_path = self.output_path + img_name
		cv2.imwrite(img_path, self.frame)
		print("[INFO] saved {}".format(img_name))
		embedding, flag = generate_embedding(img_path)

		if flag == 1:
			ones_matrix = np.ones((len(usernames), 1))
			embedding_matrix = np.matmul(ones_matrix, embedding.detach().numpy())
			distances = calc_distance(embedding_matrix, embeddings)
			if (distances[np.argmin(distances)] < 1.0000):
				print(usernames[np.argmin(distances)] + ' Marked')
				self.button_layout.remove_widget(self.label)
				self.label = Label(text=usernames[np.argmin(distances)] + ' Marked', font_size = 38, color = [255, 255, 255, 1])
				self.button_layout.add_widget(self.label)
			else:
				self.button_layout.remove_widget(self.label)
				self.label = Label(text = 'User Not Registered', font_size = 38, color = [255, 255, 255, 1])
				self.button_layout.add_widget(self.label)
		else:
			self.button_layout.remove_widget(self.label)
			self.label = Label(text='Zero/Muliple Faces Detected', font_size = 38, color = [255, 255, 255, 1])
			self.button_layout.add_widget(self.label)


	def goback(self, instance):

		if self.flag == 1:
			self.event.cancel()
			self.capture.release()
			self.remove_widget(self.layout)
			self.remove_widget(self.button_layout)
			self.__init__()
		UI_interface.screen_manager.current = "Home"


class Add_Student(GridLayout):
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.output_path = 'Output/'
		self.cols = 2
		self.flag = 0
		self.padding = [100, 100, 100, 100]
		self.spacing = [20, 20]
		self.begin = Button(text='BEGIN', font_size = 30, italic = True, background_color = [1, 255, 1, 1])
		self.begin.bind(on_press = self.start)
		self.add_widget(self.begin)
		self.back = Button(text='GO BACK', font_size = 30, italic = True, background_color = [255, 1, 1, 1])
		self.back.bind(on_press = self.goback)
		self.add_widget(self.back)

	def start(self, instance):
		self.flag = 1
		self.img=Image()
		self.layout = BoxLayout()
		self.layout.add_widget(self.img)
		self.remove_widget(self.begin)
		self.remove_widget(self.back)
		self.add_widget(self.layout)

		self.name = TextInput(multiline = False, size_hint = (.2, None), height = 40)
		add = Button(text='ADD ME', font_size = 30, italic = True, background_color = [255, 1, 1, 1])
		back = Button(text='GO BACK', font_size = 30, italic = True, background_color = [1, 1, 255, 1])
		self.label = Label(text='Add Yourself!!', font_size = 38, color = [255, 255, 255, 1])


		add.bind(on_press = self.add)
		back.bind(on_press = self.goback)

		self.button_layout = GridLayout(rows = 4, spacing = [20, 20])

		self.button_layout.add_widget(self.name)
		self.button_layout.add_widget(add)
		self.button_layout.add_widget(back)
		self.button_layout.add_widget(self.label)
		
		self.add_widget(self.button_layout)

		self.capture = cv2.VideoCapture(3)
		self.event = Clock.schedule_interval(self.update, 1.0/33.0)


	def update(self, instance):
		_, self.frame = self.capture.read()
		self.frame = extract_all_faces(self.frame)
		buf1 = cv2.flip(self.frame, 0)
		buf = buf1.tostring()
		texture = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')
		texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
		self.img.texture = texture


	def add(self, instance):

		if len(self.name.text) != 0:
			ts = datetime.datetime.now()
			img_name = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
			img_path = self.output_path + img_name
			cv2.imwrite(img_path, self.frame)
			print("[INFO] saved {}".format(img_name))
			embedding, flag = generate_embedding(img_path)
			if flag == 1:
				insertBLOB(self.name.text, embedding)
				self.button_layout.remove_widget(self.label)
				self.label = Label(text=self.name.text + ' Added', font_size = 38, color = [255, 255, 255, 1])
				self.button_layout.add_widget(self.label)
			else:
				self.button_layout.remove_widget(self.label)
				self.label = Label(text = 'Zero/Multiple Faces Detected', font_size = 38, color = [255, 255, 255, 1])
				self.button_layout.add_widget(self.label)
		else:
			self.button_layout.remove_widget(self.label)
			self.label = Label(text = 'Enter UserName', font_size = 38, color = [255, 255, 255, 1])
			self.button_layout.add_widget(self.label)

	def goback(self, instance):
		if self.flag == 1:
			self.event.cancel()
			self.capture.release()
			self.remove_widget(self.layout)
			self.remove_widget(self.button_layout)
			self.__init__()
		UI_interface.screen_manager.current = "Home"



class UI(App):

	def build(self):
		self.screen_manager = ScreenManager()

		self.home_page = Home_Page()
		screen = Screen(name='Home')
		screen.add_widget(self.home_page)
		self.screen_manager.add_widget(screen)

		self.attendance_page = Attendance_Page()
		screen = Screen(name='Attendance')
		screen.add_widget(self.attendance_page)
		self.screen_manager.add_widget(screen)

		self.add_student = Add_Student()
		screen = Screen(name='Add_Student')
		screen.add_widget(self.add_student)
		self.screen_manager.add_widget(screen)

		return self.screen_manager


if __name__ == "__main__":
	embeddings, usernames = readAllBlobData()
	UI_interface = UI()
	UI_interface.run()