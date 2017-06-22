# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.text import LabelBase 
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import NumericProperty,ReferenceListProperty,BooleanProperty
from kivy.graphics import Color,Line,Rectangle
from kivy.vector import Vector
import socket
from kivy.core.image import Image as CoreImage

class MyWidget(BoxLayout):
	address = ('<broadcast>', 11000)  
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  
	def __init__(self, **kwargs):
		super(MyWidget, self).__init__(**kwargs)
		#self.say()
		#print '123'
		pass
	def sengmsg(self,operation,text):
		msg = operation+text
		#print msg
		self.s.sendto(msg,self.address)
	def stop(self):
		#print 'stop'
		self.sengmsg('00',' ')
	def move(self,dir,angle):
		self.sengmsg('01',dir+str(angle))
	def say(self):
		#print 'say'
		self.sengmsg('02','你好，欢迎参观赫瓦机器人')
	def dance(self):
		#print 'dance'
		self.sengmsg('03','小苹果')
	def voice(self,text):
		self.sengmsg('04',text)
	
		
class MyDirectionlever(Widget):
	widget = MyWidget()
	padding = NumericProperty(50) #方向距离侧边的距离
	ball_x = NumericProperty(0)  
	ball_y = NumericProperty(0)
	circle_x = NumericProperty(0)
	circle_y = NumericProperty(0)
	ball_r = NumericProperty(30) #球的半径
	circle_r = NumericProperty(50) #方向盘半径
	
	ball_pos = ReferenceListProperty(ball_x, ball_y) #球的圆心坐标
	circle_pos = ReferenceListProperty(circle_x, circle_y)#方向圆心坐标
	is_moving = BooleanProperty(False)
	move_time = NumericProperty(0)
	def __init__(self, **kwargs):
		super(MyDirectionlever, self).__init__(**kwargs)
		self.ball_texture = CoreImage('ball.png').texture
		self.resize(self,self.size)
		
	def resize(self,ins,args):
		size = min(args[0],args[1])/2
		self.circle_r = size-self.padding
		self.ball_r = self.circle_r/3
		self.circle_pos=[size,size]
		self.ball_pos=[size,size]
		self.updata_ball()
		self.canvas.clear()	
		self.move_time=0
		with self.canvas:
			Color(1,1,1,1)
			#Line(circle=(pos, pos, pos-10),width=10)
			#Line(circle=(size,size,self.ball_r*2),width = 1)
			Rectangle(pos=[self.padding,self.padding],source='bbb.png',size=[self.circle_r*2,self.circle_r*2])
	on_pos = resize
	on_size = resize
	
	def on_touch_down(self,args):

		distance = Vector(args.pos).distance(self.circle_pos)
		if distance<self.ball_r*2:
			self.is_moving=True
			self.ball_pos=args.pos
			self.updata_ball()

	def on_touch_up(self,args):
		self.resize(self,self.size)
		if self.is_moving:
			self.is_moving=False
			self.widget.stop()
	def on_touch_move(self,args):
		if self.is_moving:
			self.move_time +=1
			distance = Vector(args.pos).distance(self.circle_pos)
			if distance<self.circle_r-self.ball_r:
				self.ball_pos=args.pos
				self.updata_ball()
			else:
				ball_v = Vector(args.x-self.circle_pos[0],args.y-self.circle_pos[1]).normalize()
				self.ball_pos = [self.circle_pos[0]+ball_v[0]*(self.circle_r-self.ball_r),self.circle_pos[1]+ball_v[1]*(self.circle_r-self.ball_r)]
				self.updata_ball()
				if self.move_time>15:
					self.move_time=0
					angle = Vector((args.pos[0]-self.circle_pos[0],args.pos[1]-self.circle_pos[1])).angle((100,0))
					#print angle
					if angle>0:
						angle = angle-90
						self.widget.move('00',angle/90)
					else:
						angle = -90-angle
						self.widget.move('01',angle/-90)
	def updata_ball(self):
		self.canvas.after.clear()
		with self.canvas.after:
			Rectangle(pos=[self.ball_pos[0]-self.ball_r,self.ball_pos[1]-self.ball_r], size=[self.ball_r*2,self.ball_r*2],texture=self.ball_texture)

class IconButton(ButtonBehavior, Image):
    pass

class DirectionleverApp(App):
	def build(self):
		LabelBase.register('Roboto','DroidSansFallback.ttf')
	
if __name__=='__main__':
    DirectionleverApp().run()