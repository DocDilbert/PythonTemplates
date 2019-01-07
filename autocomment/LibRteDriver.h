///
/// \file
/// \copyright Festo AG & Co. KG, Esslingen. All rights reserved.
/// \author cgg
///
/// Definition of the driver component to use libRTE in a oop environment
///
#pragma once

#include "IRteConfiguration.h"
#include "LibRteDeviceDescription.h"
#include "LibRteDiagnosis.h"
#include "LibRteFirmwareUpdateChannel.h"
#include "LibRteMailboxManager.h"
#include "LibRteModuleConfig.h"
#include "LibRteNrtDriver.h"
#include "LibRteProcessManager.h"
#include "LibRteWatchdog.h"
#include "FMCTypes.h"
#include "FMCReturnCodes.h"

#include "ComponentBaseLrte.h"
#include "librte.h"
#include "sciopta.h"
#include "inline.h"

#include "IEtherCatDriver.h"
#include "IProfiNetDriver.h"
#include "IDeviceIdentification.h"
#include "IMemory.h"
#include "IPhysicalGpioChannel.h"
#include "IDeviceShutdown.h"
#include "ISoftReset.h"
#include "IEtherCatStateChangeObserver.h"
#include "ICoeServiceDataHandler.h"
#include "IProcessDataConfigurationHandler.h"
#include "ICommunicationInformation.h"
#include "IHardwareInformation.h"
#include "IFirmwareVersionInformation.h"
#include "IEtherCatStateChangeHandler.h"
#include "ILed.h"

#include <atomic>

#define LIBRTE_FIELDBUS_TIMEOUT_IN_S         (1.5f)      ///< Timeout when no free mailbox is available (in seconds)
#define LIBRTE_MAILBOX_LOCK_TIMEOUT_IN_S     (1.5f)      ///< Timeout for a mailbox configuration lock that takes too long (in seconds)

#define LIBRTE_SLEEP_TIME_IN_MS              (10)       ///< Time to sleep to wait for a request to terminate
#define LIBRTE_SLEEP_TIME_LOCK_IN_MS         (1)        ///< Time to sleep to wait for the lock (lock has shorter sleep time)

