#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
import os
Ice.loadSlice('services.ice --all -I .')
import services
import sys
from RobotControllerAttacker import *
from RobotControllerDefender import *

class FactoryI(services.ControllerFactory):

    def make(self, robot, container_robots, key, current=None):
        print "******** MAKING FACTORY ********"     

        if robot.ice_isA("::drobots::Attacker"):
            rc_servant = RobotControllerAttackerI(robot, container_robots)
            rc_proxy = current.adapter.addWithUUID(rc_servant)
            print rc_proxy                  
            rc_proxy = current.adapter.createDirectProxy(rc_proxy.ice_getIdentity())
            container_robots.link(key, rc_proxy)
            rc = services.RobotControllerAttackerPrx.uncheckedCast(rc_proxy)

        else:
            rc_servant = RobotControllerDefenderI(robot, container_robots)
            rc_proxy = current.adapter.addWithUUID(rc_servant)
            print rc_proxy
            rc_proxy = current.adapter.createDirectProxy(rc_proxy.ice_getIdentity())            
            container_robots.link(key, rc_proxy)
            rc = services.RobotControllerDefenderPrx.uncheckedCast(rc_proxy)

        rc.setContainer(container_robots)    
        return rc

class ServerFactoryApp(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        adapter = broker.createObjectAdapter('FactoryAdapter')
        servant = FactoryI()
        proxy = adapter.addWithUUID(servant)

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
