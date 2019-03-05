///
/// \file FMCTypes.h
/// \copyright Festo AG & Co. KG, Esslingen. All rights reserved.
/// \author erfe (Owner)
/// $Revision: $
///
#pragma once

#ifdef __cplusplus
    #include <cstddef>
    #include <cstdint>
#else
    #include <stdint.h>
#endif

#if defined(__GNUC__) || (defined _MSC_VER)
    //----------------------------------------------------------------------------------------------
    // All GNU Compilers
    //----------------------------------------------------------------------------------------------

    #ifdef FESTO_TYPES_COMPILER_FOUND_
        #error multiple compiler sections match
    #else
        #define FESTO_TYPES_COMPILER_FOUND_
    #endif

    /// Definition of a boolean type.
    #ifdef __cplusplus
        typedef bool BOOL;
    #elif defined(MATLAB)
        typedef bool BOOL;
    #else
        //#pragma message "nurC"
        typedef unsigned char BOOL;
    #endif

    #ifdef __cplusplus
        /// Definition of true.
        #define true true
        /// Definition of false.
        #define false false
    #else
        /// Definition of true.
        #define true (1)
        /// Definition of false.
        #define false (0)

    #endif

    typedef char CHAR;

    typedef uint8_t UINT08;
    typedef int8_t SINT08;

    typedef uint16_t UINT16;
    typedef int16_t SINT16;

    typedef uint32_t UINT32;
    typedef int32_t SINT32;

    typedef uint64_t UINT64;
    typedef int64_t SINT64;

    /// Definition of a 64-bit time.
    typedef UINT64 TIME;

    typedef float FLOAT32;
    typedef double FLOAT64;

    typedef union
    {
        FLOAT32 f32;
        UINT32 u32;
        SINT32 i32;
    } F32UNION;

    typedef union
    {
        FLOAT32 f32[2];
        UINT32  u32[2];
        SINT32  i32[2];
        FLOAT64 f64;
        UINT64  u64;
        SINT64  i64;
    } F64UNION;

    typedef struct
    {
        UINT64 low;
        SINT64 high;
    } int128sub;

    typedef struct
    {
        UINT32 lw_low;
        UINT32 lw_high;
        UINT32 hw_low;
        SINT32 hw_high;
    } int2x64sub;

    typedef struct
    {
        SINT64 quotienth;
        UINT64 quotientl;
        SINT32 modulo;
    } ResultDiv128;

    typedef union
    {
        int2x64sub i32;
        int128sub i64;
    } int128var;

    typedef struct
    {
        SINT32 high;
        UINT32 low;
    } int64sub;

    typedef struct
    {
        UINT32 high;
        UINT32 low;
    } usign64sub;

    // Reihenfolge entspricht LEON3 Normierung
    typedef struct
    {
        SINT32 high;
        SINT32 low;
    } int32separate;

    typedef union
    {
        int64sub        i32;        // Zugriff als 64bit Integer
        usign64sub      u32;        // Zugriff als 64bit Unsigned
        SINT64          i64;
        UINT64          u64;
        int32separate   isep;       // 2x int32
        SINT16          u16[4];     // 4x word
        unsigned char   u8[8];      // 8x byte
    } int64var;

    typedef int64var usign64var;

    typedef struct
    {
        FLOAT32 re;
        FLOAT32 im;
    } CFLOAT32;

    #ifndef NULL
    #define NULL (void *)0

    #endif // defined(__GNUC__)
#endif


#ifndef FESTO_TYPES_COMPILER_FOUND_
    #error no compiler section matches
#else
    #undef FESTO_TYPES_COMPILER_FOUND_
#endif


#ifndef MIN
// Returns the minimum value out of two values
#define MIN( X, Y )  ((X) < (Y) ? (X) : (Y))
#endif

#ifndef MAX
// Returns the maximum value out of two values
#define MAX( X, Y )  ((X) > (Y) ? (X) : (Y))
#endif


// Returns the dimension of an array
#define DIM_UINT32( X )   (static_cast<UINT32>((sizeof(X)) / (sizeof(X[0]))))
#define DIM_UINT16( X )   (static_cast<UINT16>((sizeof(X)) / (sizeof(X[0]))))
#define DIM_SINT32( X )   (static_cast<SINT32>((sizeof(X)) / (sizeof(X[0]))))
#define DIM_SINT16( X )   (static_cast<SINT16>((sizeof(X)) / (sizeof(X[0]))))

