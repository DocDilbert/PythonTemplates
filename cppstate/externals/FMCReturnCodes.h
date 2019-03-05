///
/// \file FMCReturnCodes.h
/// \copyright Festo AG & Co. KG, Esslingen. All rights reserved.
/// \author cgg (Owner)
/// $Revision: $
/// \brief This file implements the all possible Festo return codes and some useful macros to work with them.
///
#pragma once

/// List of all possible Festo return codes.
typedef enum
{
    // Generic return codes
    /// Everything worked fine. No error happened.
    RC_SUCCESS = 0, // 0
    /// Fail during Call
    RC_FAIL, // 1
    /// The state is at this time undefined
    RC_WORK_IN_PROCESS, // 2
    /// An invalid ID was supplied
    RC_UNKNOWN_ID, // 3
    /// A null pointer check failed.
    RC_NULLPOINTER, // 4
    /// The supplied buffer was to small.
    RC_BUFFER_TOO_SMALL, // 5
    /// The given value is below minimum.
    RC_RANGE_BELOW_MIN, // 6
    /// The given value is above maximum.
    RC_RANGE_ABOVE_MAX, // 7
    /// The enum value is not supported
    RC_ENUM_VALUE_NOT_SUPPORTED, // 8
    /// The supplied parameter(s) are invalid.
    RC_INVALID_PARAMETER, // 9
    /// The access was denied.
    RC_ACCESS_DENIED, // 10
    /// The requested action was denied because the component is out of RAM memory.
    RC_OUT_OF_MEMORY, // 11
    /// There is no space left on the storage medium (file system, EEPROM, ...).
    RC_DISK_FULL, // 12
    /// The requested state transtion is not allowed.
    RC_INVALID_STATE_TRANSITION, // 13
    /// The requested method/function is currently not implemented.
    RC_NOT_IMPLEMENTED, // 14
    /// The method is asynchronous and will return its results at later time.
    RC_ASYNCHRONOUS_CALL, // 15
    /// The requested data is not available
    RC_DATA_NOT_AVAILABLE, // 16
    /// No more data is available (e.g. end of file)
    RC_NO_MORE_DATA, // 17
    /// The requested initialization of the component failed
    RC_INITIALIZATION_FAILED, // 18
    /// The request is not valid because the initialization was not completed.
    RC_INITIALIZATION_NOT_COMPLETED, // 19
    /// The requested resource was not ready
    RC_ERROR_NOT_READY, // 20
    /// The address is not aligned correctly
    RC_ERROR_ADDRESS_ALIGNMENT, // 21
    /// Overrun
    RC_OVERRUN, // 22
    /// Timeout
    RC_TIMEOUT, // 23
    /// The maximum number of connections is reached
    RC_TOO_MANY_CONNECTIONS, // 24
    /// an division by zero operation was avoided
    RC_DIVISON_BY_ZERO, // 25
    /// requested index is not available
    RC_INDEX_OUT_OF_RANGE, // 26
    /// Fpga Image missing
    RC_FPGA_LOADER_IMAGE_MISSING, // 27
    ///
    RC_UNINITIALIZED, // 28
    /// The data is not valid
    RC_DATA_NOT_VALID, // 29
    /// a compatibility issue occurred
    RC_NOT_COMPATIBLE, // 30
    /// a write error occurred
    RC_NOT_WRITABLE, // 31
    /// a read error occurred
    RC_NOT_READABLE, // 32
    /// an internal error occurred
    RC_INTERNAL_ERROR, // 33
    ///
    RC_INVALID_DATATYPE, // 34
    ///
    RC_ARRAY_NOT_DEFINED, // 35
    /// maxium number of pdo elements reached
    RC_COE_PDO_EXCEEDED, // 36
    /// no complete access possible
    RC_COE_COMPLETE_ACCESS_NOT_SUPPORTED, // 37
    /// timeout in fieldbus communication
    RC_FIELDBUS_TIMEOUT, // 38

    RC_FIELDBUS_SEND_WRITE_RESPONSE_FAILED, // 39

    RC_FIELDBUS_SEND_READ_RESPONSE_FAILED, // 40

    RC_FIELDBUS_SEND_DIAG_MESSAGE_FAILED,

    RC_FIELDBUS_PNU_MAPPER_CONTROL_STATUS_NULL,
    ///
    RC_DMA_INIT_ERROR = 0x101, ///< Oops. The dma initialization returned an error.
} FMCReturnCode;

/// \brief This function is used to prevent overwriting the return code, once an error is received
/// \param oldReturnCode old (current) return code value
/// \param newReturnCode new return code value
void keepFirstErrorCode(FMCReturnCode &oldReturnCode, FMCReturnCode newReturnCode);

/// This macro checks the return code of \_FUNC\_. If RC_SUCESS is returned, the program flow continues. If
///  an error is returned, the macro returns this error.
#define RET(_FUNC_)\
    {\
        FMCReturnCode __re = _FUNC_;\
        if (__re != RC_SUCCESS)\
        {\
            return __re;\
        }\
    }

/// This macro checks if the pointer \_PTR\_ is a nullpointer. If it is a nullpointer, RC_NULLPOINTER is returned. If it's not
/// a nullpointer, the program flow continues.
#define RETNULL(_PTR_)\
    {\
        if (!_PTR_)\
        {\
            return RC_NULLPOINTER;\
        }\
    }

