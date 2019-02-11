#pragma once

// Interface eines Observers
class Observer 
{
public:

    /// Update the state of this observer
    /// @param temp new temperaure
    /// @param humidity new humidity
    /// @param pressure new pressure
    virtual void update(float temp, float humidity, float pressure) = 0;
};

