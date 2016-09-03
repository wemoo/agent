import re
import platform

from wemoo_agent.system.shell import exec_shell_script

uname = platform.uname()


def os_uuid():
    os = uname.system
    script = None

    if os == 'Linux':
        script = """
        cat /etc/machine-id
        """
    elif os == 'Darwin':
        script = """
        system_profiler SPHardwareDataType | awk '/Serial/ {print $4}'
        """

    output = exec_shell_script(script)
    if not output:
        return None

    return output.decode("utf-8").strip('\n')


system = {
    'system': uname.system,
    'node': uname.node,
    'release': uname.release,
    'version': uname.version,
    'machine': uname.machine,
    'processor': uname.processor,
    'uuid': os_uuid()
}
