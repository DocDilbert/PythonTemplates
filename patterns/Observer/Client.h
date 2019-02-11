#pragma once

#include "Observer.h"


// Ein Client der das Observer Interface implementiert
class Client : public Observer 
{
public:
    float temp;
    float humidity;
    float pressure;
    
    Client();

private:
    virtual void update(float temp, float humidity, float pressure) override;

};
