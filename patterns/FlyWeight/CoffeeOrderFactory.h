#pragma once

#include <stdlib.h>
#include <map>
#include <string>
#include "CoffeeFlavor.h"

//FlyweightFactory object
class CoffeeFlavorFactory 
{
    std::map<std::string, CoffeeFlavor> flavors;

public:

    CoffeeFlavor getCoffeeFlavor(std::string flavorName) 
    {
        auto it = flavors.find(flavorName);
        if (it == flavors.end())
        {
            CoffeeFlavor flavor(flavorName);
            flavors.emplace(flavorName, flavor);
            return flavor;
        } 
        else
        {
            return it->second;
        }
    }

    int getTotalCoffeeFlavorsMade() 
    {
        return flavors.size();
    }
};