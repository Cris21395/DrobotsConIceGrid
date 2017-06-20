// -*- mode:c++ -*-
// **********************************************************************
//
// Authors: Cristian Gómez Portes, Pedro Gómez Martín
//
// **********************************************************************

#include <drobots.ice>

module transmission {
    
    interface Information {
        void enemyPosition(drobots::Point position);
    };
};
