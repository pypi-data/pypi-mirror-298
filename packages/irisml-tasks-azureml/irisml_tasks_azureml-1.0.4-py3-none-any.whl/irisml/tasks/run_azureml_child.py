import dataclasses
import typing
import irisml.core


class Task(irisml.core.TaskBase):
    """Run AzureML child job. Not Implemented yet."""
    VERSION = '0.0.0'
    CACHE_ENABLED = False

    @dataclasses.dataclass
    class Config:
        tasks: typing.List[irisml.core.TaskDescription]

    def execute(self, inputs):
        raise NotImplementedError

    def dry_run(self, inputs):
        raise NotImplementedError