namespace DSL
{
namespace Drivers
{

/// This class is essentially a wrapper between the object oriented world of c++
/// and the ansi c librte implementation.
class LibRteDriver :
    public Autogen::ComponentBaseClasses::ComponentBaseLrte,
    public Interfaces::IEtherCatDriver,
    public Interfaces::IProfiNetDriver,
    public Interfaces::ILedTest
{
public:
    /// Default constructor
    LibRteDriver();

    /// Initialize the component:basic communication with fieldbus chip
    /// \param processP0Handler A reference to a librte process handler interface
    /// \param processP1Handler A reference to a librte process handler interface
    /// \param processP2Handler A reference to a librte process handler interface
    /// \param moduleConfig TODO
    /// \param communicationInformation interface for identifier of protocol variant EtherCAT, PROFINET, ...
    /// \param powerFailRTE power fail output signal for RTE Controller
    /// \param chipReset reset output
    /// \param pdIrq pdIrq output
    /// \param mbxIrq mailbox output
    /// \param memory reference to memory management component for file access
    /// \param deviceShutdown reference to device shutdown component (this interface informs when a shutdown will happen)
    /// \param reset TODO
    /// \param hardwareInformation TODO
    /// \param firmwareVersionInformation TODO
    FMCReturnCode initBase(
        LibRteProcessHandler& processP0Handler,
        LibRteProcessHandler& processP1Handler,
        LibRteProcessHandler& processP2Handler,
        LibRteModuleConfig& moduleConfig,
        Interfaces::ICommunicationInformation& communicationInformation,
        Interfaces::IPhysicalGpioChannel& powerFailRTE,
        Interfaces::IPhysicalGpioChannel& chipReset,
        Interfaces::IPhysicalGpioChannel& pdIrq,
        Interfaces::IPhysicalGpioChannel& mbxIrq,
        Interfaces::IMemory& memory,
        Interfaces::IDeviceShutdown& deviceShutdown,
        Interfaces::ISoftReset& reset,
        Interfaces::IHardwareInformation & hardwareInformation,
        Interfaces::IFirmwareVersionInformation& firmwareVersionInformation
    );

    /// Sends all necessary device informations to bring librte into operational state
    /// \param deviceIdent  class providing device identification code
    FMCReturnCode sendDeviceInformations(Interfaces::IDeviceIdentification& deviceIdent);

    /// doLedTest at rte controller
    // \param state send led state
    FMCReturnCode doLedTest(const Autogen::LedTestStates state);

    /// Enables periodic transfers in librte
    void enableProcessDataTransfer();

    /// Enables LibRTE specific irqs
    void startCyclicOperation();

    /// Get Process ID of acyclic process
    /// \retval ID of acyclic process (SC_ILLEGAL_PID in case of error)
    sc_pid_t getPidP0() const;

    /// Get Process ID of acyclic process
    /// \retval ID of acyclic process (SC_ILLEGAL_PID in case of error)
    sc_pid_t getPidP1() const;

    /// Get Process ID of acyclic process
    /// \retval ID of acyclic process (SC_ILLEGAL_PID in case of error)
    sc_pid_t getPidP2() const;

    /// Get diagnosis handler for consumer registration
    /// \return reference to diagnosis handler sub-component
    LibRteDiagnosis& getDiagnosisHandler();

    /// Returns memory channel for RTE chip firmware update
    /// \return reference to firmware update channel
    Interfaces::IMemory& getMemoryChannel();

    /// Returns protocol layer access to RTE chip
    /// \return pointer to libRTE driver
    rte_driver_t* getBaseDriver();

    /// Returns a reference to the nrt driver
    LibRteNrtDriver& getNrtDriver();

    /// cyclic method to update watchdog sub-component
    void updateWatchdog();

    /// cyclic method to check mailboxes for new messages
    /// note: if new messages are found here, the respective callback routines are executed
    void updateAsync();

    /// cyclic method to check device shutdown for power fail signaling to RTE controller
    void checkDeviceShutdown();

    /// Returns a reference to the Lib Rte Mailbox handler
    LibRteMailboxManager& getMailboxManager();

    /// Returns a reference to the Lib Rte Mailbox handler
    LibRteProcessManager& getProcessManager();

    /// \copydoc Interfaces::IEtherCatDriver
    void newPDxData(void *data, size_t buf_size);

    /// \copydoc Interfaces::IEtherCatDriver
    Interfaces::PdState processPDxData(void *buf, size_t buf_size);

    /// Returns the polling time of process p0.
    AINLINE UINT32 getPollTimeP0()
    {
        auto updateCycle = data_Get_updateCycle();
        UINT32 pollTime = static_cast<UINT32>(updateCycle * 1000.0f);
        return pollTime;
    }

    /// Raises an out of order read error
    AINLINE void raiseOutOfOrderReadError()
    {
        this->diag_Set_comModuleOutOfOrderRead();
    }

    /// Raises an librte watchdog error
    AINLINE void raiseWatchdogError()
    {
        if ((!this->softResetInterface->isSoftResetRequested()) && (!this->shutdownInterface->isShutdownActive()))
        {
            // avoid watchdogError on soft reset
            // todo: is watchdogError really necessary if system is beeing shutdown?
            this->diag_Set_comModuleWatchdogError(true);
        }
    }

    /// Raises a fieldbus timeout error when mailbox can not be used
    AINLINE void raiseComModuleMailboxTimeoutError(UINT32 errorId)
    {
        this->diag_Set_comModuleMailboxTimeoutError(errorId);
    }

    /// Raises a fieldbus internal communication error
    AINLINE void raiseComModuleInternalCommunicationError(UINT32 processId, UINT32 returnCode)
    {
        this->diag_Set_comModuleInternalCommunicationError(processId, returnCode);
    }

    // ****************************************************************************
    // IRQ related stuff
    // ****************************************************************************
    /// Set state of process data irq
    /// \param state  set/reset irq line
    void pdIrqSetState(bool state);

    /// Set state of mailbox irq
    /// \param state  set/reset irq line
    void mbxIrqSetState(bool state);

    // ****************************************************************************
    // CANOpen over EtherCat specific methods (COE)
    // All methods here are included in the IEtherCatDriver interface
    // ****************************************************************************

    /// see Interfaces::ILibRteDriver
    /// Additional notes: Can be called from every process except LibRteDriver.
    void sendCoeServiceDataReadRequest(UINT32 index, UINT32 subIndex, UINT32 dataSize, bool completeAccess);

    /// Registers a handler for service data processing.
    /// Attention: Only one handler can be registered. If you register more than one the last one registered will be called
    /// \param serviceDataHandler A reference to the handler
    void registerCoeServiceDataHandler(Interfaces::ICoeServiceDataHandler& serviceDataHandler);

    /// Registers a handler for foe data processing.
    /// \param foeHandler A reference to the handler
    void registerFoeServiceDataHandler(Interfaces::IFoeHandler& foeHandler);

    /// Registers a handler for process data configuration requests.
    /// \param pdConfigHandler  interface to component handling process data configuration requests
    void registerProcessDataConfigurationHandler(Interfaces::IProcessDataConfigurationHandler& pdConfigHandler);

    // ****************************************************************************
    // Methods used for driver statistic output
    // ****************************************************************************
    /// Increments p0 process counter
    AINLINE void incrementStats_cyclesP0()
    {
        data_Set_stats_cyclesP0(data_Get_stats_cyclesP0() + 1);
    }

    /// Increments p1 process counter
    AINLINE void incrementStats_cyclesP1()
    {
        data_Set_stats_cyclesP1(data_Get_stats_cyclesP1() + 1);
    }

    /// Increments p2 process counter
    AINLINE void incrementStats_cyclesP2()
    {
        data_Set_stats_cyclesP2(data_Get_stats_cyclesP2() + 1);
    }

    /// Increments the process esm ack counter
    AINLINE void incrementStats_processSendEsmAck()
    {
        data_Set_stats_processSendEsmAck(data_Get_stats_processSendEsmAck() + 1);
    }

    /// Increments the the process sdo request counter
    AINLINE void incrementStats_processSendSdoReadRequest()
    {
        data_Set_stats_processSendSdoReadRequest(data_Get_stats_processSendSdoReadRequest() + 1);
    }

    /// Increments the process send diagnosis message counter
    AINLINE void incrementStats_processSendDiagnosisMessage()
    {
        data_Set_stats_processSendDiagnosisMessage(data_Get_stats_processSendDiagnosisMessage() + 1);
    }

    /// Increments the process receive module config request counter
    AINLINE void incrementStats_processModuleConfigRequest()
    {
        data_Set_stats_processModuleConfigRequest(data_Get_stats_processModuleConfigRequest() + 1);
    }

    /// Increments the process receive esm request counter
    AINLINE void incrementStats_processEsmRequest()
    {
        data_Set_stats_processEsmRequest(data_Get_stats_processEsmRequest() + 1);
    }

    /// Increments the as read response frame received counter
    AINLINE void incrementStats_frameAsReadResponse()
    {
        data_Set_stats_frameAsReadResponse(data_Get_stats_frameAsReadResponse() + 1);
    }

    /// Increments the read frame received counter
    AINLINE void incrementStats_frameAsRead()
    {
        data_Set_stats_frameAsRead(data_Get_stats_frameAsRead() + 1);
    }

    /// Increments the as write frame received counter
    AINLINE void incrementStats_frameAsWrite()
    {
        data_Set_stats_frameAsWrite(data_Get_stats_frameAsWrite() + 1);
    }

    /// Increments the esm state change frame received counter
    AINLINE void incrementStats_frameEsmStateChange()
    {
        data_Set_stats_frameEsmStateChange(data_Get_stats_frameEsmStateChange() + 1);
    }

    /// Increments the module config frame received counter
    AINLINE void incrementStats_frameModuleConfig()
    {
        data_Set_stats_frameModuleConfig(data_Get_stats_frameModuleConfig() + 1);
    }


    virtual FMCReturnCode updateProfinetModuleConfiguration();

    /// returns true when sendDeviceInformations() has been finished
    BOOL isSendDeviceInformationDone()
    {
        return static_cast<BOOL>(sendDeviceInformationDone);
    }


private:

    /// Sends ethercat device information to the librte.
    /// \param explDevId Explicit device id
    FMCReturnCode sendEtherCatDeviceIdentification(UINT16 explDevId);

    /// Sends profinet device information to the librte.
    /// \param macAddress The to be used mac address of the profinet device
    /// \param deviceTypeName The device type name of the profinet device
    /// \param deviceId The device id of the profinet device
    /// \param dapModuleId The dap module id of the profinet device
    FMCReturnCode sendProfiNetDeviceIdentification(
        Interfaces::IDeviceIdentification& deviceIdent
    );

    /// is true when sendDeviceInformations() has been finished
    std::atomic<BOOL> sendDeviceInformationDone;

    /// Generic driver structure for data exchange with libRTE
    rte_driver_t appDriver;

    LibRteNrtDriver nrtDriver;

    LibRteMailboxManager mailboxManager;

    /// holds sub-component for firmware updates
    LibRteFirmwareUpdateChannel firmwareUpdateChannel;

    /// holds sub-component for device description file
    LibRteDeviceDescription deviceDescription;

    /// holds a reference to a sub-component used for module configuration
    LibRteModuleConfig* moduleConfig;

    /// holds sub-component for libRTE diagnosis
    LibRteDiagnosis diagnosis;

    /// holds sub-component for watchdog handling
    LibRteWatchdog watchdog;

    /// holds channel to process data irq
    Interfaces::IPhysicalGpioChannel* pdIrq;

    /// holds channel to mailbox irq
    Interfaces::IPhysicalGpioChannel* mbxIrq;

    /// holds channel to reset the rte chip
    Interfaces::IPhysicalGpioChannel* chipReset;

    /// holds channel to reset the rte chip
    Interfaces::IPhysicalGpioChannel* powerFailRTE;

    /// Holds interface to shutdown
    Interfaces::IDeviceShutdown* shutdownInterface;

    /// Holds interface to softReset
    Interfaces::ISoftReset* softResetInterface;

    /// Holds interface to communicationInformation (protocol type, hardware type)
    Interfaces::ICommunicationInformation* communicationInformation;

    /// Holds interface to hardwareInformation
    Interfaces::IHardwareInformation* hardwareInformation;

    /// Holds interface to firmwareVersionInformation
    Interfaces::IFirmwareVersionInformation* firmwareVersionInformation;

    /// Holds the currently active protocol type
    Autogen::ComProtocolType comProtocolType;

    /// The lib rte process Manager. This class handles the registration to the librte process p0, p1, p2
    LibRteProcessManager processManager;

    /// Abstract fieldbus process handler
    LibRteProcessHandler* processP0Handler;

    /// Abstract fieldbus process handler
    LibRteProcessHandler* processP1Handler;

    /// Abstract fieldbus process handler
    LibRteProcessHandler* processP2Handler;

};


}}
