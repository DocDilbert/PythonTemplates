#include <stdio.h>
#include "observer.h"
#include "WeatherData.h"
#include "Client.h"

#define CATCH_CONFIG_MAIN  // This tells Catch to provide a main() - only do this in one cpp file
#include "catch.hpp"

unsigned int Factorial( unsigned int number ) {
    return number <= 1 ? number : Factorial(number-1)*number;
}


TEST_CASE( "Factorials are computed", "[factorial]" ) {
    REQUIRE( Factorial(1) == 1 );
    REQUIRE( Factorial(2) == 2 );
    REQUIRE( Factorial(3) == 6 );
    REQUIRE( Factorial(10) == 3628800 );

    WeatherData weatherStation;
    Client one(1), two(2), three(3);

    float temp, humidity, pressure;

    weatherStation.registerObserver(&one);
    weatherStation.registerObserver(&two);
    weatherStation.registerObserver(&three);

    weatherStation.setState(temp,humidity,pressure);

    weatherStation.removeObserver(&two);

    weatherStation.setState(temp,humidity,pressure);

}

