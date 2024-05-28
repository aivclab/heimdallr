from typing import Dict

from warg import is_windows


def get_docker_stats() -> Dict:
    """
      TODO: MAYBE USE
      docker stats --all --format "table {{.Container}}\t{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"


      returns

       {
        "read": "2024-05-27T13:01:14.006005743Z",
        "preread": "2024-05-27T13:01:13.004430972Z",
        "pids_stats": {"current": 27, "limit": 38302},
        "blkio_stats": {
            "io_service_bytes_recursive": [
                {"major": 259, "minor": 0, "op": "read", "value": 8192},
                {"major": 259, "minor": 0, "op": "write", "value": 0},
                {"major": 8, "minor": 0, "op": "read", "value": 49577984},
                {"major": 8, "minor": 0, "op": "write", "value": 12587008},
            ],
            "io_serviced_recursive": None,
            "io_queue_recursive": None,
            "io_service_time_recursive": None,
            "io_wait_time_recursive": None,
            "io_merged_recursive": None,
            "io_time_recursive": None,
            "sectors_recursive": None,
        },
        "num_procs": 0,
        "storage_stats": {},
        "cpu_stats": {
            "cpu_usage": {
                "total_usage": 324337485000,
                "usage_in_kernelmode": 93836364000,
                "usage_in_usermode": 230501120000,
            },
            "system_cpu_usage": 46594618350000000,
            "online_cpus": 20,
            "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0},
        },
        "precpu_stats": {
            "cpu_usage": {
                "total_usage": 324337380000,
                "usage_in_kernelmode": 93836334000,
                "usage_in_usermode": 230501045000,
            },
            "system_cpu_usage": 46594598370000000,
            "online_cpus": 20,
            "throttling_data": {"periods": 0, "throttled_periods": 0, "throttled_time": 0},
        },
        "memory_stats": {
            "usage": 71208960,
            "stats": {
                "active_anon": 18841600,
                "active_file": 8724480,
                "anon": 20594688,
                "anon_thp": 0,
                "file": 48140288,
                "file_dirty": 0,
                "file_mapped": 37302272,
                "file_writeback": 0,
                "inactive_anon": 1753088,
                "inactive_file": 39415808,
                "kernel_stack": 442368,
                "pgactivate": 2,
                "pgdeactivate": 0,
                "pgfault": 99756,
                "pglazyfree": 0,
                "pglazyfreed": 0,
                "pgmajfault": 383,
                "pgrefill": 71,
                "pgscan": 359,
                "pgsteal": 355,
                "shmem": 0,
                "slab": 1681160,
                "slab_reclaimable": 1352096,
                "slab_unreclaimable": 329064,
                "sock": 0,
                "thp_collapse_alloc": 0,
                "thp_fault_alloc": 0,
                "unevictable": 0,
                "workingset_activate": 0,
                "workingset_nodereclaim": 0,
                "workingset_refault": 0,
            },
            "limit": 33547591680,
        },
        "name": "/gitlab-runner",
        "id": "77d48b687be4e1948c2b5a08245d2a73481a95e042686c8c3015fed61b9233b5",
        "networks": {
            "eth0": {
                "rx_bytes": 70139312,
                "rx_packets": 206012,
                "rx_errors": 0,
                "rx_dropped": 0,
                "tx_bytes": 226155543,
                "tx_packets": 380518,
                "tx_errors": 0,
                "tx_dropped": 0,
            }
        },
    }


    """
    import docker  # pip install docker-py

    if is_windows():
        client = docker.Client(base_url="http://localhost:2375")
        for container in client.containers():
            yield dict(client.stats(container, decode=None, stream=False))
    else:
        client = docker.DockerClient(base_url="unix:///var/run/docker.sock")
        for container in client.containers.list():
            yield container.stats(decode=None, stream=False)


if __name__ == "__main__":
    for i in get_docker_stats():
        print(i)
