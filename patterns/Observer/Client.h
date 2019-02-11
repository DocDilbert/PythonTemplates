#pragma once

#include <iostream>

#include "Observer.h"


// Ein Client der das Observer Interface implementiert
class Client : public Observer 
{
    int id;

public:

    Client(int id);

    virtual void update(float temp, float humidity, float pressure) override;

};
