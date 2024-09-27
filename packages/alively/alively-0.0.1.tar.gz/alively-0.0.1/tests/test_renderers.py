from rich.console import Console
from alively.renderers import LogLineRenderer, LiveRenderer
from alively.app import App


def test_log_line_renderer(console: Console, app: App):
    renderer = LogLineRenderer(app=app, console=console)
    list(renderer.run(['dbt']))
    lines = console.file.getvalue()
    assert lines


def test_live_renderer(console: Console, app: App):
    renderer = LiveRenderer(app=app, console=console)
    list(renderer.run(['dbt', 'build']))
    lines = console.file.getvalue()
    assert lines
