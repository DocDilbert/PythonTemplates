#include <stdio.h>
#include "observer.h"
#include "WeatherData.h"
#include "Client.h"

#define CATCH_CONFIG_MAIN  // This tells Catch to provide a main() - only do this in one cpp file
#include "catch.hpp"

unsigned int Factorial( unsigned int number ) {
    return number <= 1 ? number : Factorial(number-1)*number;
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

