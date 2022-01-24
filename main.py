from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy import platform
from kivy.app import App
from kivy.properties import Clock
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics.vertex_instructions import Line
from kivy.graphics.context_instructions import Color


class MainWidget(Widget):
	from transforms import transform, tranform_perspective, transform_2D
	from user_actions import keyboard_closed, on_keyboard_down, on_keyboard_up, on_touch_down, on_touch_up

	perspective_point_x = NumericProperty(0)
	perspective_point_y = NumericProperty(0)
	current_offset_y = NumericProperty(0)
	current_offset_x = NumericProperty(0)
	current_speed_x = NumericProperty(0)
	
	V_NB_LINES = 8		# number of lines
	V_LINES_SPACING = 0.25		# persentage in screen width
	vertical_lines = []

	H_NB_LINES = 16		# number of lines
	H_LINES_SPACING = 0.1		# persentage in screen height
	horizontal_lines = []

	SPEED = 4
	SPEED_X = 4
	
	def __init__(self, **kwargs):
		super(MainWidget, self).__init__(**kwargs)
		self.init_vertical_lines()
		self.init_horizontal_lines()

		if self.is_desktop():
			self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
			self._keyboard.bind(on_key_down=self.on_keyboard_down)
			self._keyboard.bind(on_key_up=self.on_keyboard_up)

		Clock.schedule_interval(self.update, 1.0 / 60)	# 60 fps
	

	def is_desktop(self):
		if platform in ('linux', 'win', 'macosc'):
			return True
		else:
			return False
	

	def init_vertical_lines(self):
		with self.canvas:
			Color(1, 1, 1)
			# self.line = Line(points=[self.width/2, 0, self.width/2, 100])
			for i in range(0, self.V_NB_LINES):
				self.vertical_lines.append(Line())


	def init_horizontal_lines(self):
		with self.canvas:
			Color(1, 1, 1)
			# self.line = Line(points=[self.width/2, 0, self.width/2, 100])
			for i in range(0, self.H_NB_LINES):
				self.horizontal_lines.append(Line())


	def get_line_x_from_index(self, index):
		central_line_x = self.perspective_point_x
		spacing = self.V_LINES_SPACING * self.width
		offset = index - 0.5
		line_x = central_line_x + offset * spacing + self.current_offset_x

		return line_x

		
	def update_vertical_lines(self):
		start_index = -int(self.V_NB_LINES / 2) + 1

		for i in range(start_index, self.V_NB_LINES + start_index):
			line_x = self.get_line_x_from_index(i)
			
			x1, y1 = self.transform(line_x, 0)
			x2, y2 = self.transform(line_x, self.height)
			
			self.vertical_lines[i].points = [x1, y1, x2, y2]


	def update_horizontal_lines(self):
		start_index = -int(self.V_NB_LINES / 2) + 1
		end_index = start_index + self.V_NB_LINES - 1

		xmin = self.get_line_x_from_index(start_index)
		xmax = self.get_line_x_from_index(end_index)
		spacing_y = self.H_LINES_SPACING * self.height
		
		for i in range(0, self.V_NB_LINES):
			line_y = i * spacing_y - self.current_offset_y
			
			x1, y1 = self.transform(xmin, line_y)
			x2, y2 = self.transform(xmax, line_y)
			
			self.horizontal_lines[i].points = [x1, y1, x2, y2]


	def update(self, dt):
		time_factor = dt*60

		self.perspective_point_x = self.width/2
		self.perspective_point_y = self.height * 0.75

		self.update_vertical_lines()
		self.update_horizontal_lines()
		#self.current_offset_y += self.SPEED * time_factor

		spacing_y = self.H_LINES_SPACING * self.height
		if self.current_offset_y >= spacing_y:
			self.current_offset_y -= spacing_y

		#self.current_offset_x += self.current_speed_x * self.SPEED_X * time_factor


class GalaxyApp(App):
	pass
	

GalaxyApp().run()

