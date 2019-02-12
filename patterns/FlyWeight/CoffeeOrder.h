#pragma once

#include "CoffeeOrderContext.h"

// Flyweight object interface
class CoffeeOrder 
{
    public:
        virtual void serveCoffee(CoffeeOrderContext context) = 0;
};