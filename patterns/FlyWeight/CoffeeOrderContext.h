#pragma once

class CoffeeOrderContext 
{
public:
   int tableNumber;

   CoffeeOrderContext(int tableNumber) 
   {
       this->tableNumber = tableNumber;
   }

   int getTable() 
   {
       return this->tableNumber;
   }

};