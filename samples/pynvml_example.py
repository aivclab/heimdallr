#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 02-12-2020
           """

#################################################################################
# Copyright (c) 2020, NVIDIA Corporation.  All rights reserved.                 #
#                                                                               #
# Redistribution and use in source and binary forms, with or without            #
# modification, are permitted provided that the following conditions are met:   #
#                                                                               #
#    * Redistributions of source code must retain the above copyright notice,   #
#      this list of conditions and the following disclaimer.                    #
#    * Redistributions in binary form must reproduce the above copyright        #
#      notice, this list of conditions and the following disclaimer in the      #
#      documentation and/or other materials provided with the distribution.     #
#    * Neither the name of the NVIDIA Corporation nor the names of its          #
#      contributors may be used to endorse or promote products derived from     #
#      this software without specific prior written permission.                 #
#                                                                               #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"   #
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE     #
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE    #
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE     #
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR           #
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF          #
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS      #
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN       #
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)       #
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF        #
# THE POSSIBILITY OF SUCH DAMAGE.                                               #
#################################################################################

#
# Sample script to demonstrate the usage of NVML API python bindings
#

#
# Helper function
#
from pynvml import (
    NVMLError,
    NVML_BRAND_GEFORCE,
    NVML_BRAND_GEFORCE_RTX,
    NVML_BRAND_GRID,
    NVML_BRAND_NVIDIA,
    NVML_BRAND_NVIDIA_RTX,
    NVML_BRAND_NVIDIA_VAPPS,
    NVML_BRAND_NVIDIA_VCS,
    NVML_BRAND_NVIDIA_VGAMING,
    NVML_BRAND_NVIDIA_VPC,
    NVML_BRAND_NVIDIA_VWS,
    NVML_BRAND_NVS,
    NVML_BRAND_QUADRO,
    NVML_BRAND_QUADRO_RTX,
    NVML_BRAND_TESLA,
    NVML_BRAND_TITAN,
    NVML_BRAND_TITAN_RTX,
    NVML_BRAND_UNKNOWN,
    NVML_ERROR_NOT_SUPPORTED,
    NVML_GPU_VIRTUALIZATION_MODE_HOST_VGPU,
    NVML_GPU_VIRTUALIZATION_MODE_HOST_VSGA,
    NVML_GPU_VIRTUALIZATION_MODE_NONE,
    NVML_GPU_VIRTUALIZATION_MODE_PASSTHROUGH,
    NVML_GPU_VIRTUALIZATION_MODE_VGPU,
    nvmlDeviceGetBrand,
    nvmlDeviceGetCount,
    nvmlDeviceGetGridLicensableFeatures,
    nvmlDeviceGetHandleByIndex,
    nvmlDeviceGetName,
    nvmlDeviceGetPciInfo,
    nvmlDeviceGetSerial,
    nvmlDeviceGetUUID,
    nvmlDeviceGetVirtualizationMode,
    nvmlInit,
    nvmlShutdown,
    nvmlSystemGetDriverVersion,
)


def str_virt(mode):
    """

    Args:
      mode:

    Returns:

    """
    if mode == NVML_GPU_VIRTUALIZATION_MODE_NONE:
        return "None"
    elif mode == NVML_GPU_VIRTUALIZATION_MODE_PASSTHROUGH:
        return "Pass-Through"
    elif mode == NVML_GPU_VIRTUALIZATION_MODE_VGPU:
        return "VGPU"
    elif mode == NVML_GPU_VIRTUALIZATION_MODE_HOST_VGPU:
        return "Host VGPU"
    elif mode == NVML_GPU_VIRTUALIZATION_MODE_HOST_VSGA:
        return "Host VSGA"
    else:
        return "Unknown"


#
# Converts errors into string messages
#
def handle_error(err):
    """

    Args:
      err:

    Returns:

    """
    if err.value == NVML_ERROR_NOT_SUPPORTED:
        return "N/A"
    else:
        return err.__str__()


#######
def device_query():
    """

    Returns:

    """
    str_result = ""
    try:
        #
        # Initialize NVML
        #
        nvmlInit()

        str_result += (
            f"  <driver_version>{str(nvmlSystemGetDriverVersion())}</driver_version>\n"
        )

        device_count = nvmlDeviceGetCount()
        str_result += f"  <attached_gpus>{str(device_count)}</attached_gpus>\n"

        for i in range(0, device_count):
            handle = nvmlDeviceGetHandleByIndex(i)

            pci_nfo = nvmlDeviceGetPciInfo(handle)

            str_result += f'  <gpu id="{pci_nfo.busId}">\n'

            str_result += (
                f"    <product_name>{str(nvmlDeviceGetName(handle))}</product_name>\n"
            )

            brand_names = {
                NVML_BRAND_UNKNOWN: "Unknown",
                NVML_BRAND_QUADRO: "Quadro",
                NVML_BRAND_TESLA: "Tesla",
                NVML_BRAND_NVS: "NVS",
                NVML_BRAND_GRID: "Grid",
                NVML_BRAND_TITAN: "Titan",
                NVML_BRAND_GEFORCE: "GeForce",
                NVML_BRAND_NVIDIA_VAPPS: "NVIDIA Virtual Applications",
                NVML_BRAND_NVIDIA_VPC: "NVIDIA Virtual PC",
                NVML_BRAND_NVIDIA_VCS: "NVIDIA Virtual Compute Server",
                NVML_BRAND_NVIDIA_VWS: "NVIDIA RTX Virtual Workstation",
                NVML_BRAND_NVIDIA_VGAMING: "NVIDIA vGaming",
                NVML_BRAND_QUADRO_RTX: "Quadro RTX",
                NVML_BRAND_NVIDIA_RTX: "NVIDIA RTX",
                NVML_BRAND_NVIDIA: "NVIDIA",
                NVML_BRAND_GEFORCE_RTX: "GeForce RTX",
                NVML_BRAND_TITAN_RTX: "TITAN RTX",
            }

            try:
                # If nvmlDeviceGetBrand() succeeds it is guaranteed to be in the dictionary
                brand_name = brand_names[nvmlDeviceGetBrand(handle)]
            except NVMLError as err:
                brand_name = handle_error(err)

            str_result += f"    <product_brand>{brand_name}</product_brand>\n"

            try:
                serial = nvmlDeviceGetSerial(handle)
            except NVMLError as err:
                serial = handle_error(err)

            str_result += f"    <serial>{serial}</serial>\n"

            try:
                uuid = nvmlDeviceGetUUID(handle)
            except NVMLError as err:
                uuid = handle_error(err)

            str_result += f"    <uuid>{str(uuid)}</uuid>\n"

            str_result += "    <gpu_virtualization_mode>\n"
            try:
                mode = str_virt(nvmlDeviceGetVirtualizationMode(handle))
            except NVMLError as err:
                mode = handle_error(err)
            str_result += f"      <virtualization_mode>{mode}</virtualization_mode>\n"
            str_result += "    </gpu_virtualization_mode>\n"

            try:
                grid_licensable_features = nvmlDeviceGetGridLicensableFeatures(handle)
                if grid_licensable_features.isGridLicenseSupported == 1:
                    str_result += "    <vgpu_software_licensed_product>\n"
                    for i in range(grid_licensable_features.licensableFeaturesCount):
                        if (
                            grid_licensable_features.gridLicensableFeatures[
                                i
                            ].featureState
                            == 0
                        ):
                            if (
                                nvmlDeviceGetVirtualizationMode(handle)
                                == NVML_GPU_VIRTUALIZATION_MODE_PASSTHROUGH
                            ):
                                str_result += "        <licensed_product_name>NVIDIA Virtual Applications</licensed_product_name>\n"
                                str_result += "        <license_status>Licensed</license_status>\n"
                            else:
                                str_result += f"        <licensed_product_name>{str(grid_licensable_features.gridLicensableFeatures[i].productName)}</licensed_product_name>\n"
                                str_result += "        <license_status>Unlicensed</license_status>\n"
                        else:
                            str_result += f"        <licensed_product_name>{str(grid_licensable_features.gridLicensableFeatures[i].productName)}</licensed_product_name>\n"
                            str_result += (
                                "        <license_status>Licensed</license_status>\n"
                            )
                    str_result += "    </vgpu_software_licensed_product>\n"
            except NVMLError as err:
                grid_licensable_features = handle_error(err)

            str_result += "  </gpu>\n"

    except NVMLError as err:
        str_result += f"example.py: {err.__str__()}\n"

    nvmlShutdown()

    return str_result


# If this is not exectued when module is imported
if __name__ == "__main__":
    print(device_query())
