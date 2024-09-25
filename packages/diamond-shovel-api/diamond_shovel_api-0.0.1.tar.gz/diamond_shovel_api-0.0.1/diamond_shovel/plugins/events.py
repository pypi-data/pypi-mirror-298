import configparser

from diamond_shovel.function.task import TaskPipeline


class Event:
    ...

class DiamondShovelInitEvent(Event):
    config: configparser.ConfigParser
    daemon: bool
    ...

class PipelineInitEvent(Event):
    pipeline: TaskPipeline
    ...

def register_event(evt_class, handler):
    ...

def call_event(evt):
    ...
