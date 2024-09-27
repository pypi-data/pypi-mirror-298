import sys
from rich.console import Console
from .app import App, RunState
from .runners import dbtSubprocessRunner
from .renderers import LiveRenderer


def main(*args: list[str]):
    args = args or sys.argv[1:]
    runner = dbtSubprocessRunner()
    state = RunState(events=list())
    app = App(runner=runner, state=state)
    console = Console()
    renderer = LiveRenderer(app=app, console=console)
    for _ in renderer.run(args):
        pass


if __name__ == "__main__":
    main()