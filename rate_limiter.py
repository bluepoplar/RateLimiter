"""
A simple client side rate limiter to be used as a decorator.
"""
import time
import threading


class RateLimiter:
    """
    A generic client side rate limiter to throttle calls over a period of time
    to reduce the server side pressure.
    It is thread-safe for concurrent callers and easy to use.
   
    Usage Example as Decorator (Easy to use, without extra code)

        # decorate the function you want to throttle calls. In this example, we
        # limit this function to run at most 5 times in a second.
        @RateLimiter(5, 1)
        def double_me(x):
            print(x * 2)

        # it takes about 20 seconds to run. 20 = 100 total calls/5 times in a second
        for i in range(100):
            t = threading.Thread(target=double_me, args=(i,))
            t.start()

    Usage Example as Regular Function:

        rate_limiter = RateLimiter(5,1)
        rate_limiter.wait()
        doSomething()  # your own function


    """

    def __init__(self, rate, period=1):
        """
        :param rate: how many times callers can call the rate-limited function
        in a specified time period.
        :param period: specified time period, default to 1 second.
        :rtype :
        """
        self.rate = rate
        self.period = period
        self.timestamps = []
        self.mutex = threading.Lock()

    def __call__(self, func):
        """
        Continue decorate the function after __init__.
        In __init__, it gets the decorator arguments and initialize the class
        instance.
        In __call__, it gets the function and return the decorated one with
        rate-limiting.

        :param func: the function that you want to limit call rate.
        :rtype : decorated function.
        """

        def rate_limited_func(*args):
            # this is where rate limiting happens.
            self.wait()
            return func(*args)

        return rate_limited_func

    def wait(self):
        # thread-safe for concurrent callers. Acquire lock before checking and
        # updating the rate.
        self.mutex.acquire()

        try:
            while True:
                # remove the timestamps which are not in current rate-limited
                # window.
                while self.timestamps and \
                                self.timestamps[0] < time.time() - self.period:
                    self.timestamps.pop(0)

                if len(self.timestamps) < self.rate:
                    # if the rate has not reach to the up limit, then return
                    # directly, no need to wait.
                    self.timestamps.append(time.time())
                    return
                else:
                    # if the rate has reached to the up limit, wait for some
                    # time to let the old ones move out of the current
                    # rate-limited window.
                    wait_time = self.timestamps[0] + self.period - time.time()

                    # some old ones might have already moved out of the current
                    # window when they reach to this point, so no need to wait.
                    if wait_time > 0:
                        time.sleep(wait_time)
        finally:
            self.mutex.release()


# example
if __name__ == '__main__':
    # decorate the function you want to throttle calls. In this example, we
    # limit this function to run at most 5 times in a second.
    @RateLimiter(5, 1)
    def double_me(x):
        print(x * 2)

    # it takes about 20 seconds to run. 20 = 100(total calls)/5(the rate in a second)
    for i in range(100):
        t = threading.Thread(target=double_me, args=(i,))
        t.start()
    

