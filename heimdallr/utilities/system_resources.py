import psutil


def get_list_of_process_sorted_by_memory():
    """
    Get list of running process sorted by Memory Usage
    """
    list_of_proc_objects = []
    # Iterate over the list
    for proc in psutil.process_iter():
        try:
            # Fetch process details as dict
            proc_info = proc.as_dict(attrs=["pid", "name", "username"])
            proc_info["vms"] = proc.memory_info().vms / (1024 * 1024)
            # Append dict to list
            list_of_proc_objects.append(proc_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    # Sort list of dict by key vms i.e. memory usage
    list_of_proc_objects = sorted(
        list_of_proc_objects, key=lambda proc_obj: proc_obj["vms"], reverse=True
    )
    return list_of_proc_objects


def main():
    print("*** Iterate over all running process and print process ID & Name ***")
    # Iterate over all running process
    for proc in psutil.process_iter():
        try:
            # Get process name & pid from process object.
            process_name = proc.name()
            process_id = proc.pid
            print(process_name, " ::: ", process_id)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    print("*** Create a list of all running processes ***")
    list_of_process_names = list()
    # Iterate over all running processes
    for proc in psutil.process_iter():
        # Get process detail as dictionary
        p_info_dict = proc.as_dict(attrs=["pid", "name", "cpu_percent"])
        # Append dict of process detail in list
        list_of_process_names.append(p_info_dict)
    # Iterate over the list of dictionary and print each elem
    for elem in list_of_process_names:
        print(elem)
    print("*** Top 5 process with highest memory usage ***")
    list_of_running_process = get_list_of_process_sorted_by_memory()
    for elem in list_of_running_process[:5]:
        print(elem)


if __name__ == "__main__":
    main()
