from sched import scheduler

class ScheduledTaskExecutor():
    def __init__(self, scheduler):
        self.scheduler = scheduler
        # self.thread = Thread()

    # def run_scheduled(self):
    #     self.thread.run(scheduler.run())
