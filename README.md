Simple Client Side Rate Limiter
===============================

A generic client side rate limiter to throttle calls over a period of time to reduce the server side pressure.  It is thread-safe for concurrent callers and easy to use.

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
