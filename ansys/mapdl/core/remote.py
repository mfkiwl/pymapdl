"""Library to obtain some data from the MAPDL in case it is non-local."""

import weakref

class Remote:
    """Class to group all the commands related to getting info from the MAPDL system when it is remote."""

    def __init__(self, mapdl) -> None:
        """Initialize remote instance"""
        from ansys.mapdl.core.mapdl import _MapdlCore

        if not isinstance(mapdl, _MapdlCore):  # pragma: no cover
            raise TypeError("Must be initialized using Mapdl instance")
        self._mapdl_weakref = weakref.ref(mapdl)
        self._set_loaded = False

        self._remote = False if self._mapdl._local else True

    @property
    def _mapdl(self):
        """Return the weakly referenced instance of MAPDL"""
        return self._mapdl_weakref()

    @property
    def _log(self):
        """alias for mapdl log"""
        return self._mapdl._log

    def _set_log_level(self, level):
        """alias for mapdl._set_log_level"""
        return self._mapdl._set_log_level(level)

    def _get_remote_os_name(self):
        mapdl_os = self._mapdl.get('__tmp__', 'active', 0, 'platform')
        # this will sometimes return 'LINUX x6', 'LIN', or 'L'
        if 'LI' in mapdl_os.upper():
            mapdl_os = 'posix'
        elif 'WIN' in mapdl_os.upper():
            mapdl_os = 'nt'
        self._mapdl.run("__tmp__=")  # Deleting variable

        return mapdl_os

    @property
    def remote_os(self):
        return self._get_remote_os_name()

    @remote_os.setter
    def remote_os(self):
        """Forbidden"""
        pass

    def exist_var(self, env_name):
        if self._remote_os == 'posix':
            cmd = r'if [ -n "${' + env_name + '+set}" ]; then echo "exist"; else echo "do not exist"; fi'
        elif self._remote_os == 'nt':
            cmd = r"if defined " + env_name + " (echo 'exist') else (echo 'do not exist')"

        output = self._mapdl.sys(cmd, mute=False)

        if 'not exist' in output:
            return False
        elif 'exist' in output:
            return True

    # def get_env_var(self, env_name):
    #     """Check the existence of env variables in the remote MAPDL system."""
    #     if self._remote_os == 'posix':
    #         cmd = r'MyVar="${' + env_name + '}:-' + '__non_set__' + '}"'

    #     elif self._remote_os == 'nt':
    #         cmd =

    #     out = self._mapdl.run(f"/sys,{cmd}")
