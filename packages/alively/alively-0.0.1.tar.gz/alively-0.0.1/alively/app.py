from typing import Iterable
from .events import dbtEvent
from .runners import Runner
from .state import RunState, NodeState


class App:
    def __init__(self, runner: Runner, state: RunState):
        self.runner = runner
        self.state = state

    def run(self, args: list[str]) -> Iterable[dbtEvent]:
        for event in self.runner.run(args):
            self.handle(event)
            yield event
        else:
            self.state.finished = True

    def get_handler(self, event: dbtEvent):
        handler_name = f"handle_{event.name}"
        handler = getattr(self, handler_name, None)
        return handler

    def handle(self, event: dbtEvent) -> RunState:
        self.state.add_event(event)
        _handle = self.get_handler(event)
        if _handle:
            return _handle(event)
        else:
            return self.noop_handler(event)

    def noop_handler(self, event: dbtEvent) -> RunState:
        return self.state

    def handle_StatsLine(self, event: dbtEvent) -> RunState:
        return self.state

    def handle_MainReportVersion(self, event: dbtEvent) -> RunState:
        self.state.dbt_version = event.data['version']
        self.state.dbt_log_version = event.data['log_version']        
        self.state.invocation_id = event.info.invocation_id
        self.state.run_started_at = event.info.ts
        return self.state
    
    def handle_AdapterRegistered(self, event: dbtEvent) -> RunState:
        self.state.adapter_name = event.data['adapter_name']
        self.state.adapter_version = event.data['adapter_version']
        return self.state

    def handle_ConcurrencyLine(self, event: dbtEvent) -> RunState:
        self.state.node_count = event.data['node_count']
        self.state.num_threads = event.data['num_threads']
        self.state.target_name = event.data['target_name']
        return self.state

    def handle_LogStartLine(self, event: dbtEvent) -> RunState:
        node_info = event.data['node_info']
        node = NodeState(**node_info)
        self.state.update_node(node)
        return self.state

    def handle_LogModelResult(self, event: dbtEvent) -> RunState:
        node_info = event.data['node_info']
        node = NodeState(**node_info)
        self.state.update_node(node)
        return self.state

    def handle_LogTestResult(self, event: dbtEvent) -> RunState:
        node_info = event.data['node_info']
        node = NodeState(**node_info)
        self.state.update_node(node)
        return self.state

    def handle_SkippingDetails(self, event: dbtEvent) -> RunState:
        node_info = event.data['node_info']
        node = NodeState(**node_info)
        self.state.update_node(node)
        return self.state

    def handle_LogSnapshotResult(self, event: dbtEvent) -> RunState:
        node_info = event.data['node_info']
        node = NodeState(**node_info)
        self.state.update_node(node)
        return self.state

    def handle_LogSeedResult(self, event: dbtEvent) -> RunState:
        node_info = event.data['node_info']
        node = NodeState(**node_info)
        self.state.update_node(node)
        return self.state
