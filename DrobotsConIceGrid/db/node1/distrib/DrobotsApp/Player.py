#!/usr/bin/python
# -*- coding: utf-8 -*-

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
        game = drobots.GamePrx.checkedCast(proxy_game)
        #gameFact = drobots.GameFactoryPrx.checkedCast(proxy_game)
        #game = gameFact.makeGame("GameRobots", 2)
        
        try:
            print ('Trying to do login...')
            game.login(player, 'Cris' + str(random.randint(0,99)))
            print ('Waiting to receive the robot controllers')
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
        self.counter = 0
        self.container_factories = self.createContainerFactories()
        self.container_robots = self.createContainerControllers()

    def createContainerFactories(self, current=None):
        factories_container = self.container
        factories_container.setType("ContainerFactories")
        list = self.container.listFactories()
        key = 0

        print "******** CREATING FACTORIES ********"
        for factory_proxy in list.values():
            print factory_proxy
            factory = services.ControllerFactoryPrx.checkedCast(factory_proxy)
            
            if not  factory:
                raise RuntimeError('Invalid factory '+key+' proxy')
        
            factories_container.link(key, factory_proxy)
            key = key + 1
        
        sys.stdout.flush()
        return factories_container

    def createContainerControllers(self):
        controller_container = self.container
        controller_container.setType("ContainerController")

        if not controller_container:
            raise RuntimeError('Invalid factory proxy')
        
        return controller_container

    def makeController(self, robot, current=None): 
        if self.counter == 0 :
            print "******** CREATING CONTROLLERS ********"

        i = self.counter % 4
        print ('Making a robot controller at the factory ' + str(i))
        factory_proxy = self.container_factories.getElementAt(i)
        print factory_proxy
        factory = services.ControllerFactoryPrx.checkedCast(factory_proxy)
        rc = factory.make(robot, self.container_robots, self.counter)
        self.counter += 1
        sys.stdout.flush()
        return rc        
    
    def win(self, current=None): 
        print "We have won!"
        current.adapter.getCommunicator().shutdown()

    def lose(self, current=None):
        print "We have lost!"
        current.adapter.getCommunicator().shutdown()

    def gameAbort(self, current=None):
        print "Game aborted. Exiting"
        current.adapter.getCommunicator().shutdown()

if __name__ == '__main__':
	sys.exit(PlayerApp().main(sys.argv))