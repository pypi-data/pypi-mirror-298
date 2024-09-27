import time


def sleep(nsec):
    """
    Sleep for a specified number of nanoseconds.
    @param nsec: time to sleep in nanoseconds
    @type  nsec: int
    """
    time.sleep(nsec / 1e9)


class Rate:
    """
    Convenience class for sleeping in a loop at a specified rate
    """

    def __init__(self, hz, timefun=time.monotonic_ns, sleepfun=sleep):
        """
        Constructor.
        @param hz: hz rate to determine sleeping
        @type  hz: int
        """
        self.timefun = timefun
        self.sleepfun = sleepfun
        self.last_time = self.timefun()
        self.sleep_dur = int(1e9/hz)

    def _remaining(self, curr_time):
        """
        Calculate the time remaining for rate to sleep.
        @param curr_time: current time
        @type  curr_time: L{Time}
        @return: time remaining
        @rtype: L{Time}
        """
        # detect time jumping backwards
        if self.last_time > curr_time:
            self.last_time = curr_time

        # calculate remaining time
        elapsed = curr_time - self.last_time
        return self.sleep_dur - elapsed

    def remaining(self):
        """
        Return the time remaining for rate to sleep.
        @return: time remaining
        @rtype: L{Time}
        """
        curr_time = self.timefun()
        return self._remaining(curr_time)

    def sleep(self):
        """
        Attempt sleep at the specified rate. sleep() takes into
        account the time elapsed since the last successful
        sleep().
        TODO: Check shutdown.
        TODO: Check backward time move.
        """
        curr_time = self.timefun()
        self.sleepfun(self._remaining(curr_time))
        self.last_time = self.last_time + self.sleep_dur

        # detect time jumping forwards, as well as loops that are
        # inherently too slow
        if curr_time - self.last_time > self.sleep_dur * 2:
            self.last_time = curr_time
