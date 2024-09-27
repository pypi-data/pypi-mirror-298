import json
from subprocess import Popen, PIPE
from abc import ABC, abstractmethod
from typing import Iterable
from .events import dbtEvent


class Runner(ABC):

    @abstractmethod
    def run(self, *args: list[str]) -> Iterable[dbtEvent]:
        pass


class dbtSubprocessRunner(Runner):

    def __init__(self):
        self.return_code = None
        self.completed = False
        self.stdout_lines = list()

    def run(self, args: list[str]) -> Iterable[str]:
        command = self.build_command(args)
        proc = Popen(command, stdout=PIPE, stderr=PIPE, text=True)
        while True:
            if line := proc.stdout.readline():
                self.stdout_lines.append(line)
                event = self.deserialize_event(line)
                yield event
            if return_code := proc.poll():
                self.return_code = return_code
                self.completed = True
                break

    def deserialize_event(self, event: str) -> dbtEvent:
        parsed = json.loads(event)
        return dbtEvent(**parsed)

    def build_command(self, args: list[str]):
        cmd = args.copy()
        if '--log-format' not in args:
            cmd.insert(1, 'json')
            cmd.insert(1, '--log-format')
        return cmd
