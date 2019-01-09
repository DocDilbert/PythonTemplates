///
/// \file
/// \copyright Festo AG & Co. KG, Esslingen. All rights reserved.
/// \author de6u4437 (Owner)
/// $Revision: $
///
#pragma once

#include "ComponentBaseUft.h"
#include "ComponentCommon.h"
#include "FMCReturnCodes.h"
#include "FMCTypes.h"
#include "FileHandle.h"
#include "IEngineeringConnection.h"
#include "IFileTransfer.h"
#include "IMemory.h"
#include "IUnifiedFileTransfer.h"

namespace BMC
{
namespace Services
{
namespace FileTransfer
{

class UnifiedFileTransfer :
    public Autogen::ComponentBaseClasses::ComponentBaseUft,
    public Interfaces::IUnifiedFileTransfer,
    public Interfaces::IEngineeringConnection
{
public:
    UnifiedFileTransfer();

    FMCReturnCode init(Interfaces::IMemory& memManager);
    FMCReturnCode registerFileTransferConsumer(Autogen::FileType fileType, Interfaces::IFileTransfer* ftc);

    void notifyConnectionOpen(UINT32 connectionId);
    void notifyConnectionMessage(UINT32 connectionId);
    void notifyConnectionClosed(UINT32 connectionId);

    void method_Execute_readStart(Autogen::methodInputStruct_readStart& in, UINT32 inDataPointerLength, Autogen::methodOutputStruct_readStart& out, UINT32 outDataPointerLength);
    void method_Execute_readData(Autogen::methodInputStruct_readData& in, UINT32 inDataPointerLength, Autogen::methodOutputStruct_readData& out, UINT32 outDataPointerLength);
    void method_Execute_readEnd(Autogen::methodInputStruct_readEnd& in, UINT32 inDataPointerLength, Autogen::methodOutputStruct_readEnd& out, UINT32 outDataPointerLength);

    void method_Execute_writeStart(Autogen::methodInputStruct_writeStart& in, UINT32 inDataPointerLength, Autogen::methodOutputStruct_writeStart& out, UINT32 outDataPointerLength);
    void method_Execute_writeData(Autogen::methodInputStruct_writeData& in, UINT32 inDataPointerLength, Autogen::methodOutputStruct_writeData& out, UINT32 outDataPointerLength);
    void method_Execute_writeEnd(Autogen::methodInputStruct_writeEnd& in, UINT32 inDataPointerLength, Autogen::methodOutputStruct_writeEnd& out, UINT32 outDataPointerLength);

    void readStart(Autogen::methodInputStruct_readStart& in, UINT32 inDataPointerLength, Autogen::methodOutputStruct_readStart& out, UINT32 outDataPointerLength, UINT32 connectionId);
    void readData(Autogen::methodInputStruct_readData& in, UINT32 inDataPointerLength, Autogen::methodOutputStruct_readData& out, UINT32 outDataPointerLength, UINT32 connectionId);
    void readEnd(Autogen::methodInputStruct_readEnd& in, UINT32 inDataPointerLength, Autogen::methodOutputStruct_readEnd& out, UINT32 outDataPointerLength, UINT32 connectionId);

    void writeStart(Autogen::methodInputStruct_writeStart& in, UINT32 inDataPointerLength, Autogen::methodOutputStruct_writeStart& out, UINT32 outDataPointerLength, UINT32 connectionId);
    void writeData(Autogen::methodInputStruct_writeData& in, UINT32 inDataPointerLength, Autogen::methodOutputStruct_writeData& out, UINT32 outDataPointerLength, UINT32 connectionId);
    void writeEnd(Autogen::methodInputStruct_writeEnd& in, UINT32 inDataPointerLength, Autogen::methodOutputStruct_writeEnd& out, UINT32 outDataPointerLength, UINT32 connectionId);


private:
    struct FileTransfer
    {
        bool isActive;
        UINT32 slotNo;
        Autogen::FileType fileType;
        Utilities::FileHandle fileHandle;        /// Holds file handle
        UINT32 connectionId;
    };

    Interfaces::IFileTransfer* ftConsumer[FileType_ELEMENT_COUNT];

    Interfaces::IMemory* memManager;

    FileTransfer readTransfer;
    FileTransfer writeTransfer;

    UINT32 lastConnId;
};

}}}


