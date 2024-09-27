import heapq
import pytz
import asyncio
import logging
from datetime import datetime
from croniter import croniter


logger = logging.getLogger(__name__)


class CronJob:
    def __init__(self, async_func, cron, args=None, kwargs=None, name=None) -> None:
        self.async_func = async_func
        self.cron = cron
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.name = name

    def __str__(self) -> str:
        return f"job {self.name if self.name else ''} {self.cron}"


class LightweightCron:
    """
    wait exact time then trigger the earliest job
    """

    def __init__(self, jobs=None, tz_name=None, log_next_run_datetime=True) -> None:
        """
        jobs: add jobs in init, backward compatible
        tz_name: time zone name, default to local datetime
        log_next_run_datetime: log next run datetime
        """
        self._tz_name = tz_name
        self._log_next_run_datetime = log_next_run_datetime

        self._wait_event = None
        self._job_index = 0
        self._q = []

        if jobs:
            curr_dt = self._get_curr_dt()
            for job in jobs:
                self.add(job, curr_dt)

    def add(self, job, curr_dt=None):
        """
        add job to schedule
        return job id
        """
        # create job record first
        job_id = self._job_index
        self._job_index += 1
        if curr_dt is None:
            curr_dt = self._get_curr_dt()
        iter = croniter(job.cron, curr_dt)
        next_dt = iter.get_next(datetime)
        if self._log_next_run_datetime:
            logger.info(f"job_id:{job_id}, {job}, next run at {next_dt}")
        t = next_dt, job_id, iter, job, None

        # cancel current wait if needed
        cancel_wait = False
        if self._wait_event and not self._wait_event.is_set():
            if self._q:
                if t < self._q[0]:
                    # a earlier job came, cancel wait
                    cancel_wait = True
            else:
                # no job yet, cancel wait
                cancel_wait = True

        heapq.heappush(self._q, t)
        if cancel_wait:
            self._wait_event.set()
        return job_id

    def remove(self, job_id):
        """
        remove job by id
        return removed job object
        """
        for idx, (_, curr_job_id, _, job, _) in enumerate(self._q):
            if curr_job_id == job_id:
                # remove current item and re-heap
                self._q[idx] = self._q[-1]
                self._q.pop()
                heapq.heapify(self._q)
                return job
        return None

    async def run(self):
        self._wait_event = asyncio.Event()

        while True:
            if self._q:
                # check job from queue
                curr_dt = self._get_curr_dt()
                run_dt, job_id, iter, job, _ = self._q[0]
                if run_dt > curr_dt:
                    # wait until first job can run
                    wait_seconds = (run_dt - curr_dt).total_seconds()
                    await self._cancellable_wait(self._wait_event, wait_seconds)
                else:
                    # run job
                    task = asyncio.create_task(job.async_func(*job.args, **job.kwargs), name=job.name)

                    # add job next
                    next_dt = iter.get_next(datetime)
                    if self._log_next_run_datetime:
                        logger.info(f"job_id:{job_id}, {job}, next run at {next_dt}")
                    heapq.heapreplace(self._q, (next_dt, job_id, iter, job, task))

                    # let tasks run
                    await asyncio.sleep(0)
            else:
                # no jobs, wait until cancelled
                await self._cancellable_wait(self._wait_event)

    def _get_curr_dt(self):
        return datetime.now(pytz.timezone(self._tz_name)) if self._tz_name else datetime.now()

    @staticmethod
    async def _cancellable_wait(wait_event, timeout=None):
        """
        wait for event with timeout
        return if cancelled (by event)
        """
        try:
            await asyncio.wait_for(wait_event.wait(), timeout=timeout)
        except asyncio.TimeoutError:
            return False
        else:
            return True
        finally:
            wait_event.clear()
