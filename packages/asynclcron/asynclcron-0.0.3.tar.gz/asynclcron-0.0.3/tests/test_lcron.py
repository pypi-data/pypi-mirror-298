import time
import asyncio
from datetime import datetime
from asynclcron.lcron import LightweightCron, CronJob
from unittest import IsolatedAsyncioTestCase
from unittest import mock


class Test(IsolatedAsyncioTestCase):

    async def test_cancellable_wait(self):
        # no timeout, cancelled
        event = asyncio.Event()
        t = asyncio.create_task(LightweightCron._cancellable_wait(event))
        await asyncio.sleep(0.5)
        t1 = time.time()
        event.set()
        await t
        t2 = time.time()
        self.assertTrue(t.result())
        self.assertAlmostEqual(t1, t2, 1)
        self.assertFalse(event.is_set())

        # with timeout, cancelled
        event = asyncio.Event()
        t = asyncio.create_task(LightweightCron._cancellable_wait(event, 10))
        await asyncio.sleep(0.5)
        t1 = time.time()
        event.set()
        await t
        t2 = time.time()
        self.assertTrue(t.result())
        self.assertAlmostEqual(t1, t2, 1)
        self.assertFalse(event.is_set())

        # with timeout, timeouted
        event = asyncio.Event()
        t1 = time.time()
        t = asyncio.create_task(LightweightCron._cancellable_wait(event, 0.5))
        await t
        t2 = time.time()
        self.assertFalse(t.result())
        self.assertAlmostEqual(t1 + 0.5, t2, 1)
        self.assertFalse(event.is_set())

    def test_add_remove(self):
        schedule = LightweightCron(log_next_run_datetime=False)
        curr_dt = datetime(2024, 9, 26, 10, 0)

        # remove, empty queue
        self.assertIsNone(schedule.remove(1))
        self.assertEqual(len(schedule._q), 0)

        # add, before schedule run
        job1 = CronJob(mock.AsyncMock, "0 11 * * *", name="job1")
        self.assertEqual(schedule.add(job1, curr_dt), 0)
        self.assertEqual(len(schedule._q), 1)
        _, job_id, _, job, _ = schedule._q[0]
        self.assertEqual(job_id, 0)
        self.assertEqual(job.name, "job1")

        # remove by non-existing id
        self.assertIsNone(schedule.remove(1))

        # add another job
        job2 = CronJob(mock.AsyncMock, "30 10 * * *", name="job2")
        self.assertEqual(schedule.add(job2, curr_dt), 1)
        self.assertEqual(len(schedule._q), 2)
        _, job_id, _, job, _ = schedule._q[0]
        self.assertEqual(job_id, 1)
        self.assertEqual(job.name, "job2")

        # remove job2
        job = schedule.remove(1)
        self.assertEqual(job.name, "job2")

        # add job without cancelling wait
        schedule._wait_event = asyncio.Event()
        mocked_event_set = schedule._wait_event.set = mock.Mock()
        job3 = CronJob(mock.AsyncMock, "0 12 * * *", name="job3")
        self.assertEqual(schedule.add(job3, curr_dt), 2)
        self.assertEqual(len(schedule._q), 2)
        _, job_id, _, job, _ = schedule._q[1]
        self.assertEqual(job_id, 2)
        self.assertEqual(job.name, "job3")
        self.assertEqual(mocked_event_set.call_count, 0)
        mocked_event_set.close()

        # add job with cancelling wait
        schedule._wait_event = asyncio.Event()
        mocked_event_set = schedule._wait_event.set = mock.Mock()
        job4 = CronJob(mock.AsyncMock, "30 10 * * *", name="job4")
        self.assertEqual(schedule.add(job4, curr_dt), 3)
        self.assertEqual(len(schedule._q), 3)
        _, job_id, _, job, _ = schedule._q[0]
        self.assertEqual(job_id, 3)
        self.assertEqual(job.name, "job4")
        self.assertEqual(mocked_event_set.call_count, 1)
        mocked_event_set.close()

        # empty queue with cancelling wait
        self.assertIsNotNone(schedule.remove(0))
        self.assertIsNotNone(schedule.remove(2))
        self.assertIsNotNone(schedule.remove(3))

        schedule._wait_event = asyncio.Event()
        mocked_event_set = schedule._wait_event.set = mock.Mock()
        job5 = CronJob(mock.AsyncMock, "0 11 * * *", name="job5")
        self.assertEqual(schedule.add(job5, curr_dt), 4)
        self.assertEqual(len(schedule._q), 1)
        _, job_id, _, job, _ = schedule._q[0]
        self.assertEqual(job_id, 4)
        self.assertEqual(job.name, "job5")
        self.assertEqual(mocked_event_set.call_count, 1)
        mocked_event_set.close()
