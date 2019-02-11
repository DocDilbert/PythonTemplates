#pragma once

#include <vector>
#include <algorithm>
#include <iostream>

#include "Subject.h"
#include "Observer.h"

// Eine konkrete Implementierung des Subject Interfaces
class WeatherData : public Subject {
    std::vector<Observer *> observers; // observers

    float temp = 0.0f;
    float humidity = 0.0f;
    float pressure = 0.0f;

public:

    void registerObserver(Observer *observer) override;

    void removeObserver(Observer *observer) override;

    void notifyObservers() override;

    /**
     * Set the new state of the weather station
     * @param temp new temperature
     * @param humidity new humidity
     * @param pressure new pressure
     */
    void setState(float temp, float humidity, float pressure);

};
