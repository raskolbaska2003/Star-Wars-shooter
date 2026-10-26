import pygame
from Values import height, width
class Particles:
	
	def __init__(self,circle,speed):
		# circle = [screen, (color),[x,y],radius(int)]
		# speed = [speed_x,speed_y]
		self.screen=circle[0]
		self.color=circle[1]
		self.position=circle[2].copy()
		self.radius=circle[3]

		self.speed=speed
	

	def move(self):
		self.position[0]+=self.speed[0]
		self.position[1]+=self.speed[1]

		if self.position[0]>width or self.position[0]<0:
			self.speed[0] = -self.speed[0]
		if self.position[1]>height or self.position[1]<0:
			self.speed[1] = -self.speed[1]
		
		self.speed[1]+=0.4
		self.radius-=0.04


		pygame.draw.circle(self.screen,self.color,self.position,self.radius)


	


	
		