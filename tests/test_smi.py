import sys

import pytest

# Fixture to initialize and finalize nvml
if sys.platform == "linux":
    from heimdallr.utilities.nvidia.smi_parsing import NvidiaSMI


@pytest.mark.skipif(sys.platform != "linux", reason="Test only on linux")
@pytest.fixture(scope="module")
def smi(request):
    """ """
    return NvidiaSMI.getInstance()


@pytest.mark.skipif(sys.platform != "linux", reason="Test only on linux")
@pytest.fixture
def ngpus(smi):
    """ """
    result = smi.DeviceQuery("count")["count"]
    assert result > 0
    print("[" + str(result) + " GPUs]", end=" ")
    return result


## ---------------------------- ##
##       Start Query Tests      ##
## ---------------------------- ##

# Test free-memory query


@pytest.mark.skipif(sys.platform != "linux", reason="Test only on linux")
def test_query_memory(ngpus, smi):
    result = smi.DeviceQuery("memory.free")
    for i in range(ngpus):
        assert result["gpu"][i]["fb_memory_usage"]["free"] >= 0


# Test gpu-utilization query
@pytest.mark.skipif(sys.platform != "linux", reason="Test only on linux")
def test_gpu_utilization(ngpus, smi):
    for i in range(ngpus):
        result = smi.DeviceQuery("utilization.gpu")["gpu"][i]["utilization"]["gpu_util"]
        assert result >= 0


# Test memory-utilization query
@pytest.mark.skipif(sys.platform != "linux", reason="Test only on linux")
def test_memory_utilization(ngpus, smi):
    for i in range(ngpus):
        result = smi.DeviceQuery("utilization.memory")["gpu"][i]["utilization"][
            "memory_util"
        ]
        assert result >= 0


# Test pstate query
@pytest.mark.skipif(sys.platform != "linux", reason="Test only on linux")
def test_pstate(ngpus, smi):
    for i in range(ngpus):
        result = smi.DeviceQuery("pstate")["gpu"][i]["performance_state"]
        assert result[0] == "P"


# Test temperature query
@pytest.mark.skipif(sys.platform != "linux", reason="Test only on linux")
def test_temperature(ngpus, smi):
    for i in range(ngpus):
        temp = smi.DeviceQuery("temperature.gpu")["gpu"][i]["temperature"]["gpu_temp"]
        max_temp = smi.DeviceQuery("temperature.gpu")["gpu"][i]["temperature"][
            "gpu_temp_max_threshold"
        ]
        assert (temp > 0) and (temp < max_temp)
