#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
import os
Ice.loadSlice('services.ice --all -I .')
import drobots
import services
import drobots, sys

class DetectorControllerI(drobots.DetectorController):

	def alert(self, enemy_position, enemies, current=None):
		print("Alert! Detected %d enemies. Position: (%d, %d)" % (enemies, enemy_position.x, enemy_position.y))
