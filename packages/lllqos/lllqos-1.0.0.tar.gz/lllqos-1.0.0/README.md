# `lllqos`: Linux Low-Latency QoS for Python

The Linux kernel provides the [PM Quality Of Service Interface](https://docs.kernel.org/power/pm_qos_interface.html), which allows userspace processes to indicate acceptable wake-up latency. Processes seeking low wake-up latency (e.g., `cyclictest`) use this interface to tell the kernel the acceptable target latency (in microseconds). 

The kernel documentation describes the interface as follows:

> To register the default PM QoS target for the CPU latency QoS, the process must open `/dev/cpu_dma_latency`.
>
> As long as the device node is held open that process has a registered request on the parameter.
>
> To change the requested target value, the process needs to write an `s32` value to the open device node. 

This package provides a simple context-manager API `low_wakeup_latency(target_value)` that automates this. By default, the target value is 0.

On platforms other than Linux (or if the `/dev` filesystem is not mounted in the usual place), this context manager has no effect.

## Example

```python
from lllqos import low_wakeup_latency

# Standard use:
with low_wakeup_latency():
    print('Hi, but quickly!')

# Check whether lease was acquired:
with low_wakeup_latency() as lease:
    print(f'Lease acquired: {lease.acquired()}')
    
# Setting some nonzero goal:
with low_wakeup_latency(1000):
    print('Up to 1ms latency is acceptable here.')
```

A typical use-case is to combine this package with the [`abs-sleep` package](https://pypi.org/project/abs-sleep/) to achieve low-latency periodic activations. 

```python
from lllqos import low_wakeup_latency
from abs_sleep import periodic
import time

# tell Linux to minimize wake-up latency
with low_wakeup_latency():
  	# periodic wake-ups with a period of 500ms
    for t in periodic(0.5, align_secs=1):
      	now = time.monotonic()
      	print(f"periodic activation @ {t}s with {(now - t) * 1000000:.2f}µs latency")
```

NB: To achieve consistently low latency, you must run the Python interpreter with real-time priority (e.g., with the`SCHED_FIFO` or `SCHED_RR` scheduling policies). 

## See Also

- [Linux kernel documentation](https://docs.kernel.org/power/pm_qos_interface.html)
- [`cyclictest` implementation](https://git.kernel.org/pub/scm/utils/rt-tests/rt-tests.git/tree/src/cyclictest/cyclictest.c#n243)
