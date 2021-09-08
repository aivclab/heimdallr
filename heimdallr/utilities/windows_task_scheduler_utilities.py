__all__ = ["disable_service", "remove_service", "install_service", "enable_service"]

from draugr.windows_utilities import (
    delete_task,
    new_user_logon_execute_task,
    set_task_activity,
)


def disable_service():
    set_task_activity("heimdallr_publisher", False)


def enable_service():
    set_task_activity("heimdallr_publisher", True)


def install_service():
    new_user_logon_execute_task(
        "heimdallr_publisher",
        "Heimdallr publisher",
        "python.exe",
        "-m heimdallr publish",
    )


def remove_service():
    delete_task("heimdallr_publisher")


if __name__ == "__main__":
    # remove_service()
    install_service()
    disable_service()
    # enable_service()
