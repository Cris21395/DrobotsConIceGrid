#!/usr/bin/python
# -*- coding: utf-8 -*-

import Ice
Ice.loadSlice('servicies.ice --all -I .')
import drobots
import sys, time, random

class PlayerApp(Ice.Application): 
    def run(self, argv):

        broker = self.communicator()
        adapter = broker.createObjectAdapter('PlayerAdapter')
        adapter.activate()

        player_servant = PlayerI(broker, adapter)
        proxy_player = adapter.addWithUUID(player_servant)
        print ('Proxy player: ' +str(proxy_player))
        direct_player = adapter.createDirectProxy(proxy_player.ice_getIdentity())
        player = drobots.PlayerPrx.uncheckedCast(direct_player)

        proxy_game = broker.propertyToProxy('Player') 
        print ('Proxy game: ' +str(proxy_game))
        game = drobots.GamePrx.checkedCast(proxy_game)

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
        
        sys.stdout.flush()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        return 0

class PlayerI(drobots.Player):
    def __init__(self, broker, adapter):
        self.broker = broker
        self.adapter = adapter    
        self.counter = 0
        self.container_factories = self.createContainerFactories()
        self.container_robots = self.createContainerControllers()

    def createContainerFactories(self, current=None):
        string_prx = 'container -t -e 1.1:tcp -h localhost -p 9190 -t 60000'
        container_proxy = self.broker.stringToProxy(string_prx)
        factories_container = drobots.ContainerPrx.checkedCast(container_proxy)
        factories_container.setType("ContainerFactories")

        print "******** CREATING FACTORIES ********"
        for i in range(0,4):
            string_prx = 'factory -t -e 1.1:tcp -h localhost -p 909'+str(i)+' -t 60000'
            factory_proxy = self.broker.stringToProxy(string_prx)
            print factory_proxy
            factory = drobots.FactoryPrx.checkedCast(factory_proxy)
            
            if not  factory:
                raise RuntimeError('Invalid factory '+i+' proxy')
        
            factories_container.link(i, factory_proxy)
        
        sys.stdout.flush()
        return factories_container

    def makeController(self, robot, current=None): 
        if self.counter == 0 :
            print "******** CREATING CONTROLLERS ********"

        i = self.counter % 4
        print ('Making a robot controller at the factory ' + str(i))
        factory_proxy = self.container_factories.getElementAt(i)
        print factory_proxy
        factory = drobots.FactoryPrx.checkedCast(factory_proxy)
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

    def createContainerControllers(self):
        container_proxy = self.broker.stringToProxy('container -t -e 1.1:tcp -h localhost -p 9190 -t 60000')
        controller_container = drobots.ContainerPrx.checkedCast(container_proxy)
        controller_container.setType("ContainerController")

        if not controller_container:
            raise RuntimeError('Invalid factory proxy')
        
        return controller_container

if __name__ == '__main__':
	sys.exit(PlayerApp().main(sys.argv))