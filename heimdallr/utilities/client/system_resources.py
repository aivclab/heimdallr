from typing import Dict, Mapping, Tuple

import psutil

__all__ = ["get_list_of_process_sorted_by_memory"]


def select(mapping: Mapping, *a) -> Mapping:
    return {k: v for k, v in mapping.items() if k in a}


def get_list_of_process_sorted_by_memory(
    attrs: Tuple = ("name", "username"), scaling: float = (1024 ** 2), top_k: int = 10
) -> Dict:
    """
    Get list of running process sorted by Memory Usage
    """
    list_of_proc_objects = []  # TODO: REFACTOR TO PID,VAL DICT DIRECTLY?
    for proc in psutil.process_iter():
        try:
            proc_info = proc.as_dict(attrs={"pid", *attrs})
            proc_info["vms"] = proc.memory_info().vms / scaling
            list_of_proc_objects.append(proc_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    sorted_entries = sorted(
        list_of_proc_objects, key=lambda proc_obj: proc_obj["vms"], reverse=True
    )
    if top_k:
        sorted_entries = sorted_entries[:top_k]
    return {v["pid"]: select(v, "vms", *attrs) for v in sorted_entries}


if __name__ == "__main__":

    def main():
        print("*** Iterate over all running process and print process ID & Name ***")
        for proc in psutil.process_iter():
            try:
                process_name = proc.name()
                process_id = proc.pid
                print(process_name, " ::: ", process_id)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        print("*** Create a list of all running processes ***")

    def all_info_procs():
        list_of_process_names = list()
        for proc in psutil.process_iter():
            p_info_dict = proc.as_dict()
            list_of_process_names.append(p_info_dict)
        for elem in list_of_process_names:
            print(elem)

    # main()
    print(get_list_of_process_sorted_by_memory())
    # all_info_procs()
