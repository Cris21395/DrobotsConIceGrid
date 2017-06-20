#!/usr/bin/python
# -*- coding: utf-8 -*-
# **********************************************************************
#
# Authors: Cristian Gómez Portes, Pedro Gómez Martín
#
# **********************************************************************

import Ice
Ice.loadSlice('services.ice --all -I .')
import services
import drobots
import sys, time, random

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
        #game = drobots.GamePrx.checkedCast(proxy_game)
        gameFact = drobots.GameFactoryPrx.checkedCast(proxy_game)
        game = gameFact.makeGame("GameRobots", 2)
        
        try:
            print ('Trying to do login...')
            game.login(player, 'Cris' + str(random.randint(0,99)))
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
        self.robot = 0
        self.factory = 1
        self.detector = 0

    def makeDetectorController(self, current=None):
        if self.detector == 0:
            print "******** CREATING DETECTOR ********"
        self.container.setType("ContainerDetector")

        print ('Making a detector controller at the factory ' + str(self.factory))

        factory_proxy = self.broker.stringToProxy("detector")
        factory = services.ControllerFactoryPrx.checkedCast(factory_proxy)
        dc = factory.makeDetector(self.container)
        print("{0}: link: {1} -> {2}".format(self.factory, factory_proxy, dc))
        self.detector += 1
        sys.stdout.flush()
        return dc

    def makeController(self, robot, current=None): 
        if self.robot == 0 :
            print "******** CREATING CONTROLLERS ********"
            self.container.setType("ContainerController")

        print ('Making a robot controller at the factory ' + str(self.factory))

        factory_proxy = self.broker.stringToProxy("factory"+str(self.factory))
        factory = services.ControllerFactoryPrx.checkedCast(factory_proxy)
        rc = factory.make(robot, self.container, self.robot)
        print("{0}: link: {1} -> {2}".format(self.factory, factory_proxy, rc))
        self.container.link(self.robot, rc)
        self.robot += 1
        self.factory += 1

        sys.stdout.flush()
        return rc   
    
    def win(self, current=None): 
        print "Player1 wins!"
        current.adapter.getCommunicator().shutdown()

    def lose(self, current=None):
        print "Player1 loses!"
        current.adapter.getCommunicator().shutdown()

    def gameAbort(self, current=None):
        print "Game aborted. Exiting"
        current.adapter.getCommunicator().shutdown()

if __name__ == '__main__':
	sys.exit(PlayerApp().main(sys.argv))