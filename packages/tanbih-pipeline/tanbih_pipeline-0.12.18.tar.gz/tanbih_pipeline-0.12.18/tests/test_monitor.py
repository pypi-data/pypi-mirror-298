from dataclasses import dataclass
from pipeline.monitor import Monitor, WorkerMonitor
from unittest import TestCase


class TestMonitor(TestCase):
    def test_monitor(self):
        monitor = Monitor()
        monitor.use_counter("test_counter", "test_counter")
        monitor.counter("test_counter")
        monitor.use_info("test_info", "test_info")
        monitor.info("test_info")
        monitor.use_state(
            "test_state", "test_state", labels=[], states=["running", "stopped"]
        )
        monitor.state("test_state", state="running")
        monitor.use_histogram("test_histogram1", "test_histogram")
        monitor.histogram("test_histogram1").observe(10)
        monitor.use_histogram("test_histogram2", "test_histogram", labels=["name"])
        monitor.histogram("test_histogram2", labels={"name": "test"}).observe(10)

    def test_worker_monitor(self):
        @dataclass
        class Worker:
            name = "worker"

        worker_monitor = WorkerMonitor(Worker())
        worker_monitor.record_start()
        worker_monitor.record_finish()
        worker_monitor.record_error(msg="error")
        worker_monitor.record_write()
        worker_monitor.record_read()
