from typing import Callable
from enum import Enum


class PipelineWorkerScope(Enum):
    INFO_COLLECTION = "info_collection"
    VULNERABILITY_SCAN = "vulnerability_scan"
    REPORT_GENERATION = "report_generation"

class TaskContext:
    ...

class TaskPipeline:
    def add(self, scope: PipelineWorkerScope, worker_id: str, worker: Callable[[TaskContext], None], nice: float = 0):
        ...

    def insert_before(self, before_id: str, worker_id: str, worker: Callable[[TaskContext], None],
                      nice_delta: float = 0.5):
        ...

    def insert_after(self, after_id: str, worker_id: str, worker: Callable[[TaskContext], None],
                     nice_delta: float = 0.5):
        ...

    def insert_first(self, worker_id: str, scope: PipelineWorkerScope, worker: Callable[[TaskContext], None],
                     nice_delta: float = 0.5):
        ...
