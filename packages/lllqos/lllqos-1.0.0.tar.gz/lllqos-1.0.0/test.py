from lllqos import low_wakeup_latency

from abs_sleep import periodic
import time

# tell Linux to minimize wake-up latency
with low_wakeup_latency() as lease:
    print(f'Lease acquired: {lease.acquired()}')
  	# periodic wake-ups with a period of 500ms
    for t in periodic(0.5, align_secs=1):
      	now = time.monotonic()
      	print(f"periodic activation @ {t}s with {(now - t) * 1000000:.2f}µs latency")

