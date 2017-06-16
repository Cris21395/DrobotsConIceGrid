#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
import os
Ice.loadSlice('services.ice --all -I .')
import services
import sys
from RobotControllerAttacker import *
from RobotControllerDefender import *
from DetectorController import *

class FactoryI(services.ControllerFactory):

	def make(self, robot, container_robots, key, current=None):
		print "******** MAKING FACTORY ********"     

		if robot.ice_isA("::drobots::Attacker"):
			rc_servant = RobotControllerAttackerI(robot, container_robots, key)
			rc_proxy = current.adapter.addWithUUID(rc_servant)
			print rc_proxy                  
			rc_proxy = current.adapter.createDirectProxy(rc_proxy.ice_getIdentity())
			container_robots.link(key, rc_proxy)
			rc = services.RobotControllerAttackerPrx.checkedCast(rc_proxy)

		else:
			rc_servant = RobotControllerDefenderI(robot, container_robots, key)
			rc_proxy = current.adapter.addWithUUID(rc_servant)
			print rc_proxy
			rc_proxy = current.adapter.createDirectProxy(rc_proxy.ice_getIdentity())            
			container_robots.link(key, rc_proxy)
			rc = services.RobotControllerDefenderPrx.checkedCast(rc_proxy)

		rc.setContainer(container_robots)    
		return rc

	def makeDetector(self, current=None):
		dc_servant = DetectorControllerI()
		dc_proxy = current.adapter.addWithUUID(dc_servant)
		print dc_proxy
		dc_poxy = current.adapter.createDirectProxy(dc_proxy.ice_getIdentity())
		dc = drobots.DetectorControllerPrx.checkedCast(dc_poxy)
		return dc

class ServerFactoryApp(Ice.Application):
	def run(self, argv):
		broker = self.communicator()
		adapter = broker.createObjectAdapter('FactoryAdapter')
		servant = FactoryI()

		identity = broker.getProperties().getProperty("Identity")
		proxy = adapter.add(servant, broker.stringToIdentity(identity))

		container_proxy = broker.stringToProxy('container')
		container = services.ContainerPrx.checkedCast(container_proxy)

		container.linkFactories("Factory"+"--"+str(os.getpid()), proxy)              

		print(proxy)

		adapter.activate()
		self.shutdownOnInterrupt()
		broker.waitForShutdown()

		return 0

if __name__ == '__main__':
	sys.exit(ServerFactoryApp().main(sys.argv))
