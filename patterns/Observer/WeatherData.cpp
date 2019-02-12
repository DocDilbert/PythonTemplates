#include "WeatherData.h"

void WeatherData::registerObserver(Observer *observer) 
{
    observers.push_back(observer);
}

void WeatherData::removeObserver(Observer *observer) 
{
    // find the observer
    auto iterator = std::find(observers.begin(), observers.end(), observer);

    if (iterator != observers.end()) // observer found
    {
        observers.erase(iterator); // remove the observer
    }
}

void WeatherData::notifyObservers() 
{
    // notify all observers
    for (Observer *observer : observers) 
    { 
        observer->update(temp, humidity, pressure);
    }
}

void WeatherData::setState(float temp, float humidity, float pressure) 
{
    this->temp = temp;
    this->humidity = humidity;
    this->pressure = pressure;
    
    notifyObservers();
}