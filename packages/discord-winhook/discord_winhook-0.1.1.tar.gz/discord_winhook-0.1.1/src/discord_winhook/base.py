import sched
import time

from discord_webhook import DiscordWebhook

_scheduler = sched.scheduler(timefunc=time.time, delayfunc=time.sleep)
_scheduler_started = False

class Hook:
    def __init__(self, url : str):
        self.__url = url
        self.__testmode = False
        self.__recur_set = False
        self.__event = None

    @property
    def url(self):
        return self.__url

    def testmode(self):
        self.__testmode = True

    def __send(self, hook : DiscordWebhook):
        if self.__testmode:
            print(f"supposed to send {self.info} now at {time.time()}")
        else:
            hook.execute()
            
        if self.__event:
            self.__event = _scheduler.enter(self.__every, 1, self)

    def run(self):
        raise NotImplementedError
    
    def __call__(self):
        return self.run()

    def recur(self, every : float = 5*60):
        global _scheduler_started
        if self.__recur_set:
            return

        self.__recur_set = True
        self.__every = every
        self.__event = _scheduler.enter(every, 1, self)
        if not _scheduler_started:
            _scheduler_started = True
            scheduler_nonblocking()

    @property
    def info(self):
        return "<HOOK>"


def scheduler_blocking():
    _scheduler.run()

def scheduler_nonblocking():
    from threading import Thread
    t = Thread(target=scheduler_blocking)
    t.start()
