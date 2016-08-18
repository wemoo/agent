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
        dmidecode -t 4 | grep ID | sed 's/.*ID://;s/ //g' | head -n 1 | sha256sum | awk '{print $1}'
        """
    elif os == 'Darwin':
        script = r"""
        ioreg -rd1 -c IOPlatformExpertDevice| grep IOPlatformUUID| awk '{split($0, line, "\""); print line[4]}' | shasum -a 256 | awk '{print $1}'
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
