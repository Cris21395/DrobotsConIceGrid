#!/usr/bin/python
# -*- coding: utf-8 -*-
# **********************************************************************
#
# Authors: Cristian Gómez Portes, Pedro Gómez Martín
#
# **********************************************************************

import Ice
import os
Ice.loadSlice('services.ice --all -I .')
Ice.loadSlice('transmission.ice --all -I .')
import transmission
import drobots
import services
import sys

class DetectorControllerI(drobots.DetectorController, transmission.Information):
	def __init__(self, container):
		self.container = container

	def alert(self, enemy_position, enemies, current=None):
		for value in range(0,4):
			robot = self.container.getElementAt(value)
			if(robot.ice_isA("::services::RobotControllerAttacker")):
				attacker = transmission.InformationPrx.uncheckedCast(robot)
				print "Sending position to attacker"
				attacker.enemyPosition(enemy_position)
		return None