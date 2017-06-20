// -*- mode:c++ -*-
// **********************************************************************
//
// Authors: Cristian Gómez Portes, Pedro Gómez Martín
//
// **********************************************************************

#include <drobots.ice>

module services {

    dictionary<string, Object*> ObjectPrxDict;
    
    interface Container {
        void link(int key, Object* proxy);
        void linkFactories(string key, Object* proxy);
        void unlink(int key);
        ObjectPrxDict list();
        ObjectPrxDict listFactories();
        Object* getElementAt(int key);
        void setType(string type);
        string getType();
    };   

    interface ControllerFactory {
        drobots::RobotController* make(drobots::Robot* bot, Container* container, int key);
        drobots::DetectorController* makeDetector(Container* container);
    };

    interface RobotControllerAttacker extends drobots::RobotController{
        void setContainer(Container* container);
        void friendPosition(drobots::Point point, int id);
    };

	interface RobotControllerDefender extends drobots::RobotController{ 
        void setContainer(Container* container);
        void friendPosition(drobots::Point point, int id);
    };
   
};
