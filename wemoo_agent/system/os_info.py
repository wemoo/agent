import re
import platform

from wemoo_agent.system.shell import exec_shell_script


def os_type():
    return platform.system()


def os_uuid():
    os = os_type()
    script = None

    if os == 'Linux':
        script = r"""
        cat /etc/machine-id
        """
    elif os == 'Darwin':
        script = r"""
        system_profiler SPHardwareDataType | awk '/Serial/ {print $4}'
        """

    output = exec_shell_script(script)
    if not output:
        return None

    return ''.join(output.split())


def hostname():
    script = r'hostname'
    output = exec_shell_script(script)
    if not output:
        return None

    return ''.join(output.split())
