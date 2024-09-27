from datetime import timedelta
from typing import Iterable
from abc import ABC, abstractmethod
from rich.console import Console
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner
from rich.console import group
from rich.progress import Progress, SpinnerColumn, MofNCompleteColumn, BarColumn, TimeElapsedColumn, Task
from .app import App
from .events import dbtEvent
from .state import NodeState
from .utils import format_timedelta


class CustomTimeElapsedColumn(TimeElapsedColumn):
    def render(self, task: Task) -> Text:
        elapsed = task.finished_time if task.finished else task.elapsed
        if elapsed is None:
            return Text("[00:00]", style="default")
        delta = timedelta(seconds=max(0, int(elapsed)))
        fdelta = format_timedelta(delta)
        return Text(f"[{fdelta}]", style="default")


class CustomMofNCompleteColumn(MofNCompleteColumn):
    def render(self, task: "Task") -> Text:
        """Show completed/total."""
        completed = int(task.completed)
        total = int(task.total) if task.total is not None else "?"
        total_width = len(str(total))
        return Text(
            f"[ {completed:{total_width}d}{self.separator}{total} ]".rjust(10),
            style="bold",
        )

class Renderer(ABC):
    def __init__(self, app: App, console: Console):
        self.app = app
        self.console = console
        self.logged_node_ids = set()
        # TODO: make the styles dynamic based on the state of the App. Eg the finished text should be a 
        # X symbol if there are any errors in the run. And the finished style should be red in that case.
        self.progress = Progress(
            SpinnerColumn(style="blue", finished_text=Text('D', style='blue')),
            CustomTimeElapsedColumn(),
            BarColumn(bar_width=60, style='default', finished_style="blue", complete_style="blue"),
            CustomMofNCompleteColumn(),
            console=self.console
        )
        self.progress_task = self.progress.add_task("Node Run")
    
    @abstractmethod
    def run(self):
        pass


class LogLineRenderer(Renderer):
    def run(self, args) -> Iterable[dbtEvent]:
        for event in self.app.run(args):
            self.console.print(event.info.hourstamp(), ' ', event.info.msg, markup=False, highlight=False)
            yield event


class NodeRenderer:
    icon_map = {
        'success': '✓',
        'pass': '✓',
        'skipped': '!',
        'fail': '✗',
        'error': '✗',
    }

    color_map = {
        'success': 'green',
        'pass': 'green',
        'skipped': 'yellow',
        'fail': 'red',
        'error': 'red',
        'started': 'blue'
    }

    spinners = dict()

    def __init__(self, node: NodeState):
        self.node = node

    @property
    def icon(self):
        if self.node.node_status == 'started':
            return Text('')
        color = self.color_map[self.node.node_status]
        icon = self.icon_map[self.node.node_status]
        return Text(icon + ' ', style=color)

    @property
    def status(self):
        color = self.color_map[self.node.node_status]
        return Text(self.node.node_status.rjust(10) + ' ', style=color)
    
    @property
    def name(self):
        text = (self.node.node_name + ' ').ljust(60, '.') + ' '
        return Text(text, style='default')
    
    @property
    def duration(self):
        td = format_timedelta(self.node.duration())
        return Text(f"[{td}] ", style='default')

    def render(self):
        result = self.icon.append(self.duration).append(self.name).append(self.status)
        if self.node.node_status == 'started':
            if self.node.unique_id in self.spinners:
                spinner = self.spinners[self.node.unique_id]
                spinner.text = result
            else:
                spinner = Spinner('dots', text=result, style='blue')
                self.spinners[self.node.unique_id] = spinner
            return spinner
        else:
            return result


# Log the errors / failures from those nodes
# Colorize the resource types
# Generate timestamps
# Progress bar for the parsing staging
# Ensure the nodes only get fully logged one time (right now we log all nodes at the end of the run instead of in the middle)
class LiveRenderer(Renderer):

    @group()
    def get_renderable(self):
        for node in self.app.state.nodes_with_status('started'):
            yield self.render_node(node)
        if self.app.state.node_count:
            yield self.progress

    def run(self, args) -> Iterable[dbtEvent]:
        with Live(console=self.console, refresh_per_second=8, get_renderable=self.get_renderable):
            for event in self.app.run(args):
                self.progress.update(self.progress_task, total=self.app.state.node_count, completed=self.app.state.finished_node_count())
                self.log_finished_nodes()
                yield event

    def log_finished_nodes(self):
        for node in self.app.state.finished_nodes():
            if node.unique_id in self.logged_node_ids:
                continue
            else:
                self.console.print(self.render_node(node))
                self.logged_node_ids.add(node.unique_id)

    def render_node(self, node: NodeState):
        return NodeRenderer(node).render()
