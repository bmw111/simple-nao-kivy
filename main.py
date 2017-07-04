# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.text import LabelBase 
from kivy.core.window import WindowBase
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen,TransitionBase,FadeTransition
from kivy.properties import NumericProperty,ReferenceListProperty,BooleanProperty,ObjectProperty,ListProperty
from kivy.graphics import Color,Line,Rectangle
from kivy.vector import Vector
import socket
from kivy.core.image import Image as CoreImage
from kivy.storage.jsonstore import JsonStore
import threading 
import kivy.resources
kivy.resources.resource_add_path('data/images')
kivy.resources.resource_add_path('data/ttf')
class MyScreenManager(ScreenManager):
	def __init__(self,*args, **kwargs):
		super(MyScreenManager,self).__init__(*args, **kwargs)
		self.transition = FadeTransition()
		self.add_widget(MenuScreen())
		self.add_widget(MoveScreen())
		self.add_widget(SayScreen())
		self.add_widget(DanceScreen())
		self.add_widget(EmailScreen())
		self.add_widget(EditScreen())


	def updata_say_screen(self):
		if self.has_screen('say'):
			self.remove_widget(self.get_screen('say'))
		self.add_widget(SayScreen())
		self.current = 'say'

class MenuScreen(Screen):
	pass
class MoveScreen(Screen):
	pass
class SayScreen(Screen):
	say_text_list = ListProperty([])
	def __init__(self,*args, **kwargs):
		super(SayScreen,self).__init__(*args, **kwargs)
		self.txt_namelist= ['txt1','txt2','txt3','txt4']
		self.updata_say_text()
		self.get_layout()
	def get_layout(self):
		layout = BoxLayout(orientation='vertical',pos_hint={'x':.2,'top':.6},size_hint=(.6,.4))
		layout_2 = BoxLayout()
		textinput = TextInput(text='请在此输入想说的话')
		button_say = Button(text='say',background_color=[0,0,1,1])
		button_say.bind(on_press= lambda x:cli.say(textinput.text.encode('utf-8')))
		layout_2.add_widget(textinput)
		layout_2.add_widget(button_say)
		layout.add_widget(layout_2)
		#print self.direct.say_text_list
		
		text1 = self.say_text_list[0]
		layout.add_widget(Button(background_color=[0,0,1,1],text=text1,on_press=lambda x:cli.say(text1)))
		text2 = self.say_text_list[1]
		layout.add_widget(Button(background_color=[0,0,1,1],text=text2,on_press=lambda x:cli.say(text2)))
		text3 = self.say_text_list[2]#encode('utf-8')
		layout.add_widget(Button(background_color=[0,0,1,1],text=text3,on_press=lambda x:cli.say(text3)))
		text4 = self.say_text_list[3]#encode('utf-8')
		layout.add_widget(Button(background_color=[0,0,1,1],text=text4,on_press=lambda x:cli.say(text4)))

		self.add_widget(layout)
	
	def updata_say_text(self):
		self.text_list = []
		store = JsonStore('tts.json')
		for i in range(4):
			self.text_list.append(store.get('text')[self.txt_namelist[i]].encode('utf-8'))
		self.say_text_list = self.text_list
		

class DanceScreen(Screen):
    pass
	
class EditScreen(Screen):
	#sm = MyScreenManager()
	def __init__(self,*args, **kwargs):
		super(EditScreen,self).__init__(*args, **kwargs)
		pass
		#MyScreenManager().updata_say_screen()
	def updata_say_text_list(self,text_list):
		store = JsonStore('tts.json')
		store.put('text',txt1=text_list[0],txt2=text_list[1],txt3=text_list[2],txt4=text_list[3])
		
class EmailScreen(Screen):
	pass

class MyUdpClient(threading.Thread):
	address = ('<broadcast>', 11000)  
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  
	def __init__(self,*args, **kwargs):
		super(MyUdpClient,self).__init__(*args, **kwargs)
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
	def say(self,text):
		#print 'say'
		self.sengmsg('02',text)
	def dance(self,text):
		#print 'dance'
		self.sengmsg('03',text)
	def voice(self,text):
		self.sengmsg('04',text)
	
		
class MyDirectionlever(Widget):
	
	padding = NumericProperty(60) #方向距离侧边的距离
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
			cli.stop()
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
						cli.move('00',angle/90)
					else:
						angle = -90-angle
						cli.move('01',angle/-90)
	def updata_ball(self):
		self.canvas.after.clear()
		with self.canvas.after:
			Rectangle(pos=[self.ball_pos[0]-self.ball_r,self.ball_pos[1]-self.ball_r], size=[self.ball_r*2,self.ball_r*2],texture=self.ball_texture)

class IconButton(ButtonBehavior, Image):
    pass

class DirectionleverApp(App):
	import os,sys
	
	#os.chdir(sys.path[0])
	cli=MyUdpClient()
	say_text_list = ListProperty([])
	store = JsonStore('tts.json')
	txt_namelist= ['txt1','txt2','txt3','txt4']
	default_text_list=['你好','你吃饭了吗','欢迎光临','下午好']
	text_list = []
	
	if store.exists('text'):
		for i in range(4):
			text_list.append(store.get('text')[txt_namelist[i]].encode('utf-8'))
	else:
		store.put('text',txt1=default_text_list[0],txt2=default_text_list[1],txt3=default_text_list[2],txt4=default_text_list[3])
		text_list = default_text_list
	say_text_list = text_list
	def build(self):
		self.icon = 'nao.png'
		WindowBase.softinput_mode='below_target'
		LabelBase.register('Roboto','DroidSansFallback.ttf')
		return MyScreenManager()

if __name__=='__main__':
	
	cli=MyUdpClient()
	DirectionleverApp().run()