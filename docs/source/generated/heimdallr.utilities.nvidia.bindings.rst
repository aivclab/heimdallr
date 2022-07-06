heimdallr.utilities.nvidia.bindings
===================================

.. automodule:: heimdallr.utilities.nvidia.bindings

   
   
   

   
   
   .. rubric:: Functions

   .. autosummary::
      :toctree:
   
      check_return
      friendly_object_to_struct
      get_func_pointer
      nvmlDeviceClearAccountingPids
      nvmlDeviceClearCpuAffinity
      nvmlDeviceClearEccErrorCounts
      nvmlDeviceFreezeNvLinkUtilizationCounter
      nvmlDeviceGetAPIRestriction
      nvmlDeviceGetAccountingBufferSize
      nvmlDeviceGetAccountingMode
      nvmlDeviceGetAccountingPids
      nvmlDeviceGetAccountingStats
      nvmlDeviceGetApplicationsClock
      nvmlDeviceGetAutoBoostedClocksEnabled
      nvmlDeviceGetBAR1MemoryInfo
      nvmlDeviceGetBoardId
      nvmlDeviceGetBrand
      nvmlDeviceGetBridgeChipInfo
      nvmlDeviceGetClockInfo
      nvmlDeviceGetComputeMode
      nvmlDeviceGetComputeRunningProcesses
      nvmlDeviceGetCount
      nvmlDeviceGetCpuAffinity
      nvmlDeviceGetCurrPcieLinkGeneration
      nvmlDeviceGetCurrPcieLinkWidth
      nvmlDeviceGetCurrentClocksThrottleReasons
      nvmlDeviceGetCurrentDriverModel
      nvmlDeviceGetCurrentEccMode
      nvmlDeviceGetCurrentGpuOperationMode
      nvmlDeviceGetDecoderUtilization
      nvmlDeviceGetDefaultApplicationsClock
      nvmlDeviceGetDetailedEccErrors
      nvmlDeviceGetDisplayActive
      nvmlDeviceGetDisplayMode
      nvmlDeviceGetDriverModel
      nvmlDeviceGetEccMode
      nvmlDeviceGetEncoderUtilization
      nvmlDeviceGetEnforcedPowerLimit
      nvmlDeviceGetFanSpeed
      nvmlDeviceGetGpuOperationMode
      nvmlDeviceGetGraphicsRunningProcesses
      nvmlDeviceGetHandleByIndex
      nvmlDeviceGetHandleByPciBusId
      nvmlDeviceGetHandleBySerial
      nvmlDeviceGetHandleByUUID
      nvmlDeviceGetIndex
      nvmlDeviceGetInforomConfigurationChecksum
      nvmlDeviceGetInforomImageVersion
      nvmlDeviceGetInforomVersion
      nvmlDeviceGetMaxClockInfo
      nvmlDeviceGetMaxPcieLinkGeneration
      nvmlDeviceGetMaxPcieLinkWidth
      nvmlDeviceGetMemoryErrorCounter
      nvmlDeviceGetMemoryInfo
      nvmlDeviceGetMinorNumber
      nvmlDeviceGetMultiGpuBoard
      nvmlDeviceGetName
      nvmlDeviceGetNvLinkCapability
      nvmlDeviceGetNvLinkErrorCounter
      nvmlDeviceGetNvLinkRemotePciInfo
      nvmlDeviceGetNvLinkState
      nvmlDeviceGetNvLinkUtilizationControl
      nvmlDeviceGetNvLinkUtilizationCounter
      nvmlDeviceGetNvLinkVersion
      nvmlDeviceGetPciInfo
      nvmlDeviceGetPcieReplayCounter
      nvmlDeviceGetPcieThroughput
      nvmlDeviceGetPendingDriverModel
      nvmlDeviceGetPendingEccMode
      nvmlDeviceGetPendingGpuOperationMode
      nvmlDeviceGetPerformanceState
      nvmlDeviceGetPersistenceMode
      nvmlDeviceGetPowerManagementDefaultLimit
      nvmlDeviceGetPowerManagementLimit
      nvmlDeviceGetPowerManagementLimitConstraints
      nvmlDeviceGetPowerManagementMode
      nvmlDeviceGetPowerState
      nvmlDeviceGetPowerUsage
      nvmlDeviceGetRetiredPages
      nvmlDeviceGetRetiredPagesPendingStatus
      nvmlDeviceGetSamples
      nvmlDeviceGetSerial
      nvmlDeviceGetSupportedClocksThrottleReasons
      nvmlDeviceGetSupportedEventTypes
      nvmlDeviceGetSupportedGraphicsClocks
      nvmlDeviceGetSupportedMemoryClocks
      nvmlDeviceGetTemperature
      nvmlDeviceGetTemperatureThreshold
      nvmlDeviceGetTopologyCommonAncestor
      nvmlDeviceGetTopologyNearestGpus
      nvmlDeviceGetTotalEccErrors
      nvmlDeviceGetTotalEnergyConsumption
      nvmlDeviceGetUUID
      nvmlDeviceGetUtilizationRates
      nvmlDeviceGetVbiosVersion
      nvmlDeviceGetViolationStatus
      nvmlDeviceOnSameBoard
      nvmlDeviceRegisterEvents
      nvmlDeviceResetApplicationsClocks
      nvmlDeviceResetNvLinkErrorCounters
      nvmlDeviceResetNvLinkUtilizationCounter
      nvmlDeviceSetAPIRestriction
      nvmlDeviceSetAccountingMode
      nvmlDeviceSetApplicationsClocks
      nvmlDeviceSetAutoBoostedClocksEnabled
      nvmlDeviceSetComputeMode
      nvmlDeviceSetCpuAffinity
      nvmlDeviceSetDefaultAutoBoostedClocksEnabled
      nvmlDeviceSetDriverModel
      nvmlDeviceSetEccMode
      nvmlDeviceSetGpuOperationMode
      nvmlDeviceSetNvLinkUtilizationControl
      nvmlDeviceSetPersistenceMode
      nvmlDeviceSetPowerManagementLimit
      nvmlDeviceValidateInforom
      nvmlEventSetCreate
      nvmlEventSetFree
      nvmlEventSetWait
      nvmlInit
      nvmlShutdown
      nvmlSystemGetDriverVersion
      nvmlSystemGetHicVersion
      nvmlSystemGetNVMLVersion
      nvmlSystemGetProcessName
      nvmlSystemGetTopologyGpuSet
      nvmlUnitGetCount
      nvmlUnitGetDeviceCount
      nvmlUnitGetDevices
      nvmlUnitGetFanSpeedInfo
      nvmlUnitGetHandleByIndex
      nvmlUnitGetLedState
      nvmlUnitGetPsuInfo
      nvmlUnitGetTemperature
      nvmlUnitGetUnitInfo
      nvmlUnitSetLedState
      nvml_error_string
      struct_to_friendly_object
   
   

   
   
   .. rubric:: Classes

   .. autosummary::
      :toctree:
      :template: custom_autosummary/class.rst
   
      FriendlyObject
      PrintableStructure
      c_nvmlAccountingStats_t
      c_nvmlBAR1Memory_t
      c_nvmlBridgeChipHierarchy_t
      c_nvmlBridgeChipInfo_t
      c_nvmlDevice_t
      c_nvmlEccErrorCounts_t
      c_nvmlEventData_t
      c_nvmlEventSet_t
      c_nvmlHwbcEntry_t
      c_nvmlLedState_t
      c_nvmlMemory_t
      c_nvmlPSUInfo_t
      c_nvmlPciInfo_t
      c_nvmlProcessInfo_t
      c_nvmlSample_t
      c_nvmlUnitFanInfo_t
      c_nvmlUnitFanSpeeds_t
      c_nvmlUnitInfo_t
      c_nvmlUnit_t
      c_nvmlUtilization_t
      c_nvmlValue_t
      c_nvmlViolationTime_t
      nvmlPciInfo_t
      struct_c_nvmlDevice_t
      struct_c_nvmlEventSet_t
      struct_c_nvmlUnit_t
   
   

   
   
   .. rubric:: Exceptions

   .. autosummary::
      :toctree:
   
      NVMLError
      NVMLError_AlreadyInitialized
      NVMLError_CorruptedInforom
      NVMLError_DriverNotLoaded
      NVMLError_FunctionNotFound
      NVMLError_GpuIsLost
      NVMLError_InsufficientPower
      NVMLError_InsufficientSize
      NVMLError_InvalidArgument
      NVMLError_IrqIssue
      NVMLError_LibRmVersionMismatch
      NVMLError_LibraryNotFound
      NVMLError_NoPermission
      NVMLError_NotFound
      NVMLError_NotSupported
      NVMLError_OperatingSystem
      NVMLError_ResetRequired
      NVMLError_Timeout
      NVMLError_Uninitialized
      NVMLError_Unknown
   
   



