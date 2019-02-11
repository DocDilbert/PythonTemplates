#pragma once

#include "Observer.h"

// Interface des Subject
class Subject 
{
public:

    /// Register an observer
    /// @param observer the observer object to be registered  
    virtual void registerObserver(Observer *observer) = 0;

    /// Unregister an observer
    /// @param observer the observer object to be unregistered
    virtual void removeObserver(Observer *observer) = 0;

    /// Notify all the registered observers when a change happens
    virtual void notifyObservers() = 0;

};

