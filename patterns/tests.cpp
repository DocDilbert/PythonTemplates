#include <stdio.h>
#include "observer.h"
#include "Client.h"
#include "WeatherData.h"

#include "CoffeeOrderFactory.h"


#define CATCH_CONFIG_MAIN  // This tells Catch to provide a main() - only do this in one cpp file
#include "catch.hpp"



TEST_CASE( "FlyWeight Tests") 
{
    // Durch Zwischenspeicherung der Geschmäcker in einer Map in der Factory wird
    // jeweils nur ein Objekt des gleichen Geschmacks erzeugt und damit Speicherplatz gespart. 
    CoffeeFlavorFactory flavorFactory;
    
    auto flavor1 = flavorFactory.getCoffeeFlavor("Cappuccino");
    auto flavor2 = flavorFactory.getCoffeeFlavor("Frappe");
    auto flavor3 = flavorFactory.getCoffeeFlavor("Cappuccino");

    REQUIRE( flavor1.id == 0 );
    REQUIRE( flavor2.id == 1 );
    REQUIRE( flavor1.id == flavor3.id );

    // Diese Daten werden von jedem FlyWeight geteilt. 
    // An den Tischen können verschiedene Kaffeesorten serviert werden.
    auto context_table_1 = CoffeeOrderContext(1);
    auto context_table_2 = CoffeeOrderContext(2);

    // Die verschiedenen Kaffeesorten an verschiedene Tische servieren
    flavor1.serveCoffee(context_table_1);
    flavor1.serveCoffee(context_table_2);
}

TEST_CASE( "Observer Tests") 
{
    WeatherData weatherStation;
    Client A, B, C;

    weatherStation.registerObserver(&A);
    weatherStation.registerObserver(&B);
    weatherStation.registerObserver(&C);

    weatherStation.setState(1.0,2.0,3.0);

    REQUIRE( A.temp == Approx( 1.0 ) );
    REQUIRE( A.humidity ==Approx( 2.0 ) );
    REQUIRE( A.pressure == Approx( 3.0 ) );

    REQUIRE( B.temp == Approx( 1.0 ) );
    REQUIRE( B.humidity ==Approx( 2.0 ) );
    REQUIRE( B.pressure == Approx( 3.0 ) );

    REQUIRE( C.temp == Approx( 1.0 ) );
    REQUIRE( C.humidity ==Approx( 2.0 ) );
    REQUIRE( C.pressure == Approx( 3.0 ) );

    weatherStation.removeObserver(&B);
    weatherStation.setState(1.0,1.0,1.0);

    REQUIRE( A.temp == Approx( 1.0 ) );
    REQUIRE( A.humidity ==Approx( 1.0 ) );
    REQUIRE( A.pressure == Approx( 1.0 ) );

    REQUIRE( B.temp == Approx( 1.0 ) );
    REQUIRE( B.humidity ==Approx( 2.0 ) );
    REQUIRE( B.pressure == Approx( 3.0 ) );

    REQUIRE( C.temp == Approx( 1.0 ) );
    REQUIRE( C.humidity ==Approx( 1.0 ) );
    REQUIRE( C.pressure == Approx( 1.0 ) );

}

