import io
import shutil
import json
import os
from pytest import mark
from pytest import fixture
from rich.console import Console
from alively import App
from alively.runners import Runner
from alively.app import RunState
from alively.events import dbtEvent


class MockRunner(Runner):
    _events: list[dbtEvent] = list()

    def run(self, args: list[str]):
        for event in self._events:
            yield event


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "integration: integration tests"
    )


def pytest_addoption(parser):
    parser.addoption(
        "--integrations", action="store_true", default=False, help="run integration tests"
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--integrations"):
        # --integration given in cli: do not skip integration tests
        return
    skip_integration = mark.skip(reason="need --integration option to run")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)


@fixture(scope='session')
def test_dir():
    return os.path.abspath(os.path.dirname(__file__))


@fixture(scope='session')
def mock_events(test_dir):
    mock_logs_filename = os.path.join(test_dir, 'mock_logs.json')
    mock_logs = open(mock_logs_filename, 'r').readlines()
    mock_events = [dbtEvent(**json.loads(l)) for l in mock_logs]
    return mock_events


@fixture
def get_event(mock_events):
    def _get_event(event_name):
        for event in mock_events:
            if event.info.name == event_name:
                return event
    return _get_event

@fixture
def app_state():
    return RunState(events=[])


@fixture
def runner(mock_events):
    mock_runner = MockRunner()
    mock_runner._events = mock_events
    return mock_runner


@fixture
def app(app_state, runner):
    app = App(runner=runner, state=app_state)
    return app


@fixture
def console_output():
    return io.StringIO()


@fixture
def console(console_output):
    return Console(file=console_output)


@fixture
def mock_dbt_project(tmpdir, test_dir, monkeypatch):
    target_dir = tmpdir / 'mock_dbt_project'
    monkeypatch.setenv('DBT_PROJECT_DIR', str(target_dir))
    monkeypatch.setenv('DBT_PROFILES_DIR', str(target_dir))
    shutil.copytree(os.path.join(test_dir, 'mock_project'), target_dir)
    return target_dir
