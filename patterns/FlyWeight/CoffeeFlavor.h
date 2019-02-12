#pragma once

#include <stdlib.h>
#include <string>

#include "CoffeeOrder.h"

// ConcreteFlyweight object that creates ConcreteFlyweight
class CoffeeFlavor : CoffeeOrder 
{
    static int idCounter;

public:
    std::string flavor;
    int id;

    CoffeeFlavor(std::string newFlavor) 
    {
        this->flavor = newFlavor;
        id = idCounter++;
    }

    std::string getFlavor() 
    {
        return this->flavor;
    }

    /// Der Kontext wird von allen FlyWeights geteilt. Dieser kann entweder
    /// einer Methode direkt übergeben werden oder aber innerhalb des FlyWeights
    /// als Pointer oder Referenz gespeichert werden.
    void serveCoffee(CoffeeOrderContext context) 
    {
        // System.out.println("Serving Coffee flavor " + flavor + " to table number " + context.getTable());
    }
};
