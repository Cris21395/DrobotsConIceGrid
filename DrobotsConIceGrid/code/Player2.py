#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
Ice.loadSlice('services.ice --all -I .')
import services
import drobots
import sys, time, random
from RobotControllerAttacker import *
from RobotControllerDefender import *
from DetectorController import *

class PlayerApp(Ice.Application): 
    def run(self, argv):

        broker = self.communicator()

        #well-known object
        container_proxy = broker.stringToProxy('container')
        container = services.ContainerPrx.checkedCast(container_proxy)

        adapter = broker.createObjectAdapter('PlayerAdapter')
        adapter.activate()

        player_servant = PlayerI(broker, adapter, container)
        proxy_player = adapter.addWithUUID(player_servant)
        print ('Proxy player: ' +str(proxy_player))
        direct_player = adapter.createDirectProxy(proxy_player.ice_getIdentity())
        player = drobots.PlayerPrx.uncheckedCast(direct_player)

        proxy_game = broker.propertyToProxy('Player') 
        print ('Proxy game: ' +str(proxy_game))
        game = drobots.GamePrx.checkedCast(proxy_game)
        #gameFact = drobots.GameFactoryPrx.checkedCast(proxy_game)
        #game = gameFact.makeGame("GameRobots", 2)

        try:
            print ('Trying to do login...')
            game.login(player, 'Pedro' + str(random.randint(0,99)))
            print ('Waiting to receive both the robot controllers and the detector')
        except drobots.GameInProgress:
            print "\nGame in progress. Try it again"
            return 1
        except drobots.InvalidProxy:
            print "\nInvalid proxy"
            return 2
        except drobots.InvalidName, e:
            print "\nInvalid name. It is possible that other person be using your name"
            print str(e.reason)
            return 3
        except drobots.BadNumberOfPlayers:
            print "\nBad number of players"
            return 4            
        
        sys.stdout.flush()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0

class PlayerI(drobots.Player):
    def __init__(self, broker, adapter, container):
        self.broker = broker
        self.adapter = adapter
        self.container = container    
        self.rc_counter = 0
        self.dc_counter = 0

    def makeDetectorController(self, current=None):
        dc = None
        if self.dc_counter == 0:
            print ('Making a controller detector...')
            name = 'dc' + str(self.dc_counter)
            dc_servant = DetectorControllerI(self.container)
     
            dc_proxy = self.adapter.add(dc_servant, self.broker.stringToIdentity(name))
            print dc_proxy

            dc_proxy = current.adapter.createDirectProxy(dc_proxy.ice_getIdentity())
            dc = drobots.DetectorControllerPrx.checkedCast(dc_proxy)
            self.dc_counter = self.dc_counter + 1
        sys.stdout.flush()
        return dc

    def makeController(self, robot, current=None): 
        print ('Making a robot controller...')
        name = 'rc' + str(self.rc_counter)
        self.rc_counter += 1

        if robot.ice_isA("::drobots::Attacker"):
            rc_servant = RobotControllerAttackerI(robot, self.container, self.rc_counter)
        else:
            rc_servant = RobotControllerDefenderI(robot, self.container, self.rc_counter)
 
        rc_proxy = self.adapter.add(rc_servant, self.broker.stringToIdentity(name))
        print rc_proxy

        rc_proxy = current.adapter.createDirectProxy(rc_proxy.ice_getIdentity())
        rc = drobots.RobotControllerPrx.checkedCast(rc_proxy)
        sys.stdout.flush()
        return rc             
    
    def win(self, current=None): 
        print "Player2 wins!"
        current.adapter.getCommunicator().shutdown()

    def lose(self, current=None):
        print "Player2 loses!"
        current.adapter.getCommunicator().shutdown()

    def gameAbort(self, current=None):
        print "Game aborted. Exiting"
        current.adapter.getCommunicator().shutdown()

if __name__ == '__main__':
	sys.exit(PlayerApp().main(sys.argv))