#include "Client.h"

Client::Client() 
{
}

void Client::update(float temp, float humidity, float pressure) 
{
    this->temp = temp;
    this->humidity = humidity;
    this->pressure = pressure;
}

