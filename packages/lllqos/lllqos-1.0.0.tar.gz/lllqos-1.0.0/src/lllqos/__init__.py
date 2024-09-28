"""A thin Python wrapper for the Linux PM Quality Of Service Interface.

Provides a Python context manager that sets the Linux kernel's acceptable
wake-up latency by writing to /dev/cpu_dma_latency. Has no effect on other
platforms.

NB: Access to /dev/cpu_dma_latency is typically restricted to root.
For ease of use, this module silently ignores any permission errors.

Typical examples:

    with low_wakeup_latency():
        ...

    with low_wakeup_latency() as lease:
        assert lease.acquired()
        ...

See Also:
    Linux kernel documentation: https://docs.kernel.org/power/pm_qos_interface.html
    How cyclictest does it: https://git.kernel.org/pub/scm/utils/rt-tests/rt-tests.git/tree/src/cyclictest/cyclictest.c#n243

"""

import struct
from pathlib import Path


QOS_FILE = Path("/dev/cpu_dma_latency")


class LowLatencyLease:
    """Create and hold a lease for the Linux PM QOS wake-up latency interface."""

    def __init__(self, target_value: int = 0, dev_path=None):
        """Construct a new lease (but do not acquire it yet).

        Arguments:
            target_value: The target latency, in microseconds (default: 0).
            dev_path: Where to find the file usually located at /dev/cpu_dma_latency
                      (necessary only if not mounted in the standard location).

        Returns:
            The new lease, ready to be acquired.

        """
        self.lease = None
        self.target = target_value
        self.dev_path = dev_path

    def acquire(self) -> bool:
        """Try to open the device file and write the target latency.

        NB: Fails silently in case of permission problems.

        Returns:
            Whether the lease was successfully acquired.

        """
        # From the Linux kernel docs:
        #
        # > To register the default PM QoS target for the CPU latency
        # > QoS, the process must open /dev/cpu_dma_latency.
        #
        # > As long as the device node is held open that process has a
        # > registered request on the parameter.
        #
        # > To change the requested target value, the process needs to
        # > write an s32 value to the open device node.

        fname = QOS_FILE if self.dev_path is None else self.dev_path

        if not fname.exists():
            return False

        try:
            qos = fname.open("wb", buffering=0)
        except PermissionError:
            # fail silently if we lack permission
            return False

        if not qos:
            return False

        # write requested latency to file
        value = struct.pack("=i", self.target)
        written = qos.write(value)
        assert written == len(value)

        # keep a reference to the open file
        self.lease = qos

        return True

    def acquired(self) -> bool:
        """Check whether the lease has been acquired.

        Returns:
            Whether the lease is currently held.


        """
        return self.lease is not None

    def release(self):
        """Release the currently held lease (if any)."""
        if self.acquired():
            self.lease.close()
            self.lease = None

    def __enter__(self):
        """Enter context manager (with statement)."""
        self.acquire()
        return self

    def __exit__(self, _exc_type, _exc_value, _traceback):
        """Exit context manager (with statement)."""
        self.release()


def low_wakeup_latency(target_value=0, *args, **kargs):
    """Create low-latency lease as a context manager.

    Tell the kernel that the process wake-up latency should not
    exceed target_value, if possible. The wake-up latency target
    remains in place while the lease is being held and is reset at
    the end of the `with` block.

    NB: Access to /dev/cpu_dma_latency usually requires root privileges.
    Any permission errors are silently ignored for ease of use.

    Arguments:
        target_value: The target latency, in microseconds (default: 0).
        dev_path: Where to find the file usually located at /dev/cpu_dma_latency
                 (necessary only if not mounted in the standard location).
        args: passed through to the LowLatencyLease constructor.
        kargs: passed through to the LowLatencyLease constructor.

    Returns:
        A lease context manager.

    """
    return LowLatencyLease(target_value, *args, **kargs)
