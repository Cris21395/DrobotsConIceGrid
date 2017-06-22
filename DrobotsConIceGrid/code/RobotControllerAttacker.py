#!/usr/bin/python
# -*- coding: utf-8 -*-
# **********************************************************************
#
# Authors: Cristian Gómez Portes, Pedro Gómez Martín
#
# **********************************************************************

import Ice
Ice.loadSlice('services.ice --all -I .')
Ice.loadSlice('transmission.ice --all -I .')
import transmission
import services
import drobots
import sys, time, random, math
from State import *

class RobotControllerAttackerI(services.RobotControllerAttacker, transmission.Information):

	def __init__(self, robot, container, robot_id, current=None):
		self.robot = robot
		self.container = container
		self.robotId = robot_id
		self.state = State.MOVING
		self.x = random.randint(0, 360)
		self.y = random.randint(0, 360)
		self.shoot_angle = 0
		self.shoots_counter = 0
		self.friends_position = dict()
		self.handlers = {
			State.MOVING : self.move,
			State.SHOOTING : self.shoot,
			State.PLAYING : self.play
		}
		self.velocidad = 0
		self.distance = 0
		self.flag = 0 #flag that allows to obtain enemy's position
		
	def setContainer(self, container, current=None):
		self.container = container
		return None
	
	def friendPosition(self, point, identifier, current=None):
		self.friends_position[identifier]= point
		return None

	def enemyPosition(self, point, container=None):
		print("RobotControllerAttacker"+str(self.robotId)+" has found an enemy")
		x = point.x
		y = point.y

		location = self.robot.location()

		xrobot = location.x
		yrobot = location.y
		xEnemy = x - xrobot
		yEnemy = y - yrobot
		enemyAngle = int(math.degrees(math.atan2(xEnemy, yEnemy)) % 360.0)
		distance = int(math.hypot(xEnemy, yEnemy))
		angle = random.randint(0, enemyAngle)
		self.shoot_angle = angle
		self.distance = distance
		self.flag = 1
		return None

	def turn(self, current=None):
		try:
			self.handlers[self.state]()
		except drobots.NoEnoughEnergy:
			pass
		return None

	def play(self, current=None):
		my_location = self.robot.location()
		counter = 0

		for defender_prx in self.container.list().values():
			if(defender_prx.ice_isA("::services::RobotControllerDefender")):
				defender = services.RobotControllerDefenderPrx.uncheckedCast(defender_prx)
				defender.friendPosition(my_location, counter)
			counter += 1
			self.state = State.SHOOTING
		return None

	def move(self, current=None):
		location = self.robot.location()
		delta_x = self.x - location.x
		delta_y = self.y - location.y
		angle = int(round(self.calculate_angle(delta_x, delta_y), 0))

		if(self.velocidad == 0):
			self.robot.drive(random.randint(0,360),100)
			self.velocidad = 100
		elif(location.x > 390):
			self.robot.drive(225, 100)
			self.velocidad = 100
		elif(location.x < 100):
			self.robot.drive(45, 100)
			self.velocidad = 100
		elif(location.y > 390):
			self.robot.drive(315, 100)
			self.velocidad = 100
		elif(location.y < 100):
			self.robot.drive(135, 100)
			self.velocidad = 100

		self.robot.drive(angle, 100)
		self.state = State.PLAYING
		return None

	def shoot(self, current=None): 
		MAX_SHOOTS = 10
		if self.shoots_counter <= MAX_SHOOTS:
			if self.flag == 0:
				angle = self.shoot_angle + random.randint(0, 360)
				distance = (self.shoots_counter + 6) * 20
				self.robot.cannon(angle, distance) 
				self.shoots_counter += 1
				self.state = State.SHOOTING
			else:
				self.robot.cannon(self.shoot_angle, self.distance) 
				self.shoots_counter += 1
				self.state = State.SHOOTING
		else:
			self.shoots_counter = 0
			self.state = State.MOVING
		return None

	def robotDestroyed(self, current=None):
		if self.robot.damage() == 100:
			print("Destoryed atacant " + str(self.robotId))
		return None

	def calculate_angle(self, x, y, current=None):
		if x==0:
			if y>0:
				return 90
			return 270
		if y==0:
			if x>0:
				return 0
			return 180
		elif y>0:
			return 90 - math.degrees(math.atan(float(x)/float(y)))
		else:
			return 270 - math.degrees(math.atan(float(x)/float(y)))